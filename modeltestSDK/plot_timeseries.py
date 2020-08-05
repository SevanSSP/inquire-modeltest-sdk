import matplotlib.pyplot as plt
from typing import Any, List
import datetime
import numpy


def plot_timeseries(datas: list, test: Any, sensorList: list):

    plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
    labels = []
    for data, sensor in zip(datas, sensorList):

        plt.ylabel(sensor.unit)
        plt.plot(data["time"], data["value"], markerfacecolor='none', alpha=0.8, markersize=2, label=sensor.name)
        # plt.gcf().autofmt_xdate()
        plt.ylabel(sensor.unit)
        labels.append(sensor.name)

    plt.title(f"Test: {test.description}")
    plt.legend(labels, loc='upper right')
    plt.show()
