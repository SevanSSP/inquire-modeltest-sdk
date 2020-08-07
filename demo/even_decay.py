import os
import matplotlib.pyplot as plt
import numpy as np
from qats.readers import tdms
from qats.ts import TimeSeries, average_frequency
from qats.signal import find_maxima, smooth
from qats import TsDB
from scipy.optimize import curve_fit
from scipy.integrate import odeint
import time
# Input field: Write the names for the test to be tested.

start = time.perf_counter()

name = "test" #"surge", "heave", "moored_heave", "pitch" or "moored_pitch"
sf = 75
#dt = 0.01
n_tests = 3 # Number of decay tests in model test base file. If more than 1, the script will produce plots for all
            # individual tests but also print out a txt. file with averaged natural periods and coefficients.
db = TsDB()

if name == "surge":
    n_name = "*M207_COF X"
    f = ['Recorded Data_Y200.tdms']
    t_dur = 35  # Time-interval for each test in the decay-test.
elif name == "heave":
    n_name = "*M207_COF Z"
    f = ['Recorded Data_Y300.tdms']
    t_dur = 12  # Time-interval for each test in the decay-test.
elif name == "pitch":
    n_name = "*M207_COF Pitch"
    f = ['Recorded Data_Y301.tdms']
    t_dur = 25  # Time-interval for each test in the decay-test.
elif name == "moored_heave":
    n_name = "*M207_COF Z"
    f = ['Recorded Data_Y300_moored.tdms']
    t_dur = 12  # Time-interval for each test in the decay-test.
elif name == "moored_pitch":
    n_name = "*M207_COF Pitch"
    f = ['Recorded Data_Y301_moored.tdms']
    t_dur = 15  # Time-interval for each test in the decay-test.
elif name == "test":
    n_name = "*M206_COF X"
    f = ['Recorded Data_waveIrreg_2101.tdms']
    t_dur = 35  # Time-interval for each test in the decay-test.

# Reads in the file as a db for further work
file_path = os.path.join(os.path.split(os.getcwd())[0], os.path.split(os.getcwd())[1], 'demo\data', f[0])
db.load(file_path, read=True)

# Reads in the relevant time-signal for further work and finds the maxima during the decay test.
t,X = db.geta(name=n_name)

maxima, indices = find_maxima(X, retind=True)

plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
plt.title('Timeseries')
plt.plot(t, X)
plt.xlabel('Time [s]')
plt.ylabel("Amplitude (mm)")
plt.legend(['Free Decay Test sample'], loc='upper left')
plt.grid()


Tn = []


# Defines relevant durations for the decay tests. Also obtains an average Tn-value for the test in question.
i = 1
t1 = t[indices[-i]]
t2 = t1+t_dur
maxima, indices2 = find_maxima(X[(t1 < t) & (t <= t2)],retind=True)
Tn = np.mean(t[indices2[0:-2]]-t[indices2[1:-1]])

print("--------------------------------- OLD VERSION ---------------------------------")
print("Periods between maximas are: ")
print(t[indices2[0:-2]] - t[indices2[1:-1]])
print("Number of oscillations observed is", len(t[indices2[0:-2]] - t[indices2[1:-1]]))

print("Natural period for modeltest is", Tn, "seconds")
print("Full scale natural period is", Tn * np.sqrt(sf), "seconds")
end = time.perf_counter()
print("TOTAL COMPUTING TIME: ", end-start)

plt.show()

