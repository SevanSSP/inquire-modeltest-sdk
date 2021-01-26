from modeltestSDK import Client
from modeltestSDK.plot_timeseries import plot_timeseries


client = Client()

campaign_name = "STT"
test_names = ["waveReg_1102"]
sensor_name = "M206_COG Z"

campaign = client.campaign.get_by_name(campaign_name)
tests = campaign.get_tests(type="floatertest")

for name in test_names:
    campaign.populate_test(tests[name])

print(campaign.test)
timeseries_list = []

for test_name in test_names:
    ts = campaign.test[test_name].get_timeseries()[sensor_name]

    timeseries_list.append(ts)

plot_timeseries(timeseries_list)

'''
campaigns = client.campaign.get_all()
print(campaigns)

sensor = client.sensor.get_by_name("termometer")

sensors = client.sensor.get_all()

print(sensors)

campaign = client.campaign.get_by_name("STT")

print (campaign)

tag1 = client.tag.create('Tagz', 'Test tag', '')
'''
'''
ts = client.timeseries.get_all()

#test = client.timeseries.get_data_points(id='68fdd5bc-a279-4908-9acc-4672c0da9836')

time = [random.randrange(0, 10000) for iter in range(10000)]
value = [random.randrange(0, 100) for iter in range(10000)]
ts_id ='f569c513-a939-4bbe-9a61-1c4bab103c05'

body={}
body['timeseries_id'] = ts_id
body['data'] = {'time': time, 'value': value}

print(body)
res = client.post(resource='timeseries', endpoint=f'{ts_id}/data', body=body)
print(res)

res = client.get(resource='timeseries', endpoint=f'{ts_id}/data')
print(res)

'''