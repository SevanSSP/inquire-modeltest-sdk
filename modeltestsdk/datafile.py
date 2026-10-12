"""
Data files: the reference writer for the Parquet format (format version 1) that the API accepts as the datapoints
of one test and time base (group).

The format:

- column ``time`` (float64, seconds since test start at full scale, strictly increasing), then one float64 column
  per timeseries, named by the timeseries id (lowercase hyphenated UUID). A missing sample is null; NaN is written
  as null.
- one row group; per column dictionary encoding if it has few distinct values, otherwise BYTE_STREAM_SPLIT;
  zstd level 9; statistics and page index.
- file metadata (``modeltest.*``: campaign, test, group, import run, provenance) and column metadata (timeseries,
  sensor, fs, default window), which the API checks against what it has stored.

Example
-------
>>> run = client.import_runs.start(campaign.id, pipeline_version="2.0.0")
>>> ts = client.timeseries.upsert_many(test.id, [...])
>>> written = write_parquet(
...     {"time": t, ts[0].id: surge, ts[1].id: heave}, "3010_g0.parquet",
...     FileMetadata.from_resources(campaign, test, group=0, import_run_id=run.id, pipeline_version="2.0.0"),
...     [ColumnMetadata.from_timeseries(x, sensors.get_by_id(x.sensor_id)) for x in ts])
>>> client.test.upload_datafile(test.id, 0, written.path, run.id, sha256=written.sha256)
"""
import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Optional, Union
from uuid import UUID

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

FORMAT_VERSION = 1
META = "modeltest."
TIME = "time"
CONTENT_TYPE = "application/vnd.apache.parquet"
DICTIONARY_THRESHOLD = 0.1  # dictionary encoding if distinct values are under this fraction of the rows
COMPRESSION_LEVEL = 9


def _as_dict(obj) -> dict:
    """A resource, pydantic model or mapping as a plain dict (without the client)."""
    if obj is None:
        return {}
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude={"client"}, mode="json")
    return dict(obj)


def _float_text(value) -> str:
    """Exact text of a float, so the API's comparison with the stored value is exact."""
    return repr(float(value))


@dataclass
class FileMetadata:
    """File key-value metadata of a data file (``modeltest.*``)."""
    campaign_id: str
    test_id: str
    group: int
    import_run_id: str
    campaign_name: Optional[str] = None
    test_number: Optional[str] = None
    test_type: Optional[str] = None
    test: Optional[dict] = None
    scale_factor: Optional[float] = None
    pipeline_version: Optional[str] = None
    source_files: Optional[list] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_resources(cls, campaign, test, group: int, import_run_id: str, pipeline_version: str = None,
                       source_files: list = None) -> "FileMetadata":
        """
        Metadata from the campaign and test (SDK resources or dicts as returned by the API).

        Parameters
        ----------
        campaign : Campaign or dict
            Campaign of the test
        test : FloaterTest, WaveCalibration, WindCalibration or dict
            The test; all its fields are stored as JSON
        group : int
            Time base of the file, 0 unless the test has several
        import_run_id : str
            Import run uploading the file
        pipeline_version : str, optional
            Version of the pipeline writing the file
        source_files : list, optional
            Raw files the data was read from, see describe_source_file()
        """
        c, t = _as_dict(campaign), _as_dict(test)
        return cls(campaign_id=str(c["id"]), test_id=str(t["id"]), group=group, import_run_id=str(import_run_id),
                   campaign_name=c.get("name"), test_number=t.get("number"), test_type=t.get("type"), test=t,
                   scale_factor=c.get("scale_factor"), pipeline_version=pipeline_version, source_files=source_files)

    def to_dict(self) -> dict:
        created_at = self.created_at or datetime.now(timezone.utc)
        values = {
            "format_version": str(FORMAT_VERSION),
            "campaign_id": str(self.campaign_id),
            "campaign_name": self.campaign_name,
            "test_id": str(self.test_id),
            "test_number": self.test_number,
            "test_type": self.test_type,
            "group": str(int(self.group)),
            "test": None if self.test is None else json.dumps(self.test, default=str),
            "scale_factor": None if self.scale_factor is None else str(self.scale_factor),
            "import_run_id": str(self.import_run_id),
            "pipeline_version": self.pipeline_version,
            "source_files": None if self.source_files is None else json.dumps(self.source_files),
            "created_at": created_at.isoformat(),
        }
        return {META + k: str(v) for k, v in values.items() if v is not None}


@dataclass
class ColumnMetadata:
    """Column metadata of one timeseries in a data file. Sensor, fs and window must match the stored timeseries."""
    timeseries_id: str
    sensor_id: str
    fs: float
    default_start_time: float
    default_end_time: float
    sensor_name: Optional[str] = None
    unit: Optional[str] = None
    kind: Optional[str] = None

    @classmethod
    def from_timeseries(cls, timeseries, sensor=None) -> "ColumnMetadata":
        """
        Metadata from a timeseries and, optionally, its sensor (SDK resources or dicts as returned by the API).
        """
        ts, s = _as_dict(timeseries), _as_dict(sensor)
        return cls(timeseries_id=str(ts["id"]), sensor_id=str(ts["sensor_id"]), fs=ts["fs"],
                   default_start_time=ts["default_start_time"], default_end_time=ts["default_end_time"],
                   sensor_name=s.get("name"), unit=s.get("unit"), kind=s.get("kind"))

    def to_dict(self) -> dict:
        values = {
            "timeseries_id": _column_name(self.timeseries_id),
            "sensor_id": str(self.sensor_id),
            "sensor_name": self.sensor_name,
            "unit": self.unit,
            "kind": self.kind,
            "fs": _float_text(self.fs),
            "default_start_time": _float_text(self.default_start_time),
            "default_end_time": _float_text(self.default_end_time),
        }
        return {META + k: str(v) for k, v in values.items() if v is not None}


@dataclass
class WrittenDataFile:
    """A data file written by write_parquet()."""
    path: Path
    sha256: str
    size_bytes: int
    n_rows: int
    columns: list = field(default_factory=list)


def _column_name(name) -> str:
    """Timeseries id as column name: lowercase hyphenated UUID."""
    try:
        return str(UUID(str(name)))
    except ValueError:
        raise ValueError(f"Column {name!r} is not a timeseries id (UUID)") from None


def _float_values(values) -> np.ndarray:
    """Values as float64 array, missing values as NaN."""
    if isinstance(values, (pa.Array, pa.ChunkedArray)):
        return values.cast(pa.float64()).to_numpy(zero_copy_only=False)
    if hasattr(values, "to_numpy"):  # pandas Series, also with nullable dtypes
        return values.to_numpy(dtype="float64", na_value=np.nan)
    return np.asarray(values, dtype="float64")


def _columns(table) -> dict:
    """Name -> values for a pandas DataFrame, pyarrow Table or mapping."""
    if isinstance(table, pa.Table):
        return {name: table.column(name) for name in table.column_names}
    if hasattr(table, "columns") and hasattr(table, "__getitem__") and not isinstance(table, Mapping):
        return {name: table[name] for name in table.columns}  # pandas DataFrame
    return dict(table)


def _use_dictionary(column: pa.Array) -> bool:
    if len(column) == 0:
        return False
    return pc.count_distinct(column, mode="only_valid").as_py() < DICTIONARY_THRESHOLD * len(column)


def sha256_file(path: Union[str, os.PathLike], chunk_size: int = 1 << 20) -> str:
    """Hex sha256 of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe_source_file(path: Union[str, os.PathLike], root: Union[str, os.PathLike]) -> dict:
    """
    A raw file as listed in a data file's source_files and in the import run's raw file manifest.

    Returns
    -------
    dict
        path relative to the data root (with forward slashes), size in bytes and sha256
    """
    path = Path(path)
    return {"path": path.relative_to(root).as_posix(), "size": path.stat().st_size, "sha256": sha256_file(path)}


def build_table(table, metadata: FileMetadata, columns: Iterable[ColumnMetadata]) -> pa.Table:
    """
    Builds the Arrow table of a data file in format version 1 and checks it as far as possible without the API.

    Parameters
    ----------
    table : pandas.DataFrame, pyarrow.Table or mapping of name to values
        Column 'time' and one column per timeseries, named by timeseries id. NaN and None are missing samples.
    metadata : FileMetadata
        File metadata
    columns : iterable of ColumnMetadata
        Metadata of each timeseries column; entries for timeseries not in the table are ignored

    Raises
    ------
    ValueError
        If the table isn't valid: time missing, not finite or not strictly increasing; a column that isn't a
        timeseries id, has no metadata, has no values or has infinite values
    """
    data = _columns(table)
    if TIME not in data:
        raise ValueError("The table needs a 'time' column")
    column_meta = {_column_name(c.timeseries_id): c for c in columns}

    problems = []
    time = _float_values(data.pop(TIME))
    if not np.all(np.isfinite(time)):
        problems.append("time has missing or infinite values")
    elif np.any(np.diff(time) <= 0):
        problems.append("time must be strictly increasing")
    if not data:
        problems.append("The table has no timeseries columns")

    fields = [pa.field(TIME, pa.float64(), nullable=False)]
    arrays = [pa.array(time, type=pa.float64())]
    names = []
    for name, values in data.items():
        try:
            column = _column_name(name)
        except ValueError as e:
            problems.append(str(e))
            continue
        if column in names:
            problems.append(f"Column {column} appears twice")
            continue
        if column not in column_meta:
            problems.append(f"Column {column} has no ColumnMetadata")
            continue
        v = _float_values(values)
        if len(v) != len(time):
            problems.append(f"Column {column} has {len(v)} values, time has {len(time)}")
            continue
        if np.isinf(v).any():
            problems.append(f"Column {column} has infinite values")
            continue
        if np.isnan(v).all():
            problems.append(f"Column {column} has no values")
            continue
        names.append(column)
        fields.append(pa.field(column, pa.float64(), metadata=column_meta[column].to_dict()))
        arrays.append(pa.array(v, type=pa.float64(), from_pandas=True))  # NaN -> null
    if problems:
        raise ValueError("Invalid data file table: " + "; ".join(problems))

    return pa.Table.from_arrays(arrays, schema=pa.schema(fields, metadata=metadata.to_dict()))


def write_parquet(table, path: Union[str, os.PathLike], metadata: FileMetadata,
                  columns: Iterable[ColumnMetadata]) -> WrittenDataFile:
    """
    Writes a data file in format version 1, ready for client.test.upload_datafile().

    Parameters
    ----------
    table : pandas.DataFrame, pyarrow.Table or mapping of name to values
        Column 'time' and one column per timeseries, named by timeseries id. NaN and None are missing samples.
    path : str or path
        File to write
    metadata : FileMetadata
        File metadata
    columns : iterable of ColumnMetadata
        Metadata of each timeseries column

    Returns
    -------
    WrittenDataFile
        Path, sha256, size, number of rows and the timeseries columns

    Raises
    ------
    ValueError
        If the table isn't valid, see build_table()
    """
    arrow = build_table(table, metadata, columns)
    dictionary = [name for name in arrow.column_names if _use_dictionary(arrow.column(name))]
    encoding = {name: "BYTE_STREAM_SPLIT" for name in arrow.column_names if name not in dictionary}
    pq.write_table(arrow, path, compression="zstd", compression_level=COMPRESSION_LEVEL,
                   row_group_size=max(arrow.num_rows, 1), use_dictionary=dictionary or False,
                   column_encoding=encoding, write_statistics=True, write_page_index=True)
    path = Path(path)
    return WrittenDataFile(path=path, sha256=sha256_file(path), size_bytes=path.stat().st_size,
                           n_rows=arrow.num_rows, columns=arrow.column_names[1:])


def read_metadata(path: Union[str, os.PathLike]) -> tuple[dict, dict]:
    """
    Reads the metadata of a data file.

    Returns
    -------
    tuple of dict
        File metadata and column metadata by column name, without the 'modeltest.' prefix
    """
    def strip(raw: Optional[dict]) -> dict:
        return {k.decode()[len(META):]: v.decode() for k, v in (raw or {}).items() if k.decode().startswith(META)}

    schema = pq.read_schema(path)
    return strip(schema.metadata), {f.name: strip(f.metadata) for f in schema if f.name != TIME}
