"""
APIs

Abstraction layer between client and resources.
"""
from .utils import format_class_name
import warnings
from .resources import (Campaign, CampaignList, Test, TestList, Sensor, SensorList, Timeseries, TimeseriesList,
                        FloaterTest, FloaterTestList, WaveCalibration, WaveCalibrationList, WindCalibration,
                        WindCalibrationList, Tag, TagList, FloaterConfig, FloaterConfigList)
from .query import create_query_parameters


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
        response = self.client.get(format_class_name(self.__class__.__name__), parameters={'name': name})
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
        data = self.client.post(resource=self._resource_path, body=body)
        return Campaign.from_dict(data=data, client=self.client)

    def get(self, campaign_id: str) -> Campaign:
        data = self.client.get(self._resource_path, campaign_id)
        return Campaign.from_dict(data=data, client=self.client)

    def get_by_name(self, name: str) -> Campaign:
        response = self.get_all(filter_by=[self.client.filter.campaign.name == name])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {name}")

    def get_all(self, filter_by: list = None, sort_by: list = None) -> CampaignList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [Campaign.from_dict(data=obj, client=self.client) for obj in data]
        return CampaignList(resources=obj_list, client=None)

    def patch(self, body: dict, campaign_id: str) -> Campaign:
        data = self.client.patch(self._resource_path, endpoint=f"{campaign_id}", body=body)
        return Campaign.from_dict(data=data, client=self.client)


class TestAPI(NamedBaseAPI):

    def get(self, test_id: str) -> Test:
        data = self.client.get(self._resource_path, test_id)
        return Test.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list = None, sort_by: list = None) -> TestList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [Test.from_dict(data=obj, client=self.client) for obj in data]
        return TestList(resources=obj_list, client=None)


class FloaterTestAPI(TestAPI):

    def create(self, number: str, description: str, test_date: str, campaign_id: str, category: str, orientation: float,
               floaterconfig_id: str = None, wave_id: str = None, wind_id: str = None,
               read_only: bool = False) -> FloaterTest:
        body = dict(number=number, description=description, type="Floater Test", test_date=test_date,
                    campaign_id=campaign_id, category=category, orientation=orientation, wave_id=wave_id,
                    wind_id=wind_id, floaterconfig_id=floaterconfig_id, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return FloaterTest.from_dict(data=data, client=self.client)

    def get(self, floater_id: str) -> FloaterTest:
        data = self.client.get(self._resource_path, floater_id)
        return FloaterTest.from_dict(data=data, client=self.client)

    def get_by_test_number(self, test_number: str) -> FloaterTest:
        response = self.get_all(filter_by=[self.client.filter.floater_test.number == test_number])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for test number {test_number} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {test_number}")

    def get_all(self, filter_by: list = None, sort_by: list = None) -> FloaterTestList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [FloaterTest.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterTestList(resources=obj_list, client=None)


class WaveCalibrationAPI(TestAPI):

    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wave_spectrum: str, wave_height: float, wave_period: float, gamma: float,
               wave_direction: float, current_velocity: float, current_direction: float,
               id: str = None, read_only: bool = False) -> WaveCalibration:
        body = dict(number=number, description=description, type="Wave Calibration", test_date=test_date,
                    campaign_id=campaign_id,
                    wave_spectrum=wave_spectrum, wave_period=wave_period, wave_height=wave_height,
                    gamma=gamma, wave_direction=wave_direction, current_velocity=current_velocity,
                    current_direction=current_direction, id=id, read_only=read_only)

        data = self.client.post(self._resource_path, body=body)
        return WaveCalibration.from_dict(data=data, client=self.client)

    def get(self, wave_calibration_id: str) -> WaveCalibration:
        data = self.client.get(self._resource_path, wave_calibration_id)
        return WaveCalibration.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list = None, sort_by: list = None) -> WaveCalibrationList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [WaveCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WaveCalibrationList(resources=obj_list, client=None)

    def get_by_test_number(self, test_number: str) -> WaveCalibration:
        response = self.get_all(filter_by=[self.client.filter.wave_calibration.number == test_number])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for test number {test_number} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {test_number}")


class WindCalibrationAPI(TestAPI):

    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wind_spectrum: str, wind_velocity: float, zref: float, wind_direction: float,
               id: str = None, read_only: bool = False) -> WindCalibration:
        body = dict(number=number, description=description, test_date=test_date, type="Wind Calibration",
                    campaign_id=campaign_id, wind_spectrum=wind_spectrum, wind_velocity=wind_velocity, zref=zref,
                    wind_direction=wind_direction, id=id, read_only=read_only)

        data = self.client.post(self._resource_path, body=body)
        return WindCalibration.from_dict(data=data, client=self.client)

    def get(self, wind_condition_id: str) -> WindCalibration:
        data = self.client.get(self._resource_path, wind_condition_id)
        return WindCalibration.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list = None, sort_by: list = None) -> WindCalibrationList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [WindCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WindCalibrationList(resources=obj_list, client=None)

    def get_by_test_number(self, test_number: str) -> WindCalibration:
        response = self.get_all(filter_by=[self.client.filter.wind_calibration.number == test_number])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for test number {test_number} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {test_number}")


class SensorAPI(NamedBaseAPI):

    def create(self, name: str, description: str, unit: str, kind: str, source: str, x: float, y: float, z: float,
               position_reference: str, position_heading_lock: bool, position_draft_lock: bool,
               positive_direction_definition: str, campaign_id: str, area: float = None,
               read_only: bool = False) -> Sensor:
        body = dict(name=name, description=description, unit=unit, kind=kind, source=source, area=area, x=x,
                    y=y, z=z, position_reference=position_reference, position_heading_lock=position_heading_lock,
                    position_draft_lock=position_draft_lock,
                    positive_direction_definition=positive_direction_definition,
                    campaign_id=campaign_id, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Sensor.from_dict(data=data, client=self.client)

    def get(self, sensor_id: str) -> Sensor:
        data = self.client.get(self._resource_path, sensor_id)
        return Sensor.from_dict(data=data, client=self.client)

    def get_multiple_by_name(self, ids) -> Sensor:
        return self.client.post(self._resource_path, "ids", body=ids)

    def get_by_name(self, name: str):
        response = self.get_all(filter_by=[self.client.filter.sensor.name == name])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {name}")

    def get_all(self, filter_by: list = None, sort_by: list = None) -> SensorList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
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

    def get_all(self, filter_by: list = None, sort_by: list = None) -> TimeseriesList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=obj_list, client=None)

    def patch(self, body: dict, ts_id: str):
        return self.client.patch(resource=self._resource_path, endpoint=f"{ts_id}", body=body)

    def get_data_points(self, ts_id: str) -> dict:
        data = self.client.get(resource=self._resource_path, endpoint=f"{ts_id}/data?all_data=true")
        return data['data']

    def post_data_points(self, ts_id, body=None, form_body=None):
        if form_body is None:
            form_body = {'data': {'time': [], 'value': []}}
            for p in body:
                form_body['data']['time'].append(p['time'])
                form_body['data']['value'].append(p['value'])
        self.client.post(resource=self._resource_path, endpoint=f"{ts_id}/data", body=form_body)

    def get_standard_deviation(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics")
        return data['std']

    def get_max_value(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics")
        return data['max']

    def get_min_value(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics")
        return data['min']

    def get_mean(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics")
        return data['mean']


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

    def get_all(self, filter_by: list = None, sort_by: list = None) -> TagList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [Tag.from_dict(data=obj, client=self.client) for obj in data]
        return TagList(resources=obj_list, client=None)

    def get_by_name(self, name: str) -> Tag:
        response = self.get_all(filter_by=[self.client.filter.campaign.name == name])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
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

    def get_all(self, filter_by: list = None, sort_by: list = None) -> FloaterConfigList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        obj_list = [FloaterConfig.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterConfigList(resources=obj_list, client=None)

    def get_by_name(self, name: str) -> FloaterConfig:
        response = self.get_all(filter_by=[self.client.filter.campaign.name == name])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {name}")
