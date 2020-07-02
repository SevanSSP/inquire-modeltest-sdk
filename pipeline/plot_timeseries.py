import matplotlib.pyplot as plt
import datetime

def plot_timeseries(datas, test, sensors):

    plt.figure()
    labels = []
    for data, sensor in zip(datas, sensors):

        for i in data.index:
            #Remove the date from timestamp
            time_string = data["time"][i].split("T")[1]
            if len(time_string) == 8:
                #If timestamp is at whole second, ex. "09:00:00"
                data.at[i, "time"] = datetime.datetime.strptime(time_string, "%H:%M:%S")
            else:
                # Timestamp, ex. "09:00:00.592"
                data.at[i, "time"] = datetime.datetime.strptime(time_string, "%H:%M:%S.%f")

        plt.plot(data["time"], data["value"], 'o', markerfacecolor='none', alpha=0.8, markersize=2, label=sensor.name)
        plt.gcf().autofmt_xdate()
        plt.ylabel(sensor.unit)

        labels.append(sensor.name)

    plt.title(f"Test: {test.description}")
    plt.legend(labels)
    plt.show()