from tests.utils import rounded_compare
import pytest
from matplotlib import pyplot as plt
from modeltestsdk.resources import Timeseries, TimeseriesList
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

    all_ts = client.timeseries.get()
    assert len(all_ts) >= len(ts_list)

    assert client.timeseries.get_by_id(ts.id) == ts == client.timeseries.get_by_sensor_id_and_test_id(
        sensor_id=ts.sensor_id, test_id=ts.test_id)
    assert client.timeseries.get_by_sensor_id_and_test_id(sensor_id=ts.sensor_id,
                                                          test_id='c5f16996-cec8-4380-823d-b6e77811353a') is None
    assert client.timeseries.get_by_sensor_id_and_test_id(sensor_id='c5f16996-cec8-4380-823d-b6e77811353a',
                                                          test_id=ts.test_id) is None
    assert ts_list == client.timeseries.get_by_test_id(ts.test_id)


def test_timeseries_resource(client, secret_key, admin_key, new_timeseries, new_datapoints):
    ts = new_timeseries[0]
    sensor = ts.sensor
    assert sensor == client.sensor.get_by_id(ts.sensor_id)
    data = ts.get_data()
    statistics_fetch = ts.get_statistics()
    assert rounded_compare(statistics_fetch.mean, np.mean(data.value), 10 ** -3)

    data_qats = ts.get_qats_ts()
    ts_list_data = new_timeseries.get_data()
    qats_tsdb = new_timeseries.get_qats_tsdb()

    assert len(data) == data_qats.n
    assert len(ts_list_data) == qats_tsdb.n
    ts_new = Timeseries(sensor_id=ts.sensor_id, test_id=ts.test_id, fs=ts.fs)
    with pytest.raises(AttributeError) as e:
        ts_new.create(admin_key=admin_key)

    assert 'No client provided, unable to create object' in str(e)


def test_timeseries_plot(new_timeseries, new_datapoints):
    tss = new_timeseries
    ts = new_timeseries[0]

    ts.plot(show=False)
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'Time [s]'
    assert fig.axes[0].yaxis.label.get_text() == f'{ts.sensor.kind.capitalize()} [{ts.sensor.unit}]'
    plt.close(fig)

    ts.plot(show=False, xlabel='this one', ylabel='that one')
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'this one'
    assert fig.axes[0].yaxis.label.get_text() == 'that one'
    plt.close(fig)

    tss.plot(show=False)
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'Time [s]'
    assert fig.axes[0].yaxis.label.get_text() == ''
    plt.close(fig)

    timeseries_with_same_sensor = [ts]
    for ts_i in tss:
        if ts_i.sensor == ts.sensor:
            timeseries_with_same_sensor.append(ts_i)
            if len(timeseries_with_same_sensor) == 5:
                break

    timeseries_with_same_sensor = TimeseriesList(timeseries_with_same_sensor)

    timeseries_with_same_sensor.plot(show=False, xlabel='this one', ylabel='that one')
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'this one'
    assert fig.axes[0].yaxis.label.get_text() == 'that one'
    plt.close(fig)

    timeseries_with_same_sensor.plot(show=False, xlabel='this one')
    y_label = f'{ts.sensor.kind.capitalize()} [{ts.sensor.unit}]'
    fig = plt.gcf()
    assert fig.axes[0].xaxis.label.get_text() == 'this one'
    assert fig.axes[0].yaxis.label.get_text() == y_label
    plt.close(fig)


def test_warning_check(new_timeseries, new_datapoints, new_tags):
    total_warning = 0
    for ts in new_timeseries:
        n_warning = ts.check_tags_for_warnings()
        n_warning_found_in_tags = 0
        for tag in ts.tags():
            if tag.name == 'quality: bad' or tag.name == 'quality: questionable' or tag.name == 'failed':
                n_warning_found_in_tags += 1
                total_warning += 1

        assert n_warning_found_in_tags == n_warning
    assert total_warning != 0
