import pandas as pd
from scipy.io import loadmat
from modeltestSDK import Test, SDKclient
import time as timer


def read_datapoints_from_mat_with_pandas(data, test: Test, client: SDKclient):
    time = data['Time'][0].tolist()

    sensor_list = client.sensor.get_all(parameters={'campaign_id': test.campaign_id})
    sensor_pd = sensor_list.to_pandas()
    sensor_names = sensor_pd['name'].tolist()

    for name in sensor_names:
        if name in data:
            channel_values = data[name][0].tolist()
            sensor_index = sensor_pd[sensor_pd['name'] == name].index.values
            sensor_id = sensor_pd.loc[sensor_index, 'id'].tolist()[0]

            ts = client.timeseries.create(sensor_id=sensor_id,
                                          test_id=test.id,
                                          default_start_time=180,
                                          default_end_time=100,
                                          fs=data['fs'][0][0],
                                          read_only=True)

            body = {'timeseries_id': ts.id, 'data': {'time': time, 'value': channel_values}}
            tic = timer.perf_counter()
            client.timeseries.post_data_points(ts.id, form_body=body)
            toc = timer.perf_counter()
            print(f"Posting timeseries for sensor {name} in test {str(data['comment'])[2:-2]} took  {toc - tic:0.4f} seconds")

'''

client = SDKclient()

test = client.test.get("66c7dd9d-cfd1-4eb6-9575-c6f0974b0321")

read_datapoints_from_csv_with_pandas("", test,client)

client = SDKclient()
sensor_list = client.sensor.get_all()
sensor_pd = sensor_list.to_pandas()
sensor_names = sensor_pd['name'].tolist()

index = sensor_pd[sensor_pd['name']=='M206_COG Z'].index.values
print(sensor_pd)
print(sensor_pd.loc[index, 'id'].tolist()[0])


# mat = loadmat('C:/Users/jen.SEVAN/Documents/505 Stockman FPU_2008/Analysis/Timeseries/IrrWave/test3190.mat')
data = loadmat('C:/Users/jen.SEVAN/Documents/505 Stockman FPU_2008/Analysis/Timeseries/Decay/test1150.mat')

test_description = str(data['comment'])[2:-2]
print(test_description)

'''