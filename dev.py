import requests
import os

user = os.getenv("INQUIRE_MODELTEST_API_USER")
passwd = os.getenv("INQUIRE_MODELTEST_API_PASSWORD")

token = requests.post('http://127.0.0.1:8000/api/v1/auth/token',  data=dict(username=user, password=passwd)).json()['access_token']
headers = {
    "Authorization": f"Bearer {token}"
}
resp = requests.get('http://127.0.0.1:8000/api/v1/campaign?skip=0&limit=100', headers=headers)
resp = requests.get('http://127.0.0.1:8000/api/v1/timeseries?skip=0&limit=100', headers=headers)


from modeltestsdk import Client
client = Client()

#SDK
campaigns = client.campaign.get()
campaign = campaigns[2]

import os
os.environ["INQUIRE_MODELTEST_API_USER"] = "slf"
os.environ["INQUIRE_MODELTEST_API_PASSWORD"] = "?8ZqpVu!"
os.environ["INQUIRE_MODELTEST_API_HOST"] = r"https://inquire-modeltest.azurewebsites.net"
from modeltestsdk import Client
client = Client()
camps = client.campaign.get()

camp = camps[2]
test = camp.tests().get_by_id('092cd3d9-9bef-4138-878f-e7c5ac14d35e')
'cb0debbf-94ea-4b0b-b1bd-34fcc3f9e6f2'

ts = client.timeseries.get_by_id('cb0debbf-94ea-4b0b-b1bd-34fcc3f9e6f2')

camp = camps.get_by_id('bf6e3bab-5e3a-413e-8c75-e02e4bd16b73')
test = client.test.get_by_id('d7449c71-8c44-4c21-9acd-729796cf88f2')
ft = client.floater_test.get_by_id('88651634-0f0a-4bbb-b6b4-a8725cdebf8b')
tests = client.test.get([client.filter.test.campaign_id == camp.id])
wc = client.wave_calibration.get()
ft_list = client.floater_test.get()


camp = client.campaign.get()[0]
test = camp.tests()[0]
sensor = camp.sensors()[0]
ts = test.timeseries(sensor.id)

l = client.test.get_by_campaign_id(k.id)