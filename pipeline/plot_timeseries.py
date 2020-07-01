import matplotlib.pyplot as plt
import datetime

def plotTS(datas, test, sensors):

    plt.figure()
    labels = []
    for data, sensor in zip(datas, sensors):

        for i in data.index:
            timeS = data["time"][i].split("T")[1]
            if len(timeS) == 8:
                data.at[i, "time"] = datetime.datetime.strptime(timeS, "%H:%M:%S")
            else:
                data.at[i, "time"] = datetime.datetime.strptime(timeS, "%H:%M:%S.%f")

        plt.plot(data["time"], data["value"], 'o', markerfacecolor='none', alpha=0.8, markersize=2, label=sensor.name)
        plt.gcf().autofmt_xdate()
        plt.ylabel(sensor.unit)

        labels.append(sensor.name)

    plt.title(f"Test: {test.description}")
    plt.legend(labels)
    plt.show()