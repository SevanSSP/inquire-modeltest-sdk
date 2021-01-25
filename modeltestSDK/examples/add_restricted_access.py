from modeltestSDK import Client
import time
import matplotlib.pyplot as plt
from modeltestSDK.utils import get_datetime_date


client = Client()

'''
campaign = client.campaign.create(name="TestCamp2",
                                  description="A campaign for testing",
                                  date=get_datetime_date("110120201000"),
                                  location="Bergen",
                                  scale_factor=100,
                                  water_depth=100,
                                  read_only=True,)

print(campaign)



sensor = client.sensor.create(name="TestSens2",
                              description="A sensor for testing",
                              unit="test-meter",
                              kind="slamming panel",
                              x=0,
                              y=0,
                              z=0,
                              is_local=True,
                              fs=0.001,
                              intermittent=False,
                              campaign_id=campaign.id,
                              read_only=True)
print(sensor)

resp = client.campaign.delete(campaign.id, parameters={'secret_key': "admin"})

print(resp)
'''
tic = time.perf_counter()

ts = client.timeseries.get("bc732b7b-f9b0-47cb-a6ce-2dbbd5d2225f")
ts.get_data_points()

data = ts.data_points

toc = time.perf_counter()

print(f"Collecting timeseries took {toc-tic}s")

plt.figure()

plt.plot(data['time'], data['value'])

plt.show()