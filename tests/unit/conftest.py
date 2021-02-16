import pytest
from datetime import datetime
from modeltestSDK.resources import Campaign, Sensor, TimeSeries


@pytest.fixture(scope="module")
def new_campaign():
    camp = Campaign(
        name="asdfg",
        description="sdh dfgh rghh",
        date=datetime.utcnow(),
        location="Ålesund",
        scale_factor=1,
        water_depth=1200,
        )
    return camp


@pytest.fixture(scope="module")
def new_sensor():
    sens = Sensor(
        name="sdfghjk",
        description="eghj dfj dfgh",
        unit="kg",
        kind="length",
        source="fantasy",
        x=1.4,
        y=-1.9,
        z=1.0,
        position_reference='global',
        positive_direction_definition='onwards,',
        position_heading_lock=False,
        position_draft_lock=False,
        campaign_id="rthjkjnfd"
    )
    return sens


@pytest.fixture(scope="module")
def new_timeseries():
    ts = TimeSeries(
        sensor_id="12345678123456781234567812345678",
        test_id="12345678123456781234567812345678",
        fs=2.5,
        default_start_time=1,
        default_end_time=2,

    )
    return ts
