import matplotlib.pyplot as plt
import numpy


def plot_timeseries(datas, test, sensors):
    plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
    labels = []
    for data, sensor in zip(datas, sensors):

        plt.plot(data["time"], data["value"], markerfacecolor='none', alpha=0.8, markersize=2, label=sensor.name)
        # plt.gcf().autofmt_xdate()
        plt.xlabel('Time [s]')
        plt.ylabel(sensor.kind + ' [' + sensor.unit + ']')
        labels.append(sensor.name)

    plt.title(f"Test: {test.description}")
    plt.legend(labels, loc='upper right')
    # plt.xticks([])
    plt.show()
