from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
import time
import aiohttp
import asyncio


client = SDKclient()



#timeseries = client.timeseries.get(id="80f13ab3-82f0-45c2-b133-08a9ae22cfb2")

#print(timeseries)
#print("TEST")


#print(len (timeseries.get_data_points()))

'''
wave_current_condition_list = client.wind_current_condition.get_all()
print(wave_current_condition_list)
print(wave_current_condition_list[0].id)
print("GET wave ", client.wave_current_condition.get(id=wave_current_condition_list[0].id))
wave_current_condition = wave_current_condition_list[0]
print(wave_current_condition.get_campaign())
print(wave_current_condition.get_timeseries())
'''
async def post(session, url, body):
    async with session.post(url, json=body) as response:
        return await response.text()

async def multiple_tasks(client, body):
    url = "http://127.0.0.1:8000/api/timeseries/test/"
    tasks = []
    async with aiohttp.ClientSession() as session:
        for offset in range(0, 13):
            print(offset, len(body))
            tasks.append(post(session, url, body))
        res = await asyncio.gather(*tasks)
        print(res)
    return res


timeseries = client.timeseries.create(test_id="91ddc4f3-e47d-4500-b740-dc4a24e3c9b6",
                                      sensor_id="8ef3e529-8816-44ee-820e-a048368f5fca")

time1 = time.time()
lst=()
print(timeseries.id, "TIMESERIESID")
for i in range(130000):
    timeseries.data_points.append(DataPoint(timeseries_id=timeseries.id, time=str(datetime.datetime.now()),
                          value=random.uniform(0, 10000), client=client))

data = asyncio.get_event_loop().run_until_complete(multiple_tasks(client, body=timeseries.data_points.dump()[0:10000]))

time2 = time.time()

#print(timeseries.post_data_points())


full_time = (time2 - time1) * 1000.0
print(f'function took {full_time} milliseconds')
