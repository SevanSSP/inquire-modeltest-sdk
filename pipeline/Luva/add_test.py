import os
import re
import datetime
from scipy.io import loadmat
from modeltestSDK import SDKclient, Campaign
from .add_timeseries import read_datapoints
from .add_calibrations import add_wind_calibrations, add_current_calibrations, add_wave_calibrations

category_dict = {'Current': 'current force', 'Wind': 'wind force', 'Decay': 'decay', 'IrrWave': 'irregular wave',
                 'RegWave': 'regular wave', }


def add_tests(campaign_dir, campaign: Campaign, client: SDKclient):
    existing_wave_calibrations = {}

    os.chdir(campaign_dir)
    os.chdir(os.getcwd() + "\\" + "Analysis/Timeseries (To be modified)")
    test_categories = os.listdir(path='.')
    for category in test_categories:

        os.chdir(os.getcwd() + "\\" + category)
        tests = os.listdir(path='.')
        if category not in category_dict:
            raise KeyError('Unknown test category')
        else:
            category = category_dict[category]

        for test in tests:
            if not test.endswith('.mat'):
                continue
            if os.path.isdir(test):
                continue
            data = loadmat(os.getcwd() + "\\" + test)

            test_date_str = str(data['test_date'])[2:-2]
            test_date = datetime.datetime.strptime(test_date_str, '%Y-%m-%d %H:%M').isoformat()

            test_description = str(data['comment'])[2:-2]

            test_number = str(data['test_num'][0])[1:-1]

            wave_calibration_id = None
            wave_cal = ["WAVE_1_CAL", "WAVE_2_CAL", "WAVE_3_CAL"]

            if category == "current force":
                wave_calibration_id = add_current_calibrations(campaign=campaign,client=client)
                os.chdir('..')

            if category == "irregular wave":
                add_wave_calibrations(campaign=campaign,client=client)
                if category == 'RegWave':
                    continue
                if category == "Wind":
                    wind_calibrations = add_wind_calibrations(campaign=campaign, client=client)
                    os.chdir('..')

            floater_configs = client.floater_config.get_all().to_pandas()  # Todo: filter by campaign
            floater_config_names = floater_configs['name'].tolist()

            floater_config_id = None
            for config_name in floater_config_names:
                if config_name in test_description:
                    config_index = floater_configs[floater_configs['name'] == config_name].index.values
                    floater_config_id = floater_configs.loc[config_index, 'id'].tolist()[0]

            test = client.floater_test.create(number=test_number,
                                              description=test_description,
                                              test_date=test_date,
                                              campaign_id=campaign.id,
                                              category=category,
                                              orientation=0,
                                              floaterconfig_id=floater_config_id,
                                              wave_id=wave_calibration_id,
                                              read_only=True, )

            # Todo: Add floater_test tags

            read_datapoints(data=data, test=test, skip_channels=wave_cal, client=client)

        os.chdir(campaign_dir + "\\" + "Analysis/Timeseries (To be modified)")
