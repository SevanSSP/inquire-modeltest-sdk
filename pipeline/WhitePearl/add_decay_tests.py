import os
from modeltestSDK.resources import Campaign
from modeltestSDK.client import SDKclient
import string


def add_decay_tests(campaign_dir, campaign: Campaign, client: SDKclient):
    os.chdir(campaign_dir)
    os.chdir(os.getcwd() + "\\" + "Analysis/Timeseries")
    test_categories = os.listdir(path='.')
    for category in test_categories:

        os.chdir(os.getcwd() + "\\" + category)
        tests = os.listdir(path='.')
        if category == "Decay":
            category = category.lower()
        elif category == "IrrWave":
            category = "irregular wave"
        else:
            raise Exception
        for test in tests:
            client.floater_test.create(description=test,
                                       test_date="12012021",
                                       campaign_id=campaign.id,
                                       category=category,
                                       orientation=0,
                                       )

        os.chdir(campaign_dir + "\\" +"Analysis/Timeseries")


