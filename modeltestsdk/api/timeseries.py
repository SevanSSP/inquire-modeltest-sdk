from typing import Union, List
from modeltestsdk.resources import (
    Statistics, DataPoints, Timeseries, TimeseriesList
)
from modeltestsdk.query import create_query_parameters
from pydantic import TypeAdapter
from .base import BaseAPI


class TimeseriesAPI(BaseAPI):
    def create(self, sensor_id: str, test_id: str, default_start_time: float, default_end_time: float, fs: float,
               intermittent: bool = False, read_only: bool = False) -> Timeseries:
        """
        Create time series

        Parameters
        ----------
        sensor_id : str
            Identifier of parent sensor
        test_id : str
            Identifier of parent test
        default_start_time : float
            Default start time used when computing statistics etc.
        default_end_time : float
            Default end time used when computing statistics etc.
        fs : float
            Sampling rate
        intermittent : bool, optional
            Is the time series intermittent
        read_only : bool, optional
            Make the time series read only

        Returns
        -------
        Timeseries'
            Timeseries data

        """
        body = dict(
            sensor_id=sensor_id,
            test_id=test_id,
            default_start_time=default_start_time,
            default_end_time=default_end_time,
            fs=fs,
            intermittent=intermittent,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return Timeseries(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> TimeseriesList:
        """
        Get multiple time series

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

        Returns
        -------
        TimeseriesList
            Multiple time series
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))

        return TimeseriesList(TypeAdapter(List[Timeseries]).validate_python([dict(**i, client=self.client) for i in data]))

    def get_by_id(self, timeseries_id: str) -> Timeseries:
        """
        Get single time series by id

        Parameters
        ----------
        timeseries_id : str
            Time series identifier

        Returns
        -------
        Timeseries
            Time series
        """
        data = self.client.get(self._resource_path, timeseries_id)
        return Timeseries(**data, client=self.client)

    def get_by_sensor_id(self, sensor_id: str, limit=100, skip=0) -> TimeseriesList:
        """
        Get time series by sensor id

        Parameters
        ----------
        sensor_id : str
            Sensor id
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        TimeseriesList
            Time series
        """
        timeseries = self.get(filter_by=[self.client.filter.timeseries.sensor_id == sensor_id],
                              limit=limit, skip=skip)
        return timeseries

    def get_by_test_id(self, test_id: str, limit=100, skip=0) -> TimeseriesList:
        """
        Get time series by test id

        Parameters
        ----------
        test_id : str
            Test id
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        TimeseriesList
            Time series
        """
        return self.get(filter_by=[self.client.filter.timeseries.test_id == test_id],
                        limit=limit, skip=skip)

    def get_by_sensor_id_and_test_id(self, sensor_id: str, test_id: str) -> Union[Timeseries, None]:
        """"
        Get single time series by sensor id and test id

        Parameters
        ----------
        sensor_id : str
            Sensor identifier
        test_id : str
            Test identifier

        Returns
        -------
        Timeseries
            Time series
        """
        ts = self.get(
            filter_by=[
                self.client.filter.timeseries.sensor_id == sensor_id,
                self.client.filter.timeseries.test_id == test_id
            ]
        )
        if len(ts) == 1:
            return ts[0]
        else:
            return None

    def get_data_points(self, ts_id: str, start: float = None, end: float = None, scaling_length: float = None,
                        all_data: bool = False, cache: bool = True) -> DataPoints:
        """
        Fetch data points for time series by id.

        Parameters
        ----------
        ts_id : str
            Time series identifier
        start : float, optional
            Fetch data point after this start time (s).
        end : float, optional
            Fetch data point before this end time (s)
        scaling_length : float, optional
            Scale data points to the specified scaling length according to Froude law from the original
            reference length.
        all_data : bool, optional
            Fetch all data points including the transients which are masked by default.
        cache : bool, optional
            Cache data points for 30 days

        Returns
        -------
        DataPoints
            Data points
        """
        parameters = dict(start_time=start, end_time=end, scaling_length=scaling_length, all_data=all_data)
        data = self.client.get(resource=self._resource_path, endpoint=f"{ts_id}/data", parameters=parameters,
                               cache=cache)
        data['data']['timeseries_id'] = ts_id
        return DataPoints(**data.get("data"), client=self.client)

    def add_data_points(self, ts_id: str, time: list, values: list, secret_key: str = None) -> DataPoints:
        """
        Add data points to timeseries

        Parameters
        ----------
        ts_id : str
            Time series identifier
        time : list
            Time (s)
        values : list
            Values corresponding to time
        secret_key : str, optional
            Secret key, required to add new data points if old should be overwritten

        Returns
        -------
        DataPoints
            Data points
        """
        body = dict(data=dict(time=time, value=values))
        data = self.client.post(resource=self._resource_path, parameters=dict(secret_key=secret_key),
                                endpoint=f"{ts_id}/data", body=body)
        return DataPoints(**data.get("data"), timeseries_id=ts_id, client=self.client)

    def get_statistics(self, ts_id: str, scaling_length: float = None) -> Statistics:
        """
        Fetch time series statistics.

        Parameters
        ----------
        ts_id : str
            Time series identifier
        scaling_length : float, optional
            Scale data points to the specified scaling length according to Froude law from the original
            reference length.

        Returns
        -------
        DataPoints
            Data points
        """
        parameters = dict(scaling_length=scaling_length)
        data = self.client.get(resource=self._resource_path, endpoint=f"{ts_id}/statistics", parameters=parameters)
        return Statistics(**data)
