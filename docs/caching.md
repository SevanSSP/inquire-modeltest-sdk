# Caching

Caching of timeseries data points is supported 

## Usage
The timeseries.get_data_points accepts a cache boolean which enables storing and extracting data 
from a cache instead of getting the data from the API. By default, caching is enabled (True).

The example below shows and times

* Getting data from API
* Getting data from API and storing it in cache
* Getting data from cache

```python hl_lines="14-33"
--8<--- "caching.py"
```

This behaviour assumes that the specific time series has not been cached previously

## Cache expiration and clearing
The cache is set with an expiry time of 7 days. Data is now explicitly deleted after 7 days, but a new
call of get_data_points will replace the existing data.

!!! note

    Caching is related to the API call. Modified data behind the same API call will not be availble if the API 
    call has been cached (and not expired). 

!!! note

    It is good practise to clear the cache when new data is posted
     
The cache can be manually cleared by the client's clear_cache() method  

```python hl_lines="9"
--8<--- "clear_cache.py"
```

## Under the hood
The SDK will establish a SQLite file (mtdb.sqlite) in a local cache folder 

* C:\Users\\user\AppData\Local\ for Windows
* /home/user/.cache/ for Linux, 
* /Users/user/Library/Caches/ for macOS

!!! note

    Deleting this file will remove all cached data, but not affect the modeltestSDK otherwise.