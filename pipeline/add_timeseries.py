from modeltestSDK.resources import Campaign, Sensor, DataPoint, Timeseries
from modeltestSDK.client import SDKclient
import datetime
import pandas as pd
import time as timer


def str_to_datetime(s):
    if len(s) == 8:
        hour = int(s[0:2])
        min = int(s[3:5])
        sec = int(s[6:8])
        return datetime.datetime(year=1900, month=1, day=1, hour=hour, minute=min, second=sec)
    else:
        hour = int(s[0:2])
        min = int(s[3:5])
        sec = int(s[6:8])
        ms = int(s[9:15])
        return datetime.datetime(year=1900, month=1, day=1, hour=hour, minute=min, second=sec, microsecond=ms)


# Create timeseries for every sensor that was used for a test, by reading the .csv file
def read_datapoints_from_csv_with_pandas(file, test_id, client: SDKclient):
    df = pd.read_csv(file, sep=';')

    col_names = list(df.columns)

    # Iterate through sensor names that are found in the top row of the .csv file
    for sensor in col_names[1:]:
        sensor_strip = sensor.strip()

        tic = timer.perf_counter()

        sensor_id = client.sensor.get_id(sensor_strip)
        timeseries = client.timeseries.create(sensor_id=sensor_id,
                                              test_id=test_id)

        datapoints = df[[col_names[0], sensor]].values.tolist()
        start_time, start_value = datapoints[0]
        start_time = str_to_datetime(start_time)

        for time, value in datapoints:
            # Skip adding nan values in .csv file
            if pd.isna(value):
                continue
            time_point = str_to_datetime(time)

            datapoint = DataPoint(timeseries_id=timeseries.id,
                                  time=(time_point - start_time).total_seconds(),
                                  value=value,
                                  client=client)
            timeseries.data_points.append(datapoint)

        # Post all datapoints for a single timeseries at the same time with post_data_points() for faster uploading
        timeseries.post_data_points()

        toc = timer.perf_counter()
        print(f"Posting timeseries for sensor {sensor} in file {file} took  {toc - tic:0.4f} seconds")
