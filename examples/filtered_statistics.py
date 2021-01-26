from modeltestSDK import Client
import numpy
from qats.ts import TimeSeries
import os
import matplotlib.style as mplstyle
mplstyle.use('fast')


client = Client()

campaign = client.campaign.get_by_name("STT")
tests = ["waveIrreg_2101", "waveIrreg_2102", "waveIrreg_2103", "waveIrreg_2104", "waveIrreg_2105"]
sensor_names = ["M206_COF X", "M206_COF Z", "M206_COF Pitch", "M206_acc_pos X", "M206_acc_pos Z"]
coherence = 0.7
results_file = "statistics_SWACH.txt"
print_path = os.path.join(os.path.split(os.getcwd())[0], results_file)

for test_name in tests:
    test = client.floater.get_by_name(test_name)
    campaign.populate_test(test)
    test.populate_timeseries(test.get_timeseries())

    for sensor_name in sensor_names:
        ts = campaign.test[test_name].timeseries[sensor_name]
        ts.get_data_points()
        print("Hentet datapoints for", sensor_name)

        t0, X0 = ts.get_froude_scaled_arrays()
        zipped_lists = zip(t0, X0)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        t, X = [numpy.array(tuple) for tuple in tuples]

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
