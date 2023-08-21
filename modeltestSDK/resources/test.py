from typing import Optional, Union, Literal
from datetime import datetime
from .base import Resource, Resources
from .tag import Tags
from .timeseries import TimeSeries, TimeSeriesList


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
