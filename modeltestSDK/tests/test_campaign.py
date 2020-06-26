
from modeltestSDK.resources import Campaign
import datetime


def test_types(new_campaign):
    assert isinstance(new_campaign, Campaign)
    assert isinstance(new_campaign.id, str)
    assert isinstance(new_campaign.name, str)
    assert isinstance(new_campaign.description, str)
    assert isinstance(new_campaign.date, datetime.datetime)