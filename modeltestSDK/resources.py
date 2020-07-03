import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union
from .utils import make_serializable, from_datetime_string
import datetime
from typing import Optional

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

    @classmethod
    def from_dict(cls, data: dict, client = None):
        raise NotImplemented

class ResourceList(BaseResource):
    resources = list()

    def __iter__(self):
        for r in self.resources:
            yield r

    def __getitem__(self, key):
        return self.resources[key]

    def __len__(self):
        return len(self.resources)

    def __str__(self):
        return f"<{self.to_pandas()}>"

    def dump(self):
        return [_.dump() for _ in self]

    def to_pandas(self, ignore: List[str]=None):
        return pd.DataFrame (self.dump())

    def append(self, data: any):
        self.resources.append(data)

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
        return self._client.campaign.patch(body=self.dump(), campaign_id=self.id)

    def get_sensors(self):
        if not self.id:
            raise Exception(f'Cannot get sensor for {self.name}. Campaign has not yet been created')
        return self._client.campaign.get_sensors(id=self.id)

    def get_tests(self, type: str = None):
        if not self.id:
            raise Exception(f'Cannot get tests for {self.name}. Campaign has not yet been created')
        return self._client.campaign.get_tests(id=self.id, type=type)

    @classmethod
    def from_dict(cls, data: dict, client = None):
        return cls(name=data['name'], description=data['description'], location=data['location'],
            date=data['date'], diameter=data['diameter'], scale_factor=data['scale_factor'],
            water_density=data['water_density'], water_depth=data['water_depth'],
            transient=data['transient'], id=data['id'], client=client)

class CampaignList(ResourceList):

    def __init__(self, resources: List[Campaign], client=None):
        self.resources = resources
        self._client = client

class Sensor(BaseResource):

    def __init__(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
                 is_local: bool, campaign_id: str = None, id: str = None, client=None):

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
        return self._client.sensor.patch(body=self.dump(), sensor_id=self.id)

    def get_campaign(self):
        return self._client.sensor.get_campaign(id=self.id)

    def get_timeseries(self):
        return self._client.sensor.get_timeseries(id=self.id)

    @classmethod
    def from_dict(cls, data: dict, client = None):
        return cls(name=data['name'], description=data['description'], unit=data['unit'],
                   kind=data['kind'], x=data['y'], y=data['y'], z=data['z'], is_local=data['is_local'],
                   campaign_id=data['campaign_id'], id=data['id'], client=client)


class SensorList(ResourceList):

    def __init__(self, resources: List[Sensor], client=None):
        self.resources = resources
        self._client = client

class Test(BaseResource):
    def __init__(self, description: str, test_date: str, type: str,campaign_id: str = None, id: str = None, client=None):   # measured_hs: str = None, measured_tp: str = None,

        self.description = description
        self.test_date = test_date
        self.campaign_id = campaign_id
        self.type = type
        # self.measured_hs = measured_hs
        # self.measured_tp = measured_tp
        self.id = id
        self._client = client

    def __str__(self):
        return f"<Test: \n{self.to_pandas()}>"

    def get_campaign(self):
        return self._client.test.get_campaign(id=self.id)

    def get_timeseries(self):
        return self._client.test.get_timeseries(id=self.id)

    @classmethod
    def from_dict(cls, data: dict, client=None):
        return cls(description=data["description"], test_date=data['test_date'], campaign_id=data['campaign_id'],
                   type=data['type'], id=data['id'],    # measured_hs=data['measured_hs'], measured_tp=data['measured_tp'],
                   client=client)

class TestList(ResourceList):

    def __init__(self, resources: List[Test], client=None):
        self.resources = resources
        self._client = client

class Floater(Test):
    type = "floater"

    def __init__(self, description: str, test_date: str, campaign_id: str, # measured_hs: str, measured_tp: str,
                 category: str, orientation: float, draft: float, wave_id: str = None, wind_id: str = None,
                 id: str = None, client=None):

        super().__init__(description=description, test_date=test_date, campaign_id=campaign_id,
                        type=self.type, id=id, client=client)   # , measured_hs=measured_hs, measured_tp=measured_tp

        self.category=category
        self.orientation=orientation
        self.draft=draft
        self.wave_id=wave_id
        self.wind_id=wind_id

    @classmethod
    def from_dict(cls, data: dict, client=None):
        return cls(description=data["description"], test_date=data['test_date'], campaign_id=data['campaign_id'],
                   # measured_hs=data['measured_hs'], measured_tp=data['measured_tp'],
                   category=data['category'], orientation =data['orientation'], draft =data['draft'],
                   wave_id = data['wave_id'], wind_id = data['wind_id'], id= data['id'], client=client)

class FloaterList(ResourceList):

    def __init__(self, resources: List[Floater], client=None):
        self.resources = resources
        self._client = client

class WaveCurrentCalibration(Test):
    type = "waveCurrentCalibration"

    def __init__(self, description: str, test_date: str, campaign_id: str, # measured_hs: str, measured_tp: str,
                 wave_spectrum: str = None, wave_height: float = None, wave_period: float = None,
                 gamma: float = None, wave_direction: float = None, current_velocity: float = None,
                 current_direction: float = None, id: str = None, client=None):

        super().__init__(description=description, test_date=test_date, campaign_id=campaign_id,
                         type=self.type, id=id, client=client)  # , measured_hs=measured_hs, measured_tp=measured_tp

        self.wave_spectrum = wave_spectrum
        self.wave_height = wave_height
        self.wave_period = wave_period
        self.gamma = gamma
        self.wave_direction = wave_direction
        self.current_velocity = current_velocity
        self.current_direction = current_direction

    @classmethod
    def from_dict(cls, data: dict, client=None):
        return cls(description=data["description"], test_date=data['test_date'], campaign_id=data['campaign_id'],
                   # measured_hs=data['measured_hs'], measured_tp=data['measured_tp'],
                   wave_spectrum = data['wave_spectrum'], wave_height = data['wave_height'],
                   wave_period = data['wave_period'], gamma = data['gamma'],
                   wave_direction = data['wave_direction'], current_velocity = data['current_velocity'],
                   current_direction = data['current_direction'], id=data['id'], client=client)

class WaveCurrentCalibrationList(ResourceList):

    def __init__(self, resources: List[WaveCurrentCalibration], client=None):
        self.resources = resources
        self._client = client


class WindConditionCalibration(Test):
    type = "windConditionCalibration"

    def __init__(self, description: str, test_date: str, campaign_id: str, # measured_hs: str, measured_tp: str,
                 wind_spectrum: str = None, wind_velocity: float = None, zref: float = None,
                 wind_direction: float = None, id: str = None, client=None):
        super().__init__(description=description, test_date=test_date, campaign_id=campaign_id,
                         type=self.type, id=id, client=client)  # , measured_hs=measured_hs, measured_tp=measured_tp

        self.wind_spectrum = wind_spectrum
        self.wind_velocity = wind_velocity
        self.zref = zref
        self.wind_direction = wind_direction

    @classmethod
    def from_dict(cls, data: dict, client=None):
        return cls(description=data["description"], test_date=data['test_date'], campaign_id=data['campaign_id'],
                   # measured_hs=data['measured_hs'], measured_tp=data['measured_tp'],
                   wind_spectrum=data['wind_spectrum'], wind_velocity=data['wind_velocity'],
                   zref=data['zref'], wind_direction=data['wind_direction'], id=data['id'],  client=client)

class WindConditionCalibrationList(ResourceList):

    def __init__(self, resources: List[WindConditionCalibration], client=None):
        self.resources = resources
        self._client = client

class Timeseries(BaseResource):

    def __init__(self, sensor_id: str, test_id: str, id: str = None, client=None):

        self.sensor_id = sensor_id
        self.test_id = test_id
        self.id = id
        self.data_points = DataPointList(resources=[], client=client)
        self._client = client

    def __str__(self):
        return f"<Timeseries: \n{self.to_pandas()}>"

    def update(self):
        self._client.timeseries.patch(body=self.dump(), id=self.id)

    def get_data_points(self):
        self.data_points = self._client.timeseries.get_data_points(id=self.id)
        return self.data_points

    def post_data_points(self):
        self._client.timeseries.post_data_points(body=self.data_points.dump(), id=self.id)

    @classmethod
    def from_dict(cls, data: dict, client = None):
        return cls(sensor_id=data['sensor_id'], test_id=data['test_id'], id=data['id'], client=client)

class TimeseriesList(ResourceList):

    def __init__(self, resources: List[Timeseries], client=None):
        self.resources = resources
        self._client = client

class DataPoint(BaseResource):

    def __init__(self, time: str, value: float, timeseries_id: str = None, client=None):
        self.timeseries_id = timeseries_id
        self.time = time
        self.value = value
        self._client = client

    def __str__(self):
        return f"<DataPoint: \n{self.to_pandas()}>"

    @classmethod
    def from_dict(cls, data: dict, client = None):
        return cls(time=data['time'], value=data['value'],
                   client=client)

class DataPointList(ResourceList):

    def __init__(self, resources: List[DataPoint], client=None):
        self.resources = resources
        self._client = client



