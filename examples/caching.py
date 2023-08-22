"""
Using caching and timing get_data_point with and without caching
"""

from modeltestsdk import Client
import time
client = Client()


# timeseries id
ts_id = UUID


# Timing get_data_points without caching
t = time.time()
ts_data = client.timeseries.get_data_points(ts_id=ts_id, all_data=True, cache=False)
elapsed = time.time() - t

print(f'Get, no caching: {elapsed} s')

# Timing get_data_points with caching, storing the results to sqlite
t = time.time()
ts_data = client.timeseries.get_data_points(ts_id=ts_id, all_data=True)
elapsed = time.time() - t

print(f'Get, with caching: {elapsed} s')

# Timing get_data_points with caching, extracting the results from sqlite
t = time.time()
ts_data = client.timeseries.get_data_points(ts_id=ts_id, all_data=True)
elapsed = time.time() - t

print(f'Get from cache: {elapsed} s')
