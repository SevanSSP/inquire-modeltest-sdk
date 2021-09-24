"""
Simple example using the sort and filter objects
"""
from modeltestSDK import Client
client = Client()

campaigns = client.campaign.get(filter_by=[
     client.filter.campaign.name == "Campaign name",
     client.filter.campaign.description == "Campaign description"],
     sort_by=[client.sort.campaign.date.asc])
