from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
client = SDKclient()


floaterList = client.floater.get_all()
sensor = client.sensor.get_all()[0]
print(floaterList)
print("GET ", client.floater.get(id="4392d23a-e54f-4f80-b3b1-2c02923b1e11"))
floater = floaterList[0]
print(floater)
print(floater.get_campaign())
print(floater.get_timeseries())

timeseries = client.timeseries.create(test_id=floater.id, sensor_id=sensor.id)
print(timeseries)
for i in range(130000):
    timeseries.data_points.append(DataPoint(timeseries_id=timeseries.id, time=str(datetime.datetime.now()),
                          value=random.uniform(0, 10000), client=client))

print(timeseries.post_data_points())

