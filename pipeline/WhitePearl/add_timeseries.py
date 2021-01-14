from scipy.io import loadmat
import datetime
from modeltestSDK.client import SDKclient

import pandas as pd


def read_datapoints_from_csv_with_pandas(data, test: Test, client: SDKclient):
    time = data['time'][0]

    sensor_list = client.sensor.get_all(parameters={'campaign_id': test.campaign_id})
    sensor_pd = sensor_list.to_pandas()
    sensor_names = sensor_pd['name'].tolist()

    for name in sensor_names:
        channel_values = data[name][0]
        sensor_id = None  # Todo: Find sensor_id corresponding to name in sensor_pd

        ts = client.timeseries.create(sensor_id=sensor_id,
                                      test_id=test.id,
                                      default_start_time=0,
                                      default_end_time=100,
                                      read_only=True)

        body = {'timeseries_id': ts.id, 'data': {'time': time, 'value': channel_values}}
        client.post(resource='timeseries', endpoint=f'{ts.id}/data', body=body)

'''

client = SDKclient()

test = client.test.get("66c7dd9d-cfd1-4eb6-9575-c6f0974b0321")

read_datapoints_from_csv_with_pandas("", test,client)'''

client = SDKclient()
sensor_list = client.sensor.get_all()
sensor_pd = sensor_list.to_pandas()
sensor_names = sensor_pd['name'].tolist()

print(sensor_pd)

# mat = loadmat('C:/Users/jen.SEVAN/Documents/505 Stockman FPU_2008/Analysis/Timeseries/IrrWave/test3190.mat')
data = loadmat('C:/Users/jen.SEVAN/Documents/505 Stockman FPU_2008/Analysis/Timeseries/Decay/test1150.mat')

test_date_str = str(data['test_date'])[2:-2]
test_date = datetime.datetime.strptime(test_date_str, '%H:%M %d/%m/%y')

print(data['Time'][0][1])
