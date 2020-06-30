from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration
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

test_irreg= client.floater.get("574c97f5-e1a8-443f-90e9-1660b7b21e9d")

print(test_irreg.get_timeseries())