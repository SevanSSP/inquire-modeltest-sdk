from modeltestSDK import SDKclient
from pipeline.plot_timeseries import plot_timeseries

client = SDKclient()

campaign_name = "STT"
test_names = ["waveReg_1102", "waveReg_1103", "waveReg_1104", "waveReg_1105"]
sensor_name = "M206_COG Z"

campaign = client.campaign.get_by_name(campaign_name)
tests = campaign.get_tests(type="floater")

for name in test_names:
    campaign.populate_test(tests[name])

print(campaign.test)

data =[]
sensors = []
for test_name in test_names:
    ts = campaign.test[test_name].get_timeseries()[sensor_name]

    #ts = campaign.test[test_name].populate_timeseries(ts[sensor_name])

    data.append(ts.get_data_points().to_pandas())

    sensors.append(ts.get_sensor())

plot_timeseries(data, campaign.test[0], sensors)