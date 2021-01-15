from modeltestSDK.resources import FloaterConfig, Campaign
from modeltestSDK.client import SDKclient


def add_floater_configs(campaign: Campaign, client: SDKclient):

    client.floater_config.create(name="a",
                                 description="Model S-1079E, loaded condition 1",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=15.0,
                                 read_only=True)

    client.floater_config.create(name="h",
                                 description="Model S-1079E, loaded condition 2",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=15.0,
                                 read_only=True)

    client.floater_config.create(name="h",
                                 description="Model S-1079E, loaded condition 3",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=17.0,
                                 read_only=True,)

