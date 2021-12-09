import pytest
from datetime import datetime
from modeltestSDK.resources import Campaign, Sensor, TimeSeries, Tests, FloaterTest


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


@pytest.fixture(scope='module')
def floater_test_data():
    data = [{'number': '5011', 'description': 'IRR H18.9 T20 D0 C0/0.73 W0 LOADED, ALS-1, SEED2',
             'test_date': '2021-09-13T15:09:52', 'campaign_id': '73e3da68-d639-4325-8c6c-f8ed4dbef37c',
             'type': 'Floater Test', 'category': 'irregular wave', 'orientation': 0.0,
             'wave_id': '9bcbe75a-d527-4aa8-ae98-b8a5c778db03', 'wind_id': None,
             'floaterconfig_id': '6bb0cc4d-d450-44d8-9ace-bd293e1a099c', 'read_only': True,
             'id': 'bbb343a3-0884-4d25-b36e-e125eaccbee5'}]

    return data


@pytest.fixture(scope="module")
def tests_class():
    return Tests


@pytest.fixture(scope="module")
def floater_test_class():
    return FloaterTest
