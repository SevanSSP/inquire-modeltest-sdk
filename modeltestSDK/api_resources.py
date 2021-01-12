from .utils import format_class_name
import warnings
from .resources import (Campaign, CampaignList, Test, TestList, Sensor, SensorList, Timeseries, TimeseriesList,
                        DataPoint, DataPointList, FloaterTest, FloaterTestList, WaveCalibration,
                        WaveCalibrationList,
                        WindConditionCalibration, WindConditionCalibrationList, Tag, TagList)
import gzip
import zlib
import datetime

def get_id_from_response(response):
    return response[0]["id"]


'''Abstraction layer between client and resources'''

class BaseAPI:

    def __init__(self, client):
        self._resource_path = format_class_name(self.__class__.__name__)
        self.client = client

    def delete(self, item_id: str, parameters: dict=None):
        resp = self.client.delete(self._resource_path, endpoint=item_id, parameters=parameters)
        return resp


class NamedBaseAPI(BaseAPI):
    '''
    Only for database items with names. To retrieve id from name
    '''

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

    def get(self, id: str) -> Campaign:
        data = self.client.get(self._resource_path, id)
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

    def get_all(self) -> CampaignList:
        data = self.client.get(self._resource_path, "")
        obj_list = [Campaign.from_dict(data=obj, client=self.client) for obj in data]
        return CampaignList(resources=obj_list, client=None)

    def patch(self, body: dict, id: str) -> Campaign:
        data = self.client.patch(self._resource_path, endpoint=f"{id}", body=body)
        return Campaign.from_dict(data=data, client=self.client)

    def get_sensors(self, id: str) -> SensorList:
        data = self.client.get(self._resource_path, f"{id}/sensors")
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def get_tests(self, id: str, type: str = None) -> TestList:
        data = self.client.get(self._resource_path, f"{id}/tests", parameters={"type": type})
        resources = [Test.from_dict(data=obj, client=self.client) for obj in data]
        return TestList(resources=resources, client=self.client)


class TestAPI(NamedBaseAPI):

    def get(self, id: str) -> Test:
        data = self.client.get(self._resource_path, id)
        return Test.from_dict(data=data, client=self.client)

    def get_timeseries(self, id: str) -> TimeseriesList:
        data = self.client.get(self._resource_path, f"{id}/timeseries")
        resources = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=resources, client=self.client)


class FloaterTestAPI(TestAPI):

    def create(self, description: str, test_date: str, campaign_id: str, category: str, orientation: float,
               draft: float, wave_id: str = None, wind_id: str = None, read_only: bool = False) -> FloaterTest:
        body = dict(description=description, type="floatertest", test_date=test_date, campaign_id=campaign_id,
                    category=category, orientation=orientation, draft=draft, wave_id=wave_id,
                    wind_id=wind_id, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return FloaterTest.from_dict(data=data, client=self.client)

    def get(self, id: str) -> FloaterTest:
        data = self.client.get(self._resource_path, id)
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

    def get_all(self) -> FloaterTestList:
        data = self.client.get(self._resource_path, "")
        obj_list = [FloaterTest.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterTestList(resources=obj_list, client=None)


class WaveCalibrationAPI(TestAPI):

    def create(self, description: str, test_date: str, campaign_id: str,
               wave_spectrum: str, wave_height: float, wave_period: float, gamma: float,
               wave_direction: float, current_velocity: float, current_direction: float,
               id: str = None, read_only: bool = False) -> WaveCalibration:
        body = dict(description=description, type="Wave Calibration", test_date=test_date,
                    campaign_id=campaign_id,
                    wave_spectrum=wave_spectrum, wave_period=wave_period, wave_height=wave_height,
                    gamma=gamma, wave_direction=wave_direction, current_velocity=current_velocity,
                    current_direction=current_direction, id=id, read_only=read_only)

        data = self.client.post(self._resource_path, body=body)
        return WaveCalibration.from_dict(data=data, client=self.client)

    def get(self, id: str) -> WaveCalibration:
        data = self.client.get(self._resource_path, id)
        return WaveCalibration.from_dict(data=data, client=self.client)

    def get_all(self) -> WaveCalibrationList:
        data = self.client.get(self._resource_path, "")
        obj_list = [WaveCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WaveCalibrationList(resources=obj_list, client=None)


class WindConditionCalibrationAPI(TestAPI):

    def create(self, description: str, test_date: str, campaign_id: str,
               wind_spectrum: str, wind_velocity: float, zref: float, wind_direction: float,
               id: str = None, read_only: bool = False) -> WindConditionCalibration:
        body = dict(description=description, test_date=test_date, type="windConditionCalibration",
                    campaign_id=campaign_id,
                    wind_spectrum=wind_spectrum,
                    wind_velocity=wind_velocity, zref=zref, wind_direction=wind_direction, id=id, read_only=read_only)

        data = self.client.post(self._resource_path, body=body)
        return WindConditionCalibration.from_dict(data=data, client=self.client)

    def get(self, id: str) -> WindConditionCalibration:
        data = self.client.get(self._resource_path, id)
        return WindConditionCalibration.from_dict(data=data, client=self.client)

    def get_all(self) -> WindConditionCalibrationList:
        data = self.client.get(self._resource_path, "")
        obj_list = [WindConditionCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WindConditionCalibrationList(resources=obj_list, client=None)


class SensorAPI(NamedBaseAPI):

    def create(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
               is_local: bool, fs: float, intermittent: bool, campaign_id: str,  area: float = None,
               read_only: bool = False) -> Sensor:
        body = dict(name=name, description=description, unit=unit, kind=kind, area=area, x=x,
                    y=y, z=z, is_local=is_local, fs=fs, intermittent=intermittent,
                    campaign_id=campaign_id, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Sensor.from_dict(data=data, client=self.client)

    def get(self, id: str) -> Sensor:
        data = self.client.get(self._resource_path, id)
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

    def get_all(self) -> SensorList:
        data = self.client.get(self._resource_path, "")
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def patch(self, body: dict, sensor_id: str) -> Sensor:
        data = self.client.patch(self._resource_path, endpoint=f"{sensor_id}", body=body)
        return Sensor.from_dict(data=data, client=self.client)


class TimeseriesAPI(BaseAPI):

    def create(self, sensor_id: str, test_id: str, default_start_time: float, default_end_time: float,
               read_only: bool = False) -> Timeseries:
        body = dict(sensor_id=sensor_id, test_id=test_id, default_start_time=default_start_time,
                    default_end_time=default_end_time, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Timeseries.from_dict(data=data, client=self.client)

    def get(self, id: str) -> Timeseries:
        data = self.client.get(self._resource_path, id)
        return Timeseries.from_dict(data=data, client=self.client)

    def get_all(self) -> TimeseriesList:
        data = self.client.get(self._resource_path, "")
        obj_list = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=obj_list, client=None)

    def patch(self, body: dict, id: str):
        return self.client.patch(resource=self._resource_path, endpoint=f"{id}", body=body)

    def get_data_points(self, id: str) -> DataPointList:
        data = self.client.get(resource=self._resource_path, endpoint=f"{id}/data")
        if not data:
            return DataPointList(resources=[], client=self.client)

        resources = [DataPoint(time=float(time), value=float(value)) for time, value in [row.replace("\n", "").split("\t") for row in data]]
        resources = sorted(resources, key=lambda x: x.time)
        return DataPointList(resources=resources, client=self.client)

    def post_data_points(self, id, body):
        form_body = {'timeseries_id': id, 'data': {'time': [], 'value': []}}
        for p in body:
            form_body['data']['time'].append(p['time'])
            form_body['data']['value'].append(p['value'])
        self.client.post(resource=self._resource_path, endpoint=f"{id}/data", body=form_body)

    def get_standard_deviation(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/statistics/?stats=std")
        return data

    def get_max_value(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/statistics/?stats=max")
        return data

    def get_min_value(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/statistics/?stats=min")
        return data

    def get_mean(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/statistics/?stats=mean")
        return data

    #TODO: Finnish calls for stats
    def get_stat_moment(self, id: str):
        data = None
        return data
    """
    def get_measured_hs(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/measured_hs")
        return data

    def get_measured_tp(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/measured_tp")
        return data
    """
    def get_sensor(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/sensor")
        return Sensor.from_dict(data=data, client=self.client)

    def get_test(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/test")
        return Test.from_dict(data=data, client=self.client)


class TagAPI(NamedBaseAPI):
    def create(self, name: str, comment: str, test_id: str, sensor_id: str, timeseries_id: str,
               read_only: bool = False) -> Tag:
        body = dict(name=name, comment=comment, test_id=test_id, sensor_id=sensor_id,timeseries_id=timeseries_id)
        data = self.client.post(self._resource_path, body=body, read_only=read_only)
        return Tag.from_dict(data=data, client=self.client)

    def get(self, id: str) -> Tag:
        data = self.client.get(self._resource_path, id)
        return Tag.from_dict(data=data,client=self.client)

    def get_all(self) -> TagList:
        data = self.client.get(self._resource_path, "")
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
