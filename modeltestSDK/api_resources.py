import datetime
from typing import List
from .utils import format_class_name
import warnings
from .resources import (Campaign, CampaignList, Test, TestList, Sensor, SensorList, Timeseries, TimeseriesList,
                        DataPoint, DataPointList, Floater, FloaterList)

def get_id_from_response(response):
    return response[0]["id"]


class BaseAPI:


    def __init__(self, client):
        self._resource_path = format_class_name(self.__class__.__name__)
        self.client = client

class NamedBaseAPI(BaseAPI):
    '''
    Only for database items with names. To retrieve id from name
    '''
    def get_id(self, name: str):
        response = self.client.get(format_class_name(self.__class__.__name__), "all", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return response[0]['id']
        else:
            raise Exception(f"Could not find any object with name {name}")

class CampaignAPI(NamedBaseAPI):

    def create(self, name: str, description: str, location: str, date: any, diameter: float,
               scale_factor: float, water_density: float, water_depth: float, transient: float):
        body = dict(name=name, description=description, location=location, date=date, diameter=diameter,
                    scale_factor=scale_factor, water_density=water_density, water_depth=water_depth,
                    transient=transient)
        data = self.client.post(self._resource_path, body=body)
        return Campaign.from_dict(data=data, client=self.client)

    def get(self, id: str):
        data = self.client.get(self._resource_path, id)
        return Campaign.from_dict(data=data, client=self.client)

    def get_all(self):
        data = self.client.get(self._resource_path, "all")
        obj_list = [Campaign.from_dict(data=obj, client=self.client) for obj in data]
        return CampaignList(resources=obj_list, client=None)

    def delete(self, item_id: str):
        self.client.delete(self._resource_path, item_id)

    def patch(self, body: dict, id: str):
        data = self.client.patch(self._resource_path, endpoint=f"{id}", body=body)
        return Campaign.from_dict(data=data, client=self.client)

    def get_sensors(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/sensors")
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def get_tests(self, id: str, type: str = None):
        data = self.client.get(self._resource_path, f"{id}/tests", parameters={"type": type})
        resources = [Test.from_dict(data=obj, client=self.client) for obj in data]
        return TestList(resources=resources, client=self.client)

class TestAPI(NamedBaseAPI):

    def delete(self, item_id: str):
        self.client.delete(self._resource_path, item_id)

    def get_campaign(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/campaign")
        return Campaign.from_dict(data=data, client=self.client)

    def get_timeseries(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/timeseries")
        resources = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=resources, client=self.client)

class FloaterAPI(TestAPI):

    def create(self, description: str, test_date: str, campaign_id: str, type: str, measured_hs: str,
                 measured_tp: str, category: str, orientation: float, draft: float, wave_id: str=None, wind_id: str=None):
        body = dict(description=description, test_date=test_date, campaign_id=campaign_id,
                   type=type, measured_hs=measured_hs, measured_tp=measured_tp,
                   category=category, orientation =orientation, draft =draft, wave_id =wave_id,
                   wind_id =wind_id)
        data = self.client.post(self._resource_path, body=body)
        return Floater.from_dict(data=data, client=self.client)

    def get(self, id: str):
        data = self.client.get(self._resource_path, id)
        return Floater.from_dict(data=data, client=self.client)

    def get_all(self):
        data = self.client.get(self._resource_path, "all")
        obj_list = [Floater.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterList(resources=obj_list, client=None)

class SensorAPI(NamedBaseAPI):

    def create(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
                 is_local: bool, campaign_id: str):
        body = dict(name=name, description=description, unit=unit, kind=kind, x=x,
                    y=y, z=z, is_local=is_local, campaign_id=campaign_id)
        data = self.client.post(self._resource_path, body=body)
        return Sensor.from_dict(data=data, client=self.client)

    def get(self, id: str):
        data = self.client.get(self._resource_path, id)
        return Sensor.from_dict(data=data, client=self.client)

    def get_all(self):
        data = self.client.get(self._resource_path, "all")
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def delete(self, item_id: str):
        self.client.delete(self._resource_path, item_id)

    def patch(self, body: dict, sensor_id: str):
        data = self.client.patch(self._resource_path, endpoint=f"{sensor_id}", body=body)
        return Sensor.from_dict(data=data, client=self.client)

    def get_campaign(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/campaign")
        return Campaign.from_dict(data=data, client=self.client)

    def get_timeseries(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/timeseries")
        resources = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=resources, client=self.client)


class TimeseriesAPI(BaseAPI):

    def create(self, sensor_id: str, test_id: str):
        body = dict(sensor_id=sensor_id, test_id=test_id)
        data = self.client.post(self._resource_path, body=body)
        return Timeseries.from_dict(data=data, client=self.client)

    def get(self, id: str):
        data = self.client.get(self._resource_path, id)
        return Sensor.from_dict(data=data, client=self.client)

    def get_all(self):
        data = self.client.get(self._resource_path, "all")
        obj_list = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=obj_list, client=None)

    def delete(self, item_id: str):
        self.client.delete(self._resource_path, item_id)

    def patch(self, body: dict, id: str):
        return self.client.patch(resource=self._resource_path, endpoint=f"{id}", body=body)

    def get_data_points(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints")
        obj_list = [DataPoint.from_dict(data=obj, client=self.client) for obj in data]
        return DataPointList(resources=obj_list, client=None)

    def post_data_points(self, id, body):
        data = self.client.post(self._resource_path, f"{id}/datapoints", body=body)

'''
class DatapointAPI(BaseAPI):

    def create(self, timeseries_id: str, time: str, value: float):
        body = dict(timeseries_id=timeseries_id, time=time, value=value)
        data = self.client.post(self._resource_path, body=body)
        return DataPoint.from_dict(data=data, client=self.client)
'''