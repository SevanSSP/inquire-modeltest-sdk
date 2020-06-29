from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
from modeltestSDK.utils import from_datetime_string
from typing import List
client = SDKclient()


floaterList = client.floater.get_all()
sensor = client.sensor.get_all().resources[0]
print(floaterList)
floater = floaterList.resources[0]
print(floater)
print(floater.get_campaign())
print(floater.get_timeseries())

timeseries = client.timeseries.create(test_id=floater.id, sensor_id=sensor.id)
print(timeseries)
for i in range(100):
    timeseries.data_points.append(DataPoint(timeseries_id=timeseries.id, time=str(datetime.datetime.now()),
                          value=i, client=client))
print(timeseries.post_data_points())

