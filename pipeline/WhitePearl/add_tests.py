import os
import datetime
from scipy.io import loadmat
from modeltestSDK import SDKclient, Campaign
from .add_timeseries import read_datapoints_from_mat_with_pandas
import string


def add_tests(campaign_dir, campaign: Campaign, client: SDKclient):
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
            data = loadmat(os.getcwd() + "\\" + test)

            test_date_str = str(data['test_date'])[2:-2]
            test_date = datetime.datetime.strptime(test_date_str, '%H:%M %d/%m/%y').isoformat()

            test_description = str(data['comment'])[2:-2]

            floaterconfig_id = None  # TODO: implement system to connect config to test, maybe from comment

            test = client.floater_test.create(description=test_description,
                                              test_date=test_date,
                                              campaign_id=campaign.id,
                                              category=category,
                                              orientation=0,
                                              floaterconfig_id=floaterconfig_id,
                                              read_only=True,)

            read_datapoints_from_mat_with_pandas(data=data, test=test, client=client)

        os.chdir(campaign_dir + "\\" + "Analysis/Timeseries")
