"""
Read-only checks against a running model test API v2 (e.g. staging): pytest tests/functional --api=<host>, signed in
from the INQUIRE_MODELTEST_* settings. Nothing is written.
"""
import pandas as pd

from modeltestsdk.resources import Campaign, FloaterTest, Statistics, Test


def test_campaigns_and_their_parts(client):
    campaigns = client.campaign.get()
    assert len(campaigns) > 0 and all(isinstance(c, Campaign) for c in campaigns)
    campaign = next(c for c in campaigns if c.floater_configurations(limit=1))
    assert client.campaign.get_by_id(campaign.id).name == campaign.name
    config = campaign.floater_configurations(limit=1)[0]
    assert config.campaign_id == campaign.id and config.draft > 0
    coordinates = config.coordinates()
    assert coordinates["floaterconfig_id"] == config.id and "sensors" in coordinates
    assert all(s.campaign_id == campaign.id for s in campaign.sensors(limit=20))
    assert all(isinstance(t, Test) for t in campaign.tests(limit=5))
    assert isinstance(campaign.documents(), list)


def test_data_and_statistics(client, timeseries_with_data):
    ts = timeseries_with_data
    dps = ts.get_data()
    assert len(dps) > 0 and len(dps.time) == len(dps.value)
    assert dps.time[0] >= ts.default_start_time - 1e-6 and dps.time[-1] <= ts.default_end_time + 1e-6
    assert len(ts.get_data(all_data=True)) >= len(dps)
    stats = ts.get_statistics()
    assert isinstance(stats, Statistics) and stats.stored is True and stats.n_points == len(dps)
    window = ts.get_statistics(start=ts.default_start_time, end=ts.default_end_time)
    assert window.stored is False and abs(window.mean - stats.mean) <= 1e-9 * max(1.0, abs(stats.mean))
    assert isinstance(dps.to_pandas(), pd.DataFrame)
    assert ts.sensor.id == ts.sensor_id


def test_data_files(client, timeseries_with_data):
    test = client.test.get_by_id(timeseries_with_data.test_id)
    files = client.test.active_datafiles(test.id)
    assert files and all(f.status == "active" for f in files)
    assert timeseries_with_data.id in {i for f in files for i in f.timeseries_ids}
    if isinstance(test, FloaterTest):
        assert test.floater_config is not None
