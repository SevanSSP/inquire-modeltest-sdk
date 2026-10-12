from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

from .statistics import Statistics


class DataFile(BaseModel):
    """A Parquet file with the datapoints of one test and time base (group)."""
    id: str
    test_id: str
    group: int
    sha256: str
    size_bytes: int
    n_rows: int
    blob_path: str
    format_version: int
    import_run_id: Optional[str] = None
    created_at: Optional[datetime] = None
    status: str
    timeseries_ids: List[str] = []


class DataFileTimeseries(BaseModel):
    """What an uploaded data file holds for one timeseries."""
    timeseries_id: str
    n_points: Optional[int] = None
    t_first: Optional[float] = None
    t_last: Optional[float] = None
    statistics: Optional[Statistics] = None


class DataFileUpload(BaseModel):
    """Result of a data file upload: status 'created', or 'unchanged' if it was the group's active file already."""
    id: str
    test_id: str
    group: int
    sha256: str
    size_bytes: int
    n_rows: int
    blob_path: str
    format_version: int
    import_run_id: Optional[str] = None
    created_at: Optional[datetime] = None
    status: str
    superseded_id: Optional[str] = None
    timeseries: List[DataFileTimeseries] = []


class ImportRun(BaseModel):
    """One execution of the import pipeline for a campaign."""
    id: str
    campaign_id: str
    status: str
    pipeline_version: Optional[str] = None
    sdk_version: Optional[str] = None
    workbook_name: Optional[str] = None
    workbook_sha256: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    summary: Optional[dict[str, Any]] = None
    failures: Optional[List[dict[str, Any]]] = None
    raw_file_manifest: Optional[List[dict[str, Any]]] = None
