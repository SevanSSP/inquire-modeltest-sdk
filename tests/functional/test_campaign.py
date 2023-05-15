from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool


def test_campaign_api(client):
    """The Api is now verified good to go and tests can interact with it"""
    name = random_lower_string()
    description = random_lower_string()
    date = str(datetime.now())
    location = random_lower_string()
    scale_factor = random_float()
    water_depth = random_float()
    client.campaign.create(name, description, location, date, scale_factor, water_depth)
    assert client.campaign.get_by_name(name)

    campaigns = client.campaign.get(filter_by=[
        client.filter.campaign.name == name,
        client.filter.campaign.description == description],
        sort_by=[client.sort.campaign.date.asc])

    assert len(campaigns) == 1
    assert campaigns[0] == client.campaign.get_by_name(name) == client.campaign.get_by_id(campaigns[0].id)
