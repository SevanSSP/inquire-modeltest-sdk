from modeltestSDK import SDKclient, Campaign, Sensor, DataPoint
import datetime
import random
from modeltestSDK.utils import from_datetime_string
from typing import List
client = SDKclient()


wave_current_condition_list = client.wind_current_condition.get_all()
print(wave_current_condition_list)
print(wave_current_condition_list[0].id)
print("GET wave ", client.wave_current_condition.get(id=wave_current_condition_list[0].id))
wave_current_condition = wave_current_condition_list[0]
print(wave_current_condition.get_campaign())
print(wave_current_condition.get_timeseries())


#timeseries = client.timeseries.create(test_id=floater.id, sensor_id=sensor.id)
#print(timeseries)
#for i in range(10):
#    timeseries.data_points.append(DataPoint(timeseries_id=timeseries.id, time=str(datetime.datetime.now()),
#                          value=random.uniform(0, 10000), client=client))

#print(timeseries.post_data_points())

