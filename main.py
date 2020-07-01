from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration, Timeseries, Sensor
import datetime
import random
from modeltestSDK.utils import from_datetime_string, to_datetime_string
from typing import List

from pipeline.plot_timeseries import plotTS

import time
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
mplstyle.use('fast')


client = SDKclient()


campaigns = client.campaign.get_all()

print(campaigns)

tic = time.perf_counter()

stt = client.campaign.get("49627a4c-9b8e-4eb4-816a-2d252be6b961")



test = client.floater.get("eb4e6456-4a85-472b-91fe-21689c5201a2")

print(test.get_timeseries())

ts = client.timeseries.get_data_points("bdef448e-d924-4cce-9ca5-cfb601e5f0a8")

timeseries = client.timeseries.get("bdef448e-d924-4cce-9ca5-cfb601e5f0a8")

sensor1 = client.sensor.get(timeseries.sensor_id)

data1 = ts.to_pandas()#.head(5000)

ts = client.timeseries.get_data_points("ea1a2f9b-bc65-4ed6-8d96-25090768e7d3")

timeseries = client.timeseries.get("ea1a2f9b-bc65-4ed6-8d96-25090768e7d3")

sensor2 = client.sensor.get(timeseries.sensor_id)

data2 = ts.to_pandas()

toc = time.perf_counter()
print(f"Query took {toc-tic:0.4f} seconds")

plotTS([data1,data2], test, [sensor1,sensor2])

#stt.test[10].timeseries[0].to_pandas()

