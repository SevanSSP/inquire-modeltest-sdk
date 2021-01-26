from modeltestSDK import Test, SDKclient
import time as timer


def read_datapoints(data, test: Test, client: SDKclient, skip_channels: list = [],
                    derive_channels: dict = {}):
    time = data['Time'][0].tolist()

    sensor_list = client.sensor.get_all(filter_by=[client.filter.sensor.campaign_id == test.campaign_id])
    sensor_pd = sensor_list.to_pandas()
    sensor_names = sensor_pd['name'].tolist()

    for name in sensor_names:
        if name in data and name not in skip_channels:
            channel_values = data[name][0].tolist()
            sensor_index = sensor_pd[sensor_pd['name'] == name].index.values
            sensor_id = sensor_pd.loc[sensor_index, 'id'].tolist()[0]

            ts = client.timeseries.create(sensor_id=sensor_id,
                                          test_id=test.id,
                                          default_start_time=1419,
                                          default_end_time=1419 + 3 * 60 * 60,
                                          fs=data['fs'][0][0],
                                          read_only=True)

            body = {'data': {'time': time, 'value': channel_values}}
            tic = timer.perf_counter()
            client.timeseries.post_data_points(ts.id, form_body=body)
            toc = timer.perf_counter()
            print(
                f"Posting timeseries for sensor {name} in test {str(data['comment'])[2:-2]} took {toc - tic:0.4f}s")

        elif name not in data and name not in skip_channels:
            if name in derive_channels:
                org_channel = derive_channels[name]['from']
                if org_channel in data:
                    factors = derive_channels[name]['factors']

                    channel_values = [element * factors[0] + factors[1] for element in data[org_channel][0].tolist()]
                    sensor_index = sensor_pd[sensor_pd['name'] == name].index.values
                    sensor_id = sensor_pd.loc[sensor_index, 'id'].tolist()[0]

                    ts = client.timeseries.create(sensor_id=sensor_id,
                                                  test_id=test.id,
                                                  default_start_time=1419,
                                                  default_end_time=1419 + 3 * 60 * 60,
                                                  fs=data['fs'][0][0],
                                                  read_only=True)

                    body = {'data': {'time': time, 'value': channel_values}}

                    tic = timer.perf_counter()
                    client.timeseries.post_data_points(ts.id, form_body=body)
                    toc = timer.perf_counter()
                    print(
                        f"Posting timeseries for sensor {name} in test {str(data['comment'])[2:-2]} took  {toc - tic:0.4f} seconds")

            # Todo: timeseries tags?
