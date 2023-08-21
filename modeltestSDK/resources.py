"""
Resource models
"""
from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pydantic import BaseModel
from typing import List, Optional, Union, Any, Literal, TypeVar
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
        else:
            return None

    def create(self, admin_key=None):
        try:
            if admin_key is None:
                resource = self._api_object().create(
                    **make_serializable(self.dict(exclude={"client", 'id', 'datapoints_created_at', 'type'})))
            else:
                resource = self._api_object().create(
                    **make_serializable(self.dict(exclude={"client", 'id', 'datapoints_created_at', 'type'})),
                    admin_key=admin_key)
            self.id = resource.id
        except AttributeError as e:
            if self.client is None:
                raise AttributeError('No client provided, unable to create object')
            else:
                raise e  # pragma: no cover

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


ResourceType = TypeVar('ResourceType', bound=Resource)


class Resources(List[ResourceType]):
    def __init__(self, items: List[ResourceType] = None) -> None:
        if items:
            self._check_types(items)
            super().__init__(items)

    def filter(self, inplace: bool = False, **kwargs) -> Union[None, Resources]:
        """
        Filter resources based on keyword arguments.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments used for filtering.
        inplace : bool
            Flag to indicate if list should be filtered in-place or return new list


        Returns
        -------
            Filtered resources.
        """
        filtered_resources = [resource for resource in self if
                              all(getattr(resource, attr) == value for attr, value in kwargs.items())]
        if inplace:
            self.clear()
            self.extend(filtered_resources)
        else:
            return type(self)(filtered_resources)

    def _expected_types(self):
        return self.__orig_bases__[0].__args__[0].__args__ \
            if isinstance(self.__orig_bases__[0].__args__[0], typing._UnionGenericAlias) \
            else [self.__orig_bases__[0].__args__[0]]

    def _check_types(self, items: List[Resource]) -> None:
        for item in items:
            if not any(type(item).__name__ == t.__name__ for t in self._expected_types()):
                raise TypeError(f"Invalid type {type(item)} in {self.__class__.__name__}")

    def append(self, item: ResourceType, admin_key: str = None) -> None:
        if not any(type(item).__name__ == t.__name__ for t in self._expected_types()):
            raise TypeError(f"Invalid type {type(item)} in {self.__class__.__name__}")
        if item.id or item.__class__.__name__ == 'DataPoints':
            super().append(item)
        else:
            item.create(admin_key=admin_key)
            super().append(item)

    def get_by_id(self, id) -> Union[ResourceType, None]:
        for i in self:
            if i.id == id:
                return i
        return None

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


class FloaterConfig(Resource):
    id: Optional[str]
    name: str
    description: str
    campaign_id: str
    characteristic_length: float
    draft: float


class FloaterConfigs(Resources[FloaterConfig]):
    pass


class Statistics(BaseModel):
    min: float
    max: float
    std: float
    mean: float
    m0: float
    m1: float
    m2: float
    m4: float
    tp: float


class Tag(Resource):
    id: Optional[str]
    name: str
    comment: Optional[str]
    test_id: Optional[str]
    sensor_id: Optional[str]
    timeseries_id: Optional[str]

    @property
    def sensor(self) -> Union[Sensor, None]:
        if self.client and self.sensor_id:
            return self.client.sensor.get_by_id(self.sensor_id)
        else:
            return None

    @property
    def test(self) -> Union[FloaterTest, WindCalibration, WaveCalibration, None]:
        if self.client and self.test_id:
            test = self.client.test.get_by_id(self.test_id)
            print(test)
            if test.type == 'Floater Test':
                return self.client.floatertest.get_by_id(self.test_id)
            elif test.type == 'Wave Calibration':
                return self.client.wavecalibration.get_by_id(self.test_id)
            elif test.type == 'Wind Calibration':
                return self.client.windcalibration.get_by_id(self.test_id)
            else:
                raise ValueError('Unknown test type')
        else:
            return None

    @property
    def timeseries(self) -> Union[TimeSeries, None]:
        if self.client and self.timeseries_id:
            return self.client.timeseries.get_by_id(self.timeseries_id)
        else:
            return None


class Tags(Resources[Tag]):
    pass


class DataPoints(Resource):
    time: List[float]
    value: List[float]
    timeseries_id: str

    def __len__(self):
        return len(self.time)

    @property
    def timeseries(self):
        if self.client:
            return self.client.timeseries.get_by_id(self.timeseries_id)
        else:
            return None

    def plot(self, show: bool = True, **kwargs):
        """
        Plot the datapoints.

        Parameters
        ----------
        show : bool, default True
            Whether to show the plot
        kwargs
            See pandas.DataFrame.plot for options.
        """
        # Set the x-axis label to "Time [s]" if not specified in the additional arguments
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = 'Time [s]'

        # set the y-axis label based on the kind and unit if not specified in the additional arguments
        if 'ylabel' not in kwargs:
            try:
                kwargs['ylabel'] = f'{self.timeseries.sensor.kind.capitalize()} [{self.timeseries.sensor.unit}]'
            except AttributeError:
                pass

        self.to_pandas().plot(**kwargs)
        if show:
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
        try:
            sensor = self.timeseries.sensor
            test = self.timeseries.test
        except AttributeError:
            columns = None
        else:
            columns = [f'{test.number} - {sensor.name}']
        return pd.DataFrame(data=self.value, index=self.time, columns=columns)

    def to_qats_ts(self) -> QatsTimeSeries:
        try:
            sensor = self.timeseries.sensor
            test = self.timeseries.test
        except AttributeError:
            name = 'unknown'
            kind = None
            unit = None
        else:
            name = f'{test.number} - {sensor.name}'
            kind = sensor.kind
            unit = sensor.unit
        return QatsTimeSeries(name=name, x=np.array(self.value), t=np.array(self.time),
                              kind=kind, unit=unit)


class DataPointsList(Resources[DataPoints]):

    def plot(self, show: bool = True, **kwargs):  # pragma: no cover
        """
        Plot data points.

        Parameters
        ----------
        show : bool, default True
            Whether to show the plot
        kwargs
            See pandas.DataFrame.plot for options
        """

        # Set the x-axis label to "Time [s]" if not specified in the additional arguments
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = 'Time [s]'

        # set the y-axis label based on the kind and unit of the first data point if not specified in the additional
        # arguments and all sensor have the same kind and unit
        if 'ylabel' not in kwargs:
            try:
                first_kind = self[0].timeseries.sensor.kind
                first_unit = self[0].timeseries.sensor.unit
                equal = True
                for element in self[1:]:
                    if element.timeseries.sensor.kind != first_kind or element.timeseries.sensor.unit != first_unit:
                        equal = False
                        break

                if equal:
                    kwargs['ylabel'] = f'{first_kind.capitalize()} [{first_unit}]'
            except AttributeError:
                pass

        self.to_pandas().plot(**kwargs)
        if show:
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

    def add_data(self, time: list, values: list, secret_key: str = None) -> DataPoints:
        """
        Add data points.

        Parameters
        ----------
        time : list
            Time in seconds
        values : list
            Data corresponding to time
        secret_key : str, optional
            Secret key, required to add new data points if old should be overwritten


        Returns
        -------
        DataPoints
            Data points
        """
        dps = self.client.timeseries.add_data_points(self.id, time, values, secret_key)
        return dps

    @property
    def sensor(self):
        if self.client:
            return self.client.sensor.get_by_id(self.sensor_id)
        else:
            return None

    @property
    def test(self):
        if self.client:
            return self.client.test.get_by_id(self.test_id)
        else:
            return None

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
        all_data : bool, optional
            Flag to fetch all available data or use default start-end values. Overrides start and end.
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).

        Returns
        -------
        DataPoints
            Data points
        """
        self.check_tags_for_warnings()
        dps = self.client.timeseries.get_data_points(self.id, start=start, end=end, scaling_length=scaling_length,
                                                     all_data=all_data)
        return dps

    def plot(self, start: float = None, end: float = None, all_data: bool = False,
             scaling_length: float = None, show: bool = True, **kwargs):  # pragma: no cover
        """
        Plot time series

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        all_data : bool, optional
            Flag to fetch all available data or use default start-end values. Overrides start and end.
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).
        show: bool = True, optional
            Flag to show the plot
        kwargs
            See optional arguments for pandas.DataFrame.plot.
        """
        dps = self.get_data(start=start, end=end, all_data=all_data, scaling_length=scaling_length)

        # Set the x-axis label to "Time [s]" if not specified in the additional arguments
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = 'Time [s]'

        # set the y-axis label based on the kind and unit if not specified in the additional arguments
        if 'ylabel' not in kwargs:
            kwargs['ylabel'] = f'{self.sensor.kind.capitalize()} [{self.sensor.unit}]'

        dps.plot(show=show, **kwargs)

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
        sensor = self.sensor
        test = self.test
        return QatsTimeSeries(name=f'{test.number} - {sensor.name}', x=np.array(dp.value), t=np.array(dp.time),
                              kind=sensor.kind, unit=sensor.unit)

    def tags(self, limit: int = 100, skip: int = 0) -> Tags:
        return self.client.tag.get_by_timeseries_id(self.id, limit=limit, skip=skip)

    def check_tags_for_warnings(self) -> int:
        warning_tag_names = ['quality: bad', 'quality: questionable', 'failed']
        n_warnings = 0
        for tag in self.tags():
            if tag.name in warning_tag_names:
                n_warnings += 1
                print('## WARNING ')
                print(f'## Timeseries {self.id} is tagged {tag.name}. Use data cautiously ##')
                print('                   ###')

        return n_warnings

    def get_statistics(self, scaling_length=None) -> Statistics:
        return self.client.timeseries.get_statistics(ts_id=self.id, scaling_length=scaling_length)


class TimeSeriesList(Resources[TimeSeries]):
    def get_data(self, start: float = None, end: float = None, all_data: bool = False,
                 scaling_length: float = None) -> DataPointsList:
        """
        Get data points

        Parameters
        ----------
        start : float, optional
            Fetch data points after this time (s).
        end : float, optional
            Fetch data points before this time (s).
        all_data: bool = False, optional
            Flag to fetch all available data or use default start-end values. Overrides start and end.
        scaling_length : float, optional
            Scale the data to this reference length according to Froude law (m).

        Returns
        -------
        DataPointList
            Data points
        """
        dps = DataPointsList(
            [ts.get_data(start=start, end=end, all_data=all_data, scaling_length=scaling_length) for ts in self])
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
            db.add(i.get_qats_ts(start=start, end=end, scaling_length=scaling_length, all_data=all_data))
        return db

    def plot(self, start: float = None, end: float = None, scaling_length: float = None,
             all_data: bool = False, show: bool = True, **kwargs):  # pragma: no cover
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
        all_data: bool = False, optional
            Flag to fetch all available data or use default start-end values. true overrides start and end
        show: bool = True, optional
            Flag to show the plot
        kwargs
            See optional arguments for pandas.DataFrame.plot.
        """
        dps = self.get_data(start=start, end=end, scaling_length=scaling_length, all_data=all_data)

        # Set the x-axis label to "Time [s]" if not specified in the additional arguments
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = 'Time [s]'

        # set the y-axis label based on the kind and unit of the first data point if not specified in the additional
        # arguments and all sensor have the same kind and unit
        if 'ylabel' not in kwargs:
            try:
                first_kind = dps[0].timeseries.sensor.kind
                first_unit = dps[0].timeseries.sensor.unit
                equal = True
                for element in dps[1:]:
                    if element.timeseries.sensor.kind != first_kind or element.timeseries.sensor.unit != first_unit:
                        equal = False
                        break

                if equal:
                    kwargs['ylabel'] = f'{first_kind.capitalize()} [{first_unit}]'
            except AttributeError:
                pass

        dps.plot(show=show, **kwargs)


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

    def tags(self, limit: int = 100, skip: int = 100) -> Tags:
        """Retrieve tags on sensor."""
        return self.client.tag.get_by_sensor_id(self.id, limit=limit, skip=skip)

    def timeseries(self, limit: int = 100, skip: int = 100) -> TimeSeriesList:
        """Retrieve time series on sensor."""
        return self.client.timeseries.get_by_sensor_id(self.id, limit=limit, skip=skip)


class Sensors(Resources[Sensor]):
    def print_full(self):  # pragma: no cover
        for i in self:
            print(f'{i.to_pandas()}\n')

    def print_small(self):  # pragma: no cover
        for i in self:
            print(f"{i.to_pandas().loc[['name', 'id', 'campaign_id', 'description']]}\n")

    def print_list(self):  # pragma: no cover
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

    def delete(self, secret_key: str = None):
        """
        Delete it.

        Parameters
        ----------
        secret_key : str
            Secret key to allow deletion of read only items
        """
        self.client.test.delete(self.id, secret_key=secret_key)

    def tags(self, limit: int = 100, skip: int = 100) -> Tags:
        """Retrieve tags on time serie."""
        return self.client.tag.get_by_test_id(self.id, limit=limit, skip=skip)

    def timeseries(self, sensor_id: str = None, limit: int = 100, skip: int = 0) -> Union[TimeSeriesList, TimeSeries]:
        """
        Retrieve time series on sensor.

        Parameters
        ----------
        sensor_id : str, optional
            Retrieve the time series for the specified sensor
        limit : int, optional
            Maximum number of time series to return, default 100
        skip : int, optional
            Number of time series to skip, default 0

        Returns
        -------
        TimeSeriesList
            Time series
        """
        if self.client:
            if sensor_id is not None:
                return self.client.timeseries.get_by_sensor_id_and_test_id(sensor_id=sensor_id, test_id=self.id)
            else:
                return self.client.timeseries.get_by_test_id(test_id=self.id, limit=limit, skip=skip)
        else:
            return None


class FloaterTest(Test):
    type: Literal["Floater Test"] = 'Floater Test'
    category: str
    orientation: float
    floaterconfig_id: str
    wave_id: Optional[str]
    wind_id: Optional[str]
    read_only: Optional[bool] = False

    @property
    def wave_calibration(self):
        if self.client and self.wave_id:
            return self.client.wavecalibration.get_by_id(self.wave_id)
        else:
            return None

    @property
    def wind_calibration(self):
        if self.client and self.wind_id:
            return self.client.wind_calibration.get_by_id(self.wind_id)
        else:
            return None

    @property
    def floater_config(self):
        if self.client:
            return self.client.floater_config.get_by_id(self.floaterconfig_id)
        else:
            return None


class WaveCalibration(Test):
    type: Literal["Wave Calibration"] = "Wave Calibration"
    wave_spectrum: Optional[str]
    wave_height: Optional[float]
    wave_period: Optional[float]
    gamma: Optional[float]
    wave_direction: Optional[float]
    current_velocity: Optional[float]
    current_direction: Optional[float]
    read_only: Optional[bool] = False

    def floater_tests(self, limit: int = 100, skip: int = 0):
        return self.client.floater_test.get(
            filter_by=[self.client.filter.floater_test.wave_calibration_id == self.id],
            limit=limit, skip=skip)


class WindCalibration(Test):
    type: Literal["Wind Calibration"] = "Wind Calibration"
    wind_spectrum: Optional[str]
    wind_velocity: Optional[float]
    zref: Optional[float]
    wind_direction: Optional[float]
    read_only: Optional[bool] = False

    def floater_tests(self, limit: int = 100, skip: int = 0):
        return self.client.floater_test.get(
            filter_by=[self.client.filter.floater_test.wind_calibration_id == self.id],
            limit=limit, skip=skip)


class Tests(Resources[Union[Test, FloaterTest, WaveCalibration, WindCalibration]]):
    __test__ = False

    def print_full(self):  # pragma: no cover
        for i in self:
            print(f'{i.to_pandas()}\n')

    def print_small(self):  # pragma: no cover
        for i in self:
            print(f"{i.to_pandas().loc[['id', 'campaign_id', 'description', 'type']]}\n")

    def print_list(self):  # pragma: no cover
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

    def sensors(self, limit: int = 100, skip: int = 0) -> Sensors:
        """Fetch sensors."""
        return self.client.sensor.get_by_campaign_id(self.id, limit=limit, skip=skip)

    def tests(self, limit: int = 100, skip: int = 0) -> Tests:
        """Fetch tests."""
        return self.client.test.get_by_campaign_id(self.id, limit=limit, skip=skip)

    def floater_configurations(self, limit: int = 100, skip: int = 0) -> FloaterConfigs:
        """Fetch floater configurations."""
        return self.client.floaterconfig.get_by_campaign_id(self.id, limit=limit, skip=skip)


class Campaigns(Resources[Campaign]):
    pass
