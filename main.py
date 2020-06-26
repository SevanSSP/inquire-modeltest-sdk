from modeltestSDK import SDKclient, Campaign, Sensor
import datetime

client = SDKclient()

print(1)
campaign = Campaign.get_existing(name="Test", client=client)

print(campaign)

#print(campaign.update())
#print(campaign2)
print(2)

sensor = Sensor(name="MK206",
                 description="En test sensor",
                 unit="kg",
                 kind="mass",
                 x=0,y=0,z=0,
                 is_local=True,
                 campaign_id=campaign.id,
                 client=client)
print(3)

print(sensor.update())
print(4)

print(sensor)
print(Sensor.get_existing(name="MK206", client=client))
print(5)

print(campaign.get_sensors())


# print(campaign.get(campaign.get_id("SDKlasse")))
# print(campaign.get_sensors(campaign.get_id("SDKlasse")))
# print(sensors.get(sensors.get_id("MK206")))
# print(campaign.get_tests(campaign.get_id("SDKlasse")))
# print(campaign.get_all())
