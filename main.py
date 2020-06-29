from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
from modeltestSDK.utils import from_datetime_string
from typing import List
client = SDKclient()


campaign = client.campaign.get(id="c4c623c2-b0e8-46d2-906d-767efddeda94")
sensor = client.sensor.get(id="9f16eada-423e-4e98-be93-479857730639")
test_id = "df60063d-4847-4361-8b90-fe9c8515a5ed"

timeseries = client.timeseries.create(test_id=test_id, sensor_id=sensor.id)
lst = list()
for i in range(100):
    lst.append(DataPoint(timeseries_id=timeseries.id, time=str(datetime.datetime.now()),
                          value=i, client=client).dump())

print(client.timeseries.post_data_points(body=lst, id=timeseries.id))


# print(campaign.get(campaign.get_id("SDKlasse")))
# print(campaign.get_sensors(campaign.get_id("SDKlasse")))
# print(sensors.get(sensors.get_id("MK206")))
# print(campaign.get_tests(campaign.get_id("SDKlasse")))
# print(campaign.get_all())
