from modeltestSDK import SDKclient, Campaign, SensorAPI
import datetime

client = SDKclient()


campaign = Campaign.get_existing(name="SDKlasse", client=client)

campaign.water_density = 20
campaign.update()

#print(campaign.update())
#print(campaign2)

# sensors = SensorAPI(client)
# sensors.create(name="MK206",
#                 description="En test sensor",
#                 unit="kg",
#                 kind="mass",
#                 x=0,y=0,z=0,
#                 is_local=True,
#                 campaign_id=campaign.get_id("SDKlasse"))

# print(campaign.get(campaign.get_id("SDKlasse")))
# print(campaign.get_sensors(campaign.get_id("SDKlasse")))
# print(sensors.get(sensors.get_id("MK206")))
# print(campaign.get_tests(campaign.get_id("SDKlasse")))
# print(campaign.get_all())
