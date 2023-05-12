import requests
from urllib.parse import urljoin
from modeltestSDK.config import Config
from modeltestSDK.client import Client


def test_create_user(http_service, admin_key):
    """The Api is now verified good to go and tests can interact with it"""
    api_url = http_service
    user_dict = dict(username='tester494234',
                     full_name='',
                     email='test@testing.com',
                     password='password',
                     disabled=False)

    config = Config
    config.host = api_url
    client = Client(config)
    resp = requests.post(f'{api_url}/api/v1/auth/users?administrator_key={admin_key}', json=user_dict)
    assert resp.status_code == 200
