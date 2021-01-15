import pytest
from datetime import datetime
from modeltestSDK import Campaign, BaseResource, Sensor, Timeseries

@pytest.fixture(scope="module")
def new_campaign():
    camp = Campaign(
        name = "asdfg",
        description = "sdh dfgh rghh",
        date = datetime.utcnow(),
        location= "Ålesund",
        scale_factor= 1,
        water_depth= 1200,
        )
    return camp

@pytest.fixture(scope="module")
def new_base_resource():
    base = BaseResource()

@pytest.fixture(scope="module")
def new_sensor():
    sens = Sensor(
        name = "sdfghjk",
        description="eghj dfj dfgh",
        unit="kg",
        kind="length",
        x = 1.4,
        y= -1.9,
        z = 1.0,
        is_local=True,
        campaign_id="rthjkjnfd"
    )
    return sens

@pytest.fixture(scope="module")
def new_timeseries():
    ts = Timeseries(
        sensor_id="12345678123456781234567812345678",
        test_id="12345678123456781234567812345678",
        fs = 2.5
    )
    return ts

