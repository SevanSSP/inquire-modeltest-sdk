import numpy as np
from typing import Optional
from qats import TimeSeries as QatsTimeseries
from qats import TsDB as QatsTsDB
from .base import Resource, Resources
from .statistics import Statistics
from .tag import Tags
from .datapoint import DataPoints, DataPointsList


class Timeseries(Resource):
    id: Optional[str]
    sensor_id: str
    test_id: str
    fs: float
    datapoints_created_at: Optional[str]
    intermittent: Optional[bool] = False
    default_start_time: Optional[float]
    default_end_time: Optional[float]

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
             scaling_length: float = None, show: bool = True, **kwargs):
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
                    all_data: bool = False) -> QatsTimeseries:
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
        QatsTimeseries
            Qats Timeseries object
        """
        dp = self.get_data(start=start, end=end, scaling_length=scaling_length, all_data=all_data)
        sensor = self.sensor
        test = self.test
        return QatsTimeseries(name=f'{test.number} - {sensor.name}', x=np.array(dp.value), t=np.array(dp.time),
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


class TimeseriesList(Resources[Timeseries]):
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
             all_data: bool = False, show: bool = True, **kwargs):
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
