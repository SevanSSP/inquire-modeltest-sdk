import os

os.environ["INQUIRE_MODELTEST_API_USER"] = "ebg"
os.environ["INQUIRE_MODELTEST_API_PASSWORD"] = "pass"
os.environ["INQUIRE_MODELTEST_API_HOST"] = r"http://127.0.0.1:8000"

import pandas as pd
import datetime
from modeltestSDK import Client
from modeltestSDK.resources import (SensorList, FloaterConfigList, WaveCalibrationList, \
                                    WindCalibrationList, FloaterTestList)
from pipeline.utils import sintef_matlab_import

client = Client()

xls_loc = "Pipeline_Input_Luva_I.xls"
data_folder = r"C:\MTDBimport\Luva_I"

df_campaign = pd.read_excel(xls_loc, sheet_name='Campaign', skiprows=2)
df_sensor = pd.read_excel(xls_loc, sheet_name='Sensor', skiprows=2, true_values="TRUE", false_values="FALSE")
df_floater_config = pd.read_excel(xls_loc, sheet_name='FloaterConfig', skiprows=2)
df_wave_calibration = pd.read_excel(xls_loc, sheet_name='WaveCal', skiprows=2)
df_wind_calibration = pd.read_excel(xls_loc, sheet_name='WindCal', skiprows=2)
df_floater_test = pd.read_excel(xls_loc, sheet_name='FloaterTest', skiprows=2,
                                converters={'wave HUID': str, 'wind HUID': str, 'floater config HUID': str})
df_tag = pd.read_excel(xls_loc, sheet_name='Tag', skiprows=2)
df_timeseries_tag = pd.read_excel(xls_loc, sheet_name='Tag TS', skiprows=2)

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

sensors = SensorList(resources=[])
sensor_huid_mapper = dict()

for index, sensor in df_sensor.iterrows():
    sensor_input = {key: sensor[key] for key in ['name', 'description', 'unit', 'kind', 'source', 'x', 'y', 'z',
                                                 'position_reference', 'position_heading_lock', 'position_draft_lock',
                                                 'positive_direction_definition', 'area']}
    sensors.resources.append(
        client.sensor.create(**sensor_input,
                             campaign_id=campaign.id,
                             read_only=restrict_access)
    )
    sensor_huid_mapper[sensor['HUID']] = sensors.resources[-1].id

floater_configs = FloaterConfigList(resources=[])
floater_configs_huid_mapper = dict()

for index, floater in df_floater_config.iterrows():
    floater_input = {key: floater[key] for key in ['name', 'description', 'characteristic_length', 'draft']}
    floater_configs.resources.append(
        client.floater_config.create(**floater_input,
                                     campaign_id=campaign.id,
                                     read_only=restrict_access)
    )
    floater_configs_huid_mapper[floater['HUID']] = floater_configs.resources[-1].id

wave_calibrations = WaveCalibrationList(resources=[])
# wave_calibration_huid_mapper = dict()

# for index, wave_cal in df_wave_calibration.iterrows():
#     test_prefix = 'test'
#     test_suffix = ''
#     filename = test_prefix + str(wave_cal['number']) + test_suffix
#     try:
#         remaining_channels = dict()
#         data = loadmat(os.path.join(data_folder, filename), mdict=remaining_channels)
#     except FileNotFoundError:
#         wave_cal_input = {key: wave_cal[key] for key in ['number', 'description', 'test_date',
#                                                          'wave_spectrum', 'wave_height', 'wave_period', 'gamma',
#                                                          'wave_direction', 'current_velocity', 'current_direction']}
#
#         wave_cal_input['description'] = wave_cal['description'] + ' Note: timeseries not available'
#         wave_cal_input['test_date'] = datetime.datetime(year=df_campaign['campaign_date'][0].year,
#                                                         month=df_campaign['campaign_date'][0].month,
#                                                         day=1).isoformat()
#
#         wave_calibrations.resources.append(
#             client.wave_calibration.create(**wave_cal_input,
#                                            campaign_id=campaign.id,
#                                            read_only=restrict_access)
#         )
#         wave_calibration_huid_mapper[wave_cal['HUID']] = test_id = wave_calibrations.resources[-1].id
#         print(f"Wave calibration {wave_cal['number']} not found in folder {data_folder}. Creating empty test.")
#         continue
#
#     if wave_cal["description"] == '*':
#         wave_cal["description"] = data['comment']
#     if wave_cal["test_date"] == '*':
#         wave_cal["test_date"] = datetime.datetime.strptime(str(data['test_date'][0]), '%Y-%m-%d %H:%M').isoformat()
#
#     wave_cal_input = {key: wave_cal[key] for key in ['number', 'description', 'test_date',
#                                                      'wave_spectrum', 'wave_height', 'wave_period', 'gamma',
#                                                      'wave_direction', 'current_velocity', 'current_direction']}
#
#     wave_calibrations.resources.append(
#         client.wave_calibration.create(**wave_cal_input,
#                                        campaign_id=campaign.id,
#                                        read_only=restrict_access)
#     )
#     wave_calibration_huid_mapper[wave_cal['HUID']] = test_id = wave_calibrations.resources[-1].id
#
#     time = data['Time'][0].tolist()
#     fs = data['fs'][0][0]
#
#     for key in data.keys():
#         if key in ['Time', 'comment', 'test_date', 'test_num', 'fs', ] or key[0:2] == '__':
#             continue
#         elif key in df_sensor['name'].values:
#             value = data[key][0].tolist()
#             sensor_id = sensor_huid_mapper[df_sensor['HUID'][df_sensor['name'] == 'WAVE_2'].values[0]]
#         else:
#             sensor_found = False
#             for _, sensor in df_sensor.iterrows():
#                 if type(sensor['aliases']) == str:
#                     if key in [alias.strip() for alias in sensor['aliases'].split(',')]:
#                         value = data[key][0].tolist()
#                         sensor_id = sensor_huid_mapper[sensor['HUID']]
#                         sensor_found = True
#                         break
#             if not sensor_found:
#                 print(f'No sensor found for data labelled {key} skipping this record')
#                 continue
#
#         # ts = client.timeseries.create(sensor_id=sensor_id,
#         #                               test_id=test_id,
#         #                               default_start_time=1419,
#         #                               default_end_time=1419 + 3 * 60 * 60,
#         #                               fs=fs,
#         #                               read_only=True)
#         #
#         # body = {'data': {'time': time,
#         #                  'value': value}}
#         tic = timer.perf_counter()
#         # client.timeseries.post_data_points(ts.id, form_body=body)
#         toc = timer.perf_counter()
#         print(
#             f"Posting timeseries for sensor {key} in test {wave_cal_input['number']} took {toc - tic:0.4f}s")


wave_cal_keys = ['number', 'description', 'test_date', 'wave_spectrum', 'wave_height', 'wave_period', 'gamma',
                 'wave_direction', 'current_velocity', 'current_direction']

wave_calibration_huid_mapper = sintef_matlab_import(resource=wave_calibrations,
                                                    client_test_object=client.wave_calibration,
                                                    client_ts_object=client.timeseries, campaign_id=campaign.id,
                                                    restrict_access=restrict_access, default_start_time=1419,
                                                    default_end_time=1419 + 3 * 60 * 60, data_folder=data_folder,
                                                    df_test=df_wave_calibration, df_sensor=df_sensor,
                                                    required_keys=wave_cal_keys, default_date=campaign.date,
                                                    sensor_huid_mapper=sensor_huid_mapper)

wind_calibrations = WindCalibrationList(resources=[])
wind_cal_keys = ['number', 'description', 'test_date', 'wind_spectrum', 'wind_velocity', 'zref', 'wind_direction']

wind_calibration_huid_mapper = sintef_matlab_import(resource=wind_calibrations,
                                                    client_test_object=client.wind_calibration,
                                                    client_ts_object=client.timeseries, campaign_id=campaign.id,
                                                    restrict_access=restrict_access, default_start_time=1419,
                                                    default_end_time=1419 + 3 * 60 * 60, data_folder=data_folder,
                                                    df_test=df_wind_calibration, df_sensor=df_sensor,
                                                    required_keys=wind_cal_keys, default_date=campaign.date,
                                                    sensor_huid_mapper=sensor_huid_mapper)

floater_tests = FloaterTestList(resources=[])
floater_test_keys = ['number', 'description', 'test_date', 'category', 'orientation', 'wave_id', 'wind_id',
                     'floaterconfig_id']

floater_test_huid_mapper = sintef_matlab_import(resource=floater_tests,
                                                client_test_object=client.floater_test,
                                                client_ts_object=client.timeseries, campaign_id=campaign.id,
                                                restrict_access=restrict_access, default_start_time=1419,
                                                default_end_time=1419 + 3 * 60 * 60, data_folder=data_folder,
                                                df_test=df_floater_test, df_sensor=df_sensor,
                                                required_keys=floater_test_keys, default_date=campaign.date,
                                                sensor_huid_mapper=sensor_huid_mapper,
                                                wave_calibration_huid_mapper=wave_calibration_huid_mapper,
                                                wind_calibration_huid_mapper=wind_calibration_huid_mapper,
                                                floater_configs_huid_mapper=floater_configs_huid_mapper,
                                                secondary_prefix='grnw')
