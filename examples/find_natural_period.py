from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration, Timeseries, Sensor
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
import time
import asyncio
import numpy
from qats.signal import find_maxima, smooth, tfe, psd
from qats import TsDB
from qats.ts import TimeSeries
import os

from pipeline.plot_timeseries import plot_timeseries

import time
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from modeltestSDK.utils import to_datetime_string

# må tilpasses SDK
'''def find_natural_period():
    times_in_tuples = self.datapoints.with_entities(Datapoint.time).all()
    print("Fetched all datapoint times")
    times_in_list = [t[0] for t in times_in_tuples]
    times_in_array = numpy.array(times_in_list)
    start_time = times_in_array[0]
    times = numpy.array([(t - start_time).total_seconds() for t in times_in_array])
    values_in_tuples = self.datapoints.with_entities(Datapoint.value).all()
    print("Fetched all datapoint values")
    values_in_list = [value[0] for value in values_in_tuples]
    values = numpy.array(values_in_list)

    print("Datapoint times are")
    print(times)
    print("Datapoint values are")
    print(values)

    maxima, indices = find_maxima(values, retind=True)
    plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
    plt.title('Timeseries')
    plt.plot(times, values)
    plt.xlabel('Time [s]')
    plt.ylabel("Amplitude (mm)")
    plt.legend(['Free Decay Test sample'], loc='upper left')
    plt.grid()
    plt.show()

    Tn = []
    t_dur = 15

    # Defines relevant durations for the decay tests. Also obtains an average Tn-value for the test in question.
    i = 1
    t1 = times[indices[-i]]
    t2 = t1 + t_dur
    maxima, indices2 = find_maxima(values[(t1 < times) & (times <= t2)], retind=True)
    Tn = numpy.mean(times[indices2[0:-2]] - times[indices2[1:-1]])
    print("Periods between maximas are: ")
    print(times[indices2[0:-2]] - times[indices2[1:-1]])
    print("Number of oscillations observed is", len(times[indices2[0:-2]] - times[indices2[1:-1]]))
    return Tn'''
