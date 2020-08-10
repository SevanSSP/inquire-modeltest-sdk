from modeltestSDK import SDKclient
from modeltestSDK.plot_timeseries import plot_timeseries

client = SDKclient()

campaign_name = "STT"
test_names = ["waveReg_1102"]
sensor_name = "M206_COG Z"

campaign = client.campaign.get_by_name(campaign_name)
tests = campaign.get_tests(type="floater")

for name in test_names:
    campaign.populate_test(tests[name])

print(campaign.test)
timeseries_list = []

for test_name in test_names:
    ts = campaign.test[test_name].get_timeseries()[sensor_name]

    timeseries_list.append(ts)

plot_timeseries(timeseries_list)
