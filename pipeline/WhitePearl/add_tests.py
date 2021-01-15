import os
import re
import datetime
from scipy.io import loadmat
from modeltestSDK import SDKclient, Campaign
from .add_timeseries import read_datapoints_from_mat_with_pandas, read_wave_calibration_from_mat_with_pandas


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

            wave_calibration_id = None
            wave_cal = ["WAVE_1_CAL", "WAVE_2_CAL", "WAVE_3_CAL"]

            if category == "irregular wave":
                sea_state = re.findall("\d+\.\d+", test_description)
                sea_state = [float(i) for i in sea_state]

                wave_height = sea_state[0]
                wave_period = sea_state[1]

                wave_calibration = client.wave_calibration.create(description=test_description,
                                                                  test_date=test_date,
                                                                  campaign_id=campaign.id,
                                                                  wave_spectrum="jonswap",
                                                                  wave_height=wave_height,
                                                                  wave_period=wave_period,
                                                                  gamma=3.3, # Assumption
                                                                  wave_direction=0,
                                                                  current_velocity=0,
                                                                  current_direction=0,
                                                                  read_only=True,)
                wave_calibration_id = wave_calibration.id

                client.tag.create(name='comment', comment='Gamma unknown, 3.3 assumed', test_id=wave_calibration_id)

                read_wave_calibration_from_mat_with_pandas(data=data, test=wave_calibration,
                                                           calibration_sensors=wave_cal, client=client)


            floater_configs = client.floater_config.get_all().to_pandas() #Todo: filter by campaign
            floater_config_names = floater_configs['name'].tolist()

            floaterconfig_id = None
            for config_name in floater_config_names:
                if config_name in test_description:
                    config_index = floater_configs[floater_configs['name'] == config_name].index.values
                    floaterconfig_id = floater_configs.loc[config_index, 'id'].tolist()[0]

            test = client.floater_test.create(description=test_description,
                                              test_date=test_date,
                                              campaign_id=campaign.id,
                                              category=category,
                                              orientation=0,
                                              floaterconfig_id=floaterconfig_id,
                                              wave_id=wave_calibration_id,
                                              read_only=True,)

            #Todo: Add floater_test tags

            read_datapoints_from_mat_with_pandas(data=data, test=test, skip_channels=wave_cal, client=client)



        os.chdir(campaign_dir + "\\" + "Analysis/Timeseries")
