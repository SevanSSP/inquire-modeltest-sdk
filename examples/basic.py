"""
Basic example showing how to initiate the client and list available model test campaigns.
"""
from modeltestsdk import Client


client = Client()
campaigns = client.campaign.get()
