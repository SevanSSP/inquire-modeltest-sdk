"""
Test the Timeseries models
"""


def test_types(new_timeseries):
    assert isinstance(new_timeseries.sensor_id, str)
    assert isinstance(new_timeseries.test_id, str)
    assert new_timeseries.test is None
    assert new_timeseries.sensor is None
