import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union
from .utils import make_serializable, from_datetime_string
import datetime


class BaseResource(object):
    def __str__(self):
        return json.dumps(make_serializable(self.dump()), indent=2)

    def __repr__(self):
        return self.__str__()

    def dump(self):
         '''
         Dump the instance into a json serializable Python data type.

         Parameters
         ----------
         camel_case : bool, optional
             Use camelCase for attribute names. Defaults to False.

         Returns
         -------
         Dict[str, Any]
             A dictionary representation of the instance.
        '''
         d = {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}
         return d

    def to_pandas(self, ignore: List[str]=None):
        """
        Convert the instance into a pandas DataFrame.

        Parameters
        ----------
        ignore : List[str]
            List of row keys to not include when converting to a data frame.

         Returns
         -------
        pandas.DataFrame
            The dataframe.
        """
        ignore = list() if ignore is None else ignore
        dumped = self.dump()

        df = pd.DataFrame(columns=["value"])
        for name, value in dumped.items():
            if name not in ignore:
                df.loc[name] = [value]
        return df


class ResourceList(BaseResource):
    resources = list()

    def __iter__(self):
        for r in self.resources:
            yield r

    def __len__(self):
        return len(self.resources)

    def dump(self):
        return [_.dump() for _ in self]

    def to_pandas(self, ignore: List[str]=None):
        return pd.DataFrame (self.dump())


class Campaign(BaseResource):

    def __init__(self, name: str, description: str, location: str, date: any, diameter: float,
               scale_factor: float, water_density: float, water_depth: float, transient: float, id: str = None, client=None):
        #if not isinstance(date, datetime.datetime):
        #    try:
        #        date = from_datetime_string(date)
        #    except ValueError:
        #        raise ValueError("Could not convert datetime string to datetime object")

        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.date = date
        self.diameter = diameter
        self.scale_factor = scale_factor
        self.water_density = water_density
        self.water_depth = water_depth
        self.transient = transient
        self._client = client

    def __str__(self):
        return f"<Campaign {self.name}: \n{self.to_pandas()}>"

    def update(self):
        body = self.dump()
        if not self.id:
            data = self._client.campaign.create(body=body)
            if 'id' in data:
                self.id = data['id']
        else:
            self._client.campaign.patch(body=body, campaign_id=self.id)

    def get_sensors(self):
        if not self.id:
            raise Exception(f'Cannot get sensor for {self.name}. Campaign has not yet been created')
        data = self._client.campaign.get_sensors(campaign_id=self.id)
        sensors = [Sensor.from_dict(data=sensor, client=self._client) for sensor in data]
        return SensorList(sensors=sensors, client=self._client)

    @classmethod
    def get_existing(cls, name: str, client=None):
        data = client.campaign.get(client.campaign.get_id(name=name))

        return cls.from_dict(data=data, client=client)

    @classmethod
    def from_dict(cls, data, client=None):

        return cls(name=data['name'], description=data['description'], location=data['location'],
            date=data['date'], diameter=data['diameter'], scale_factor=data['scale_factor'],
            water_density=data['water_density'], water_depth=data['water_depth'],
            transient=data['transient'], id=data['id'], client=client)

class CampaignList(ResourceList):

    def __init__(self, campaign: List[Campaign], client=None):
        self.resources = campaign
        self._client = client

    def __str__(self):
        return f"{self.to_pandas()}"

class Sensor(BaseResource):

    def __init__(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
                 is_local: bool, campaign_id: str, id: str = None, client=None):

        self.id = id
        self.name = name
        self.description = description
        self.unit = unit
        self.kind = kind
        self.x = x
        self.y = y
        self.z = z
        self.is_local= is_local
        self.campaign_id= campaign_id
        self._client = client

    def __str__(self):
        return f"<Sensor {self.name}: \n{self.to_pandas()}>"

    def update(self):
        body = self.dump().copy()
        if not self.id:
            data = self._client.sensor.create(body=body)
            if 'id' in data:
                self.id = data['id']
        else:
            self._client.sensor.patch(body=body, sensor_id=self.id)

    @classmethod
    def get_existing(cls, name: str, client=None):
        data = client.sensor.get(client.sensor.get_id(name=name))
        return cls.from_dict(data=data, client=client)

    @classmethod
    def from_dict(cls, data, client):
        return cls(name=data['name'], description=data['description'], unit=data['unit'],
                   kind=data['kind'], x=data['y'], y=data['y'], z=data['z'], is_local=data['is_local'],
                   campaign_id=data['campaign_id'], id=data['id'], client=client)


class SensorList(ResourceList):

    def __init__(self, sensors: List[Sensor], client=None):
        self.resources = sensors
        self._client = client

    def __str__(self):
        return f"{self.to_pandas()}"

class Timeseries(BaseResource):

    def __init__(self, sensor_id, test_id, id: str = None, client=None):

        self.sensor_id = sensor_id
        self.test_id = test_id
        self.id = id
        self._client = client

    def __str__(self):
        return f"<Timeseries: {self.name}: \n{self.to_pandas()}>"

    def update(self):
        body = self.dump().copy()
        if not self.id:
            data = self._client.timeseries.create(body=body)
            if 'id' in data:
                self.id = data['id']
        else:
            self._client.timeseries.patch(body=body, sensor_id=self.id)

    @classmethod
    def get_existing(cls, name: str, client=None):
        data = client.timeseries.get(client.sensor.get_id(name=name))
        return cls.from_dict(data=data, client=client)

    @classmethod
    def from_dict(cls, data, client):
        return cls(sensor_id=data['sensor_id'], test_id=data['test_id'], id=data['id'], client=client)
