from modeltestSDK import SDKclient, CampaignAPI, SensorAPI
import datetime

client = SDKclient()

campaign = CampaignAPI(client)

campaign.create(name="SDKlasse",
                description="Et campaign laget fra SDK klasse",
                location= 'string',
                date= (datetime.datetime.utcnow()).isoformat(),
                diameter= 0,
                scale_factor= 0,
                water_density= 0,
                water_depth= 0,
                transient= 0)

sensors = SensorAPI(client)
sensors.create(name="MK206",
               description="En test sensor",
               unit="kg",
               kind="mass",
               x=0,y=0,z=0,
               is_local=True,
               campaign_id=campaign.get_id("SDKlasse"))

print(campaign.get(campaign.get_id("SDKlasse")))
print(campaign.get_sensors(campaign.get_id("SDKlasse")))
print(sensors.get(sensors.get_id("MK206")))
print(campaign.get_tests(campaign.get_id("SDKlasse")))
print(campaign.get_all())
