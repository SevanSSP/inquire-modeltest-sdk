from modeltestSDK import SDKclient

client = SDKclient()

campaign_name = "STT"
test_name = "X300"
sensor_name = "M206_COG"
dof = ["X", "Y", "Z", "Roll", "Pitch", "Yaw"]

sensors = []
for i in dof:
    sensors.append(sensor_name + " " + i)

campaign = client.campaign.get_by_name(campaign_name)
v2_test = campaign.get_tests(type='floater')[test_name]
all_timeseries = v2_test.get_timeseries()

curr_timeseries = [all_timeseries[sensor] for sensor in sensors]

for timeseries in curr_timeseries:
    timeseries.get_data_points()

dof_dict = dict.fromkeys(dof)
times, X = curr_timeseries[0].to_arrays()
Y = curr_timeseries[0].to_arrays()[1]
Z = curr_timeseries[0].to_arrays()[1]
Roll = curr_timeseries[0].to_arrays()[1]
Pitch = curr_timeseries[0].to_arrays()[1]
Yaw = curr_timeseries[0].to_arrays()[1]

print(X, Z, Y)