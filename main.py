from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List


client = SDKclient()


campaigns = client.campaign.get_all()

print(campaigns)

swatch = client.campaign.get(client.campaign.get_id("SWATCH"))

print(swatch.get_sensors())

print(swatch.get_tests())