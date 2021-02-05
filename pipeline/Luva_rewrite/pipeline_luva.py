import os

os.environ["INQUIRE_MODELTEST_API_USER"] = "ebg"
os.environ["INQUIRE_MODELTEST_API_PASSWORD"] = "pass"
os.environ["INQUIRE_MODELTEST_API_HOST"] = r"http://127.0.0.1:8000"

import pandas as pd
import datetime
from modeltestSDK import Client
from modeltestSDK.resources import SensorList, FloaterConfigList, WaveCalibrationList
from scipy.io import loadmat

client = Client()

xls_loc = "Pipeline_Input_Luva_I.xls"
data_folder = r"c:\LuvaIimport"

df_campaign = pd.read_excel(xls_loc, sheet_name='Campaign', skiprows=2)
df_sensor = pd.read_excel(xls_loc, sheet_name='Sensor', skiprows=2, true_values="TRUE", false_values="FALSE")
df_floater_config = pd.read_excel(xls_loc, sheet_name='FloaterConfig', skiprows=2)
df_wave_calibration = pd.read_excel(xls_loc, sheet_name='WaveCal', skiprows=2)

restrict_access = True

campaign = client.campaign.create(name=df_campaign['name'][0],
                                  description=df_campaign['description'][0],
                                  location=df_campaign['location'][0],
                                  date=datetime.datetime(year=df_campaign['campaign_date'][0].year,
                                                         month=df_campaign['campaign_date'][0].month,
                                                         day=1).isoformat(),
                                  scale_factor=df_campaign['scale_factor'][0],
                                  water_depth=df_campaign['water_depth'][0],
                                  read_only=restrict_access)
#
# sensors = SensorList(resources=[])
# sensor_huid_mapper = dict()
#
# for index, sensor in df_sensor.iterrows():
#     sensor_input = {key: sensor[key] for key in ['name', 'description', 'unit', 'kind', 'source', 'x', 'y', 'z',
#                                                  'position_reference', 'position_heading_lock', 'position_draft_lock',
#                                                  'positive_direction_definition', 'area']}
#     sensors.resources.append(
#         client.sensor.create(**sensor_input,
#                              campaign_id=campaign.id,
#                              read_only=restrict_access)
#     )
#     sensor_huid_mapper[sensor['HUID']] = sensors.resources[-1].id
#
#
# floater_configs = FloaterConfigList(resources=[])
# floater_configs_huid_mapper = dict()
#
# for index, floater in df_floater_config.iterrows():
#     floater_input = {key: floater[key] for key in ['name', 'description', 'characteristic_length', 'draft']}
#     floater_configs.resources.append(
#         client.floater_config.create(**floater_input,
#                                      campaign_id=campaign.id,
#                                      read_only=restrict_access)
#     )
#     floater_configs_huid_mapper[floater['HUID']] = floater_configs.resources[-1].id

wave_calibrations = WaveCalibrationList(resources=[])
wave_calibration_huid_mapper = dict()

for index, wave_cal in df_wave_calibration.iterrows():
    test_prefix = 'test'
    test_suffix = ''
    filename = test_prefix + str(wave_cal['number']) + test_suffix
    try:
        remaining_channels = dict()
        data = loadmat(os.path.join(data_folder, filename), mdict=remaining_channels)
    except FileNotFoundError:
        raise FileNotFoundError(f"Wave calibration {wave_cal['number']} not found in folder {data_folder}")

    if wave_cal["description"] == '*':
        wave_cal["description"] = data['description']
    if wave_cal["test_date"] == '*':
        wave_cal["test_date"] = datetime.datetime.strptime(str(data['test_date'][0]), '%Y-%m-%d %H:%M').isoformat()

    wave_cal_input = {key: wave_cal[key] for key in ['number', 'description', 'test_date',
                                                     'wave_spectrum', 'wave_height', 'wave_period', 'gamma',
                                                     'wave_direction', 'current_velocity', 'current_direction']}

    wave_calibrations.resources.append(
        client.wave_calibration.create(**wave_cal_input,
                                       campaign_id=campaign.id,
                                       read_only=restrict_access)
    )
    wave_calibration_huid_mapper[wave_cal['HUID']] = wave_calibrations.resources[-1].id
