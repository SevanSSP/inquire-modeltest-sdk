from modeltestSDK.resources import Campaign, Sensor, DataPoint, Timeseries
from modeltestSDK.client import SDKclient
import datetime
import pandas as pd
import time as TIME

def read_datapoints_from_csv_with_pandas(file, test_id,client: SDKclient):
    df = pd.read_csv(file, sep=';').head(1000)

    col_names = list(df.columns)
    for sensor in col_names[1:]:
        sensor_strip = sensor.strip()
        tic =TIME.perf_counter()
        sensor_id = client.sensor.get_id(sensor_strip)
        timeseries = client.timeseries.create(sensor_id=sensor_id,
                                test_id=test_id)
        datapoints = df[[col_names[0], sensor]].values.tolist()
        #print(col_names[0], sensor)
        for time, value in datapoints:
            datapoint = DataPoint(timeseries_id=timeseries.id,
                                  time=datetime.datetime.utcnow().isoformat(),
                                  value=value,
                                  client=client)
            timeseries.data_points.append(datapoint)
        timeseries.post_data_points()
        toc = TIME.perf_counter()
        print(f"Posting timeseries for sensor {sensor} in file {file} took  {toc - tic:0.4f} seconds")