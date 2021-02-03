import json
import pandas as pd
from typing import List
from .utils import make_serializable
import numpy
import warnings

'''
User-side classes 
'''


class BaseResource:
    def __str__(self):
        return json.dumps(make_serializable(self.dump()), indent=2)

    def __repr__(self):
        return self.__str__()

    def dump(self):
        """
        Dump the instance into a json serializable Python data type.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the instance.
        """
        d = {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}
        return d

    def to_pandas(self, ignore: List[str] = None) -> pd.DataFrame:
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
    def from_dict(cls, data: dict, client=None):
        # noinspection PyArgumentList
        data.pop('read_only')
        return cls(**data, client=client)


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

    def to_pandas(self, ignore: List[str] = None) -> pd.DataFrame:
        return pd.DataFrame(self.dump())

    def append(self, data: any):
        self.resources.append(data)


class Campaign(BaseResource):

    def __init__(self, name: str, description: str, location: str, date: any,
                 scale_factor: float, water_depth: float, id: str = None,
                 client=None):

        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.date = date
        self.scale_factor = scale_factor
        self.water_depth = water_depth
        self._client = client
        self.test = TestList(resources=[], client=client)
        self.sensor = SensorList(resources=[], client=client)

    def __str__(self):
        return f"<Campaign {self.name}: \n{self.to_pandas()}>"

    def update(self):
        return self._client.campaign.patch(body=self.dump(), campaign_id=self.id)

    def delete(self):
        warnings.warn("\nDeleting a campaign cascade deletes all underlying data.\n"
                      "If the campaign is large this can take several minutes.\n")
        ans = input("\nAre you sure you still want to continue the delete? [y/N] ")
        if ans == "y":
            self._client.campaign.delete(id=self.id)

    def get_sensors(self):
        if not self.id:
            raise Exception(f'Cannot get sensor for {self.name}. Campaign has not yet been created')
        return self._client.campaign.get_sensors(id=self.id)

    def get_tests(self, test_type: str = None):
        if not self.id:
            raise Exception(f'Cannot get tests for {self.name}. Campaign has not yet been created')
        return self._client.campaign.get_tests(id=self.id, type=test_type)

    def populate_test(self, child):
        if isinstance(child, TestList):
            for item in child:
                self.test.append(item)
        else:
            self.test.append(child)

    def populate_sensor(self, child):
        if isinstance(child, SensorList):
            for item in child:
                self.sensor.append(item)
        else:
            self.sensor.append(child)


class CampaignList(ResourceList):

    def __init__(self, resources: List[Campaign], client=None):
        self.resources = resources
        self._client = client


class Sensor(BaseResource):

    def __init__(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
                 position_reference: str, position_heading_lock: bool, position_draft_lock: bool,
                 positive_direction_definition: str, area: float = None, campaign_id: str = None,
                 id: str = None, client=None):
        self.id = id
        self.name = name
        self.description = description
        self.unit = unit
        self.kind = kind
        self.area = area
        self.x = x
        self.y = y
        self.z = z
        self.position_reference = position_reference,
        self.position_heading_lock = position_heading_lock,
        self.position_draft_lock = position_draft_lock,
        self.positive_direction_definition = positive_direction_definition,
        self.campaign_id = campaign_id
        self._client = client

    def __str__(self):
        return f"<Sensor {self.name}: \n{self.to_pandas()}>"

    def update(self):
        return self._client.sensor.patch(body=self.dump(), sensor_id=self.id)


class SensorList(ResourceList):

    def __init__(self, resources: List[Sensor], client=None):
        self.resources = resources
        self._client = client

    def __getitem__(self, key) -> Sensor:
        if isinstance(key, int):
            return self.resources[key]
        if isinstance(key, str):
            try:
                for item in self:
                    if item.name == key:
                        return item
            except KeyError:
                raise Exception(f"Sensor {key} not found under campaign ")


class Test(BaseResource):
    def __init__(self, number: str, description: str, test_date: str, test_type: str, campaign_id: str = None,
                 test_id: str = None,
                 client=None):

        self.number = number
        self.description = description
        self.test_date = test_date
        self.campaign_id = campaign_id
        self.type = test_type
        self.id = test_id
        self._client = client

        self.timeseries = TimeseriesList(resources=[], client=client)

    def __str__(self):
        return f"<Test: \n{self.to_pandas()}>"

    def get_timeseries(self):
        return self._client.test.get_timeseries(id=self.id)

    def populate_timeseries(self, child):
        if isinstance(child, TimeseriesList):
            for item in child:
                self.timeseries.append(item)
        else:
            self.timeseries.append(child)


class TestList(ResourceList):

    def __init__(self, resources: List[Test], client=None):
        self.resources = resources
        self._client = client

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.resources[key]
        if isinstance(key, str):
            try:
                for t in self:
                    if t.description == key:
                        return t
            except KeyError:
                raise Exception(f"Test {key} not found under campaign ")


class FloaterTest(Test):
    type = "Floater Test"

    def __init__(self, number: str, description: str, test_date: str, campaign_id: str,
                 category: str, orientation: float, floaterconfig_id: str = None, wave_id: str = None,
                 wind_id: str = None, floater_id: str = None, client=None):
        super().__init__(number=number, description=description, test_date=test_date, campaign_id=campaign_id,
                         test_type=self.type, test_id=floater_id, client=client)

        self.category = category
        self.orientation = orientation
        self.wave_id = wave_id
        self.wind_id = wind_id
        self.floaterconfig_id = floaterconfig_id
        self.id = floater_id
        self._client = client


class FloaterTestList(ResourceList):

    def __init__(self, resources: List[FloaterTest], client=None):
        self.resources = resources
        self._client = client


class WaveCalibration(Test):
    type = "Wave Calibration"

    def __init__(self, number: str, description: str, test_date: str, campaign_id: str,
                 wave_spectrum: str = None, wave_height: float = None, wave_period: float = None,
                 gamma: float = None, wave_direction: float = None, current_velocity: float = None,
                 current_direction: float = None, wave_calibration_id: str = None, client=None):
        super().__init__(number=number, description=description, test_date=test_date, campaign_id=campaign_id,
                         test_type=self.type, test_id=wave_calibration_id, client=client)

        self.wave_spectrum = wave_spectrum
        self.wave_height = wave_height
        self.wave_period = wave_period
        self.gamma = gamma
        self.wave_direction = wave_direction
        self.current_velocity = current_velocity
        self.current_direction = current_direction


class WaveCalibrationList(ResourceList):

    def __init__(self, resources: List[WaveCalibration], client=None):
        self.resources = resources
        self._client = client


class WindCalibration(Test):
    type = "Wind Calibration"

    def __init__(self, number: str, description: str, test_date: str, campaign_id: str,
                 wind_spectrum: str = None, wind_velocity: float = None, zref: float = None,
                 wind_direction: float = None, wind_condition_id: str = None, client=None):
        super().__init__(number=number, description=description, test_date=test_date, campaign_id=campaign_id,
                         test_type=self.type, test_id=wind_condition_id, client=client)

        self.wind_spectrum = wind_spectrum
        self.wind_velocity = wind_velocity
        self.zref = zref
        self.wind_direction = wind_direction


class WindCalibrationList(ResourceList):

    def __init__(self, resources: List[WindCalibration], client=None):
        self.resources = resources
        self._client = client


class Timeseries(BaseResource):

    def __init__(self, sensor_id: str, test_id: str, fs: float, intermittent: bool = False,
                 ts_id: str = None, client=None):

        self.sensor_id = sensor_id
        self.test_id = test_id
        self.fs = fs
        self.intermittent = intermittent
        self.id = ts_id
        self.data_points = DataPointList(resources=[], client=client)
        self._client = client

    def __str__(self):
        return f"<Timeseries: \n{self.to_pandas()}>"

    def to_pandas(self, ignore: List[str] = None) -> pd.DataFrame:
        ignore = list() if ignore is None else ignore
        dumped = self.dump()

        df = pd.DataFrame(columns=["value"])
        for name, value in dumped.items():
            if name == "sensor_id":
                df.loc[name] = self._client.sensor.get(value).name
            elif name == "data_points":
                df.loc[name] = len(self.data_points)
            elif name not in ignore:
                df.loc[name] = [value]
        return df

    def update(self):
        self._client.timeseries.patch(body=self.dump(), id=self.id)

    def get_data_points(self):
        self.data_points = self._client.timeseries.get_data_points(id=self.id)['data']
        return self.data_points

    def to_arrays(self):
        if not self.data_points:
            self.get_data_points()
        times_in_tuples = []
        values = []
        for data_point in self.data_points:
            times_in_tuples.append(data_point.time)
            values.append(data_point.value)
        times_in_array = numpy.array(times_in_tuples)
        times = []
        for Time in times_in_array:
            times.append(float(Time))

        times = numpy.array(times)
        values = numpy.array(values)
        return times, values

    def get_froude_scaled_arrays(self):
        times, values = self.to_arrays()

        # Get the scale factor from the campaign that the timeseries belongs to
        scale_factor = self._client.campaign.get(self._client.test.get(self.test_id).campaign_id).scale_factor

        # Froude scaling
        t = times * (scale_factor ** 0.5)
        sensor = self.get_sensor()
        if sensor.kind == "length":
            froude_factor = 1
        elif sensor.kind == "velocity":
            froude_factor = 0.5
        elif sensor.kind == "acceleration":
            froude_factor = 0
        elif sensor.kind == "force":
            froude_factor = 3
        elif sensor.kind == "pressure":
            froude_factor = 1
        elif sensor.kind == "volume":
            froude_factor = 3
        elif sensor.kind == "mass":
            froude_factor = 3
        elif sensor.kind == "angle":
            froude_factor = 0
        else:
            raise Exception(f"Automatic froude scaling for {sensor.kind} sensors is not supported.")

        v = values * (scale_factor ** froude_factor)

        return t, v

    def post_data_points(self):
        self._client.timeseries.post_data_points(body=self.data_points.dump(), id=self.id)

    def get_standard_deviation(self):
        return self._client.timeseries.get_standard_deviation(id=self.id)

    def get_max_value(self):
        return self._client.timeseries.get_max_value(id=self.id)

    def get_min_value(self):
        return self._client.timeseries.get_min_value(id=self.id)

    def get_mean(self):
        return self._client.timeseries.get_mean(id=self.id)

    def get_measured_hs(self):
        return self._client.timeseries.get_measured_hs(id=self.id)

    def get_measured_tp(self):
        return self._client.timeseries.get_measured_tp(id=self.id)

    def get_sensor(self) -> Sensor:
        return self._client.timeseries.get_sensor(id=self.id)

    def get_test(self):
        return self._client.timeseries.get_test(id=self.id)


class TimeseriesList(ResourceList):

    def __init__(self, resources: List[Timeseries], client=None):
        self.resources = resources
        self._client = client
        # self._sensor_names = []

    def to_pandas(self, ignore: List[str] = None) -> pd.DataFrame:
        df = pd.DataFrame(self.dump())
        '''
        df.rename(columns={'sensor_id': 'sensor', 'data_points': 'length'}, inplace=True)
        if 'test_id' in df:
            df.drop(columns={'test_id'}, inplace=True)

        print(df['sensor'].tolist())
        #names = self._client.sensor.get_multiple_by_name(df['sensor'].tolist())
        #names = [(self._client.sensor.get(sensor_id)).name for sensor_id in df['sensor'].tolist()]
        for i in df.index:
            df.at[i, 'sensor'] = names[i]
            df.at[i, 'length'] = len(self.resources[i].data_points)
        '''
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
            except KeyError:
                raise Exception(f"Timeseries {key} not found under campaign ")

    def __str__(self):
        return f"<Timeseries: \n{self.to_pandas()}>"


class DataPoint(BaseResource):

    def __init__(self, time: float, value: float, client=None):

        self.time = time
        self.value = value
        self._client = client

    def __str__(self):
        return f"<DataPoint: \n{self.to_pandas()}>"

    @classmethod
    def from_dict(cls, data: str, client=None):
        if data.find("\n") and data.find("\t"):
            time, value = data.replace("\n", "").split("\t")
            return cls(time=float(time), value=float(value),
                       client=client)
        else:
            warnings.warn("Imported an empty datapoint.")
            return cls(time=None, value=float(None),
                       client=client)


class DataPointList(ResourceList):

    def __init__(self, resources: List[DataPoint], client=None):
        self.resources = resources
        self._client = client


'''
    def from_dict(cls, data: dict, client=None):
        dp_list = []
        for dp in data['data']:
            dp_list.append(DataPoint(time))
'''


class Tag(BaseResource):

    def __init__(self, name: str, comment: str, test_id: str = None, sensor_id: str = None, timeseries_id: str = None,
                 tag_id: str = None, client=None):
        self.name = name
        self.comment = comment
        self.test_id = test_id
        self.sensor_id = sensor_id
        self.timeseries_id = timeseries_id
        self.id = tag_id
        self._client = client

    def __str__(self):
        return f"<Tag: \n{self.to_pandas()}>"

    def delete(self):
        self._client.tag.delete(id=self.id)


class TagList(ResourceList):

    def __init__(self, resources: List[Tag], client=None):
        self.resources = resources
        self._client = client


class FloaterConfig(BaseResource):

    def __init__(self, name: str, description: str, characteristic_length: float, draft: float, campaign_id: str,
                 floater_id: str = None, client=None):
        self.name = name
        self.description = description
        self.characteristic_length = characteristic_length
        self.draft = draft
        self.campaign_id = campaign_id
        self.id = floater_id
        self._client = client

    def __str__(self):
        return f"<Concept: \n{self.to_pandas()}>"


class FloaterConfigList(ResourceList):

    def __init__(self, resources: List[Tag], client=None):
        self.resources = resources
        self._client = client
