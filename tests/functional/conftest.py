import pytest
import requests
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool, \
    random_int
from modeltestSDK.config import Config
from modeltestSDK.client import Client
from modeltestSDK.resources import (Campaign, Campaigns, Sensor, Sensors, Tests, Test, FloaterTest, WindCalibrationTest,
                                    WaveCalibrationTest, FloaterConfiguration, FloaterConfigurations, TimeSeries,
                                    TimeSeriesList, DataPointsList, Tags, Tag)
from datetime import datetime
import os
import random


@pytest.fixture(scope="module")
def client(http_service, admin_key):
    """The Api is now verified good to go and tests can interact with it"""
    api_url = http_service
    user_dict = dict(username='tester',
                     full_name='Test',
                     email='test@testing.com',
                     password='password',
                     disabled=False)
    config = Config
    config.host = api_url
    os.environ['INQUIRE_MODELTEST_API_USER'] = 'tester'
    os.environ['INQUIRE_MODELTEST_API_PASSWORD'] = 'password'

    client = Client(config)
    assert client.__str__()

    # check if user exists
    resp = requests.get(f'{api_url}/api/v1/auth/users?username=tester&administrator_key={admin_key}')
    if resp.status_code != 404:
        resp = requests.delete(f'{api_url}/api/v1/auth/users?username=tester&administrator_key={admin_key}')
        assert resp.status_code == 200

    resp = requests.post(f'{api_url}/api/v1/auth/users?administrator_key={admin_key}', json=user_dict)
    assert resp.status_code == 200

    # add user to admin group (create group if required)
    resp = requests.get(f'{api_url}/api/v1/auth/group?group_description=admin')
    if resp.status_code != 200:
        group_dict = dict(description='admin')
        resp = requests.post(f"{api_url}/api/v1/auth/group?administrator_key={admin_key}", json=group_dict)
        assert resp.status_code == 200
        admin_group_existed = False
    else:
        admin_group_existed = True

    resp = requests.patch(
        f'{api_url}/api/v1/auth/users?username=tester&administrator_key={admin_key}&group_description=admin&remove=false')
    assert resp.status_code == 200

    yield client

    # clean-up
    user = requests.get(f'{api_url}/api/v1/auth/users?username=tester&administrator_key={admin_key}')
    resp = requests.delete(
        f'{api_url}/api/v1/auth/users?username={user.json()["username"]}&administrator_key={admin_key}')
    assert resp.status_code == 200

    if not admin_group_existed:
        resp = requests.delete(f'{api_url}/api/v1/auth/group?group_description=admin&administrator_key={admin_key}')
        assert resp.status_code == 200


@pytest.fixture(scope='module')
def new_campaigns(client, secret_key, admin_key):
    campaigns = Campaigns()
    for _ in range(random.randint(5, 40)):
        campaigns.append(Campaign(
            client=client,
            name=random_lower_string(),
            description=random_lower_string(),
            date=datetime.now(),
            location=random_lower_string(),
            scale_factor=random_float(),
            water_depth=random_float(),
            read_only=random_bool()),
            admin_key
        )

    yield campaigns

    # clean up
    for campaign in campaigns:
        campaign.delete(secret_key=secret_key)


@pytest.fixture(scope='module')
def new_sensors(client, new_campaigns, secret_key):
    sensors = Sensors()
    for campaign in new_campaigns:
        sensors.append(Sensor(
            client=client,
            campaign_id=campaign.id,
            name=random_lower_string(),
            description=random_lower_string(),
            unit=random_lower_short_string(),
            kind=random.choice([
                "length",
                "velocity",
                "acceleration",
                "force",
                "pressure",
                "volume",
                "mass",
                "moment",
                "angle",
                "angular velocity",
                "angular acceleration",
                "slamming force",
                "slamming pressure",
                "control signal",
                "rate"]),
            source=random.choice([
                "direct measurement",
                "basin derived",
                "Sevan derived",
                "external derived"]),
            x=random_float(),
            y=random_float(),
            position_reference=random.choice([
                "local",
                "global"]),
            position_draft_lock=random_bool(),
            position_heading_lock=random_bool(),
            positive_direction_definition=random_lower_string(),
            area=random_float(),
            read_only=random_bool()
        ))

    yield sensors

    # clean up
    for sensor in sensors:
        sensor.delete(secret_key=secret_key)


@pytest.fixture(scope='module')
def new_floaterconfig(client, new_campaigns, secret_key):
    floaterconfigs = FloaterConfigurations()

    for campaign in new_campaigns:
        floaterconfigs.append(FloaterConfiguration(
            client=client,
            name=random_lower_string(),
            description=random_lower_string(),
            campaign_id=campaign.id,
            characteristic_length=random_float(),
            draft=random_lower_int()
        ))
    yield floaterconfigs

    # clean up
    for floaterconfig in floaterconfigs:
        floaterconfig.delete(secret_key=secret_key)


@pytest.fixture(scope='module')
def new_tests(client, secret_key, new_floaterconfig, new_campaigns):
    tests = Tests()
    for fc in new_floaterconfig:
        tests.append(FloaterTest(
            client=client,
            floaterconfig_id=fc.id,
            category=random.choice(["current force",
                                    "wind force",
                                    "decay",
                                    "regular wave",
                                    "irregular wave",
                                    "pull out",
                                    "vim",
                                    "freak wave"
                                    ]),
            orientation=random_lower_int(),
            number=str(random_int()),
            description=random_lower_string(),
            test_date=datetime.now(),
            campaign_id=fc.campaign_id)
        )

    for camp in new_campaigns:
        tests.append(WaveCalibrationTest(
            client=client,
            wave_spectrum=random.choice(["jonswap",
                                         "torsethaugen",
                                         "broad band",
                                         "chirp wave",
                                         "regular",
                                         None]),
            wave_height=random_float(),
            wave_period=random_float(),
            gamma=random_float(),
            wave_direction=random_float(),
            current_velocity=random_float(),
            current_direction=random_float(),
            campaign_id=camp.id,
            number=random_int(),
            description=random_lower_string(),
            test_date=datetime.now(),
        )
        )

    for camp in new_campaigns:
        tests.append(WindCalibrationTest(
            client=client,
            wind_spectrum=random_lower_short_string(),
            wind_velocity=random_float(),
            zref=random_float(),
            wind_direction=random_float(),
            campaign_id=camp.id,
            number=random_int(),
            description=random_lower_string(),
            test_date=datetime.now(),
        )
        )

    yield tests

    # clean up
    for test in tests:
        test.delete(secret_key=secret_key)


@pytest.fixture(scope='module')
def new_timeseries(client, secret_key, new_campaigns, new_sensors, new_tests):
    ts_list = TimeSeriesList()
    for camp in new_campaigns:
        sensors = camp.sensors()
        tests = camp.tests()
        for sensor in sensors:
            for test in tests:
                ts_list.append(TimeSeries(
                    client=client,
                    sensor_id=sensor.id,
                    test_id=test.id,
                    fs=random_float(),
                    default_start_time=0,
                    default_end_time=100000
                ))

    yield ts_list

    # clean up
    for ts in ts_list:
        ts.delete(secret_key=secret_key)


@pytest.fixture(scope='module')
def new_datapoints(client, secret_key, new_timeseries):
    time = [random_float() for i in range(0, 400)]
    time.sort()

    dp_list = DataPointsList()
    for ts in new_timeseries:
        values = [random_float() for i in range(0, len(time))]
        dp_list.append(ts.add_data(
            time=time,
            values=values
        ))

    yield dp_list


@pytest.fixture(scope='module')
def new_tags(client, secret_key, new_timeseries, new_sensors, new_tests):
    tag_list = Tags()
    for ts in new_timeseries:
        tag_list.append(Tag(client=client, name='quality: bad', comment=random_lower_string(), timeseries_id=ts.id))
    for sensor in new_sensors:
        tag_list.append(Tag(client=client, name='pitch', comment=random_lower_string(), sensor_id=sensor.id))
    for test in new_tests:
        tag_list.append(Tag(client=client, name='comment', comment=random_lower_string(), test_id=test.id))

    yield tag_list

    for tag in tag_list:
        tag.delete(secret_key=secret_key)
