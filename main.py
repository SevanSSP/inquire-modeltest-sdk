from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration, Timeseries
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List


client = SDKclient()


campaigns = client.campaign.get_all()

print(campaigns)

stt = client.campaign.get(client.campaign.get_id("STT"))

print(stt.get_tests())
print(stt.get_sensors())

test = client.floater.get("5a157173-7216-4c02-a3a8-f2b5d15d3658")

print(test.get_timeseries())

ts = client.timeseries.get("7da557b8-d2c9-4b86-878d-387268e64265")

