import pandas as pd
from scipy.io import loadmat
from modeltestSDK import Test, SDKclient
import time as timer


def read_datapoints_from_mat_with_pandas(data, test: Test, client: SDKclient, skip_channels: list=None,
                                         derive_channels: dict = None):
    time = data['Time'][0].tolist()

    sensor_list = client.sensor.get_all(parameters={'campaign_id': test.campaign_id})
    sensor_pd = sensor_list.to_pandas()
    sensor_names = sensor_pd['name'].tolist()

    print(test.campaign_id)

    for name in sensor_names:
        if name in data and name not in skip_channels:
            channel_values = data[name][0].tolist()
            sensor_index = sensor_pd[sensor_pd['name'] == name].index.values
            sensor_id = sensor_pd.loc[sensor_index, 'id'].tolist()[0]

            ts = client.timeseries.create(sensor_id=sensor_id,
                                          test_id=test.id,
                                          default_start_time=1419,
                                          default_end_time=1419+3*60*60,
                                          fs=data['fs'][0][0],
                                          read_only=True)

            body = {'data': {'time': time, 'value': channel_values}}
            tic = timer.perf_counter()
            client.timeseries.post_data_points(ts.id, form_body=body)
            toc = timer.perf_counter()
            print(f"Posting timeseries for sensor {name} in test {str(data['comment'])[2:-2]} took  {toc - tic:0.4f} seconds")

        elif name not in data and name not in skip_channels:
            try:
                org_channel = derive_channels[name]['from']
                data[org_channel]
            except KeyError:
                print(f'{name} not for for test {test.number}')
            else:
                factors = derive_channels[name]['factors']

                channel_values = [element*factors[0] + factors[1] for element in data[org_channel][0].tolist()]
                sensor_index = sensor_pd[sensor_pd['name'] == name].index.values
                sensor_id = sensor_pd.loc[sensor_index, 'id'].tolist()[0]

                ts = client.timeseries.create(sensor_id=sensor_id,
                                              test_id=test.id,
                                              default_start_time=1419,
                                              default_end_time= 1419+3*60*60,
                                              fs=data['fs'][0][0],
                                              read_only=True)

                body = {'data': {'time': time, 'value': channel_values}}

                tic = timer.perf_counter()
                client.timeseries.post_data_points(ts.id, form_body=body)
                toc = timer.perf_counter()
                print(
                    f"Posting timeseries for sensor {name} in test {str(data['comment'])[2:-2]} took  {toc - tic:0.4f} seconds")


            #Todo: timeseries tags?



def read_wave_calibration_from_mat_with_pandas(data, test: Test, calibration_sensors: list, client: SDKclient):
    time = data['Time'][0].tolist()

    for sensor_name in calibration_sensors:
        channel_values = data[sensor_name][0].tolist()

        sensor = client.sensor.get_by_name(sensor_name[0:-4])

        ts = client.timeseries.create(sensor_id=sensor.id,
                                      test_id=test.id,
                                      default_start_time=1419,
                                      default_end_time=1419 + 3 * 60 * 60,
                                      fs=data['fs'][0][0],
                                      read_only=True)

        body = {'data': {'time': time, 'value': channel_values}}
        client.timeseries.post_data_points(ts.id, form_body=body)

    channel_values = data['WAVE_3_CAL'][0].tolist()
    sensor = client.sensor.get_by_name('WAVE_3_Sevan')

    ts = client.timeseries.create(sensor_id=sensor.id,
                                  test_id=test.id,
                                  default_start_time=1419,
                                  default_end_time=1419 + 3 * 60 * 60,
                                  fs=data['fs'][0][0],
                                  read_only=True)

    body = {'data': {'time': time, 'value': channel_values}}
    client.timeseries.post_data_points(ts.id, form_body=body)


'''

client = SDKclient()

floater_config_names = client.floater_config.get_all().to_pandas()['name'].tolist()
print(floater_config_names)

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