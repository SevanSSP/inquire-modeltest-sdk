from modeltestSDK import SDKclient
import datetime


client = SDKclient()

client.post("campaign",body={'name': 'SDKt2',
                                       'description': 'A campaign added from SDK2',
                                       'location': 'string',
                                       'date': (datetime.datetime.utcnow()).isoformat(),
                                       'diameter': 0,
                                       'scale_factor': 0,
                                       'water_density': 0,
                                       'water_depth': 0,
                                       'transient': 0})
campaign = client.get("campaign","all", parameters={"name":"SDKt"})

for camp in campaign:
    print(camp['name'])

