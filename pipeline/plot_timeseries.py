import matplotlib.pyplot as plt
import numpy


def plot_timeseries(datas, test, sensors):
    plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
    labels = []
    for data, sensor in zip(datas, sensors):

        # Temporary fix to issue where points are not delivered in order.
        x2, y2 = zip(*sorted(zip(data["time"], data["value"]), key=lambda x: x[0]))
        # x-verdiene gis som en liste med strings istedet for floats. det burde fikses så man slipper å endre det her
        x3 = []
        for x in x2:
            x3.append(float(x))
        j=-1
        for i in x3:
            if i < j:
                print(i)
            j = i
        zipped_lists = zip(x3, y2)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        times, values = [numpy.array(tuple) for tuple in tuples]
        plt.plot(times, values, markerfacecolor='none', alpha=0.8, markersize=2, label=sensor.name)
        # plt.gcf().autofmt_xdate()
        plt.xlabel('Time [s]')
        plt.ylabel(sensor.kind + ' [' + sensor.unit + ']')
        labels.append(sensor.name)

    plt.title(f"Test: {test.description}")
    plt.legend(labels, loc='upper right')
    # plt.xticks([])
    plt.show()
