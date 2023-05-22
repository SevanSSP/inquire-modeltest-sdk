import pytest
import requests
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool
from modeltestSDK.config import Config
from modeltestSDK.client import Client
from modeltestSDK.resources import (Campaign, Campaigns, Sensor, Sensors)
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

    # check if user exists
    resp = requests.get(f'{api_url}/api/v1/auth/users?username=tester&administrator_key={admin_key}')
    if resp.status_code != 404:
        resp = requests.delete(f'{api_url}/api/v1/auth/users?username=tester&administrator_key={admin_key}')
        assert resp.status_code == 200

    resp = requests.post(f'{api_url}/api/v1/auth/users?administrator_key={admin_key}', json=user_dict)
    assert resp.status_code == 200

    yield client

    # user info
    user = requests.get(f'{api_url}/api/v1/auth/users?username=tester&administrator_key={admin_key}')
    resp = requests.delete(
        f'{api_url}/api/v1/auth/users?username={user.json()["username"]}&administrator_key={admin_key}')
    assert resp.status_code == 200

    # delete groups
    for group in user.json()["groups"][0]:
        requests.delete(
            f'{api_url}/api/v1/auth/group?administrator_key={admin_key}&'
            f'group_description={group["description"]}&'
            f'group_id={group["id"]}')


@pytest.fixture(scope='module')
def new_campaigns(client, secret_key):
    campaigns = Campaigns()
    for _ in range(random.randint(5, 15)):
        campaigns.append(Campaign(
            client=client,
            name=random_lower_string(),
            description=random_lower_string(),
            date=datetime.now(),
            location=random_lower_string(),
            scale_factor=random_float(),
            water_depth=random_float(),
            read_only=random_bool())
        )

    yield campaigns

    # clean up
    for campaign in campaigns:
        campaign.delete(secret_key=secret_key)


@pytest.fixture(scope='module')
def new_sensors(client, new_campaigns, secret_key):
    sensors = Sensors

    for campaign in new_campaigns:
        sensors.append(Sensor(
            client=client,
            campaign_id=campaign.id,
            name=random_lower_string(),
            description=random_lower_string(),
            unit=random_lower_string(),
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
            z=random_float(),
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
