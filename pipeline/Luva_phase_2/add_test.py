import os
import datetime
import re
from scipy.io import loadmat
from modeltestSDK import Client
from modeltestSDK.resources import Campaign
from pipeline.Luva.add_timeseries import read_datapoints


category_dict = {'Current': 'current force', 'Wind': 'wind force', 'Decay': 'decay', 'IrrWave': 'irregular wave',
                 'RegWave': 'regular wave', }


def add_tests(campaign_dir, campaign: Campaign, client: Client):
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

            test_number = str(data['test_num'][0])[2:-2]

            wave_calibration_id = None
            wind_calibration_id = None

            if category == "current force":
                res = re.findall(r'C[-+]?[0-9]*\.?[0-9]+', test_description)
                current_velocity = res[0][1:]
                wave_calibration_id = client.wave_calibration.get_all(
                    filter_by=[client.filter.wave_calibration.current_velocity == current_velocity,
                               client.filter.wave_calibration.campaign_id == campaign.id])[0].id
            if category == "irregular wave":
                res = re.findall(r'H[-+]?[0-9]*\.?[0-9]+', test_description)
                if res:
                    wave_height = float(res[0][1:])
                else:
                    raise KeyError("Wave height not found")
                res = re.findall(r'T[-+]?[0-9]*\.?[0-9]+', test_description)
                if res:
                    wave_period = float(res[0][1:])
                else:
                    raise KeyError("Wave period not found")
                res = re.findall(r'C[-+]?[0-9]*\.?[0-9]+', test_description)
                if res:
                    current_vel = float(res[0][1:])
                else:
                    current_vel = 0
                if test_description.find("IRR") == -1:
                    wave_spectrum = "regular"
                else:
                    wave_spectrum = "jonswap"
                res = re.findall(r'W[-+]?[0-9]*\.?[0-9]+', test_description)
                if res:
                    wind_vel = float(res[0][1:])
                else:
                    wind_vel = 0
                wave_calibration_id = client.wave_calibration.get_all(
                    filter_by=[client.filter.wave_calibration.wave_height == wave_height,
                               client.filter.wave_calibration.wave_period == wave_period,
                               client.filter.wave_calibration.current_velocity == current_vel,
                               client.filter.wave_calibration.wave_spectrum == wave_spectrum,
                               client.filter.wind_calibration.campaign_id == campaign.id])[0].id

                if not wind_vel == 0:
                    wind_calibration_id = client.wind_calibration.get_all(
                        filter_by=[client.filter.wind_calibration.wind_velocity == wind_vel,
                                   client.filter.wind_calibration.campaign_id == campaign.id])[0].id

            if category == 'RegWave':
                continue
            if category == "Wind":
                res = re.findall(r'W[-+]?[0-9]*\.?[0-9]+', test_description)
                wind_speed = res[0][1:]
                wind_calibration_id = client.wind_calibration.get_all(
                    filter_by=[client.filter.wind_calibration.wind_velocity == wind_speed,
                               client.filter.wind_calibration.campaign_id == campaign.id])[0].id

            floater_configs = client.floater_config.get_all().to_pandas()  # Todo: filter by campaign
            floater_config_names = floater_configs['name'].tolist()

            floater_config_id = None
            for config_name in floater_config_names:
                if config_name in test_description:
                    config_index = floater_configs[floater_configs['name'] == config_name].index.values
                    floater_config_id = floater_configs.loc[config_index, 'id'].tolist()[0]

            if "HD60" in test_description:
                orientation = 60
            else:
                orientation = 0

            test = client.floater_test.create(number=test_number,
                                              description=test_description,
                                              test_date=test_date,
                                              campaign_id=campaign.id,
                                              category=category,
                                              orientation=orientation,
                                              floater_config_id=floater_config_id,
                                              wave_id=wave_calibration_id,
                                              wind_id=wind_calibration_id,
                                              read_only=True, )

            # Todo: Add floater_test tags

            read_datapoints(data=data, test=test, skip_channels=[], client=client)

        os.chdir(campaign_dir + "\\" + "Analysis/Timeseries (To be modified)")
