"""
API methods
"""
import logging
import warnings
from typing import Union
from .utils import format_class_name
from .resources import (
    Campaign, CampaignList, Test, TestList, Sensor, SensorList, Timeseries, TimeseriesList, DataPoints,
    FloaterTest, FloaterTestList, WaveCalibration, WaveCalibrationList, WindCalibration, WindCalibrationList, Tag,
    TagList, FloaterConfig, FloaterConfigList, Statistics
)
from .query import create_query_parameters
from .client import Client


class BaseAPI:
    """Base API with methods common for all APIs."""
    def __init__(self, client: Client):
        self._resource_path: str = format_class_name(self.__class__.__name__)
        self.client: Client = client

    def delete(self, item_id: str, admin_key: str):
        """
        Delete item by id

        Parameters
        ----------
        item_id : str
            Item identifier
        admin_key : str
            Administrator key

        Notes
        -----
        Deleting items requires administrator privileges.

        """
        resp = self.client.delete(self._resource_path, endpoint=item_id, parameters=dict(secret_key=admin_key))
        return resp


class CampaignAPI(BaseAPI):
    def create(self, name: str, description: str, location: str, date: str, scale_factor: float, water_depth: float,
               read_only: bool = False) -> Campaign:
        """
        Create a campaign

        Parameters
        ----------
        name : str
            Campaign name
        description : str
            A description
        location : str
            Location for the campaign
        date : str
            Date time string
        scale_factor : float
            Model scale
        water_depth : float
            Water depth (m)
        read_only : bool, optional
            Make the this campaign read only.

        Returns
        -------
        Campaign
            Campaign data
        """
        body = dict(
            name=name,
            description=description,
            location=location,
            date=date,
            scale_factor=scale_factor,
            water_depth=water_depth,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return Campaign(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> CampaignList:
        """
        Get multiple campaigns

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all campaigns e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        CampaignList
            Multiple campaigns
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        campaigns = [Campaign(**item, client=self.client) for item in data]
        return CampaignList(resources=campaigns, client=self.client)

    def get_by_id(self, campaign_id: str) -> Campaign:
        """
        Get single campaign by id

        Parameters
        ----------
        campaign_id : str
            Campaign identifier

        Returns
        -------
        Campaign
            Campaign data
        """
        data = self.client.get(self._resource_path, campaign_id)
        return Campaign(**data, client=self.client)

    def get_by_name(self, name: str) -> Union[Campaign, None]:
        """"
        Get single campaign by name

        Parameters
        ----------
        name : str
            Campaign name

        Returns
        -------
        Campaign
            Campaign data
        """
        campaigns = self.get(filter_by=[self.client.filter.campaign.name == name])

        if len(campaigns.resources) == 0:
            logging.info(f"Did not find a campaign with name='{name}'.")
            return None
        elif len(campaigns.resources) > 1:
            logging.warning(f"Found multiple campaigns with name='{name}'. Returning the first match.")
            return campaigns.resources[0]
        else:
            return campaigns.resources[0]


class TestAPI(BaseAPI):
    def get(self, filter_by: list = None, sort_by: list = None) -> TestList:
        """
        Get multiple tests

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        TestList
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        tests = [Test(**item, client=self.client) for item in data]
        return TestList(resources=tests, client=self.client)

    def get_by_id(self, test_id: str) -> Test:
        """
        Get single campaign by id

        Parameters
        ----------
        test_id : str
            Campaign identifier

        Returns
        -------
        Test
            Test data
        """
        data = self.client.get(self._resource_path, test_id)
        return Test(**data, client=self.client)

    def get_by_number(self, test_number: str) -> Union[Test, None]:
        """"
        Get single test by number

        Parameters
        ----------
        test_number : str
            Test number

        Returns
        -------
        Test
            Test data
        """
        tests = self.get(filter_by=[self.client.filter.test.number == test_number])

        if len(tests.resources) == 0:
            logging.info(f"Did not find a test with number='{test_number}'.")
            return None
        elif len(tests.resources) > 1:
            logging.warning(f"Found multiple tests with number='{test_number}'. Returning the first match.")
            return tests.resources[0]
        else:
            return tests.resources[0]


class FloaterTestAPI(TestAPI):

    def create(self, number: str, description: str, test_date: str, campaign_id: str, category: str, orientation: float,
               floater_config_id: str = None, wave_id: str = None, wind_id: str = None,
               read_only: bool = False) -> FloaterTest:
        """
        Create floater test

        Parameters
        ----------
        number : str
            Test number
        description : str
            A description of the test
        test_date : str
            Date of testing
        campaign_id : str
            Identifier of parent campaign
        category : str
            The kind of test
        orientation : float
            Orientation (degrees)
        floater_config_id : id
            Identifier of the applied floater configuration
        wave_id : str
            Identifier of the applied wave
        wind_id : str
            Identifier of the applied wind
        read_only : bool, optional
            Make the test read only

        Returns
        -------
        FloaterTest
            Test data
        """
        body = dict(
            number=number,
            description=description,
            type="Floater Test",
            test_date=test_date,
            campaign_id=campaign_id,
            category=category,
            orientation=orientation,
            wave_id=wave_id,
            wind_id=wind_id,
            floaterconfig_id=floater_config_id,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return FloaterTest(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> FloaterTestList:
        """
        Get multiple floater tests

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        FloaterTestList
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        tests = [FloaterTest(**item, client=self.client) for item in data]
        return FloaterTestList(resources=tests, client=self.client)

    def get_by_id(self, test_id: str) -> FloaterTest:
        """
        Get single floater test by id

        Parameters
        ----------
        test_id : str
            Test identifier

        Returns
        -------
        Test
            Test data
        """
        data = self.client.get(self._resource_path, test_id)
        return FloaterTest(**data, client=self.client)

    def get_by_number(self, test_number: str) -> Union[FloaterTest, None]:
        """"
        Get single floater test by number

        Parameters
        ----------
        test_number : str
            Test number

        Returns
        -------
        Test
            Test data
        """
        tests = self.get(filter_by=[self.client.filter.floater_test.number == test_number])

        if len(tests.resources) == 0:
            logging.info(f"Did not find a floater test with name='{test_number}'.")
            return None
        elif len(tests.resources) > 1:
            logging.warning(f"Found multiple floater tests with name='{test_number}'. Returning the first match.")
            return tests.resources[0]
        else:
            return tests.resources[0]


class WaveCalibrationAPI(TestAPI):
    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wave_spectrum: str, wave_height: float, wave_period: float, gamma: float,
               wave_direction: float, current_velocity: float, current_direction: float,
               read_only: bool = False) -> WaveCalibration:
        """
        Create wave calibration test

        Parameters
        ----------
        number : str
            Test number
        description : str
            A description
        test_date : str
            Date of testing
        campaign_id : str
            Identifier of parent campaign
        wave_spectrum : str
            Wave spectrum type
        wave_height : float
            Wave height (m)
        wave_period : float
            Wave period (s)
        gamma : float
            Wave spectrum peak enhancement factor (-)
        wave_direction : float
            Wave direction (degrees)
        current_velocity : float
            Current velocity (m/s)
        current_direction : float
            Current direction (degrees)
        read_only : bool, optional
            Make the test read only

        Returns
        -------
        WaveCalibration
            Test data
        """
        body = dict(
            number=number,
            description=description,
            type="Wave Calibration",
            test_date=test_date,
            campaign_id=campaign_id,
            wave_spectrum=wave_spectrum,
            wave_period=wave_period,
            wave_height=wave_height,
            gamma=gamma,
            wave_direction=wave_direction,
            current_velocity=current_velocity,
            current_direction=current_direction,
            read_only=read_only
        )

        data = self.client.post(self._resource_path, body=body)
        return WaveCalibration(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> WaveCalibrationList:
        """
        Get multiple wave calibration tests

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        WaveCalibrationList
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        tests = [WaveCalibration(**item, client=self.client) for item in data]
        return WaveCalibrationList(resources=tests, client=self.client)

    def get_by_id(self, test_id: str) -> WaveCalibration:
        """
        Get single wave calibration test by id

        Parameters
        ----------
        test_id : str
            Test identifier

        Returns
        -------
        Test
            Test data
        """
        data = self.client.get(self._resource_path, test_id)
        return WaveCalibration(**data, client=self.client)

    def get_by_number(self, test_number: str) -> Union[WaveCalibration, None]:
        """"
        Get single wave calibration test by number

        Parameters
        ----------
        test_number : str
            Test number

        Returns
        -------
        Test
            Test data
        """
        tests = self.get(filter_by=[self.client.filter.wave_calibration.number == test_number])

        if len(tests.resources) == 0:
            logging.info(f"Did not find a wave calibration test with name='{test_number}'.")
            return None
        elif len(tests.resources) > 1:
            logging.warning(f"Found multiple wave calibration tests with name='{test_number}'. "
                            f"Returning the first match.")
            return tests.resources[0]
        else:
            return tests.resources[0]


class WindCalibrationAPI(TestAPI):
    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wind_spectrum: str, wind_velocity: float, zref: float, wind_direction: float,
               read_only: bool = False) -> WindCalibration:
        """
        Create wind calibration test

        Parameters
        ----------
        number : str
            Test number
        description : str
            A description
        test_date : str
            Date of testing
        campaign_id : str
            Identifier of parent campaign
        wind_spectrum : str
            Wind spectrum type
        wind_velocity : float
            Wind velocity (m/s)
        zref : float
            Vertical reference heigh (m)
        wind_direction : float
            Wave direction (degrees)
        read_only : bool, optional
            Make the test read only

        Returns
        -------
        WindCalibration
            Wind calibration data
        """
        body = dict(
            number=number,
            description=description,
            test_date=test_date,
            type="Wind Calibration",
            campaign_id=campaign_id,
            wind_spectrum=wind_spectrum,
            wind_velocity=wind_velocity,
            zref=zref,
            wind_direction=wind_direction,
            read_only=read_only
        )

        data = self.client.post(self._resource_path, body=body)
        return WindCalibration(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> WindCalibrationList:
        """
        Get multiple wind calibration tests

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        WindCalibrationList
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        tests = [WindCalibration(**item, client=self.client) for item in data]
        return WindCalibrationList(resources=tests, client=self.client)

    def get_by_id(self, test_id: str) -> WindCalibration:
        """
        Get single wind calibration test by id

        Parameters
        ----------
        test_id : str
            Test identifier

        Returns
        -------
        Test
            Test data
        """
        data = self.client.get(self._resource_path, test_id)
        return WindCalibration(**data, client=self.client)

    def get_by_number(self, test_number: str) -> Union[WindCalibration, None]:
        """"
        Get single wind calibration test by number

        Parameters
        ----------
        test_number : str
            Test number

        Returns
        -------
        Test
            Test data
        """
        tests = self.get(filter_by=[self.client.filter.wind_calibration.number == test_number])

        if len(tests.resources) == 0:
            logging.info(f"Did not find a wind calibration test with name='{test_number}'.")
            return None
        elif len(tests.resources) > 1:
            logging.warning(f"Found multiple wind calibration tests with name='{test_number}'. "
                            f"Returning the first match.")
            return tests.resources[0]
        else:
            return tests.resources[0]


class SensorAPI(BaseAPI):

    def create(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
               is_local: bool, campaign_id: str, area: float = None,
               read_only: bool = False) -> Sensor:
        """
        Parameters
        ----------
        name : str
            Sensor name
        description : str
            A description
        unit : str
            Unit of measure
        kind : str
            Kind of sensor
        x : float
            Position x-coordinate
        y : float
            Position y-coordinate
        z : float
            Position z-coordinate
        is_local : bool
            Is the sensor placed in local coordinate system
        campaign_id : str
            Identifier of parent campaign
        area : float, optional
            Reference area
        read_only : bool, optional
            Make the test read only

        Returns
        -------
        Sensor
            Sensor data
        """
        body = dict(
            name=name,
            description=description,
            unit=unit, kind=kind,
            area=area,
            x=x,
            y=y,
            z=z,
            is_local=is_local,
            campaign_id=campaign_id,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return Sensor(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> SensorList:
        """
        Get multiple sensors

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        SensorList
            Multiple sensors
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        sensors = [Sensor(**item, client=self.client) for item in data]
        return SensorList(resources=sensors, client=self.client)

    def get_by_id(self, sensor_id: str) -> Sensor:
        """
        Get single sensor by id

        Parameters
        ----------
        sensor_id : str
            Sensor identifier

        Returns
        -------
        Sensor
            Sensor data
        """
        data = self.client.get(self._resource_path, sensor_id)
        return Sensor(**data, client=self.client)

    def get_by_name(self, name: str) -> Union[Sensor, None]:
        """"
        Get single sensor by name

        Parameters
        ----------
        name : str
            Sensor name

        Returns
        -------
        Sensor
            Sensor data
        """
        campaigns = self.get(filter_by=[self.client.filter.campaign.name == name])

        if len(campaigns.resources) == 0:
            logging.info(f"Did not find a sensor with name='{name}'.")
            return None
        elif len(campaigns.resources) > 1:
            logging.warning(f"Found multiple sensors with name='{name}'. Returning the first match.")
            return campaigns.resources[0]
        else:
            return campaigns.resources[0]


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

    def get(self, filter_by: list = None, sort_by: list = None) -> TimeseriesList:
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
        data = self.client.get(self._resource_path, "", parameters=params)
        timeseries = [Timeseries(**item, client=self.client) for item in data]
        return TimeseriesList(resources=timeseries, client=self.client)

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

    def get_by_sensor_id(self, sensor_id: str) -> Union[TimeseriesList, None]:
        """"
        Get time series by sensor id

        Parameters
        ----------
        sensor_id : str
            Sensor id

        Returns
        -------
        TimeseriesList
            Time series
        """
        timeseries = self.get(filter_by=[self.client.filter.timeseries.sensor_id == sensor_id])

        if len(timeseries.resources) == 0:
            logging.info(f"Did not find any time series with with sensor '{sensor_id}'.")
            return None
        else:
            return timeseries

    def get_by_test_id(self, test_id: str) -> Union[TimeseriesList, None]:
        """"
        Get time series by test id

        Parameters
        ----------
        test_id : str
            Test id

        Returns
        -------
        TimeseriesList
            Time series
        """
        timeseries = self.get(filter_by=[self.client.filter.timeseries.test_id == test_id])

        if len(timeseries.resources) == 0:
            logging.info(f"Did not find any time series with with test '{test_id}'.")
            return None
        else:
            return timeseries

    def get_data_points(self, ts_id: str, start: float = None, end: float = None, scaling_length: float = None) \
            -> DataPoints:
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
            Scale data points to the the specified scaling length according to Froude law from the original
            reference length.

        Returns
        -------
        DataPoints
            Data points
        """
        parameters = dict(start_time=start, end_time=end, scaling_length=scaling_length)
        data = self.client.get(resource=self._resource_path, endpoint=f"{ts_id}/data", parameters=parameters)
        return DataPoints(**data, client=self.client)

    def add_data_points(self, ts_id: str, time: list, values: list) -> DataPoints:
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

        Returns
        -------
        DataPoints
            Data points
        """
        body = dict(data=dict(time=time, value=values))
        data = self.client.post(resource=self._resource_path, endpoint=f"{ts_id}/data", body=body)
        return DataPoints(**data, client=self.client)

    def get_statistics(self, ts_id: str, scaling_length: float = None) -> Statistics:
        """
        Fetch time series statistics.

        Parameters
        ----------
        ts_id : str
            Time series identifier
        scaling_length : float, optional
            Scale data points to the the specified scaling length according to Froude law from the original
            reference length.

        Returns
        -------
        DataPoints
            Data points
        """
        parameters = dict(scaling_length=scaling_length)
        data = self.client.get(resource=self._resource_path, endpoint=f"{ts_id}/statistics", parameters=parameters)
        return Statistics(**data, client=self.client)


class TagsAPI(BaseAPI):
    def create(self, name: str, comment: str = None, test_id: str = None, sensor_id: str = None,
               timeseries_id: str = None, read_only: bool = False) -> Tag:
        """
        Tag a test, a sensor or a time series.

        Parameters
        ----------
        name : str
            Tag name, see API documentation for valid tag names.
        comment : str, optional
            Add a comment.
        test_id : str, optional
            Test identifier
        sensor_id: str, optional
            Sensor identifier
        timeseries_id: str, optional
            Time series identifier
        read_only : bool, optional
            Make the tag read only

        Returns
        -------
        Tag
            Tag information

        """
        assert test_id is not None or sensor_id is not None or timeseries_id is not None, \
            "Specify which test, sensor or time series the tag applies to."

        body = dict(
            name=name,
            comment=comment,
            test_id=test_id,
            sensor_id=sensor_id,
            timeseries_id=timeseries_id,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return Tag(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> TagList:
        """
        Get multiple tags

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        TagList
            Multiple tags
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        tags = [Tag(**item, client=self.client) for item in data]
        return TagList(resources=tags, client=self.client)

    def get_by_id(self, tag_id: str) -> Tag:
        """
        Get single time series by id

        Parameters
        ----------
        tag_id : str
            Tag identifier

        Returns
        -------
        Tag
            Item tag
        """
        data = self.client.get(self._resource_path, tag_id)
        return Tag(**data, client=self.client)

    def get_by_sensor_id(self, sensor_id: str) -> Union[TagList, None]:
        """"
        Get tags by sensor id

        Parameters
        ----------
        sensor_id : str
            Sensor id

        Returns
        -------
        TagList
            Sensor tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.sensor_id == sensor_id])

        if len(tags.resources) == 0:
            logging.info(f"Did not find any tags on sensor '{sensor_id}'.")
            return None
        else:
            return tags

    def get_by_test_id(self, test_id: str) -> Union[TagList, None]:
        """"
        Get tags by test id

        Parameters
        ----------
        test_id : str
            Test id

        Returns
        -------
        TagList
            Test tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.test_id == test_id])

        if len(tags.resources) == 0:
            logging.info(f"Did not find any tags on test '{test_id}'.")
            return None
        else:
            return tags

    def get_by_timeseries_id(self, ts_id: str) -> Union[TagList, None]:
        """"
        Get tags by time series id

        Parameters
        ----------
        ts_id : str
            Time series id

        Returns
        -------
        TagList
            Time series tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.timeseries_id == ts_id])

        if len(tags.resources) == 0:
            logging.info(f"Did not find any tags on time series '{ts_id}'.")
            return None
        else:
            return tags

    def get_by_name(self, name: str) -> Union[TagList, None]:
        """"
        Get tags by name

        Parameters
        ----------
        name : str
            Tag name

        Returns
        -------
        TagList
            Tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.name == name])

        if len(tags.resources) == 0:
            logging.info(f"Did not find any tags with name '{name}'.")
            return None
        else:
            return tags


class FloaterConfigAPI(BaseAPI):
    def create(self, name: str, description: str, campaign_id: str, draft: float, characteristic_length: float,
               read_only: bool = False) -> FloaterConfig:
        """
        Create a floater config

        Parameters
        ----------
        name : str
            Name
        description : str
            A description
        campaign_id : str
            Identifier of parent campaign
        draft : float
            Floater draft (m)
        characteristic_length : float
            Reference length for scaling according to Froude law.
        read_only : float
            Make it read only

        Returns
        -------
        FloaterConfig
            Floater configuration
        """
        body = dict(
            name=name,
            description=description,
            campaign_id=campaign_id,
            characteristic_length=characteristic_length,
            draft=draft,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return FloaterConfig(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> FloaterConfigList:
        """
        Get multiple floater configuration

        Parameters
        ----------
        filter_by : list, optional
            Expressions for selecting a subset of all tests e.g.
                [Client.filter.campaign.name == name,]
        sort_by : list, optional
            Expressions for sorting selection e.g.
                [{'name': height, 'op': asc}]

        Returns
        -------
        FloaterConfigList
            Multiple floater configurations
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        configs = [FloaterConfig(**item, client=self.client) for item in data]
        return FloaterConfigList(resources=configs, client=self.client)

    def get_by_id(self, config_id: str) -> FloaterConfig:
        """
        Get single floater configuration by id

        Parameters
        ----------
        config_id : str
            Configuration identifier

        Returns
        -------
        FloaterConfig
            Floater configuration
        """
        data = self.client.get(self._resource_path, config_id)
        return FloaterConfig(**data, client=self.client)

    def get_by_campaign_id_and_name(self, campaign_id: str, name: str) -> Union[FloaterConfig, None]:
        """"
        Get configuration by name and campaign id

        Parameters
        ----------
        campaign_id : str
            Campaign identifier
        name : str
            Configuration name

        Returns
        -------
        FloaterConfig
            Floater configuration
        """
        configs = self.get(
            filter_by=[self.client.filter.campaign.id == campaign_id, self.client.filter.floater_config.name == name]
        )

        if len(configs.resources) == 0:
            logging.info(f"Did not find any floater configuration with name '{name}' in campaign '{campaign_id}'.")
            return None
        else:
            return configs
