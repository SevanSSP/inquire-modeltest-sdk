
from modeltestSDK.resources import Campaign


def test_types(new_campaign):
    assert isinstance(new_campaign, Campaign)
    #assert isinstance(new_campaign.id, str)
    assert isinstance(new_campaign.name, str)
    assert isinstance(new_campaign.description, str)