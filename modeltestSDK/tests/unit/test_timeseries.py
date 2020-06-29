

def test_types(new_timeseries):
    #assert isinstance(new_timeseries.id, (uuid.UUID, UUID))
    assert isinstance(new_timeseries.sensor_id, str)
    assert isinstance(new_timeseries.test_id, str)

