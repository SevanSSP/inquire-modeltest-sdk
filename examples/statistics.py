
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

tests = client.floater.get_all()


for test in tests:
    scale_factor = 75
    coherence = 0.7
    nameofresults = "statistics_SWACH.txt"
    # Velg hvilken test som skal leses
    if test.description == "waveIrreg_2102":#.split("_")[0] == "waveIrreg":
        for ts in test.get_timeseries():
            sensor = ts.get_sensor()
            # Velg hvilken sensor som skal leses
            if sensor.name in ["M206_COF X", "M206_COF Z", "M206_COF Pitch", "M206_acc_pos X", "M206_acc_pos Z"]:

                datapoints = ts.get_data_points()
                #print(datapoints.dump())
                print("Hentet alle datapoints")
                times = []
                XX = []
                # Fyller inn tid og verdi fra datapunkter til en tidsvektor og verdivektor
                for datapoint in datapoints:
                    times.append(datapoint.time)
                    XX.append(datapoint.value)
                # Må konvertere t-vektor til antall sekunder fra start-tiden
                times_in_array = numpy.array(times)
                start_time = times_in_array[0]
                tt = []
                for ti in times_in_array:
                    tt.append((ti-start_time).total_seconds())
                tt = numpy.array(tt)

                if sensor.name == "M206_COF X":
                    power = 1
                if sensor.name == "M206_COF Z":
                    power = 1
                if sensor.name == "M206_COF Pitch":
                    power = 0
                if sensor.name == "M206_acc_pos X":
                    power = 0
                if sensor.name == "M206_acc_pos Z":
                    power = 0

                XX = numpy.array(XX)

                t = tt*(scale_factor**0.5)
                if power == 0:
                    X = XX #* scale_factor ** power
                    print(X[:20])
                else:
                    X = XX * (scale_factor ** power) / 1000

                print(isinstance(t, list))
                print(isinstance(X, list))

                w = TimeSeries('Full Scale' + sensor.name, t, X)

                if sensor.name == "M206_COF X":
                    fullSurge = w
                if sensor.name == "M206_COF Z":
                    fullHeave = w
                if sensor.name == "M206_COF Pitch":
                    fullPitch = w
                if sensor.name == "M206_acc_pos X":
                    fullAcc = w
                if sensor.name == "M206_acc_pos Z":
                    fullZacc = w


                #timeseries = TimeSeries('Full scale Navn', t, v)
                # Plotting
                '''plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
                plt.title('Timeseries')
                plt.plot(t, X)
                plt.xlabel('Time [s]')
                plt.ylabel("Amplitude (mm)")
                plt.legend(['Free Decay Test sample'], loc='upper left')
                plt.grid()
                plt.show()'''

                print("Test er", test.description, "og sensor er", sensor.name)

        newSurge_t, newSurge_x = fullSurge.filter('hp', 1. / 30., twin=(100, 1e8), taperfrac=None)
        fullPitch_t, fullPitch_x = fullPitch.filter('hp', 1. / 27., twin=(100, 1e8), taperfrac=None)
        # fullAcc_t, fullAcc_x = fullAcc.filter('hp', 1. / 27., twin=(100, 1e8), taperfrac=None)
        # fullZacc.t, fullZacc.x = fullZacc.filter('hp', 1. / 30., twin=(100, 1e8), taperfrac=None)
        # f_sigx, tf_acc = tfe(fullWave.x, fullAcc.x, dt, clim=coherence, nperseg=8700)

        # wavestats = fullWave.stats(statsdur=10800)

        newSurge = TimeSeries("New Surge", newSurge_t, newSurge_x)
        newPitch = TimeSeries("New Pitch", fullPitch_t, fullPitch_x)

        print_path = os.path.join(os.path.split(os.getcwd())[0], nameofresults)
        print(print_path)
        a = newSurge.stats(statsdur=10800.)
        b = newPitch.stats(statsdur=10800.)
        # c = fullAcc.stats(statsdur=10800.)

        d = fullHeave.stats(statsdur=10800.)
        # e = fullZacc.stats(statsdur=10800.)

        header = ['Motion', 'std', 'min', 'max']
        table = [[1, a['std'], a['min'], a['max']], [3, d['std'], d['min'], d['max']],
                 [5, b['std'], b['min'], b['max']]]
        print("--------------------------------------------------------------", file=open(print_path, "a"))
        print('namevec[k]' + ' Surge = 1, Heave = 3, Pitch = 5', file=open(print_path, "a"))
        print("---------------------------------------------------------------", file=open(print_path, "a"))
        print(''.join(column.rjust(15) for column in header), file=open(print_path, "a"))
        for row in table:
            print(''.join(f'{column:.3f}'.rjust(15) for column in row), file=open(print_path, "a"))



# gammelt
'''
            fullSurge.t, fullSurge.x = fullSurge.filter('hp', 1. / 30., twin=(100, 1e8), taperfrac=None)
            fullPitch.t, fullPitch.x = fullPitch.filter('hp', 1. / 27., twin=(100, 1e8), taperfrac=None)
            fullAcc.t, fullAcc.x = fullAcc.filter('hp', 1. / 27., twin=(100, 1e8), taperfrac=None)
            fullZacc.t, fullZacc.x = fullZacc.filter('hp', 1. / 30., twin=(100, 1e8), taperfrac=None)
            # f_sigx, tf_acc = tfe(fullWave.x, fullAcc.x, dt, clim=coherence, nperseg=8700)

            print_path = os.path.join(os.path.split(os.getcwd())[0], 'Results', nameofresults)
            a = fullSurge.stats(statsdur=10800.)
            b = fullPitch.stats(statsdur=10800.)
            c = fullAcc.stats(statsdur=10800.)

            d = fullHeave.stats(statsdur=10800.)
            e = fullZacc.stats(statsdur=10800.)

            header = ['Motion', 'std', 'min', 'max']
            table = [[1, a['std'], a['min'], a['max']], [3, d['std'], d['min'], d['max']],
                     [5, b['std'], b['min'], b['max']], [11, c['std'], c['min'], c['max']],
                     [33, e['std'], e['min'], e['max']]]
            print("--------------------------------------------------------------", file=open(print_path, "a"))
            print('namevec[k]' + ' Surge = 1, Heave = 3, Pitch = 5, Horizontal Acc = 11, vert acc = 33',
                  file=open(print_path, "a"))
            print("---------------------------------------------------------------", file=open(print_path, "a"))
            print(''.join(column.rjust(15) for column in header), file=open(print_path, "a"))
            for row in table:
                print(''.join(f'{column:.3f}'.rjust(15) for column in row), file=open(print_path, "a"))
'''



    #else:
        #print("ikke irreg")

#timeseries = client.timeseries.get("000998a6-dac6-4c51-ab46-9359518e5878")
#stddev = timeseries.standard_deviation()
#print(stddev)

'''

# finn spesifikk tidsserie på enkel måte:
campaigns = client.campaign.get_all()

print(campaigns)

#campaign_id = client.campaign.get_id("STT")
stt = client.campaign.get_by_name("STT")
#print(stt.get_tests())

#test_id = client.floater.get_id("waveIrreg_2101")
test = client.floater.get_by_name("waveIrreg_2101")
stt.populate_test(test)

timeseries = test.get_timeseries()
stt.test["waveIrreg_2101"].populate_timeseries(timeseries)

print(stt.test["waveIrreg_2101"].timeseries["M206_COG X"])

ts = stt.test["waveIrreg_2101"].timeseries["M206_COG X"]
datapoints = ts.get_data_points()
times = []
                v = []
                # Fyller inn tid og verdi fra datapunkter til en tidsvektor og verdivektor
                for datapoint in datapoints:
                    times.append(datapoint.time)
                    v.append(datapoint.value)
                # Må konvertere t-vektor til antall sekunder fra start-tiden
                times_in_array = numpy.array(times)
                start_time = times_in_array[0]
                t = []
                for ti in times_in_array:
                    t.append((ti-start_time).total_seconds())
                t = numpy.array(t)

                # Plotting
                plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
                plt.title('Timeseries')
                plt.plot(t, v)
                plt.xlabel('Time [s]')
                plt.ylabel("Amplitude (mm)")
                plt.legend(['Free Decay Test sample'], loc='upper left')
                plt.grid()
                plt.show()

                print("Test er", test.description, "og sensor er", sensor.name)'''







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
