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

df_campaign = pd.read_excel(xls_loc, sheet_name='Campaign', skiprows=2)
df_sensor = pd.read_excel(xls_loc, sheet_name='Sensor', skiprows=2, true_values="TRUE", false_values="FALSE")
# df_sensor = df_sensor.fillna(value=None)
df_floater_config = pd.read_excel(xls_loc, sheet_name='FloaterConfig', skiprows=2)
df_wave_calibration = pd.read_excel(xls_loc, sheet_name='WaveCal', skiprows=2)

restrict_access = True

campaign = client.campaign.create(name=df_campaign['name'][0],
                                  description=df_campaign['description'][0],
                                  location=df_campaign['location'][0],
                                  date=datetime.datetime(year=df_campaign['campaign_date'][0].year,
                                                         month=df_campaign['campaign_date'][0].month,
                                                         day=1).isoformat(),
                                  scale_factor=float(df_campaign['scale_factor'][0]),
                                  water_depth=float(df_campaign['water_depth'][0]),
                                  read_only=restrict_access)

# sensors = SensorList(resources=[])
#
# for index, sensor in df_sensor.iterrows():
#     sensors.resources.append(
#         client.sensor.create(name=sensor['name'],
#                              description=sensor['description'],
#                              unit=sensor['unit'],
#                              kind=sensor['kind'],
#                              x=sensor['x'],
#                              y=sensor['y'],
#                              z=sensor['z'],
#                              is_local=sensor['is_local'],
#                              campaign_id=campaign.id,
#                              read_only=restrict_access)
#     )
#
# floater_configs = FloaterConfigList(resources=[])
#
# for index, floater in df_floater_config.iterrows():
#     floater_configs.resources.append(
#         client.floater_config.create(name=floater['name'],
#                                      description=floater['description'],
#                                      campaign_id=campaign.id,
#                                      draft=floater['draft'],
#                                      characteristic_length=floater['characteristic_length'],
#                                      read_only=restrict_access)
#     )
#
# wave_calibrations = WaveCalibrationList(resources=[])
#
# for index, wave_cal in df_wave_calibration.iterrows():
#     campain_folder = "C://users/jen.SEVAN/documents/"
#     test_prefix = 'test'
#     test_suffix = ''
#     filename = test_prefix + str(wave_cal['number']) + test_suffix
#     try:
#         remaining_channels = dict()
#         data = loadmat(campain_folder + filename, mdict=remaining_channels)
#     except FileNotFoundError:
#         raise FileNotFoundError(f"Wave calibration {wave_cal['number']} not found in folder {campain_folder}")
#
#     if wave_cal["description"] == '*':
#         description = data['description']
#     else:
#         description = wave_cal["description"]
#     if wave_cal["test_date"] == '*':
#         test_date = data['date'][0][0]
#     else:
#         test_date = wave_cal["test_date"]
