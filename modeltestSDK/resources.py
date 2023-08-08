"""
Resource models
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pydantic import BaseModel
from pydantic.typing import Literal
from typing import List, Optional, Union, Any
from datetime import datetime
from .utils import make_serializable
from qats import TimeSeries as QatsTimeSeries
from qats import TsDB as QatsTsDB
import typing


class Resource(BaseModel):
    client: Optional[Any]
    id: Optional[str]

    def _api_object(self):
        if hasattr(self.client, self.__class__.__name__.lower()):
            return getattr(self.client, self.__class__.__name__.lower())
        elif hasattr(self.client, self.__class__.__name__[:-5].lower()):
            return getattr(self.client, self.__class__.__name__[:-5].lower())
        elif hasattr(self.client, self.__class__.__name__[:-7].lower()):
            return getattr(self.client, self.__class__.__name__[:-7].lower())
        elif hasattr(self.client, self.__class__.__name__[:-4].lower()):
            return getattr(self.client, self.__class__.__name__[:-4].lower())
        else:
            return None

    def create(self, admin_key=None):
        try:
            if admin_key is None:
                resource = self._api_object().create(
                    **make_serializable(self.dict(exclude={"client", 'id', 'datapoints_created_at'})))
            else:
                resource = self._api_object().create(
                    **make_serializable(self.dict(exclude={"client", 'id', 'datapoints_created_at'})),
                    admin_key=admin_key)
            self.id = resource.id
        except AttributeError as e:
            if self.client is None:
                raise AttributeError('No client provided, unable to create object')
            else:
                raise e

    def update(self, secret_key: str = None):
        self._api_object().update(item_id=self.id, body=make_serializable(self.dict(exclude={"client", 'id'})),
                                  secret_key=secret_key)

    def delete(self, secret_key: str = None):
        self._api_object().delete(item_id=self.id, secret_key=secret_key)

    def to_pandas(self, **kwargs) -> pd.DataFrame:
        """
        Convert the instance into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.

        See Also
        --------
        See keyword arguments on pydantic.BaseModel.dict()
        """
        df = pd.DataFrame(columns=["value"])
        for name, value in self.dict().items():
            if name not in ("client",):
                df.loc[name] = [value]
        return df

T = typing.TypeVar("T", bound=Resource)

class Resources(List[Resource]):
    def __init__(self, items: List[Resource] = None) -> None:
        if items:
            self._check_types(items)
            super().__init__(items)

    def _check_types(self, items: List[T]) -> None:
        expected_type = self.__orig_bases__[0].__args__[0]
        for item in items:
            if not issubclass(type(item), expected_type):
                raise TypeError(f"Invalid type {type(item)} in {self.__class__.__name__}")

    def append(self, item: T, admin_key: str = None) -> None:
        expected_type = self.__orig_bases__[0].__args__[0]
        if not issubclass(type(item), expected_type):
            raise TypeError(f"Invalid type {type(item)} in {self.__class__.__name__}")
        if item.id or item.__class__.__name__ == 'DataPoints':
            super().append(item)
        else:
            item.create(admin_key=admin_key)
            super().append(item)

    def get_by_id(self, id):
        for i in self:
            if i.id == id:
                return i
        raise KeyError(f"ID: {id} not found in  {self.__class__.__name__}")

    def to_pandas(self, **kwargs) -> pd.DataFrame:
        """
        Convert the instance into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.

        See Also
        --------
        See keyword arguments on pydantic.BaseModel.dict()
        """
        return pd.DataFrame([_.dict(exclude={"client"}, **kwargs) for _ in self])


class FloaterConfiguration(Resource):
    id: Optional[str]
    name: str
    description: str
    campaign_id: str
    characteristic_length: float
    draft: float


class FloaterConfigurations(Resources[FloaterConfiguration]):
    pass


class Statistics(Resource):
    min: float
    max: float
    std: float
    mean: float
    m0: float
    m1: float
    m2: float
    m4: float


class Tag(Resource):
    id: Optional[str]
    name: str
    comment: Optional[str]
    test_id: Optional[str]
    sensor_id: Optional[str]
    timeseries_id: Optional[str]


class Tags(Resources[Tag]):
    pass


class DataPoints(Resource):
    time: List[float]
    value: List[float]
    timeseries_id: str

    def __len__(self):
        return len(self.time)

    def plot(self, **kwargs): # pragma: no cover
        """
        Plot the dataapoints.

        Parameters
        ----------
        kwargs
            See pandas.DataFrame.plot for options.
        """
        self.to_pandas().plot(**kwargs)
        plt.show()

    def to_pandas(self) -> pd.DataFrame:
        """
        Convert the instance into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.

        See Also
        --------
        See keyword arguments on pydantic.BaseModel.dict()
        """
        return pd.DataFrame(dict(value=self.value), index=self.time)

    def to_qats_ts(self) -> QatsTimeSeries:
        ts = self.client.timeseries.get_by_id(self.timeseries_id)
        sensor = self.client.sensor.get_by_id(ts.sensor_id)
        test_name = self.client.test.get_by_id(ts.test_id).description
        return QatsTimeSeries(name=f'{test_name} - {sensor.name}', x=np.array(self.value), t=np.array(self.time),
                              kind=sensor.kind, unit=sensor.unit)


class DataPointsList(Resources[DataPoints]):

    def plot(self, **kwargs): # pragma: no cover
        """
        Plot data points.

        Parameters
        ----------
        kwargs
            See pandas.DataFrame.plot for options
        """
        self.to_pandas().plot(**kwargs)
        plt.show()

    def to_pandas(self):
        """
        Convert the data points list into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.
        """
        dfs = [dps.to_pandas() for dps in self]
        conc = pd.concat(dfs, axis="columns")
        conc.columns = [i.timeseries_id for i in self]
        return conc


class TimeSeries(Resource):
    id: Optional[str]
    sensor_id: str
    test_id: str
    fs: float
    datapoints_created_at: Optional[str]
    intermittent: Optional[bool] = False
    default_start_time: Optional[float]
    default_end_time: Optional[float]
    read_only: Optional[bool] = False

    def add_data(self, time: list, values: list) -> DataPoints:
        """
        Add data points.

        Parameters
        ----------
        time : list
            Time in seconds
        values : list
            Data corresponding to time


        Returns
        -------
        DataPoints
            Data points
        """
        dps = self.client.timeseries.add_data_points(self.id, time, values)
        return dps

    def sensor(self):
        return self.client.sensor.get_by_id(self.sensor_id)

    def get_data(self, start: float = None, end: float = None, scaling_length: float = None,
                 all_data: bool = False) -> DataPoints:
        """
        Get data points

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).

        Returns
        -------
        DataPoints
            Data points
        """
        dps = self.client.timeseries.get_data_points(self.id, start=start, end=end, scaling_length=scaling_length,
                                                     all_data=all_data)
        return dps

    def plot(self, start: float = None, end: float = None, scaling_length: float = None, **kwargs):  # pragma: no cover
        """
        Plot time series

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).
        kwargs
            See optional arguments for pandas.DataFrame.plot.
        """
        dps = self.get_data(start=start, end=end, scaling_length=scaling_length)
        dps.plot(**kwargs)

    def get_qats_ts(self, start: float = None, end: float = None, scaling_length: float = None,
                    all_data: bool = False) -> QatsTimeSeries:
        """
        Get Qats timeseries

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).
        all_data: bool = False
            Flag to fetch all available data or use default start-end values
        Returns
        -------
        QatsTimeSeries
            Qats TimeSeries object
        """
        dp = self.get_data(start=start, end=end, scaling_length=scaling_length, all_data=all_data)
        sensor = self.client.sensor.get_by_id(self.sensor_id)
        test_name = self.client.test.get_by_id(self.test_id).description
        return QatsTimeSeries(name=f'{test_name} - {sensor.name}', x=np.array(dp.value), t=np.array(dp.time),
                              kind=sensor.kind, unit=sensor.unit)


class TimeSeriesList(Resources[TimeSeries]):
    def get_data(self, start: float = None, end: float = None, scaling_length: float = None) -> DataPointsList:
        """
        Get data points

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).

        Returns
        -------
        DataPoints
            Data points
        """
        dps = DataPointsList([ts.get_data(start=start, end=end, scaling_length=scaling_length) for ts in self])
        return dps

    def get_qats_tsdb(self, start: float = None, end: float = None, scaling_length: float = None,
                      all_data: bool = False) -> QatsTsDB:
        """
        Get Qats timeseries database

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).
        all_data: bool = False
            Flag to fetch all available data or use default start-end values
        Returns
        -------
        QatsTsDB
            Qats TsDB object
        """
        db = QatsTsDB()
        for i in self:
            db.add(i.get_qats_ts())
        return db


    def plot(self, start: float = None, end: float = None, scaling_length: float = None, **kwargs):   # pragma: no cover
        """
        Plot time series

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).
        kwargs
            See optional arguments for pandas.DataFrame.plot.
        """
        dps = self.get_data(start=start, end=end, scaling_length=scaling_length)
        dps.plot(**kwargs)


class Sensor(Resource):
    id: Optional[str]
    campaign_id: str
    name: str
    description: str
    unit: str
    kind: str
    source: str
    x: float
    y: float
    z: Optional[float] = None
    position_reference: str
    position_heading_lock: bool
    position_draft_lock: bool
    positive_direction_definition: str
    area: Optional[float]
    read_only: Optional[bool]

    def tags(self) -> Tags:
        """Retrieve tags on sensor."""
        return self.client.tag.get_by_sensor_id(self.id)

    def timeseries(self) -> TimeSeriesList:
        """Retrieve time series on sensor."""
        return self.client.timeseries.get_by_sensor_id(self.id)


class Sensors(Resources[Sensor]):
    def print_full(self):    # pragma: no cover
        for i in self:
            print(f'{i.to_pandas()}\n')

    def print_small(self):    # pragma: no cover
        for i in self:
            print(f"{i.to_pandas().loc[['name', 'id', 'campaign_id', 'description']]}\n")

    def print_list(self):    # pragma: no cover
        print(f'id\tkind\tunit\tdescription')
        for i in self:
            print(f'{i.id}\t{i.kind}\t{i.unit}\t{i.description}')


class Test(Resource):
    id: Optional[str]
    number: str
    description: str
    test_date: datetime
    campaign_id: str
    type: str

    __test__ = False

    def delete(self, secret_key: str):
        """
        Delete it.

        Parameters
        ----------
        secret_key : str
            Secret key to allow deletion of read only items
        """
        self.client.test.delete(self.id, secret_key=secret_key)

    def tags(self) -> Tags:
        """Retrieve tags on time serie."""
        return self.client.tag.get_by_test_id(self.id)

    def timeseries(self, sensor_id: str = None) -> Union[TimeSeriesList, TimeSeries]:
        """
        Retrieve time series on sensor.

        Parameters
        ----------
        sensor_id : str, optional
            Retrieve the time series for the specified sensor

        Returns
        -------
        TimeSeriesList
            Time series
        """
        if sensor_id is not None:
            return self.client.timeseries.get_by_sensor_id_and_test_id(sensor_id=sensor_id, test_id=self.id)
        else:
            return self.client.timeseries.get_by_test_id(test_id=self.id)


class FloaterTest(Test):
    type: Literal["Floater Test"] = 'Floater Test'
    category: str
    orientation: float
    floaterconfig_id: str
    wave_id: Optional[str]
    wind_id: Optional[str]
    read_only: Optional[bool] = False


class WaveCalibrationTest(Test):
    type: Literal["Wave Calibration"] = "Wave Calibration"
    wave_spectrum: Optional[str]
    wave_height: Optional[float]
    wave_period: Optional[float]
    gamma: Optional[float]
    wave_direction: Optional[float]
    current_velocity: Optional[float]
    current_direction: Optional[float]
    read_only: Optional[bool] = False


class WindCalibrationTest(Test):
    type: Literal["Wind Calibration"] = "Wind Calibration"
    wind_spectrum: Optional[str]
    wind_velocity: Optional[float]
    zref: Optional[float]
    wind_direction: Optional[float]
    read_only: Optional[bool] = False


class Tests(Resources[Union[Test, FloaterTest, WaveCalibrationTest, WindCalibrationTest]]):
    __test__ = False

    def print_full(self):    # pragma: no cover
        for i in self:
            print(f'{i.to_pandas()}\n')

    def print_small(self):    # pragma: no cover
        for i in self:
            print(f"{i.to_pandas().loc[['id', 'campaign_id', 'description', 'type']]}\n")

    def print_list(self):    # pragma: no cover
        print(f'id\tnumber\ttype\tdescription')
        for i in self:
            print(f'{i.id}\t{i.number}\t{i.type}\t{i.description}')


class Campaign(Resource):
    name: str
    description: str
    location: str
    date: datetime
    scale_factor: float
    water_depth: float
    read_only: Optional[bool] = False

    def sensors(self) -> Sensors:
        """Fetch sensors."""
        return self.client.sensor.get_by_campaign_id(self.id)

    def tests(self, test_type: str = None) -> Tests:
        """Fetch tests."""
        return self.client.test.get_by_campaign_id(self.id, test_type=test_type)

    def floater_configurations(self) -> FloaterConfigurations:
        """Fetch floater configurations."""
        return self.client.floaterconfig.get_by_campaign_id(self.id)

    def floater_tests(self) -> Tests:
        """Fetch floater tests."""
        return self.client.test.get_by_campaign_id(self.id, test_type='Floater Test')


class Campaigns(Resources[Campaign]):
    pass
