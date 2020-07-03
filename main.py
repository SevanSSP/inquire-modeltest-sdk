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

#print(campaigns)

#campaign_id = client.campaign.get_id("STT")
stt = client.campaign.get_by_name("STT")
print(stt.get_tests())

#test_id = client.floater.get_id("waveIrreg_2101")
test = client.floater.get_by_name("waveIrreg_2101")
stt.populate_test(test)

#print(stt.test)

#print(client.wave_current_calibration.get(test.wave_id))

#print(test.get_timeseries())

timeseries = test.get_timeseries()
stt.test["waveIrreg_2101"].populate_timeseries(timeseries)

print(stt.test["waveIrreg_2101"].timeseries["M206_COG X"])

timeseries = timeseries.to_pandas()

data =[]
sensors = []
for i in range(5):
    timeseries_id = timeseries["id"][i]
    ts = client.timeseries.get(timeseries_id)
    timeseries_data = ts.get_data_points().to_pandas()
    sensor = client.sensor.get(ts.sensor_id)
    data.append(timeseries_data)
    sensors.append(sensor)

plot_timeseries(data, test, sensors)

'''
ts = client.timeseries.get_data_points("b377256e-665b-41f9-be97-942f99ec7524")

timeseries = client.timeseries.get("b377256e-665b-41f9-be97-942f99ec7524")

sensor1 = client.sensor.get(timeseries.sensor_id)

data1 = ts.to_pandas()#.head(5000)

toc1 = time.perf_counter()

ts = client.timeseries.get_data_points("ff253475-dd0f-4b0b-9eeb-f548d2700885")

timeseries = client.timeseries.get("ff253475-dd0f-4b0b-9eeb-f548d2700885")

sensor2 = client.sensor.get(timeseries.sensor_id)

data2 = ts.to_pandas()

toc2 = time.perf_counter()

print(f"Query 1 took {toc1-tic:0.4f} seconds")
print(f"Query 2 took {toc2-toc1:0.4f} seconds")

plot_timeseries([data1,data2], test, [sensor1,sensor2])

#stt.test[10].timeseries[0].to_pandas()

'''

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