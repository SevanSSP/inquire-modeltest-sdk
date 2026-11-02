import hashlib
import json
from datetime import datetime
from uuid import uuid4

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from modeltestsdk.datafile import (ColumnMetadata, FileMetadata, build_table, describe_source_file, read_metadata,
                                   sha256_file, write_parquet)
from modeltestsdk.resources import Campaign, FloaterTest, Sensor, Timeseries

CAMPAIGN_ID, TEST_ID, RUN_ID = str(uuid4()), str(uuid4()), str(uuid4())


def file_metadata(**kwargs):
    return FileMetadata(campaign_id=CAMPAIGN_ID, test_id=TEST_ID, group=0, import_run_id=RUN_ID, **kwargs)


def column(ts_id=None, **kwargs):
    values = dict(timeseries_id=ts_id or str(uuid4()), sensor_id=str(uuid4()), fs=100 / 60 ** 0.5,
                  default_start_time=1.0, default_end_time=8.0)
    values.update(kwargs)
    return ColumnMetadata(**values)


def test_writes_format_version_1(tmp_path):
    n = 1000
    t = np.arange(n) / 10.0
    smooth = np.sin(t)
    smooth[[3, 500]] = np.nan  # missing samples
    quantised = np.round(np.cos(t) * 3)  # 7 distinct values
    a, b = column(), column(sensor_name="TENSION02", unit="N", kind="force")
    path = tmp_path / "file.parquet"

    written = write_parquet({"time": t, a.timeseries_id: smooth, b.timeseries_id.upper(): quantised}, path,
                            file_metadata(campaign_name="Mariner", source_files=[{"path": "a.mat"}],
                                          created_at=datetime(2026, 10, 12)),
                            [a, b, column()])  # metadata of a timeseries not in the file is ignored

    assert written.sha256 == sha256_file(path) and written.size_bytes == path.stat().st_size
    assert written.n_rows == n and written.columns == [a.timeseries_id, b.timeseries_id]

    pf = pq.ParquetFile(path)
    assert pf.metadata.num_row_groups == 1
    assert pf.schema_arrow.names == ["time", a.timeseries_id, b.timeseries_id]
    assert all(f.type == pa.float64() for f in pf.schema_arrow)
    table = pf.read()
    assert table.column(a.timeseries_id).null_count == 2
    assert not np.isnan(table.column(a.timeseries_id).to_numpy(zero_copy_only=False)[[0, 4]]).any()
    np.testing.assert_array_equal(table.column("time").to_numpy(), t)

    row_group = pf.metadata.row_group(0)
    encodings = {row_group.column(i).path_in_schema: row_group.column(i).encodings for i in range(3)}
    assert "BYTE_STREAM_SPLIT" in encodings["time"] and "BYTE_STREAM_SPLIT" in encodings[a.timeseries_id]
    assert "RLE_DICTIONARY" in encodings[b.timeseries_id]
    assert row_group.column(0).compression == "ZSTD" and row_group.column(0).statistics is not None

    meta, columns = read_metadata(path)
    assert meta["format_version"] == "1" and meta["test_id"] == TEST_ID and meta["group"] == "0"
    assert meta["import_run_id"] == RUN_ID and meta["campaign_name"] == "Mariner"
    assert json.loads(meta["source_files"]) == [{"path": "a.mat"}]
    assert meta["created_at"] == "2026-10-12T00:00:00"
    assert "test" not in meta and "scale_factor" not in meta
    assert columns[a.timeseries_id]["timeseries_id"] == a.timeseries_id
    assert float(columns[a.timeseries_id]["fs"]) == a.fs  # exact
    assert columns[b.timeseries_id]["unit"] == "N" and "unit" not in columns[a.timeseries_id]


def test_metadata_from_resources():
    campaign = Campaign(id=CAMPAIGN_ID, name="Mariner", description="d", location="Marintek",
                        date=datetime(2011, 5, 1), scale_factor=65, water_depth=120)
    test = FloaterTest(id=TEST_ID, number="3010", description="irr", test_date=datetime(2011, 5, 2),
                       campaign_id=CAMPAIGN_ID, category="irregular wave", orientation=0.0)
    meta = FileMetadata.from_resources(campaign, test, group=1, import_run_id=RUN_ID, pipeline_version="2.0.0")
    d = meta.to_dict()
    assert d["modeltest.test_number"] == "3010" and d["modeltest.test_type"] == "Floater Test"
    assert d["modeltest.scale_factor"] == "65.0" and d["modeltest.group"] == "1"
    assert d["modeltest.pipeline_version"] == "2.0.0"
    assert json.loads(d["modeltest.test"])["category"] == "irregular wave"
    assert "client" not in json.loads(d["modeltest.test"])

    sensor = Sensor(id=str(uuid4()), campaign_id=CAMPAIGN_ID, name="HEAVE", description="", unit="m", kind="length",
                    source="direct measurement", x=0, y=0, position_reference="local",
                    position_heading_lock=False, position_draft_lock=False, positive_direction_definition="up")
    ts = Timeseries(id=str(uuid4()), sensor_id=sensor.id, test_id=TEST_ID, fs=10, default_start_time=0,
                    default_end_time=100)
    c = ColumnMetadata.from_timeseries(ts, sensor).to_dict()
    assert c["modeltest.sensor_name"] == "HEAVE" and c["modeltest.kind"] == "length"
    assert c["modeltest.fs"] == "10.0" and c["modeltest.default_end_time"] == "100.0"
    assert "modeltest.unit" not in ColumnMetadata.from_timeseries(ts.model_dump()).to_dict()


def test_accepts_pandas_and_arrow(tmp_path):
    a = column()
    df = pd.DataFrame({"time": [0.0, 0.1, 0.2], a.timeseries_id: pd.array([1.0, None, 3.0], dtype="Float64")})
    written = write_parquet(df, tmp_path / "df.parquet", file_metadata(), [a])
    assert pq.read_table(written.path).column(a.timeseries_id).null_count == 1

    arrow = pa.table({"time": [0.0, 1.0], a.timeseries_id: pa.array([1, None], type=pa.int32())})
    assert build_table(arrow, file_metadata(), [a]).column(a.timeseries_id).type == pa.float64()


@pytest.mark.parametrize("table, message", [
    ({"t": [0.0]}, "needs a 'time' column"),
    ({"time": [0.0, 0.0]}, "strictly increasing"),
    ({"time": [0.0, np.nan]}, "missing or infinite"),
    ({"time": [0.0]}, "no timeseries columns"),
    ({"time": [0.0], "surge": [1.0]}, "not a timeseries id"),
    ({"time": [0.0], "{other}": [1.0]}, "has no ColumnMetadata"),
    ({"time": [0.0], "{id}": [np.nan]}, "has no values"),
    ({"time": [0.0], "{id}": [np.inf]}, "infinite values"),
    ({"time": [0.0, 1.0], "{id}": [1.0]}, "has 1 values"),
])
def test_invalid_tables(table, message):
    a = column()
    table = {k.format(id=a.timeseries_id, other=uuid4()): v for k, v in table.items()}
    with pytest.raises(ValueError, match=message):
        build_table(table, file_metadata(), [a])


def test_duplicate_columns():
    a = column()
    with pytest.raises(ValueError, match="appears twice"):
        build_table({"time": [0.0], a.timeseries_id: [1.0], a.timeseries_id.upper(): [2.0]}, file_metadata(), [a])


def test_describe_source_file(tmp_path):
    (tmp_path / "Mariner" / "IRR").mkdir(parents=True)
    raw = tmp_path / "Mariner" / "IRR" / "3010.mat"
    raw.write_bytes(b"raw data")
    assert describe_source_file(raw, tmp_path) == {
        "path": "Mariner/IRR/3010.mat", "size": 8, "sha256": hashlib.sha256(b"raw data").hexdigest()}
