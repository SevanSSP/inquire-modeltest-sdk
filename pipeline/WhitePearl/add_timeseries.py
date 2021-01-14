from scipy.io import loadmat
from modeltestSDK import Campaign, Test, SDKclient

import pandas as pd

def read_datapoints_from_csv_with_pandas(file, test, client: SDKclient):

    mat = loadmat('')

    sensor_list = client.sensor.get_all(parameters={'campaign_id': test.campaign_id})
    sensor_pd = sensor_list.to_pandas()
    sensor_names = sensor_pd['name']

    for name in sensor_names:
        print(name)



client = SDKclient()

test = client.test.get("66c7dd9d-cfd1-4eb6-9575-c6f0974b0321")

read_datapoints_from_csv_with_pandas("", test,client)