import json
import pandas as pd
from typing import List, Union
from .utils import make_serializable, from_datetime_string
import datetime
import numpy
from typing import Optional
import warnings

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
        self.test = TestList(resources=[], client=client)
        self.sensor = SensorList(resources=[], client=client)

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

    def populate_test(self, child):
        if isinstance(child, list):
            for item in child:
                self.test.append(item)
        else:
            self.test.append(child)
    '''
    def find_test(self, name):
        try:
            for t in self.test:
                if t.description == name:
                    return t
        except:
            raise Exception(f"Test not found under {self.name} campaign ")
    '''
    def populate_sensor(self, child):
        if isinstance(child, list):
            for item in child:
                self.sensor.append(item)
        else:
            self.sensor.append(child)

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

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.resources[key]
        if isinstance(key,str):
            try:
                for item in self:
                    if item.name == key:
                        return item
            except:
                raise Exception(f"Sensor {key} not found under campaign ")

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

        self.timeseries = TimeseriesList(resources=[],client=client)

    def __str__(self):
        return f"<Test: \n{self.to_pandas()}>"

    def get_campaign(self):
        return self._client.test.get_campaign(id=self.id)

    def get_timeseries(self):
        return self._client.test.get_timeseries(id=self.id)

    def populate_timeseries(self, child):
        if isinstance(child, TimeseriesList):
            for item in child:
                self.timeseries.append(item)
        else:
            self.timeseries.append(child)

    @classmethod
    def from_dict(cls, data: dict, client=None):
        return cls(description=data["description"], test_date=data['test_date'], campaign_id=data['campaign_id'],
                   type=data['type'], id=data['id'],    # measured_hs=data['measured_hs'], measured_tp=data['measured_tp'],
                   client=client)


class TestList(ResourceList):

    def __init__(self, resources: List[Test], client=None):
        self.resources = resources
        self._client = client

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.resources[key]
        if isinstance(key,str):
            try:
                for t in self:
                    if t.description == key:
                        return t
            except:
                raise Exception(f"Test {key} not found under campaign ")


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

    def to_pandas(self, ignore: List[str]=None):
        ignore = list() if ignore is None else ignore
        dumped = self.dump()

        df = pd.DataFrame(columns=["value"])
        for name, value in dumped.items():
            if name == "sensor_id":
                df.loc[name] = self._client.sensor.get(value).name
            elif name not in ignore:
                df.loc[name] = [value]
        return df

    def update(self):
        self._client.timeseries.patch(body=self.dump(), id=self.id)

    def get_data_points(self):
        self.data_points = self._client.timeseries.get_data_points(id=self.id)
        return self.data_points

    # De to følgende metodene returnerer datapunktene i to arrays. Begge variantene kan brukes, vet ikke hvilken som er best.
    # Tiden er gitt som antall sekunder etter testen startet
    def get_data_points_as_arrays(self):
        self.data_points = self._client.timeseries.get_data_points(id=self.id)
        times_in_tuples = []
        values = []
        for data_point in self.data_points:
            times_in_tuples.append(data_point.time)
            values.append(data_point.value)
        times_in_array = numpy.array(times_in_tuples)
        start_time = times_in_array[0]
        times = []
        for Time in times_in_array:
            times.append((Time - start_time).total_seconds())

        times = numpy.array(times)
        values = numpy.array(values)
        return times, values

    # Fordelen med denne metoden er at det kan være enklere å bruke hvis man i tillegg til tidsseriens datapunkter
    # har et sett med froude-skalerte datapunkter, så man får spesifisert hvilke datapunkter som skal brukes
    def to_arrays(self, data_points):
        times_in_tuples = []
        values = []
        for data_point in data_points:
            times_in_tuples.append(data_point.time)
            values.append(data_point.value)
        times_in_array = numpy.array(times_in_tuples)
        start_time = times_in_array[0]
        times = []
        for Time in times_in_array:
            times.append((Time - start_time).total_seconds())

        times = numpy.array(times)
        values = numpy.array(values)
        return times, values

    # Eksempel på automatisk froude skalering. Bør kanskje flyttes til API. times og values er arrays i denne varianten.
    def get_froude_scaled_arrays(self, times, values, scale_factor):
        t = times * (scale_factor ** 0.5)
        sensor = self.get_sensor()
        print(sensor.kind)
        if sensor.kind == "length":
            v = values * (scale_factor ** 1) / 1000
        if sensor.kind == "velocity":
            v = values * (scale_factor ** 0.5) / 1000
        if sensor.kind == "acceleration":
            v = values * (scale_factor ** 0) / 1000
        if sensor.kind == "force":
            v = values * (scale_factor ** 3)
        if sensor.kind == "pressure":
            v = values * (scale_factor ** 1)
        if sensor.kind == "volume":
            v = values * (scale_factor ** 3)
        if sensor.kind == "mass":
            v = values * (scale_factor ** 3)
        if sensor.kind == "angle":
            v = values * (scale_factor ** 0)
        return t, v

    def post_data_points(self):
        self._client.timeseries.post_data_points(body=self.data_points.dump(), id=self.id)

    def __len__(self):
        return len(self.data_points)

    def standard_deviation(self):
        #return self._client.timeseries.standard_deviation(self, id=self.id)
        return self._client.timeseries.get_standard_deviation(id=self.id)

    def get_max_value(self):
        return self._client.timeseries.get_max_value(id=self.id)

    def get_min_value(self):
        return self._client.timeseries.get_min_value(id=self.id)

    def get_measured_hs(self):
        return self._client.timeseries.get_measured_hs(id=self.id)

    def get_measured_tp(self):
        return self._client.timeseries.get_measured_tp(id=self.id)

    def get_sensor(self):
        return self._client.timeseries.get_sensor(id=self.id)

    @classmethod
    def from_dict(cls, data: dict, client = None):
        return cls(sensor_id=data['sensor_id'], test_id=data['test_id'], id=data['id'], client=client)


class TimeseriesList(ResourceList):

    def __init__(self, resources: List[Timeseries], client=None):
        self.resources = resources
        self._client = client
        #self._sensor_names = []

    def to_pandas(self, ignore: List[str]=None):
        df = pd.DataFrame(self.dump())

        df.rename(columns={'sensor_id': 'sensor', 'data_points':'length'},inplace=True)
        if 'test_id' in df:
            df.drop(columns={'test_id'},inplace=True)
        for i in df.index:
            df.at[i, 'sensor'] = self._client.sensor.get(df['sensor'][i]).name
            df.at[i, 'length'] = len(self.resources[i])
        return df

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.resources[key]
        if isinstance(key, str):
            key_id = self._client.sensor.get_by_name(key).id
            try:
                for item in self:
                    if item.sensor_id == key_id:
                        return item
            except:
                raise Exception(f"Timeseries {key} not found under campaign ")

    def __str__(self):
        return f"<Test: \n{self.to_pandas()}>"


class DataPoint(BaseResource):

    def __init__(self, time: str, value: float, timeseries_id: str = None, client=None):

        self.timeseries_id = timeseries_id
        self.time = time
        self.value = value
        self._client = client

    def __str__(self):
        return f"<DataPoint: \n{self.to_pandas()}>"

    @classmethod
    def from_dict(cls, data: str, client = None):
        # VERY BAD PRACTICE; BUT DONE FOR INCREASED PERFORMANCE. Object sent as text file
        if data.find("\n") and data.find("\t"):
            time, value = data.replace("\n", "").split("\t")
            time_string = time.split(" ")[1]
            if len(time_string) == 8:
                # If timestamp is at whole second, ex. "09:00:00"
                time = datetime.datetime.strptime(time_string, "%H:%M:%S")
            else:
                # Timestamp, ex. "09:00:00.592"
                time = datetime.datetime.strptime(time_string, "%H:%M:%S.%f")
            return cls(time=time, value=float(value),
                       client=client)
        else:
            warnings.warn("Imported an empty datapoint.")
            return cls(time=None, value=float(None),
                       client=client)


class DataPointList(ResourceList):

    def __init__(self, resources: List[DataPoint], client=None):
        self.resources = resources
        self._client = client

