from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
import time
import aiohttp
import asyncio


client = SDKclient()



#timeseries = client.timeseries.get(id="80f13ab3-82f0-45c2-b133-08a9ae22cfb2")

#print(timeseries)
#print("TEST")


#print(len (timeseries.get_data_points()))


timeseries = client.timeseries.get(id="b893da62-d5dc-4e92-b281-edac22223b26")
time1 = time.time()

print(len(timeseries.get_data_points()), "TEST")

time2 = time.time()
full_time = (time2 - time1) * 1000.0
print(f'function took {full_time} milliseconds')




timeseries = client.timeseries.create(test_id="bee124c3-3d25-4fdd-8e22-e33ef8ecd17c",
                                      sensor_id="0c0e130d-d370-4cd2-8709-961c8dd74b8c")

time1 = time.time()
lst=()
print(timeseries.id, "TIMESERIESID")
for i in range(130000):
    timeseries.data_points.append(DataPoint(timeseries_id=timeseries.id, time=str(datetime.datetime.now()),
                          value=random.uniform(0, 10000), client=client))

#data = asyncio.get_event_loop().run_until_complete(multiple_tasks(client, body=timeseries.data_points.dump()[0:10000]))

print(timeseries.post_data_points())

time2 = time.time()

full_time = (time2 - time1) * 1000.0
print(f'function took {full_time} milliseconds')
