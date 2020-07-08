
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
mplstyle.use('fast')


client = SDKclient()

stt = client.campaign.get_by_name("STT")
tests = ["waveIrreg_2101", "waveIrreg_2102", "waveIrreg_2103", "waveIrreg_2104", "waveIrreg_2105"]
sensor_names = ["M206_COF X", "M206_COF Z", "M206_COF Pitch", "M206_acc_pos X", "M206_acc_pos Z"]
coherence = 0.7
results_file = "statistics_SWACH.txt"
print_path = os.path.join(os.path.split(os.getcwd())[0], results_file)

for test_name in tests:
    test = client.floater.get_by_name(test_name)
    stt.populate_test(test)
    timeseries = test.get_timeseries()
    stt.test[test_name].populate_timeseries(timeseries)

    for sensor_name in sensor_names:
        ts = stt.test[test_name].timeseries[sensor_name]
        ts.get_data_points()
        print("Hentet datapoints for", sensor_name)

        # To alternative metoder for å få datapunktene som arrays
        # tt, XX = ts.get_data_points_as_arrays()
        tt, XX = ts.to_arrays(ts.data_points)
        # t, X = ts.get_froude_scaled_arrays(tt, XX, stt.scale_factor)
        # Nå ligger noen sensorer i databasen med feil 'kind' så automatisk froude skalering går ikke før det er fikset

        # Froude skalering:
        if sensor_name == "M206_COF X":
            power = 1
        if sensor_name == "M206_COF Z":
            power = 1
        if sensor_name == "M206_COF Pitch":
            power = 0
        if sensor_name == "M206_acc_pos X":
            power = 0
        if sensor_name == "M206_acc_pos Z":
            power = 0

        t = tt * (stt.scale_factor ** 0.5)
        if power == 0:
            X = XX
        else:
            X = XX * (stt.scale_factor ** power) / 1000

        # TimeSeries fra qatz
        w = TimeSeries('Full Scale' + sensor_name, t, X)
        if sensor_name == "M206_COF X":
            fullSurge = w
        if sensor_name == "M206_COF Z":
            fullHeave = w
        if sensor_name == "M206_COF Pitch":
            fullPitch = w
        if sensor_name == "M206_acc_pos X":
            fullAcc = w
        if sensor_name == "M206_acc_pos Z":
            fullZacc = w

        # Plotting
        # plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
        # plt.title('Timeseries')
        # plt.plot(t, X)
        # plt.xlabel('Time [s]')
        # plt.ylabel(ts.get_sensor().kind)
        # plt.legend(['Free Decay Test sample'], loc='upper left')
        # plt.grid()
        # plt.show()

        print("Test er", test.description, "og sensor er", sensor_name)

    newSurge_t, newSurge_x = fullSurge.filter('hp', 1. / 30., twin=(100, 1e8), taperfrac=None)
    fullPitch_t, fullPitch_x = fullPitch.filter('hp', 1. / 27., twin=(100, 1e8), taperfrac=None)
    # fullAcc_t, fullAcc_x = fullAcc.filter('hp', 1. / 27., twin=(100, 1e8), taperfrac=None)
    # fullZacc.t, fullZacc.x = fullZacc.filter('hp', 1. / 30., twin=(100, 1e8), taperfrac=None)
    # f_sigx, tf_acc = tfe(fullWave.x, fullAcc.x, dt, clim=coherence, nperseg=8700)

    # wavestats = fullWave.stats(statsdur=10800)

    newSurge = TimeSeries("New Surge", newSurge_t, newSurge_x)
    newPitch = TimeSeries("New Pitch", fullPitch_t, fullPitch_x)


    a = newSurge.stats(statsdur=10800.)
    b = newPitch.stats(statsdur=10800.)
    # c = fullAcc.stats(statsdur=10800.)

    d = fullHeave.stats(statsdur=10800.)
    # e = fullZacc.stats(statsdur=10800.)

    header = ['Motion', 'std', 'min', 'max']
    table = [[1, a['std'], a['min'], a['max']], [3, d['std'], d['min'], d['max']],
             [5, b['std'], b['min'], b['max']]]
    print("--------------------------------------------------------------", file=open(print_path, "a"))
    print(test_name, ' Surge = 1, Heave = 3, Pitch = 5', file=open(print_path, "a"))
    print("---------------------------------------------------------------", file=open(print_path, "a"))
    print(''.join(column.rjust(15) for column in header), file=open(print_path, "a"))
    for row in table:
        print(''.join(f'{column:.3f}'.rjust(15) for column in row), file=open(print_path, "a"))

print("Resulter ligger i", print_path)












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
