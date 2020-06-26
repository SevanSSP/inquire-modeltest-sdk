from modeltestSDK import SDKclient, Campaign, Sensor
import datetime

client = SDKclient()


campaign = client.campaign.create("test",
                    "dest",
                    "2020-06-25 12:39:26.13573",
                    12,
                    1,
                    1025,
                    5,
                    10,
                    19)

print(campaign)
print(client.campaign.get(id=campaign.id))

sensor = client.sensor.create("test sensor",
                              "desc",
                              "SI",
                              "mass",
                              x=10,
                              y=10,
                              z=10,
                              is_local=True,
                              campaign_id=campaign.id)

print(sensor)
print(sensor.get_campaign())

# print(campaign.get(campaign.get_id("SDKlasse")))
# print(campaign.get_sensors(campaign.get_id("SDKlasse")))
# print(sensors.get(sensors.get_id("MK206")))
# print(campaign.get_tests(campaign.get_id("SDKlasse")))
# print(campaign.get_all())
