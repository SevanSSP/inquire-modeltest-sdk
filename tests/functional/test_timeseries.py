from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool
import random

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

    assert len(client.timeseries.get()) == len(new_timeseries)
    assert client.timeseries.get_by_id(ts.id) == ts == client.timeseries.get_by_sensor_id_and_test_id(sensor_id=ts.sensor_id, test_id=ts.test_id)
    assert ts_list == client.timeseries.get_by_test_id(ts.test_id)

