"""
Resource models
"""
import pandas as pd
import matplotlib.pyplot as plt
from pydantic import BaseModel
from pydantic.typing import Literal
from typing import List, Optional, Union


class Resource(BaseModel):
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
        return pd.DataFrame(self.dict(**kwargs))


class Resources(BaseModel):
    __root__: List[Resource]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item: int):
        return self.__root__[item]

    def __len__(self):
        return len(self.__root__)

    def append(self, item: Resource):
        self.__root__.append(item)

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
        return pd.DataFrame([_.dict(**kwargs) for _ in self.__root__])


class FloaterConfiguration(Resource):
    id: Optional[str]
    name: str
    description: str
    campaign_id: str
    characteristic_length: float
    draft: float
    _client: None


class FloaterConfigurations(Resources):
    __root__ = List[FloaterConfiguration]

    def append(self, item: FloaterConfiguration):
        self.__root__.append(item)


class Statistics(Resource):
    min: float
    max: float
    std: float
    mean: float
    m0: float
    m1: float
    m2: float
    m4: float
    _client: None


class Tag(Resource):
    id: Optional[str]
    name: str
    comment: Optional[str]
    test_id: Optional[str]
    sensor_id: Optional[str]
    timeseries_id: Optional[str]
    _client: None

    def create(self):
        """Add it to the database."""
        tag = self._client.tag.create(**self.dict())
        self.id = tag.id  # update with id from database

    def delete(self, admin_key: str):
        """
        Delete it.

        Parameters
        ----------
        admin_key : str
            Administrator secret key
        """
        self._client.tag.delete(self.id, admin_key=admin_key)


class Tags(Resources):
    __root__: List[Tag]

    def append(self, item: Tag):
        self.__root__.append(item)


class DataPoints(Resource):
    time: List[float]
    value: List[float]
    _client: None

    def plot(self, **kwargs):
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


class DataPointsList(Resources):
    __root__: List[DataPoints]

    def append(self, item: DataPoints):
        self.__root__.append(item)

    def plot(self, **kwargs):
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
        dfs = [dps.to_pandas() for dps in self.__root__]
        return pd.concat(dfs, axis="columns")


class TimeSerie(Resource):
    id: Optional[str]
    sensor_id: str
    test_id: str
    fs: float
    datapoints_created_at: str
    intermittent: Optional[bool] = False
    default_start_time: Optional[float]
    default_end_time: Optional[float]
    read_only: Optional[bool] = False
    _client: None

    def create(self):
        """Add it to the database."""
        ts = self._client.timeseries.create(**self.dict())
        self.id = ts.id  # update with id from database

    def delete(self, admin_key: str):
        """
        Delete it.

        Parameters
        ----------
        admin_key : str
            Administrator secret key
        """
        self._client.timeseries.delete(self.id, admin_key=admin_key)

    def add_data(self, time: list, value: list, admin_key: str) -> DataPoints:
        """
        Add data points.

        Parameters
        ----------
        time : list
            Time in seconds
        value : list
            Data corresponding to time
        admin_key : str
            Administrator secret key

        Returns
        -------
        DataPoints
            Data points
        """
        dps = self._client.timeseries.add_data_points(self.id, time, value, admin_key)
        return dps

    def get_data(self, start: float = None, end: float = None, scaling_length: float = None) -> DataPoints:
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
        dps = self._client.timeseries.get_data_points(self.id, start=start, end=end, scaling_length=scaling_length)
        return dps

    def plot(self, start: float = None, end: float = None, scaling_length: float = None, **kwargs):
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


class TimeSeries(Resources):
    __root__: List[TimeSerie]

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
        dps = DataPointsList.parse_obj(
            [ts.get_data(start=start, end=end, scaling_length=scaling_length) for ts in self.__root__]
        )

        return dps

    def plot(self, start: float = None, end: float = None, scaling_length: float = None, **kwargs):
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

    def to_pandas(self) -> pd.DataFrame:
        """
        Convert the data points list into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.
        """
        dfs = [ts.to_pandas() for ts in self.__root__]
        return pd.concat(dfs, axis="columns")


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
    z: float
    position_reference: str
    position_heading_lock: bool
    position_draft_lock: bool
    positive_direction_definition: str
    area: Optional[float]
    read_only: Optional[bool]
    _client: None

    def create(self):
        """Add it to the database."""
        sensor = self._client.sensor.create(**self.dict())
        self.id = sensor.id     # update with id from database

    def delete(self, admin_key: str):
        """
        Delete it.

        Parameters
        ----------
        admin_key : str
            Administrator secret key
        """
        self._client.sensor.delete(self.id, admin_key=admin_key)

    def tags(self) -> Tags:
        """Retrieve tags on sensor."""
        return self._client.tag.get_by_sensor_id(self.id)

    def timeseries(self) -> TimeSeries:
        """Retrieve time series on sensor."""
        return self._client.timeseries.get_by_sensor_id(self.id)


class Sensors(Resources):
    __root__: List[Sensor]

    def append(self, item: Sensor):
        self.__root__.append(item)


class Test(Resource):
    id: Optional[str]
    number: str
    description: str
    test_date: str
    campaign_id: str
    type: str
    _client: None

    def delete(self, admin_key: str):
        """
        Delete it.

        Parameters
        ----------
        admin_key : str
            Administrator secret key
        """
        self._client.test.delete(self.id, admin_key=admin_key)

    def tags(self) -> Tags:
        """Retrieve tags on time serie."""
        return self._client.tag.get_by_test_id(self.id)

    def timeseries(self) -> TimeSeries:
        """Retrieve time series on sensor."""
        return self._client.timeseries.get_by_test_id(self.id)


class FloaterTest(Test):
    type: Literal["Floater Test"]
    category: str
    orientation: float
    floater_config_id: str
    wave_id: Optional[str]
    wind_id: Optional[str]
    read_only: Optional[bool] = False

    def create(self):
        """Add it to the database."""
        sensor = self._client.floater_test.create(**self.dict())
        self.id = sensor.id  # update with id from database


class WaveCalibrationTest(Test):
    type: Literal["Wave Calibration"]
    wave_spectrum: Optional[str]
    wave_height: Optional[float]
    wave_period: Optional[float]
    gamma: Optional[float]
    wave_direction: Optional[float]
    current_velocity: Optional[float]
    current_direction: Optional[float]
    read_only: Optional[bool] = False

    def create(self):
        """Add it to the database."""
        sensor = self._client.wave_calibration.create(**self.dict())
        self.id = sensor.id  # update with id from database


class WindCalibrationTest(Test):
    type: Literal["Wind Calibration"]
    wind_spectrum: Optional[str]
    wind_velocity: Optional[float]
    zref: Optional[float]
    wind_direction: Optional[float]
    read_only: Optional[bool] = False

    def create(self):
        """Add it to the database."""
        sensor = self._client.wind_calibration.create(**self.dict())
        self.id = sensor.id  # update with id from database


class Tests(Resources):
    __root__: List[Union[Test, FloaterTest, WaveCalibrationTest, WindCalibrationTest]]

    def append(self, item: Union[Test, FloaterTest, WaveCalibrationTest, WindCalibrationTest]):
        self.__root__.append(item)


class Campaign(Resource):
    id: Optional[str]
    name: str
    description: str
    location: str
    date: str
    scale_factor: float
    water_depth: float
    _client: None

    def create(self):
        """Create this campaign."""
        campaign = self._client.campaign.create(**self.dict())
        self.id = campaign.id  # update with id from database

    def delete(self, admin_key: str):
        """
        Delete it.

        Parameters
        ----------
        admin_key : str
            Administrator secret key
        """
        self._client.campaign.delete(self.id, admin_key=admin_key)

    def sensors(self) -> Sensors:
        """Fetch sensors."""
        return self._client.sensor.get_by_campaign_id(self.id)

    def tests(self, test_type: str = None) -> Tests:
        """Fetch tests."""
        return self._client.test.get_by_campaign_id(self.id)

    def floater_configurations(self) -> FloaterConfigurations:
        """Fetch floater configurations."""
        return self._client.floater_config.get_by_campaign_id(self.id)


class Campaigns(Resources):
    __root__: List[Campaign]
