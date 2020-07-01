from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
from modeltestSDK.resources import WaveCurrentCalibration, Timeseries
import datetime
import random
from modeltestSDK.utils import from_datetime_string, to_datetime_string
from typing import List

import time
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
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

