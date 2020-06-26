from modeltestSDK import SDKclient, Campaign, Sensor
import datetime

client = SDKclient()

campaign = Campaign.get_existing(name="SDKlasse", client=client)

print(sensor.update())

print(sensor)

print(Sensor.get_existing(name="MK206", client=client))

print(campaign.get_sensors())


# print(campaign.get(campaign.get_id("SDKlasse")))
# print(campaign.get_sensors(campaign.get_id("SDKlasse")))
# print(sensors.get(sensors.get_id("MK206")))
# print(campaign.get_tests(campaign.get_id("SDKlasse")))
# print(campaign.get_all())
