import datetime
from typing import List
from .utils import format_class_name
import warnings

def get_id_from_response(response):
    return response[0]["id"]


class BaseAPI:

    def __init__(self, client):
        self.client = client

    def create(self, body: dict):
        return self.client.post(format_class_name(self.__class__.__name__), body=body)

    def get(self, item_id: str):
        return self.client.get(format_class_name(self.__class__.__name__), item_id)

    def get_all(self):
        return self.client.get(format_class_name(self.__class__.__name__), "all")

    def delete(self, item_id: str):
        return self.client.delete(format_class_name(self.__class__.__name__), item_id)


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

    def patch(self, body: dict, campaign_id: str):
        return self.client.patch(resource="campaign", endpoint=f"{campaign_id}", body=body)

    def get_sensors(self, campaign_id: str):
        return self.client.get("campaign", f"{campaign_id}/sensors")

    def get_tests(self, campaign_id: str):
        return self.client.get("campaign", f"{campaign_id}/tests")

class TestAPI(NamedBaseAPI):

    def get_campaign(self, sensor_id: str):
        return self.client.get("sensor", f"{sensor_id}/campaign")


    def get_timeseries(self, sensor_id: str):
        return self.client.get("sensor", f"{sensor_id}/timeseries")

class SensorAPI(NamedBaseAPI):

    def patch(self, body: dict, sensor_id: str):
        return self.client.patch(resource="sensor", endpoint=f"{sensor_id}", body=body)

    def get_campaign(self, sensor_id: str):
        return self.client.get("sensor", f"{sensor_id}/campaign")

    def get_timeseries(self, sensor_id: str):
        return self.client.get("sensor", f"{sensor_id}/timeseries")


class TimeseriesAPI(BaseAPI):

    def create(self, sensor_id: str, test_id: str, data: List=None):
        body = {'sensor_id': sensor_id, 'test_id': test_id}
        response = self.client.post("timeseries", body=body)
        '''
        if data is not None and isinstance(data, List):
            dp =    DatapointAPI(self.client)
            timeseries_id = get_id_from_response(response)
            for datapoint in data:
                dp.create(timeseries_id,)
        ''' #TODO: Må gjøres smartere for å få med klokkeslett

    def patch(self, body: dict, sensor_id: str):
        return self.client.patch(resource="timeseries", endpoint=f"{sensor_id}", body=body)

    def get_test(self, sensor_id: str):
        return self.client.get("timeseries", f"{sensor_id}/campaign")

    def get_sensor(self, sensor_id: str):
        return self.client.get("sensor", f"{sensor_id}/timeseries")


class DatapointAPI(BaseAPI):

    def create(self, timeseries_id: str, time: datetime, value: float):
        body = {'timeseries_id': timeseries_id, 'time': time, 'value': value }
        self.client.post("datapoint", body=body)
