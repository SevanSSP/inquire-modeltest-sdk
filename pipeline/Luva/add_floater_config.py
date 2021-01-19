from modeltestSDK.resources import Campaign
from modeltestSDK.client import SDKclient


def add_floater_configs(campaign: Campaign, client: SDKclient):

    client.floater_config.create(name="Base case",
                                 description="Base Case - Loaded condition GM2 (GM=6[m])",
                                 campaign_id=campaign.id,
                                 characteristic_length=70.0,
                                 draft=30.0,
                                 read_only=True)

    client.floater_config.create(name="Design A",
                                 description="Design A - Loaded condition GM3 (GM=7[m])",
                                 campaign_id=campaign.id,
                                 characteristic_length=76.0,
                                 draft=30.0,
                                 read_only=True)

    client.floater_config.create(name="Design B",
                                 description="Design B - Loaded condition GM3 (GM=7[m])",
                                 campaign_id=campaign.id,
                                 characteristic_length=76.0,
                                 draft=30.0,
                                 read_only=True)