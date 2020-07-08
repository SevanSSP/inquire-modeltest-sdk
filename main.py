from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration, Timeseries, Sensor
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
import time
import asyncio

from pipeline.plot_timeseries import plot_timeseries

import time
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from modeltestSDK.utils import to_datetime_string
mplstyle.use('fast')


client = SDKclient()

'''
campaigns = client.campaign.get_all()




tic = time.perf_counter()

#print(campaigns)

#campaign_id = client.campaign.get_id("STT")
stt = client.campaign.get_by_name("STT")
print(stt.get_tests())

#test_id = client.floater.get_id("waveIrreg_2101")
test = client.floater.get_by_name("waveIrreg_2101")
stt.populate_test(test)

timeseries = test.get_timeseries()
stt.test["waveIrreg_2101"].populate_timeseries(timeseries)

print(stt.test["waveIrreg_2101"].timeseries["M206_COG X"])

timeseries = timeseries.to_pandas()

print(stt.test["waveIrreg_2101"].timeseries, "TESt")

data =[]
sensors = []
for ts in list(stt.test["waveIrreg_2101"].timeseries.values())[0:3]:
    tic = time.perf_counter()
    timeseries_data = ts.get_data_points().to_pandas()

    toc1 = time.perf_counter()
    print(f"Query 1 took {toc1 - tic:0.4f} seconds")

    sensor = client.sensor.get(ts.sensor_id)
    data.append(timeseries_data)
    sensors.append(sensor)

plot_timeseries(data, test, sensors)

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
'''

#stt.test[10].timeseries[0].to_pandas()




#timeseries = client.timeseries.get(id="14ec6b18-a4b0-4d69-941b-602c6641d98b")
#print(timeseries.get_data_points(), "TEST")

campaign = client.campaign.get(id="3b891863-3cb1-4bf8-8582-49a15c5a2e65")
testsList = campaign.get_tests()
sensors = campaign.get_sensors()



time1 = time.time()

lst = []
for test in testsList:
    time1 = time.time()
    lst.append(test.get_timeseries())
    time2 = time.time()
    full_time = (time2 - time1) * 1000.0
    print(f'function took {full_time} milliseconds')

for timeseriesList in lst:
    print(timeseriesList)
    for ts in timeseriesList:
        time1 = time.time()
        ts.get_data_points()
        print(len(ts.data_points), "LEN")
        time2 = time.time()
        full_time = (time2 - time1) * 1000.0
        print(f'function took {full_time} milliseconds')


time2 = time.time()

full_time = (time2 - time1) * 1000.0
print(f"FINISHED IN {full_time}")

'''
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