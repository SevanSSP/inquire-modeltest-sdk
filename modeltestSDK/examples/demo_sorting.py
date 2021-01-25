from modeltestSDK import Client

client = Client()

print(client.campaign.get_all(filter_by=[client.filter.campaign.scale_factor >= 100]))

print(client.campaign.get_all(filter_by=[client.filter.campaign.scale_factor >= 100,
                                         client.filter.campaign.water_depth > 300],
                              sort_by=[client.sort.campaign.name.ascending]))

print(client.campaign.get_all(sort_by=[client.sort.campaign.name.asc]))

print(client.sensor.get_all(filter_by=[client.filter.sensor.name == "REL_WAVE_0"]))

print(client.tag.get_all(filter_by=[client.filter.tags.name == "comment"]))

camp = client.campaign.get_by_name("WhitePearl")
