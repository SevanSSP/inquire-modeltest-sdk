from modeltestSDK.resources import Campaign
from modeltestSDK.client import Client


def add_floater_configs(campaign: Campaign, client: Client):
    client.floater_config.create(name="GM3 NEW DESIGN A",
                                 description="Design A - Loaded condition GM3 (GM=7[m])"
                                             "Model S-1107B",
                                 campaign_id=campaign.id,
                                 characteristic_length=76.0,
                                 draft=30.0,
                                 read_only=True)

    client.floater_config.create(name="GM3 NEW DESIGN B",
                                 description="Design B - Loaded condition GM3 (GM=7[m])"
                                             "Model S-1107C",
                                 campaign_id=campaign.id,
                                 characteristic_length=76.0,
                                 draft=30.0,
                                 read_only=True)
