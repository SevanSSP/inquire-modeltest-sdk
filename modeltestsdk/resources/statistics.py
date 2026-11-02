from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Statistics(BaseModel):
    """
    Statistics of a timeseries over its default window, or over a custom window.

    std and the spectral quantities (m0, m1, m2, m4, tp) are None for intermittent timeseries; every quantity is None
    if the window has no samples.
    """
    timeseries_id: Optional[str] = None
    min: Optional[float] = None
    max: Optional[float] = None
    std: Optional[float] = None
    mean: Optional[float] = None
    m0: Optional[float] = None
    m1: Optional[float] = None
    m2: Optional[float] = None
    m4: Optional[float] = None
    tp: Optional[float] = None
    n_points: Optional[int] = None
    window_start: Optional[float] = None
    window_end: Optional[float] = None
    stored: Optional[bool] = None
    scaling_length: Optional[float] = None
    computed_at: Optional[datetime] = None
    stats_version: Optional[int] = None
