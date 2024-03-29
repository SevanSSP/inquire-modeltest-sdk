"""
Test the DataPoints models
"""
from modeltestsdk.resources import DataPoints, DataPointsList, Timeseries
from tests.utils import random_lower_int, random_float
from uuid import uuid4


def test_types(new_datapoints):
    assert len(new_datapoints) == 100

    ts = Timeseries(
        sensor_id='2',
        test_id='2',
        fs=2.5,
        default_start_time=1,
        default_end_time=2,

    )
    ts.id = str(uuid4())

    dp2 = DataPoints(
        time=new_datapoints.time,
        value=[random_float() for i in range(0, 100)],
        timeseries_id=ts.id
    )

    dplist = DataPointsList([new_datapoints, dp2])

    assert len(dplist.to_pandas()) == 100


def test_to_qats(new_datapoints):
    ts = new_datapoints.to_qats_ts()

    assert ts.name == 'unknown'
    assert ts.kind is None
    assert ts.unit is None
