import datetime
from typing import List
from .utils import format_class_name


def get_id_from_response(response):
    return response[0]["id"]


class BaseAPI:

    def __init__(self, client):
        self.client = client

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
            return response[0]['id']
        else:
            raise Exception(f"Could not find any object with name {self.__class__.__name__}")

class CampaignAPI(NamedBaseAPI):

    def create(self, body: dict):
        return self.client.post("campaign", body=body)

    def patch(self, body: dict, campaign_id: str):
        self.client.patch(resource="campaign", endpoint=f"{campaign_id}", body=body)

    def get_sensors(self, campaign_id: str):
        return self.client.get("campaign", f"{campaign_id}/sensors")

    def get_tests(self, campaign_id: str):
        return self.client.get("campaign", f"{campaign_id}/tests")


class SensorAPI(NamedBaseAPI):

    def create(self,
               name: str,
               description: str,
               unit: str,
               kind: str,
               x: float,
               y: float,
               z: float,
               is_local: bool,
               campaign_id: str):
        body = {'name': name,
                'description': description,
                'unit': unit,
                'kind': kind,
                'x': x,
                'y': y,
                'z': z,
                'is_local': is_local,
                'campaign_id': campaign_id}
        self.client.post("sensor", body=body)

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





class DatapointAPI(BaseAPI):

    def create(self, timeseries_id: str, time: datetime, value: float):
        body = {'timeseries_id': timeseries_id, 'time': time, 'value': value }
        self.client.post("datapoint", body=body)
