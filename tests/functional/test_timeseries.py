from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool
import random

def test_timeseries_api(client, secret_key, admin_key, new_timeseries):
    """The Api is now verified good to go and tests can interact with it"""
    ts = new_timeseries[0]
    assert ts
