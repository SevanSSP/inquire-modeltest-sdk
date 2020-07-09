import matplotlib.pyplot as plt
import datetime



def plot_timeseries(datas, test, sensors):

    plt.figure(1, figsize=(20, 6), facecolor='w', edgecolor='k')
    labels = []
    for data, sensor in zip(datas, sensors):

        time = []
        start_time = data["time"].iloc[0]

        for i in data.index:
            time.append((data["time"][i] - start_time).total_seconds())

        # Temporary fix to issue where points are not delivered in order.
        x2, y2 = zip(*sorted(zip(time, data["value"]), key=lambda x: x[0]))

        plt.plot(x2, y2, markerfacecolor='none', alpha=0.8, markersize=2, label=sensor.name)
        #plt.gcf().autofmt_xdate()
        plt.ylabel(sensor.unit)
        labels.append(sensor.name)

    plt.title(f"Test: {test.description}")
    plt.legend(labels, loc='upper right')
    plt.show()