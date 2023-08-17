from tests.utils import rounded_compare
import pytest
from modeltestSDK.resources import TimeSeries
import numpy as np

def test_timeseries_api(client, secret_key, admin_key, new_timeseries):
    """The Api is now verified good to go and tests can interact with it"""
    ts = new_timeseries[0]
    assert ts

    assert client.timeseries.get_by_sensor_id(ts.sensor_id)

    ts_list = client.timeseries.get(filter_by=[
        client.filter.timeseries.sensor_id == ts.sensor_id,
        client.filter.timeseries.test_id == ts.test_id],
        sort_by=[client.sort.timeseries.test_id.asc])

    assert len(ts_list) == 1

    len_get_timeseries = 0
    sensor_ids = set([ts_i.sensor_id for ts_i in new_timeseries])
    for sensor_id in sensor_ids:
        len_get_timeseries += len(client.timeseries.get(filter_by=[
            client.filter.timeseries.sensor_id == sensor_id
        ]))

    assert len_get_timeseries == len(new_timeseries)

    assert client.timeseries.get_by_id(ts.id) == ts == client.timeseries.get_by_sensor_id_and_test_id(
        sensor_id=ts.sensor_id, test_id=ts.test_id)
    assert ts_list == client.timeseries.get_by_test_id(ts.test_id)


def test_timeseries_resource(client, secret_key, admin_key, new_timeseries, new_datapoints):
    ts = new_timeseries[0]
    sensor = ts.sensor()
    assert sensor == client.sensor.get_by_id(ts.sensor_id)
    data = ts.get_data()
    statistics_fetch = ts.statistics()
    assert rounded_compare(statistics_fetch.mean, np.mean(data.value), 10 ** -3)


    data_qats = ts.get_qats_ts()
    ts_list_data = new_timeseries.get_data()
    qats_tsdb = new_timeseries.get_qats_tsdb()

    assert len(data) == data_qats.n
    assert len(ts_list_data) == qats_tsdb.n
    ts_new = TimeSeries(sensor_id=ts.sensor_id, test_id=ts.test_id, fs=ts.fs)
    with pytest.raises(AttributeError) as e:
        ts_new.create(admin_key=admin_key)
