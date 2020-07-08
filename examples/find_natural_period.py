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


client = SDKclient()

campaign = client.campaign.get_by_name("STT")
test_name = "X300"
sensor_name = "M206_COG Z"

test = client.floater.get_by_name(test_name)

campaign.populate_test(test)
timeseries = test.get_timeseries()
campaign.test[test_name].populate_timeseries(timeseries)

ts = campaign.test[test_name].timeseries[sensor_name]
ts.get_data_points()
print("Hentet datapoints for", sensor_name)


times, values = ts.to_arrays(ts.data_points)

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

print("Natural period is", Tn)