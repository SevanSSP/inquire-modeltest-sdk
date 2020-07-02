from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration, Timeseries
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
import time
import aiohttp
import asyncio

import time
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from modeltestSDK.utils import to_datetime_string
mplstyle.use('fast')


client = SDKclient()


campaigns = client.campaign.get_all()

tic = time.perf_counter()

stt = client.campaign.get("fc1d9764-3a0d-46ac-ad26-301768ef0fed")

test = client.floater.get("fe7ba2aa-5c6d-4268-8ff3-3d171a4b6422")

print(test.get_timeseries())

ts = client.timeseries.get_data_points("ee4c545f-aee6-459c-9af2-12e38b07016e")



data = ts.to_pandas()#.head(250)


print(data)

for time in data["time"]:
    time = to_datetime_string(time)


plt.figure()

plt.scatter(data["time"], data["value"])

toc = time.perf_counter()
print(f"Query took {toc-tic:0.4f} seconds")

plt.show()


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