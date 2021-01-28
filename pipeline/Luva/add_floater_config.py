from modeltestSDK.resources import Campaign
from modeltestSDK.client import Client


def add_floater_configs(campaign: Campaign, client: Client):

    client.floater_config.create(name="GM2",
                                 description="Base Case - Loaded condition GM2 (GM=6[m])",
                                 campaign_id=campaign.id,
                                 characteristic_length=70.0,
                                 draft=30.0,
                                 read_only=True)

    client.floater_config.create(name="GM1",
                                 description="Base Case - Loaded condition GM1 (GM=3[m])",
                                 campaign_id=campaign.id,
                                 characteristic_length=70.0,
                                 draft=30.0,
                                 read_only=True)

    client.floater_config.create(name="D2",
                                 description="Base Case - Loaded condition GM2 - New draft(GM=6[m])",
                                 campaign_id=campaign.id,
                                 characteristic_length=70.0,
                                 draft=33.0,
                                 read_only=True)
