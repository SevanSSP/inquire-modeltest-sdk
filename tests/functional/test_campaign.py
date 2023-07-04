from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool


def test_campaign_api(client, secret_key, admin_key):
    """The Api is now verified good to go and tests can interact with it"""
    name = random_lower_string()
    description = random_lower_string()
    date = str(datetime.now())
    location = random_lower_string()
    scale_factor = random_float()
    water_depth = random_float()
    camp = client.campaign.create(name, description, location, date, scale_factor, water_depth, admin_key)
    assert client.campaign.get_by_name(name)

    campaigns = client.campaign.get(filter_by=[
        client.filter.campaign.name == name,
        client.filter.campaign.description == description],
        sort_by=[client.sort.campaign.date.asc])

    assert len(campaigns) == 1
    assert campaigns[0] == client.campaign.get_by_name(name) == client.campaign.get_by_id(campaigns[0].id)
    assert client.campaign.get_by_name('not existing name') is None

    camp_with_same_name = client.campaign.create(name, 'description', 'location', date, scale_factor, water_depth, admin_key)
    assert camp_with_same_name.id != camp.id
    assert client.campaign.get_by_name(name) == client.campaign.get_by_id(camp.id)
    assert client.campaign.get_by_name(name) != client.campaign.get_by_id(camp_with_same_name.id)

    client.campaign.delete(camp.id, secret_key=secret_key)
    client.campaign.delete(camp_with_same_name.id, secret_key=secret_key)


def test_campaign_resources(client, new_campaigns, new_sensors):
    campaigns_from_db = client.campaign.get()

    for campaign in new_campaigns:
        assert campaign in campaigns_from_db

        sensors_from_db = client.sensor.get(filter_by=[client.filter.sensor.campaign_id == campaign.id])

        for sensor in campaign.sensors():
            assert sensor in sensors_from_db
