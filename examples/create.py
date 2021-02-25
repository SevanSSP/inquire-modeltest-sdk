"""
Simple create example
"""
from datetime import datetime
from modeltestSDK import Client

client = Client()
campaign = client.campaign.create(name="Campaign name",
                                  description="Campaign description",
                                  date=datetime(year=2000, month=1, day=1).isoformat(),
                                  location="Test location",
                                  scale_factor=52,
                                  water_depth=300,
                                  read_only=True)
