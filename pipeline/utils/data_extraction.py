import os
import datetime
from typing import List, Union
import pandas as pd
from scipy.io import loadmat
from numpy import isnan
import time as timer
from modeltestSDK.resources import WaveCalibrationList, WindCalibrationList, FloaterTestList
from modeltestSDK.api import WaveCalibrationAPI, WindCalibrationAPI, FloaterTestAPI, TimeseriesAPI


def sintef_matlab_import(resource: Union[WaveCalibrationList, WindCalibrationList, FloaterTestList],
                         client_test_object: Union[WaveCalibrationAPI, WindCalibrationAPI, FloaterTestAPI],
                         client_ts_object: TimeseriesAPI,
                         campaign_id: str, restrict_access: bool, default_start_time: float, default_end_time: float,
                         data_folder: str, df_test: pd.DataFrame, df_sensor: pd.DataFrame, required_keys: List[str],
                         default_date: datetime.datetime, sensor_huid_mapper: dict,
                         wave_calibration_huid_mapper: dict = None,  wind_calibration_huid_mapper: dict = None,
                         floater_configs_huid_mapper: dict = None, secondary_prefix: str = None):

    huid_mapper = dict()
    for _, test_data in df_test.iterrows():

        if 'wave HUID' in test_data and type(test_data['wave HUID']) is not str \
                and not isnan(test_data['wave HUID']) and wave_calibration_huid_mapper is not None:
            test_data['wave_id'] = wave_calibration_huid_mapper[test_data['wave HUID']]
        else:
            test_data['wave_id'] = None
        if 'wind HUID' in test_data and type(test_data['wind HUID']) is not str \
                and not isnan(test_data['wind HUID']) and wind_calibration_huid_mapper is not None:
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

            test_data_input['description'] = test_data['description'] + ' Note: timeseries not available'
            test_data_input['test_date'] = default_date

            resource.append(
                client_test_object.create(**test_data_input,
                                          campaign_id=campaign_id,
                                          read_only=restrict_access)
            )
            huid_mapper[test_data['HUID']] = test_id = resource[-1].id
            if e is FileNotFoundError:
                print(f"Test {test_data['number']} not found in folder {data_folder}. Creating empty test.")
            elif e is TypeError:
                print(
                    f"Test {test_data['number']} corrupted in folder {data_folder}. Creating empty test.")
            continue

        if test_data["description"] == '*':
            test_data["description"] = ts_data['comment'][0]
        if test_data["test_date"] == '*':
            test_data["test_date"] = datetime.datetime.strptime(str(ts_data['test_date'][0]),
                                                                '%Y-%m-%d %H:%M').isoformat()
        test_data_input = {key: test_data[key] for key in required_keys}

        resource.append(
            client_test_object.create(**test_data_input,
                                      campaign_id=campaign_id,
                                      read_only=restrict_access)
        )
        huid_mapper[test_data['HUID']] = test_id = resource[-1].id

        mat_to_ts(ts_data=ts_data, test_id=test_id, test_number=test_data['number'], df_sensor=df_sensor,
                  sensor_huid_mapper=sensor_huid_mapper,
                  client_ts_object=client_ts_object, default_start_time=default_start_time,
                  default_end_time=default_end_time)

        if secondary_prefix:
            filename = secondary_prefix + str(test_data['number'])
            try:
                secondary_ts_data = loadmat(os.path.join(data_folder, filename))
                mat_to_ts(ts_data=secondary_ts_data, test_id=test_id, test_number=test_data['number'],
                          df_sensor=df_sensor,
                          sensor_huid_mapper=sensor_huid_mapper, client_ts_object=client_ts_object,
                          default_start_time=default_start_time, default_end_time=default_end_time)
            except FileNotFoundError:
                print(f"Secondary file {secondary_prefix}{test_data['number']} not found in folder {data_folder}. "
                      f"No additional timeseries created")

    return huid_mapper


def mat_to_ts(ts_data: dict, test_id: str, test_number: str, df_sensor: pd.DataFrame,
              sensor_huid_mapper: dict, client_ts_object: TimeseriesAPI,
              default_start_time: float, default_end_time: float):
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

        # ts = client_ts_object.create(sensor_id=sensor_id,
        #                              test_id=test_id,
        #                              default_start_time=default_start_time,
        #                              default_end_time=default_end_time,
        #                              fs=fs,
        #                              read_only=True)

        body = {'data': {'time': time,
                         'value': value}}
        tic = timer.perf_counter()
        # client_ts_object.post_data_points(ts.id, form_body=body)
        toc = timer.perf_counter()
        print(
            f"Posting timeseries for sensor {key} in test {test_number} took {toc - tic:0.4f}s")
