from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration, Timeseries, Sensor
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
import time
import aiohttp
import asyncio

from pipeline.plot_timeseries import plot_timeseries

import time
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from modeltestSDK.utils import to_datetime_string
mplstyle.use('fast')


client = SDKclient()


campaigns = client.campaign.get_all()


tic = time.perf_counter()

stt = client.campaign.get("49627a4c-9b8e-4eb4-816a-2d252be6b961")



test = client.floater.get("eb4e6456-4a85-472b-91fe-21689c5201a2")

print(test.get_timeseries())

ts = client.timeseries.get_data_points("bdef448e-d924-4cce-9ca5-cfb601e5f0a8")

timeseries = client.timeseries.get("bdef448e-d924-4cce-9ca5-cfb601e5f0a8")

sensor1 = client.sensor.get(timeseries.sensor_id)

data1 = ts.to_pandas()#.head(5000)

toc1 = time.perf_counter()

ts = client.timeseries.get_data_points("ea1a2f9b-bc65-4ed6-8d96-25090768e7d3")

timeseries = client.timeseries.get("ea1a2f9b-bc65-4ed6-8d96-25090768e7d3")

sensor2 = client.sensor.get(timeseries.sensor_id)

data2 = ts.to_pandas()

toc2 = time.perf_counter()

print(f"Query 1 took {toc1-tic:0.4f} seconds")
print(f"Query 2 took {toc2-toc1:0.4f} seconds")

plot_timeseries([data1,data2], test, [sensor1,sensor2])

#stt.test[10].timeseries[0].to_pandas()



'''
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
'''