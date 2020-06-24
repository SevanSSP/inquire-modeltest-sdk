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
sensors.create("MK206","En test sensor","kg","mass",0,0,0,True,campaign.get_id("SDKlasse"))

print(campaign.get(campaign.get_id("SDKlasse")))
print(campaign.get_sensors(campaign.get_id("SDKlasse")))

