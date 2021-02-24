"""
Basic example showing how to initiate the client and list available model test campaigns.
"""
from modeltestSDK import Client


client = Client()
campaigns = client.campaign.get()
