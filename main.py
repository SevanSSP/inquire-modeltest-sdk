from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
from modeltestSDK.utils import from_datetime_string
from typing import List
client = SDKclient()


campaign = client.campaign.get(id="7e763374-4cc0-4cfe-b79c-674bec485315")
print(campaign.get_tests(type="floater"))
print(client.test.get_all())

# timeseries = client.timeseries.create(test_id=test_id, sensor_id=sensorList.resources[0].)
# print(timeseries)
# for i in range(100):
#     timeseries.data_points.append(DataPoint(timeseries_id=timeseries.id, time=str(datetime.datetime.now()),
#                           value=i, client=client))
#
# print(timeseries.post_data_points())


# print(campaign.get(campaign.get_id("SDKlasse")))
# print(campaign.get_sensors(campaign.get_id("SDKlasse")))
# print(sensors.get(sensors.get_id("MK206")))
# print(campaign.get_tests(campaign.get_id("SDKlasse")))
# print(campaign.get_all())
