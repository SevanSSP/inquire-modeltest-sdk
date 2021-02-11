import os
import datetime
from typing import List, Union
import pandas as pd
from scipy.io import loadmat
import numpy as np
import time as timer
from modeltestSDK.api import WaveCalibrationAPI, WindCalibrationAPI, FloaterTestAPI, TimeseriesAPI
from modeltestSDK import Client


def sintef_matlab_import(client_test_object: Union[WaveCalibrationAPI, WindCalibrationAPI, FloaterTestAPI],
                         client_ts_object: TimeseriesAPI,
                         campaign_id: str, read_only: bool, default_start_time: float, default_end_time: float,
                         data_folder: str, df_test: pd.DataFrame, df_sensor: pd.DataFrame, required_keys: List[str],
                         default_date: datetime.datetime, sensor_huid_mapper: dict, dateformat: str = '%Y-%m-%d %H:%M',
                         wave_calibration_huid_mapper: dict = None, wind_calibration_huid_mapper: dict = None,
                         floater_configs_huid_mapper: dict = None, secondary_prefix: str = None,
                         secondary_duplicates: list = (),
                         cals_from_floater_test: list = []):
    huid_mapper = dict()
    for _, test_data in df_test.iterrows():

        if 'wave HUID' in test_data and wave_calibration_huid_mapper is not None:
            if isinstance(test_data['wave HUID'], float) and np.isnan(test_data['wave HUID']):
                test_data['wave_id'] = None
            else:
                test_data['wave_id'] = wave_calibration_huid_mapper[test_data['wave HUID']]
        else:
            test_data['wave_id'] = None

        if 'wind HUID' in test_data and wind_calibration_huid_mapper is not None:
            if isinstance(test_data['wind HUID'], float) and np.isnan(test_data['wind HUID']):
                test_data['wind_id'] = None
            else:
                test_data['wind_id'] = wind_calibration_huid_mapper[test_data['wind HUID']]
        else:
            test_data['wind_id'] = None

        if 'floater config HUID' in test_data and floater_configs_huid_mapper is not None:
            test_data['floaterconfig_id'] = floater_configs_huid_mapper[test_data['floater config HUID']]

        test_prefix = 'test'
        filename = test_prefix + str(test_data['number'])
        try:
            ts_data = loadmat(os.path.join(data_folder, filename))
        except (FileNotFoundError, TypeError) as e:
            test_data_input = {key: test_data[key] for key in required_keys}
            if 'derive from floater test' in test_data and test_data['derive from floater test'] is True:
                cals_from_floater_test.append(test_data['HUID'])
            else:
                test_data_input['description'] = test_data['description'] + ' Note: timeseries not available'

            test_data_input['test_date'] = default_date

            created_test = client_test_object.create(**test_data_input,
                                                     campaign_id=campaign_id,
                                                     read_only=read_only)

            huid_mapper[test_data['HUID']] = test_id = created_test.id
            if isinstance(e, FileNotFoundError):
                print(f"Test {test_data['number']} not found in folder {data_folder}. Creating empty test.")
            elif isinstance(e, TypeError):
                print(
                    f"Test {test_data['number']} corrupted in folder {data_folder}. Creating empty test.")
            continue

        if test_data["description"] == '*':
            test_data["description"] = ts_data['comment'][0]
        if test_data["test_date"] == '*':
            test_data["test_date"] = datetime.datetime.strptime(str(ts_data['test_date'][0]),
                                                                dateformat).isoformat()
        test_data_input = {key: test_data[key] for key in required_keys}

        created_test = client_test_object.create(**test_data_input,
                                                 campaign_id=campaign_id,
                                                 read_only=read_only)

        huid_mapper[test_data['HUID']] = test_id = created_test.id

        mat_to_ts(ts_data=ts_data, test_id=test_id, df_sensor=df_sensor,
                  sensor_huid_mapper=sensor_huid_mapper,
                  client_ts_object=client_ts_object, default_start_time=default_start_time,
                  default_end_time=default_end_time, read_only=read_only)

        if secondary_prefix:
            filename = secondary_prefix + str(test_data['number'])
            try:
                secondary_ts_data = loadmat(os.path.join(data_folder, filename))
                for duplicate in secondary_duplicates:
                    try:
                        secondary_ts_data.pop(duplicate)
                    except KeyError:
                        print(f"failed to pop {duplicate} from secondary input "
                              f"{filename}. Continuing...")

                mat_to_ts(ts_data=secondary_ts_data, test_id=test_id,
                          df_sensor=df_sensor,
                          sensor_huid_mapper=sensor_huid_mapper, client_ts_object=client_ts_object,
                          default_start_time=default_start_time, default_end_time=default_end_time, read_only=read_only)
            except FileNotFoundError:
                print(f"Secondary file {secondary_prefix}{test_data['number']} not found in folder {data_folder}. "
                      f"No additional timeseries created")

        if 'wave HUID' in test_data and test_data['wave HUID'] in cals_from_floater_test:
            cals_from_floater_test.remove(test_data['wave HUID'])

            cal_ts_data = {'WAVE_1': ts_data['WAVE_1_CAL'],
                           'WAVE_2': ts_data['WAVE_2_CAL'],
                           'WAVE_3': ts_data['WAVE_3_CAL'],
                           'Time': ts_data['Time'],
                           'fs': ts_data['fs'],
                           'test_num': [[test_data['wave HUID']]]}

            mat_to_ts(ts_data=cal_ts_data, test_id=wave_calibration_huid_mapper[test_data['wave HUID']],
                      df_sensor=df_sensor,
                      sensor_huid_mapper=sensor_huid_mapper, client_ts_object=client_ts_object,
                      default_start_time=default_start_time, default_end_time=default_end_time, read_only=read_only)

    return huid_mapper, cals_from_floater_test


def mat_to_ts(ts_data: dict, test_id: str, df_sensor: pd.DataFrame,
              sensor_huid_mapper: dict, client_ts_object: TimeseriesAPI,
              default_start_time: float, default_end_time: float, read_only: bool):
    time = ts_data['Time'][0].tolist()
    fs = ts_data['fs'][0][0]

    for key in ts_data.keys():
        if key in ['Time', 'comment', 'test_date', 'test_num', 'fs', ] or key[0:2] == '__':
            continue
        elif key in df_sensor['name'].values:
            value = ts_data[key][0].tolist()
            sensor_id = sensor_huid_mapper[df_sensor['HUID'][df_sensor['name'] == key].values[0]]
        else:
            sensor_found = False
            for _, sensor in df_sensor.iterrows():
                if type(sensor['aliases']) == str:
                    if key in [alias.strip() for alias in sensor['aliases'].split(',')]:
                        value = ts_data[key][0].tolist()
                        sensor_id = sensor_huid_mapper[sensor['HUID']]
                        sensor_found = True
                        break
            if not sensor_found:
                print(f'No sensor found for data labelled {key}, skipping this record')
                continue

        ts = client_ts_object.create(sensor_id=sensor_id,
                                     test_id=test_id,
                                     default_start_time=default_start_time,
                                     default_end_time=default_end_time,
                                     fs=fs,
                                     read_only=read_only)

        body = {'data': {'time': time,
                         'value': value}}
        tic = timer.perf_counter()
        # client_ts_object.post_data_points(ts.id, form_body=body)
        toc = timer.perf_counter()
        print(
            f"Posting timeseries for sensor {key} in test {ts_data['test_num'][0][0]} took {toc - tic:0.4f}s")


def apply_sensor_tag(client: Client, sensor_id: str,
                     sensor_tag_input: str, df_tag: pd.DataFrame, read_only: bool):
    if type(sensor_tag_input) is not str and np.isnan(sensor_tag_input):
        pass
    else:
        for tag in [tg.strip() for tg in sensor_tag_input.split(',')]:
            tag_input = df_tag[df_tag['HUID'] == tag].squeeze()
            if tag_input.size != 0:
                client.tag.create(name=tag_input['name'],
                                  comment=tag_input['comment'],
                                  sensor_id=sensor_id,
                                  read_only=read_only)

            else:
                print(f'No tag HUID {tag} found. Skipping tag creation')


def add_ts_tags(client: Client, df_timeseries_tag: pd.DataFrame, df_tag: pd.DataFrame,
                test_mapper: dict, sensor_mapper: dict,
                read_only: bool):
    for _, ts_tag_input in df_timeseries_tag.iterrows():

        tag_input = df_tag[df_tag['HUID'] == ts_tag_input['tag HUID']].squeeze()
        if tag_input.size == 0:
            print(f"Tag HUID {ts_tag_input['tag HUID']} not found in tag list. Skipping record")
            continue

        try:
            sensor_id = sensor_mapper[ts_tag_input['sensor HUID']]
        except KeyError:
            print(f"Sensor id for HUID {ts_tag_input['sensor HUID']} not found in tag list. Skipping record")
            continue

        try:
            test_id = test_mapper[ts_tag_input['test HUID']]
        except KeyError:
            print(f"Test id for HUID {ts_tag_input['test HUID']} not found in test list. Skipping record")
            continue

        try:
            ts_id = client.timeseries.get_all(filter_by=[client.filter.timeseries.sensor_id == sensor_id,
                                                         client.filter.timeseries.test_id == test_id])[0].id
        except IndexError:
            print(f"Timeseries for sensor HUID {ts_tag_input['sensor HUID']} and test HUID {ts_tag_input['test HUID']} "
                  f"not found in test list. Skipping record")
            continue

        client.tag.create(name=tag_input['name'],
                          comment=tag_input['comment'],
                          timeseries_id=ts_id,
                          read_only=read_only)


def add_derived_sensor_timeseries(client: Client, df_derived_sensor: pd.DataFrame, sensor_huid_mapper: dict,
                                  test_mapper: dict):
    for _, derived_sensor in df_derived_sensor.iterrows():
        sensor_id = sensor_huid_mapper[derived_sensor['HUID']]

        derived_on = [contributor.strip() for contributor in derived_sensor['derived_on'].split(',')]
        derived_input = list()
        for contributor in derived_on:
            cont_split = [part.strip() for part in contributor.split(':')]
            if cont_split == contributor:
                derived_input.append({'sensor': '', 'factor': float(cont_split[0])})
            else:
                try:
                    derived_from_sensor_id = sensor_huid_mapper[cont_split[0]]
                except KeyError:
                    print(f'Derived sensor dependency HUID {cont_split[0]} not found')
                    continue

                derived_input.append({'sensor': derived_from_sensor_id, 'factor': float(cont_split[1])})

        if len(derived_on) == 0:
            continue

        for test_huid, test_id in test_mapper.items():
            ts_data = list()
            time = None
            default_start_time = None
            default_end_time = None
            fs = None
            data_extraction_failed = False
            for contributor in derived_input:
                if contributor['sensor'] == '':
                    ts_data.append({'time': [], 'value': contributor['factor']})
                else:
                    try:
                        ts_derived_from = client.timeseries.get_all(
                            filter_by=[client.filter.timeseries.test_id == test_id,
                                       client.filter.timeseries.sensor_id == contributor['sensor']])[0]

                        if default_start_time is not None:
                            assert default_start_time == ts_derived_from.default_start_time
                        else:
                            default_start_time = ts_derived_from.default_start_time

                        if default_end_time is not None:
                            assert default_end_time == ts_derived_from.default_end_time
                        else:
                            default_end_time = ts_derived_from.default_end_time

                        if fs is not None:
                            assert fs == ts_derived_from.fs
                        else:
                            fs = ts_derived_from.fs

                        ts_data_addition = client.timeseries.get_data_points(ts_id=ts_derived_from.id)

                        if time is not None:
                            assert time == ts_data_addition['time']
                        else:
                            time = ts_data_addition['time']

                        ts_data.append(ts_data_addition)

                    except:
                        print(f"Data not available to derive HUID {derived_sensor['HUID']} for test HUID {test_huid}")
                        data_extraction_failed = True
                        break

            if not data_extraction_failed and time is not None and len(time) is not 0:
                value = 0
                for contributor, ts_data_addition in zip(derived_input, ts_data):
                    value = value + np.array(ts_data_addition['value']) * contributor['factor']

                ts = client.timeseries.create(sensor_id=sensor_id,
                                              test_id=test_id,
                                              default_start_time=default_start_time,
                                              default_end_time=default_end_time,
                                              fs=fs,
                                              read_only=True)

                body = {'data': {'time': time,
                                 'value': list(value)}}
                tic = timer.perf_counter()
                # client.timeseries.post_data_points(ts.id, form_body=body)
                toc = timer.perf_counter()
                print(
                    f"Posting derived timeseries for sensor {derived_sensor['HUID']} "
                    f"in test {test_huid} took {toc - tic:0.4f}s")


def add_test_tags(client: Client, df_tag: pd.DataFrame,
                  df_tests: List[pd.DataFrame], test_mapper: dict, read_only: bool):
    for df_test in df_tests:
        for _, test_data in df_test.iterrows():
            test_huid = test_data['HUID']
            test_tag_huids = test_data['tags']

            if type(test_tag_huids) is not str and np.isnan(test_tag_huids):
                pass
            else:
                for tag in [tg.strip() for tg in test_tag_huids.split(',')]:
                    tag_input = df_tag[df_tag['HUID'] == tag].squeeze()
                    if tag_input.size == 0:
                        print(f"Tag HUID {tag} not found in tag list. Skipping record")
                        continue

                    try:
                        test_id = test_mapper[test_huid]
                    except KeyError:
                        print(
                            f"Test id for HUID {test_huid} not found in tag list. Skipping record")
                        continue

                    client.tag.create(name=tag_input['name'],
                                      comment=tag_input['comment'],
                                      test_id=test_id,
                                      read_only=read_only)


def import_based_on_xls(client: Client, xls_loc: str, data_folder: str,
                        default_start_time: float, default_end_time: float, dateformat: str = '%Y-%m-%d %H:%M'):
    df_campaign = pd.read_excel(xls_loc, sheet_name='Campaign', skiprows=2)
    df_sensor = pd.read_excel(xls_loc, sheet_name='Sensor', skiprows=2, converters={'HUID': str},
                              true_values="TRUE", false_values="FALSE")
    df_derived_sensor = pd.read_excel(xls_loc, sheet_name='DerivedSensor', skiprows=2,
                                      converters={'HUID': str},
                                      true_values="TRUE", false_values="FALSE")
    df_floater_config = pd.read_excel(xls_loc, sheet_name='FloaterConfig', skiprows=2,
                                      converters={'HUID': str})
    df_wave_calibration = pd.read_excel(xls_loc, sheet_name='WaveCal', skiprows=2,
                                        converters={'derive from floater test': bool, 'HUID': str},
                                        true_values="TRUE", false_values="FALSE")
    df_wind_calibration = pd.read_excel(xls_loc, sheet_name='WindCal', skiprows=2,
                                        converters={'HUID': str})
    df_floater_test = pd.read_excel(xls_loc, sheet_name='FloaterTest', skiprows=2,
                                    converters={'HUID': str, 'wave HUID': str,
                                                'wind HUID': str, 'floater config HUID': str})
    df_tag = pd.read_excel(xls_loc, sheet_name='Tag', skiprows=2, converters={'HUID': str})
    df_timeseries_tag = pd.read_excel(xls_loc, sheet_name='Tag TS', skiprows=2,
                                      converters={'test HUID': str, 'sensor HUID': str, 'tag HUID': str})

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

    sensor_huid_mapper = dict()

    for _, sensor in df_sensor.iterrows():
        sensor_input = {key: sensor[key] for key in ['name', 'description', 'unit', 'kind', 'source', 'x', 'y', 'z',
                                                     'position_reference', 'position_heading_lock',
                                                     'position_draft_lock',
                                                     'positive_direction_definition', 'area']}

        created_sensor = client.sensor.create(**sensor_input,
                                              campaign_id=campaign.id,
                                              read_only=restrict_access)

        sensor_huid_mapper[sensor['HUID']] = sensor_id = created_sensor.id
        apply_sensor_tag(client=client, sensor_id=sensor_id,
                         sensor_tag_input=sensor['tags'], df_tag=df_tag, read_only=restrict_access)

    for _, sensor in df_derived_sensor.iterrows():
        sensor_input = {key: sensor[key] for key in ['name', 'description', 'unit', 'kind', 'source', 'x', 'y', 'z',
                                                     'position_reference', 'position_heading_lock',
                                                     'position_draft_lock',
                                                     'positive_direction_definition', 'area']}

        created_sensor = client.sensor.create(**sensor_input,
                                              campaign_id=campaign.id,
                                              read_only=restrict_access)

        sensor_huid_mapper[sensor['HUID']] = sensor_id = created_sensor.id
        apply_sensor_tag(client=client, sensor_id=sensor_id,
                         sensor_tag_input=sensor['tags'], df_tag=df_tag, read_only=restrict_access)

    floater_configs_huid_mapper = dict()

    for index, floater in df_floater_config.iterrows():
        floater_input = {key: floater[key] for key in ['name', 'description', 'characteristic_length', 'draft']}

        created_floater_config = client.floater_config.create(**floater_input,
                                                              campaign_id=campaign.id,
                                                              read_only=restrict_access)

        floater_configs_huid_mapper[floater['HUID']] = created_floater_config.id

    wave_cal_keys = ['number', 'description', 'test_date', 'wave_spectrum', 'wave_height', 'wave_period', 'gamma',
                     'wave_direction', 'current_velocity', 'current_direction']

    wave_calibration_huid_mapper, cals_from_floater_test = sintef_matlab_import(
        client_test_object=client.wave_calibration,
        client_ts_object=client.timeseries, campaign_id=campaign.id,
        read_only=restrict_access, default_start_time=default_start_time,
        default_end_time=default_end_time, data_folder=data_folder,
        df_test=df_wave_calibration, df_sensor=df_sensor,
        required_keys=wave_cal_keys, default_date=campaign.date,
        sensor_huid_mapper=sensor_huid_mapper,
        dateformat=dateformat)

    wind_cal_keys = ['number', 'description', 'test_date', 'wind_spectrum', 'wind_velocity', 'zref', 'wind_direction']

    wind_calibration_huid_mapper, _ = sintef_matlab_import(client_test_object=client.wind_calibration,
                                                           client_ts_object=client.timeseries, campaign_id=campaign.id,
                                                           read_only=restrict_access,
                                                           default_start_time=default_start_time,
                                                           default_end_time=default_end_time, data_folder=data_folder,
                                                           df_test=df_wind_calibration, df_sensor=df_sensor,
                                                           required_keys=wind_cal_keys, default_date=campaign.date,
                                                           sensor_huid_mapper=sensor_huid_mapper,
                                                           dateformat=dateformat)

    floater_test_keys = ['number', 'description', 'test_date', 'category', 'orientation', 'wave_id', 'wind_id',
                         'floaterconfig_id']

    floater_test_huid_mapper, _ = sintef_matlab_import(client_test_object=client.floater_test,
                                                       client_ts_object=client.timeseries, campaign_id=campaign.id,
                                                       read_only=restrict_access, default_start_time=default_start_time,
                                                       default_end_time=default_end_time, data_folder=data_folder,
                                                       df_test=df_floater_test, df_sensor=df_sensor,
                                                       required_keys=floater_test_keys, default_date=campaign.date,
                                                       sensor_huid_mapper=sensor_huid_mapper,
                                                       wave_calibration_huid_mapper=wave_calibration_huid_mapper,
                                                       wind_calibration_huid_mapper=wind_calibration_huid_mapper,
                                                       floater_configs_huid_mapper=floater_configs_huid_mapper,
                                                       dateformat=dateformat,
                                                       cals_from_floater_test=cals_from_floater_test)

    add_derived_sensor_timeseries(client=client, df_derived_sensor=df_derived_sensor,
                                  sensor_huid_mapper=sensor_huid_mapper,
                                  test_mapper={**wave_calibration_huid_mapper, **wind_calibration_huid_mapper,
                                               **floater_test_huid_mapper})

    add_test_tags(client=client, df_tag=df_tag,
                  df_tests=[df_wave_calibration, df_wind_calibration, df_floater_test],
                  test_mapper={**wave_calibration_huid_mapper, **wind_calibration_huid_mapper,
                               **floater_test_huid_mapper},
                  read_only=restrict_access)

    add_ts_tags(client=client, df_timeseries_tag=df_timeseries_tag, df_tag=df_tag,
                test_mapper={**wave_calibration_huid_mapper, **wind_calibration_huid_mapper,
                             **floater_test_huid_mapper},
                sensor_mapper=sensor_huid_mapper, read_only=restrict_access)
