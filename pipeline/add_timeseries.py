from modeltestSDK.resources import Campaign, Sensor, DataPoint, Timeseries
from modeltestSDK.client import SDKclient
import datetime
import pandas as pd
import time as timer


def read_datapoints_from_csv_with_pandas(file, test_id, client: SDKclient):
    df = pd.read_csv(file, sep=';')

    col_names = list(df.columns)
    for sensor in col_names[1:]:
        sensor_strip = sensor.strip()
        tic = timer.perf_counter()
        sensor_id = client.sensor.get_id(sensor_strip)
        timeseries = client.timeseries.create(sensor_id=sensor_id,
                                              test_id=test_id)
        datapoints = df[[col_names[0], sensor]].values.tolist()
        start_time, start_value = datapoints[0]
        start_time = datetime.datetime.strptime(start_time, "%H:%M %S.%f").isoformat()

        time_string = start_time.split("T")[1]
        if len(time_string) == 8:
            # If timestamp is at whole second, ex. "09:00:00"
            start_time = datetime.datetime.strptime(time_string, "%H:%M:%S")
        else:
            # Timestamp, ex. "09:00:00.592"
            start_time = datetime.datetime.strptime(time_string, "%H:%M:%S.%f")

        for time, value in datapoints:
            if pd.isna(value):
                continue

            datapoint_time = datetime.datetime.strptime(time, "%H:%M %S.%f").isoformat()

            time_string = datapoint_time.split("T")[1]
            if len(time_string) == 8:
                # If timestamp is at whole second, ex. "09:00:00"
                time_point = datetime.datetime.strptime(time_string, "%H:%M:%S")
            else:
                # Timestamp, ex. "09:00:00.592"
                time_point = datetime.datetime.strptime(time_string, "%H:%M:%S.%f")

            # print("Time: ", time_point, "Start time: ", start_time, "Total seconds: ", (time_point-start_time).total_seconds())

            datapoint = DataPoint(timeseries_id=timeseries.id,
                                  time=(time_point - start_time).total_seconds(),
                                  value=value,
                                  client=client)
            timeseries.data_points.append(datapoint)
        timeseries.post_data_points()
        toc = timer.perf_counter()
        print(f"Posting timeseries for sensor {sensor} in file {file} took  {toc - tic:0.4f} seconds")
