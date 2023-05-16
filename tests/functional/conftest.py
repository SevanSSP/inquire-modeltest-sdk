import pytest
import requests
from urllib.parse import urljoin
from modeltestSDK.config import Config
from modeltestSDK.client import Client
import os
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool
from datetime import datetime
from modeltestSDK.resources import Campaign, Sensor, TimeSeries, Tests, FloaterTest, FloaterConfiguration, WaveCalibrationTest, WindCalibrationTest, DataPoints


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
    return client


@pytest.fixture(scope='function')
def create_random_campaign(client) -> Campaign:
    name = random_lower_string()
    description = random_lower_string()
    date = str(datetime.now())
    location = random_lower_string()
    scale_factor = random_float()
    water_depth = random_float()
    return client.campaign.create(name, description, location, date, scale_factor, water_depth)


