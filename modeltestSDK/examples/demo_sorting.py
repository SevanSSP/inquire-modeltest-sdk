from modeltestSDK import SDKclient

client = SDKclient()

print(client.campaign.get_all(filter_by=[client.query.campaign.scale_factor >= 100]))

print(client.campaign.get_all(filter_by=[client.query.campaign.scale_factor >= 100, client.query.campaign.water_depth > 300], sort_by=[client.query.campaign.name.ascending]))

print(client.campaign.get_all(sort_by=[client.query.campaign.name.ascending]))

