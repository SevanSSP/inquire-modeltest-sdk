from modeltestSDK import SDKclient


client = SDKclient()
client.printAllCampaignNames()


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

'''