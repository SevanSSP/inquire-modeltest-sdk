from modeltestSDK import SDKclient
import requests
import datetime
from requests.exceptions import HTTPError

'''
resource = "campaign"
version = ""
endpoint = "all"
print( "/" + "/".join([p for p in ["api", resource, version, endpoint] if p.strip()]))


client = SDKclient()
print(client.get('campaign', 'all', "/all/"))
'''




for url in ['http://127.0.0.1:8000/api/campaign/']:
    try:
        response = requests.post(url,
                                 json={'name': 'SDKtesting2',
                                       'description': 'A campaign added from SDK2',
                                       'location': 'string',
                                       'date': (datetime.datetime.utcnow()).isoformat(),
                                       'diameter': 0,
                                       'scale_factor': 0,
                                       'water_density': 0,
                                       'water_depth': 0,
                                       'transient': 0})

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Posted!')
print( response.json())

for url in ['http://127.0.0.1:8000/api/campaign/all/']:
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

camp_json= response.json()
for camp in camp_json:
    print(camp['name'])