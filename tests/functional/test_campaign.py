from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool

def test_campaign(client, create_random_campaign):
    """The Api is now verified good to go and tests can interact with it"""
    assert client.campaign.get_by_name(create_random_campaign.name) == create_random_campaign
    assert client.campaign.get_by_id(create_random_campaign.id) == create_random_campaign

def test_same_named_campaign(client, admin_key):
    """The Api is now verified good to go and tests can interact with it"""
    name = 'samename'
    description = random_lower_string()
    date = str(datetime.now())
    location = random_lower_string()
    scale_factor = random_float()
    water_depth = random_float()
    campaign = client.campaign.create(name, description, location, date, scale_factor, water_depth)
    campaign2 = client.campaign.create(name, description, location, date, scale_factor, water_depth)

    assert client.campaign.get_by_name(name).name == name

    client.campaign.delete(campaign.id, admin_key=admin_key)
    client.campaign.delete(campaign2.id, admin_key=admin_key)
    assert client.campaign.get_by_name(name) is None