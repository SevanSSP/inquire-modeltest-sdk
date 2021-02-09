import os

os.environ["INQUIRE_MODELTEST_API_USER"] = "ebg"
os.environ["INQUIRE_MODELTEST_API_PASSWORD"] = "pass"
os.environ["INQUIRE_MODELTEST_API_HOST"] = r"http://127.0.0.1:8000"

import pandas as pd
import datetime
from modeltestSDK import Client
from modeltestSDK.resources import (SensorList, FloaterConfigList, WaveCalibrationList,
                                    WindCalibrationList, FloaterTestList, TagList)
from pipeline.utils import (sintef_matlab_import, apply_sensor_tag, add_ts_tags, add_test_tags,
                            add_derived_sensor_timeseries)

client = Client()

xls_loc = "Pipeline_Input_Luva_I.xls"
data_folder = r"C:\MTDBimport\Luva_I"

df_campaign = pd.read_excel(xls_loc, sheet_name='Campaign', skiprows=2)
df_sensor = pd.read_excel(xls_loc, sheet_name='Sensor', skiprows=2, true_values="TRUE", false_values="FALSE")
df_derived_sensor = pd.read_excel(xls_loc, sheet_name='DerivedSensor', skiprows=2,
                                  true_values="TRUE", false_values="FALSE")
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

tags = TagList(resources=[])
sensors = SensorList(resources=[])
sensor_huid_mapper = dict()

for _, sensor in df_sensor.iterrows():
    sensor_input = {key: sensor[key] for key in ['name', 'description', 'unit', 'kind', 'source', 'x', 'y', 'z',
                                                 'position_reference', 'position_heading_lock', 'position_draft_lock',
                                                 'positive_direction_definition', 'area']}
    sensors.resources.append(
        client.sensor.create(**sensor_input,
                             campaign_id=campaign.id,
                             read_only=restrict_access)
    )
    sensor_huid_mapper[sensor['HUID']] = sensor_id = sensors.resources[-1].id
    apply_sensor_tag(tag_list=tags, client_tag_object=client.tag, sensor_id=sensor_id,
                     sensor_tag_input=sensor['tags'], df_tag=df_tag, read_only=restrict_access)

for _, sensor in df_derived_sensor.iterrows():
    sensor_input = {key: sensor[key] for key in ['name', 'description', 'unit', 'kind', 'source', 'x', 'y', 'z',
                                                 'position_reference', 'position_heading_lock', 'position_draft_lock',
                                                 'positive_direction_definition', 'area']}
    sensors.resources.append(
        client.sensor.create(**sensor_input,
                             campaign_id=campaign.id,
                             read_only=restrict_access)
    )
    sensor_huid_mapper[sensor['HUID']] = sensor_id = sensors.resources[-1].id
    apply_sensor_tag(tag_list=tags, client_tag_object=client.tag, sensor_id=sensor_id,
                     sensor_tag_input=sensor['tags'], df_tag=df_tag, read_only=restrict_access)

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
wave_cal_keys = ['number', 'description', 'test_date', 'wave_spectrum', 'wave_height', 'wave_period', 'gamma',
                 'wave_direction', 'current_velocity', 'current_direction']

wave_calibration_huid_mapper = sintef_matlab_import(resource=wave_calibrations,
                                                    client_test_object=client.wave_calibration,
                                                    client_ts_object=client.timeseries, campaign_id=campaign.id,
                                                    read_only=restrict_access, default_start_time=1419,
                                                    default_end_time=1419 + 3 * 60 * 60, data_folder=data_folder,
                                                    df_test=df_wave_calibration, df_sensor=df_sensor,
                                                    required_keys=wave_cal_keys, default_date=campaign.date,
                                                    sensor_huid_mapper=sensor_huid_mapper)

wind_calibrations = WindCalibrationList(resources=[])
wind_cal_keys = ['number', 'description', 'test_date', 'wind_spectrum', 'wind_velocity', 'zref', 'wind_direction']

wind_calibration_huid_mapper = sintef_matlab_import(resource=wind_calibrations,
                                                    client_test_object=client.wind_calibration,
                                                    client_ts_object=client.timeseries, campaign_id=campaign.id,
                                                    read_only=restrict_access, default_start_time=1419,
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
                                                read_only=restrict_access, default_start_time=1419,
                                                default_end_time=1419 + 3 * 60 * 60, data_folder=data_folder,
                                                df_test=df_floater_test, df_sensor=df_sensor,
                                                required_keys=floater_test_keys, default_date=campaign.date,
                                                sensor_huid_mapper=sensor_huid_mapper,
                                                wave_calibration_huid_mapper=wave_calibration_huid_mapper,
                                                wind_calibration_huid_mapper=wind_calibration_huid_mapper,
                                                floater_configs_huid_mapper=floater_configs_huid_mapper,
                                                secondary_prefix='grnw')

add_derived_sensor_timeseries(client=client, df_derived_sensor=df_derived_sensor, sensor_huid_mapper=sensor_huid_mapper,
                              test_mapper={**wave_calibration_huid_mapper, **wind_calibration_huid_mapper,
                                           **floater_test_huid_mapper})

add_test_tags(tag_list=tags, client_tag_object=client.tag, df_tag=df_tag,
              df_tests=[df_wave_calibration, df_wind_calibration, df_floater_test],
              test_mapper={**wave_calibration_huid_mapper, **wind_calibration_huid_mapper, **floater_test_huid_mapper},
              read_only=restrict_access)

add_ts_tags(tag_list=tags, client_tag_object=client.tag, df_timeseries_tag=df_timeseries_tag, df_tag=df_tag,
            ts_client=client.timeseries, filter=client.filter,
            test_mapper={**wave_calibration_huid_mapper, **wind_calibration_huid_mapper, **floater_test_huid_mapper},
            sensor_mapper=sensor_huid_mapper, read_only=restrict_access)
