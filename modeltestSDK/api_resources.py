from .utils import format_class_name
import warnings
from .resources import (Campaign, CampaignList, Test, TestList, Sensor, SensorList, Timeseries, TimeseriesList,
                        FloaterTest, FloaterTestList, WaveCalibration, WaveCalibrationList, WindConditionCalibration,
                        WindConditionCalibrationList, Tag, TagList, FloaterConfig, FloaterConfigList)
from .utils import query_dict_to_url


def get_id_from_response(response):
    return response[0]["id"]


'''Abstraction layer between client and resources'''


class BaseAPI:

    def __init__(self, client):
        self._resource_path = format_class_name(self.__class__.__name__)
        self.client = client

    def delete(self, item_id: str, parameters: dict = None):
        resp = self.client.delete(self._resource_path, endpoint=item_id, parameters=parameters)
        return resp


class NamedBaseAPI(BaseAPI):
    """
    Only for database items with names. To retrieve id from name
    """

    def get_id(self, name: str) -> str:
        response = self.client.get(format_class_name(self.__class__.__name__), "", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return response[0]['id']
        else:
            raise Exception(f"Could not find any object with name {name}")


class CampaignAPI(NamedBaseAPI):

    def create(self, name: str, description: str, location: str, date: any,
               scale_factor: float, water_depth: float, read_only: bool = False) -> Campaign:
        body = dict(name=name, description=description, location=location, date=date,
                    scale_factor=scale_factor, water_depth=water_depth, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Campaign.from_dict(data=data, client=self.client)

    def get(self, campaign_id: str) -> Campaign:
        data = self.client.get(self._resource_path, campaign_id)
        return Campaign.from_dict(data=data, client=self.client)

    def get_by_name(self, name: str) -> Campaign:
        response = self.client.get(format_class_name(self.__class__.__name__), "", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return Campaign.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {name}")

    def get_all(self, filter_by: list, sort_by: list) -> CampaignList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [Campaign.from_dict(data=obj, client=self.client) for obj in data]
        return CampaignList(resources=obj_list, client=None)

    def patch(self, body: dict, campaign_id: str) -> Campaign:
        data = self.client.patch(self._resource_path, endpoint=f"{campaign_id}", body=body)
        return Campaign.from_dict(data=data, client=self.client)


'''
    def get_sensors(self, id: str) -> SensorList:
        data = self.client.get(self._resource_path, f"{id}/sensors")
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def get_tests(self, id: str, type: str = None) -> TestList:
        data = self.client.get(self._resource_path, f"{id}/tests", parameters={"type": type})
        resources = [Test.from_dict(data=obj, client=self.client) for obj in data]
        return TestList(resources=resources, client=self.client)
'''


class TestAPI(NamedBaseAPI):

    def get(self, test_id: str) -> Test:
        data = self.client.get(self._resource_path, test_id)
        return Test.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list, sort_by: list) -> TestList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [Test.from_dict(data=obj, client=self.client) for obj in data]
        return TestList(resources=obj_list, client=None)


class FloaterTestAPI(TestAPI):

    def create(self, number: str, description: str, test_date: str, campaign_id: str, category: str, orientation: float,
               floater_config_id: str = None, wave_id: str = None, wind_id: str = None,
               read_only: bool = False) -> FloaterTest:
        body = dict(number=number, description=description, type="Floater Test", test_date=test_date,
                    campaign_id=campaign_id, category=category, orientation=orientation, wave_id=wave_id,
                    wind_id=wind_id, floaterconfig_id=floater_config_id, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return FloaterTest.from_dict(data=data, client=self.client)

    def get(self, floater_id: str) -> FloaterTest:
        data = self.client.get(self._resource_path, floater_id)
        return FloaterTest.from_dict(data=data, client=self.client)

    def get_by_name(self, description: str) -> FloaterTest:
        response = self.client.get(format_class_name(self.__class__.__name__), "",
                                   parameters={'description': description})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {description} returned several objects,"
                              f" first was returned")
            return FloaterTest.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {description}")

    def get_all(self, filter_by: list, sort_by: list) -> FloaterTestList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [FloaterTest.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterTestList(resources=obj_list, client=None)


class WaveCalibrationAPI(TestAPI):

    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wave_spectrum: str, wave_height: float, wave_period: float, gamma: float,
               wave_direction: float, current_velocity: float, current_direction: float,
               wave_calibration_id: str = None, read_only: bool = False) -> WaveCalibration:
        body = dict(number=number, description=description, type="Wave Calibration", test_date=test_date,
                    campaign_id=campaign_id,
                    wave_spectrum=wave_spectrum, wave_period=wave_period, wave_height=wave_height,
                    gamma=gamma, wave_direction=wave_direction, current_velocity=current_velocity,
                    current_direction=current_direction, id=wave_calibration_id, read_only=read_only)

        data = self.client.post(self._resource_path, body=body)
        return WaveCalibration.from_dict(data=data, client=self.client)

    def get(self, wave_calibration_id: str) -> WaveCalibration:
        data = self.client.get(self._resource_path, wave_calibration_id)
        return WaveCalibration.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list, sort_by: list) -> WaveCalibrationList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [WaveCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WaveCalibrationList(resources=obj_list, client=None)


class WindConditionCalibrationAPI(TestAPI):

    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wind_spectrum: str, wind_velocity: float, zref: float, wind_direction: float,
               wind_condition_id: str = None, read_only: bool = False) -> WindConditionCalibration:
        body = dict(number=number, description=description, test_date=test_date, type="windConditionCalibration",
                    campaign_id=campaign_id, wind_spectrum=wind_spectrum, wind_velocity=wind_velocity, zref=zref,
                    wind_direction=wind_direction, id=wind_condition_id, read_only=read_only)

        data = self.client.post(self._resource_path, body=body)
        return WindConditionCalibration.from_dict(data=data, client=self.client)

    def get(self, wind_condition_id: str) -> WindConditionCalibration:
        data = self.client.get(self._resource_path, wind_condition_id)
        return WindConditionCalibration.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list, sort_by: list) -> WindConditionCalibrationList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [WindConditionCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WindConditionCalibrationList(resources=obj_list, client=None)


class SensorAPI(NamedBaseAPI):

    def create(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
               is_local: bool, campaign_id: str, area: float = None,
               read_only: bool = False) -> Sensor:
        body = dict(name=name, description=description, unit=unit, kind=kind, area=area, x=x,
                    y=y, z=z, is_local=is_local, campaign_id=campaign_id, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Sensor.from_dict(data=data, client=self.client)

    def get(self, sensor_id: str) -> Sensor:
        data = self.client.get(self._resource_path, sensor_id)
        return Sensor.from_dict(data=data, client=self.client)

    def get_multiple_by_name(self, ids) -> Sensor:
        return self.client.post(self._resource_path, "ids", body=ids)

    def get_by_name(self, name: str):
        response = self.client.get(format_class_name(self.__class__.__name__), "", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return Sensor.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {name}")

    def get_all(self, filter_by: list, sort_by: list) -> SensorList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def patch(self, body: dict, sensor_id: str) -> Sensor:
        data = self.client.patch(self._resource_path, endpoint=f"{sensor_id}", body=body)
        return Sensor.from_dict(data=data, client=self.client)


class TimeseriesAPI(BaseAPI):

    def create(self, sensor_id: str, test_id: str, default_start_time: float, default_end_time: float, fs: float,
               intermittent: bool = False, read_only: bool = False) -> Timeseries:
        body = dict(sensor_id=sensor_id, test_id=test_id, default_start_time=default_start_time,
                    default_end_time=default_end_time, fs=fs, intermittent=intermittent, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Timeseries.from_dict(data=data, client=self.client)

    def get(self, ts_id: str) -> Timeseries:
        data = self.client.get(self._resource_path, ts_id)
        return Timeseries.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list, sort_by: list) -> TimeseriesList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=obj_list, client=None)

    def patch(self, body: dict, ts_id: str):
        return self.client.patch(resource=self._resource_path, endpoint=f"{ts_id}", body=body)

    def get_data_points(self, ts_id: str) -> dict:
        data = self.client.get(resource=self._resource_path, endpoint=f"{ts_id}/data", parameters={'all_data': 'true'})
        return data

    def post_data_points(self, ts_id, body=None, form_body=None):
        if form_body is None:
            form_body = {'data': {'time': [], 'value': []}}
            for p in body:
                form_body['data']['time'].append(p['time'])
                form_body['data']['value'].append(p['value'])
        self.client.post(resource=self._resource_path, endpoint=f"{ts_id}/data", body=form_body)

    def get_standard_deviation(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats")
        return data['std']

    def get_max_value(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats")
        return data['max']

    def get_min_value(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats=min")
        return data['min']

    def get_mean(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats")
        return data['mean']

    """
    def get_measured_hs(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/measured_hs")
        return data

    def get_measured_tp(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/measured_tp")
        return data
    """


class TagsAPI(NamedBaseAPI):
    def create(self, name: str, comment: str = None, test_id: str = None, sensor_id: str = None,
               timeseries_id: str = None, read_only: bool = False) -> Tag:
        body = dict(name=name, comment=comment, test_id=test_id, sensor_id=sensor_id, timeseries_id=timeseries_id,
                    read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Tag.from_dict(data=data, client=self.client)

    def get(self, tag_id: str) -> Tag:
        data = self.client.get(self._resource_path, tag_id)
        return Tag.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list, sort_by: list) -> TagList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [Tag.from_dict(data=obj, client=self.client) for obj in data]
        return TagList(resources=obj_list, client=None)

    def get_by_name(self, name: str) -> Tag:
        response = self.client.get(format_class_name(self.__class__.__name__), "", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return Tag.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {name}")


class FloaterConfigAPI(NamedBaseAPI):
    def create(self, name: str, description: str, campaign_id: str, draft: float, characteristic_length: float = 0,
               read_only: bool = False) -> FloaterConfig:
        body = dict(name=name, description=description, campaign_id=campaign_id,
                    characteristic_length=characteristic_length, draft=draft, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return FloaterConfig.from_dict(data=data, client=self.client)

    def get(self, floater_id: str) -> FloaterConfig:
        data = self.client.get(self._resource_path, floater_id)
        return FloaterConfig.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list, sort_by: list) -> FloaterConfigList:
        if not filter_by == [] or not sort_by == []:
            enc_parameters = query_dict_to_url(query_filters=filter_by, query_sort_parameters=sort_by)
        else:
            enc_parameters = None
        data = self.client.get(self._resource_path, "", enc_parameters=enc_parameters)
        obj_list = [FloaterConfig.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterConfigList(resources=obj_list, client=None)

    def get_by_name(self, name: str) -> FloaterConfig:
        enc_parameters = query_dict_to_url(query_filters=[self.client.query.floater_config.name == name])
        response = self.client.get(format_class_name(self.__class__.__name__), "", enc_parameters=enc_parameters)
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return FloaterConfig.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {name}")
