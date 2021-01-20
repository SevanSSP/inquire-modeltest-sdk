import os
import re
import datetime
from scipy.io import loadmat
from modeltestSDK import SDKclient, Campaign
from .add_timeseries import read_datapoints

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
                os.chdir(os.getcwd() + "\\Calib")
                calibration = os.listdir(path='.')[0]
                calibration_data = loadmat(os.getcwd() + "\\" + calibration)
                calibration_description = str(calibration_data['comment'])[2:-2]
                calibration_number = str(calibration_data['test_num'][0])[1:-1]
                calibration_date = str(calibration_data['test_date'])[2:-2]
                current_vel_str = re.findall("\d+,\d+", calibration_description)[0]
                current_vel = float(current_vel_str.replace(',', '.'))

                current_calibration = client.wave_calibration.create(number=calibration_number,
                                                                     description=calibration_description,
                                                                     test_date=calibration_date,
                                                                     campaign_id=campaign.id,
                                                                     wave_spectrum="jonswap",
                                                                     wave_height=0,
                                                                     wave_period=0,
                                                                     gamma=0,
                                                                     wave_direction=0,
                                                                     current_velocity=current_vel,
                                                                     current_direction=0,  # TODO: Direction?
                                                                     read_only=True, )
                read_datapoints(data=calibration_data, test=current_calibration, client=client)

                wave_calibration_id = current_calibration.id

                os.chdir('..')

            if category == "irregular wave":
                sea_state = re.findall("\d+\.\d+", test_description)
                sea_state = [float(i) for i in sea_state]

                wave_height = sea_state[0]
                wave_period = sea_state[1]

                if wave_height == 9.4 and wave_period == 14.1:
                    cal_test_num = "8011"
                elif wave_height == 12 and wave_period == 13:
                    cal_test_num = "8022"
                elif wave_height == 13 and wave_period == 16:
                    cal_test_num = "8031"
                else:
                    cal_test_num = "unknown wave calib"

                if cal_test_num not in existing_wave_calibrations:
                    wave_calibration = client.wave_calibration.create(number=cal_test_num,
                                                                      description=test_description,
                                                                      test_date=test_date,
                                                                      campaign_id=campaign.id,
                                                                      wave_spectrum="jonswap",
                                                                      wave_height=wave_height,
                                                                      wave_period=wave_period,
                                                                      gamma=3.3,  # Assumption
                                                                      wave_direction=0,
                                                                      current_velocity=0,
                                                                      current_direction=0,
                                                                      read_only=True, )
                    wave_calibration_id = wave_calibration.id
                    client.tag.create(name='comment', comment='Gamma unknown, 3.3 assumed', test_id=wave_calibration_id)
                    read_wave_calibration_from_mat_with_pandas(data=data, test=wave_calibration,
                                                               calibration_sensors=wave_cal, client=client)
                    existing_wave_calibrations[cal_test_num] = wave_calibration_id

                else:
                    wave_calibration_id = existing_wave_calibrations[cal_test_num]

            floater_configs = client.floater_config.get_all().to_pandas()  # Todo: filter by campaign
            floater_config_names = floater_configs['name'].tolist()

            floaterconfig_id = None
            for config_name in floater_config_names:
                if config_name in test_description:
                    config_index = floater_configs[floater_configs['name'] == config_name].index.values
                    floaterconfig_id = floater_configs.loc[config_index, 'id'].tolist()[0]

            test = client.floater_test.create(number=test_number,
                                              description=test_description,
                                              test_date=test_date,
                                              campaign_id=campaign.id,
                                              category=category,
                                              orientation=0,
                                              floaterconfig_id=floaterconfig_id,
                                              wave_id=wave_calibration_id,
                                              read_only=True, )

            # Todo: Add floater_test tags

            read_datapoints(data=data, test=test, skip_channels=wave_cal, client=client)

        os.chdir(campaign_dir + "\\" + "Analysis/Timeseries (To be modified)")
