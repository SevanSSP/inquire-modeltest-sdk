from .client import SDKclient
import datetime
from uuid import uuid4


class BaseAPI:

    def __init__(self, SDKclient):
        self.client = SDKclient


class CampaignAPI(BaseAPI):

    def create(self, name: str, description: str, location: str, date: datetime.datetime, diameter: float,
               scale_factor: float, water_density: float, water_depth: float, transient: float):
        body = {'name': name,
                'description': description,
                'location': location,
                'date': date,
                'diameter': diameter,
                'scale_factor': scale_factor,
                'water_density': water_density,
                'water_depth': water_depth,
                'transient': transient}
        self.client.post("campaign", body=body)

    def get(self, campaign_id: str):
        return self.client.get("campaign", campaign_id)

    def get_id(self, name: str):
        response = self.client.get("campaign", "all", parameters={'name': name})
        return response[0]['id']

    def get_sensors(self, campaign_id: str):
        return self.client.get("campaign", f"{campaign_id}/sensors")


class SensorAPI(BaseAPI):

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

    def get_id(self, name: str):
        response = self.client.get("sensor", "all", parameters={'name': name})
        return response[0]['id']