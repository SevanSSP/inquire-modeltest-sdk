import pytest
from datetime import datetime
from modeltestSDK.resources import Campaign, Sensor, TimeSeries, Tests, FloaterTest, FloaterConfig, WaveCalibration, \
    WindCalibration, DataPoints, Tag, Tags
from uuid import uuid4
from tests.utils import random_lower_int, random_float
import random


@pytest.fixture(scope="module")
def new_campaign():
    camp = Campaign(
        name='TestCampaign',
        description='Description of testcampaign',
        date=datetime(2020, 10, 1),
        location='Oslo',
        scale_factor=1,
        water_depth=4,
    )
    camp.id = str(uuid4())
    return camp


@pytest.fixture(scope="module")
def new_sensor(new_campaign):
    sens = Sensor(
        name='SB accelerometer',
        description='SB accelerometer type 3',
        unit='m/s',
        kind='acceleration',
        source='basin derived',
        x=40,
        y=-20,
        z=5,
        position_reference='local',
        position_heading_lock=True,
        position_draft_lock=False,
        positive_direction_definition='up',
        campaign_id=new_campaign.id
    )
    sens.id = str(uuid4())
    return sens


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


@pytest.fixture(scope="module")
def new_wavecalibration(new_campaign):
    wavecalibration = WaveCalibration(
        type='Wave Calibration',
        number='X331',
        description='Description of test',
        test_date=datetime(2020, 10, 1),
        wave_spectrum='torsethaugen',
        wave_height=13,
        wave_period=17,
        gamma=2.4,
        wave_direction=265,
        current_velocity=7,
        current_direction=285,
        campaign_id=new_campaign.id
    )
    wavecalibration.id = str(uuid4())
    return wavecalibration


@pytest.fixture(scope='module')
def new_windcalibration(new_campaign):
    windcalibration = WindCalibration(
        type="Wind Calibration",
        number='Y331',
        description='Description of test',
        test_date=datetime(2020, 10, 1),
        wind_spectrum='NPD',
        wind_velocity=20,
        zref=10,
        wind_direction=270,
        campaign_id=new_campaign.id
    )
    windcalibration.id = str(uuid4())
    return windcalibration


@pytest.fixture(scope="module")
def new_floater_configuration(new_campaign):
    fc = FloaterConfig(
        name="test",
        description="description",
        campaign_id=new_campaign.id,
        characteristic_length=1.0,
        draft=1.0,
    )
    fc.id = str(uuid4())
    return fc


@pytest.fixture(scope='module')
def new_floatertest(new_wavecalibration, new_windcalibration, new_floater_configuration):
    floatertest = FloaterTest(
        type="Floater Test",
        number='REC331',
        description='Description of test',
        test_date=datetime(2020, 10, 1),
        category='decay',
        orientation=180,
        wave_id=new_wavecalibration.id,
        wind_id=new_windcalibration.id,
        floaterconfig_id=new_floater_configuration.id,
        campaign_id=new_wavecalibration.campaign_id
    )
    floatertest.id = str(uuid4())
    return floatertest


@pytest.fixture(scope="module")
def new_timeseries(new_sensor, new_floatertest):
    ts = TimeSeries(
        sensor_id=new_sensor.id,
        test_id=new_floatertest.id,
        fs=2.5,
        default_start_time=1,
        default_end_time=2,

    )
    ts.id = str(uuid4())
    return ts


@pytest.fixture(scope='module')
def new_datapoints(new_timeseries):
    dp = DataPoints(
        time=[random_float() for i in range(0, 100)],
        value=[random_float() for i in range(0, 100)],
        timeseries_id=new_timeseries.id
    )
    return dp


@pytest.fixture(scope='module')
def new_tags(new_timeseries, new_sensor, new_floatertest):
    tags = Tags([
        Tag(name='quality: bad', comment='bad quality', timeseries_id=new_timeseries.id),
        Tag(name='comment', comment='comment', sensor_id=new_sensor.id),
        Tag(name='comment', comment='another comment', test_id=new_floatertest.id)
    ]
    )
    for tag in tags:
        tag.id = str(uuid4())

    return tags
