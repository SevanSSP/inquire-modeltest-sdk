from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool
import random
import numpy as np


def test_datapoints_api(client, secret_key, admin_key, new_datapoints):
    """The Api is now verified good to go and tests can interact with it"""
    dp_fixture = new_datapoints[0]
    assert dp_fixture

    dp_fetch = client.timeseries.get_data_points(ts_id=dp_fixture.timeseries_id, all_data=True)
    assert dp_fixture == dp_fetch

    statistics_fetch = client.timeseries.get_statistics(ts_id=dp_fixture.timeseries_id)
    assert statistics_fetch.mean == np.mean(dp_fetch.value)


def test_datapoints_resource(client, secret_key, admin_key, new_datapoints):
    """The Api is now verified good to go and tests can interact with it"""
    dp = new_datapoints[0]
    df_list = new_datapoints.to_pandas()
    df = dp.to_pandas()
    dp_qats = dp.to_qats_ts()
    assert len(dp) == len(df_list) == len(df)