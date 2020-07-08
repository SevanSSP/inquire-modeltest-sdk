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


campaigns = client.campaign.get_all()

tic = time.perf_counter()


#print(campaigns)

#campaign_id = client.campaign.get_id("STT")
stt = client.campaign.get_by_name("STT")
print(stt.get_tests())

toc1 = time.perf_counter()

#test_id = client.floater.get_id("waveIrreg_2101")
test = client.floater.get_by_name("waveIrreg_2101")
stt.populate_test(test)

toc2 = time.perf_counter()

#print(stt.test)

timeseries = test.get_timeseries()
stt.test['waveIrreg_2101'].populate_timeseries(timeseries)

toc3 = time.perf_counter()

print(stt.test["waveIrreg_2101"].timeseries)

toc4 = time.perf_counter()

print(f"Query of timeseries took {toc4-toc3:0.4f} seconds")

#print(stt.test["waveIrreg_2101"].timeseries["M206_COG X"])

timeseries = timeseries.to_pandas()

data =[]
sensors = []
for i in range(1):
    timeseries_id = timeseries["id"][i]
    ts = client.timeseries.get(timeseries_id)
    timeseries_data = ts.get_data_points().to_pandas()
    sensor = client.sensor.get(ts.sensor_id)
    data.append(timeseries_data)
    sensors.append(sensor)

#plot_timeseries(data, test, sensors)
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
'''
'''
#stt.test[10].timeseries[0].to_pandas()




#timeseries = client.timeseries.get(id="14ec6b18-a4b0-4d69-941b-602c6641d98b")
#print(timeseries.get_data_points(), "TEST")

'''test = client.test.get(id="3d311a2b-86d0-4a9f-a8d3-ad6c92532554")
timeseriesList = test.get_timeseries()



for timeseries in timeseriesList:
    time1 = time.time()
    print(len(timeseries.get_data_points()), "TEST")
    time2 = time.time()
    full_time = (time2 - time1) * 1000.0
    print(f'function took {full_time} milliseconds')

print(timeseriesList[0].data_points[0:20])'''

'''
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



# Nicolai prøver ut SDK:

timeseries = client.timeseries.get("000998a6-dac6-4c51-ab46-9359518e5878")
stddev = timeseries.standard_deviation()
print(stddev)