from datetime import datetime
from tests.utils import random_lower_int, random_float, rounded_compare
import random
import numpy as np
from matplotlib import pyplot as plt
import pytest
from modeltestSDK.resources import DataPointsList


def test_datapoints_api(client, secret_key, admin_key, new_datapoints):
    """The Api is now verified good to go and tests can interact with it"""
    dp_fixture = new_datapoints[0]
    assert dp_fixture

    dp_fetch = client.timeseries.get_data_points(ts_id=dp_fixture.timeseries_id, all_data=True)
    assert dp_fixture == dp_fetch
    ts = client.timeseries.get_by_id(dp_fixture.timeseries_id)
    statistics_fetch = client.timeseries.get_statistics(ts_id=ts.id)
    assert rounded_compare(statistics_fetch.mean, np.mean(dp_fetch.value), 10 ** -3)


def test_datapoints_resource(client, secret_key, admin_key, new_datapoints):
    """The Api is now verified good to go and tests can interact with it"""
    dp = new_datapoints[0]
    df_list = new_datapoints.to_pandas()
    df = dp.to_pandas()
    dp_qats = dp.to_qats_ts()
    assert len(dp) == len(df_list) == len(df) == dp_qats.n
    assert np.mean(dp.value) == np.mean(df.values) == np.mean(dp_qats.x)


def test_datapoints_overwrite(client, secret_key, admin_key, new_datapoints):
    """
    GIVEN a timeseries with existing datapoint
    WHEN trying to overwrite the datapoints
    THEN ensure that the expected behaviour is seen
    """

    time = list(range(0, 1000))
    values = [random_float() for _ in range(0, len(time))]

    selected_ts = new_datapoints[0].timeseries

    with pytest.raises(Exception) as e:
        selected_ts.add_data(time=time, values=values)

    assert '403 Client Error: Forbidden for url' in str(e.value)

    selected_ts.add_data(time=time, values=values, secret_key=secret_key)

    returned_dp = client.timeseries.get_data_points(ts_id=selected_ts.id, all_data=True)

    assert returned_dp.time == time
    assert returned_dp.value == values


def test_datapoints_plot(new_datapoints):
    dps = new_datapoints
    dp = new_datapoints[0]

    dp.plot(show=False)
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'Time [s]'
    assert fig.axes[0].yaxis.label.get_text() == f'{dp.timeseries.sensor.kind.capitalize()} [{dp.timeseries.sensor.unit}]'
    plt.close(fig)

    dp.plot(show=False, xlabel='this one', ylabel='that one')
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'this one'
    assert fig.axes[0].yaxis.label.get_text() == 'that one'
    plt.close(fig)

    dps.plot(show=False)
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'Time [s]'
    assert fig.axes[0].yaxis.label.get_text() == ''
    plt.close(fig)

    dps_with_same_sensor = [dp]
    for dp_i in dps:
        if dp_i.timeseries.sensor == dp.timeseries.sensor:
            dps_with_same_sensor.append(dp_i)
            if len(dps_with_same_sensor) == 5:
                break

    timeseries_with_same_sensor = DataPointsList(dps_with_same_sensor)
    timeseries_with_same_sensor.plot(show=False, xlabel='this one', ylabel='that one')
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'this one'
    assert fig.axes[0].yaxis.label.get_text() == 'that one'
    plt.close(fig)


