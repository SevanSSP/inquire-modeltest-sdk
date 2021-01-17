from modeltestSDK.resources import FloaterConfig, Campaign
from modeltestSDK.client import SDKclient


def add_floater_configs(campaign: Campaign, client: SDKclient):

    client.floater_config.create(name="SEVAN BASE IN-LINE MOOR T15",
                                 description="Base model S-1079D. Draft 15m. Mooring setup 1. GM=7[m]",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=15.0,
                                 read_only=True)

    client.floater_config.create(name="SEVAN MOD IN-LINE MOOR2 T15",
                                 description="Model S-1079E. Draft 15m. Mooring setup 2. GM=7[m]",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=15.0,
                                 read_only=True)

    client.floater_config.create(name="SEVAN BASE IN-LINE MOOR2 T15",
                                 description="Base model S-1079D. Draft 15m. Mooring setup 2. GM=7[m]",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=15.0,
                                 read_only=True,)

    client.floater_config.create(name="SEVAN MOD IN-LINE MOOR2 T15 GM2",
                                 description="Model S-1079E. Draft 15m. Mooring setup 2. GM=10[m]",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=15.0,
                                 read_only=True,)

    client.floater_config.create(name="SEVAN MOD IN-LINE MOOR2 T17 GM2",
                                 description="Model S-1079E. Draft 15m. Mooring setup 2. GM=10[m]",
                                 campaign_id=campaign.id,
                                 characteristic_length=87.0,
                                 draft=17.0,
                                 read_only=True,)

