import matplotlib.pyplot as plt
import warnings


def plot_timeseries(timeseries_list: list):
    '''
    Plot one or more timeseries with matplotlib
    :param timeseries_list:
    :return:
    '''

    plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
    plt.axhline(0, color='slategray')

    if not isinstance(timeseries_list, list):
        timeseries_list = [timeseries_list]

    datas = []
    sensor_list = []
    for timeseries in timeseries_list:
        if not timeseries.data_points:
            warnings.warn("No datapoints in timeseries, fetching datapoints...")
            timeseries.get_data_points()
        datas.append(timeseries.data_points.to_pandas())
        sensor_list.append(timeseries.get_sensor())

    labels = []
    for data, sensor in zip(datas, sensor_list):

        plt.plot(data["time"], data["value"], markerfacecolor='none', alpha=1, markersize=2, label=sensor.name)
        plt.gcf().autofmt_xdate()
        plt.ylabel(sensor.unit)
        labels.append(sensor.name)

    plt.title(f"Test: {timeseries_list[0].get_test().description}")
    plt.legend(labels, loc='upper right')
    plt.xlabel('Time [s]')
    plt.grid()

    plt.show()
