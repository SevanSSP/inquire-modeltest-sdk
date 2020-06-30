from modeltestSDK.resources import Campaign, Sensor, DataPoint, Timeseries
from modeltestSDK.client import SDKclient
import pandas as pd


def read_datapoints_from_csv_with_pandas(file, test_id):
    df = pd.read_csv(file, sep=';')

    col_names = list(df.columns)
    for sensor in col_names[1:]:
        timeseries = Timeseries(sensor_id='sensor_id',  # må finne riktig sensor id
                                test_id=test_id)
        datapoints = df[[col_names[0], sensor]].values.tolist()
        print(col_names[0], sensor)
        for time, value in datapoints:
            datapoint = DataPoint(timeseries_id=timeseries.id,
                                  time=time,
                                  value=value)
            timeseries.datapoints.append(datapoint)
            print('time:', time, 'value:', value)