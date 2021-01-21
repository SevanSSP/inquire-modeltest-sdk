from .. import SDKclient
from ..plot_timeseries import plot_timeseries

client = SDKclient()


campaign_name = "STT"
test_name = "waveIrreg_2102"
sensor_name = "M206_COG Z"

"""
__________________________________ EXAMPLE 1 _________________________________________________

Find a timeseries by campaign, test and sensor
Populates are optional, but can be useful when working with large sets of data from a campaign.
Both versions below print same result

V1: with populate

"""



# Get overarching campaign
v1_campaign = client.campaign.get_by_name(campaign_name)

# Find test
test = v1_campaign.get_tests(type='floater')[test_name]
v1_campaign.populate_test(test)

# Find timeseries
timeseries = v1_campaign.test[test_name].get_timeseries()[sensor_name]
v1_campaign.test[test_name].populate_timeseries(timeseries)

# Get datapoints for timeseries
v1_campaign.test[test_name].timeseries[sensor_name].get_data_points()
# campaign.test[0].timeseries[0].get_data_points()


"""
V2: Without populate

"""

# Get overarching campaign
campaign = client.campaign.get_by_name(campaign_name)

# Find test. Notice the indexing by name.
v2_test = campaign.get_tests(type='floater')[test_name]

# Find timeseries
v2_timeseries = v2_test.get_timeseries()[sensor_name]

# Get datapoints for timeseries
v2_timeseries.get_data_points()


"""
Results:
"""
print("____ EXAMPLE 1, V1 ____: \n", v1_campaign.test[test_name].timeseries[sensor_name], "\n")
print("____ EXAMPLE 1, V2 ____: \n", v2_timeseries, "\n")



"""
__________________________________ EXAMPLE 2 _________________________________________________

Print all tests and sensors

"""

campaign = client.campaign.get_by_name(campaign_name)

testList = campaign.get_tests()
sensorList = campaign.get_sensors()
print("____ EXAMPLE 2 ____: \n", testList, "\n", sensorList)



"""
__________________________________ EXAMPLE 3 _________________________________________________

Plot a timeseries. (Timeseries found using example 1)

"""

#sensorList = [v2_timeseries.get_sensor()]
#datas = [v2_timeseries.data_points.to_pandas()]

plot_timeseries(v2_timeseries)  # datas=datas, test=v2_test, sensorList=sensorList)


"""
__________________________________ EXAMPLE 4 _________________________________________________

Plot multiple timeseries. 

"""

sensor_names = ["M206_COG Z", "M206_COG Y", "M206_COG X"]

# Get overarching campaign
campaign = client.campaign.get_by_name("STT")

# Find test. Notice the indexing by name.
test_name = "waveIrreg_2102"
test = campaign.get_tests(type='floater')[test_name]

test.populate_timeseries(test.get_timeseries())

timeseries_list = []
for sensor_name in sensor_names:

    timeseries = test.timeseries[sensor_name]
    timeseries.get_data_points()
    timeseries_list.append(timeseries)

plot_timeseries(timeseries_list)
