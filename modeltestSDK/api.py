"""
API methods
"""
import logging
from typing import Union
from .utils import format_class_name
from .resources import (
    Campaign, Campaigns, Test, Tests, Sensor, Sensors, TimeSeries, TimeSeriesList, DataPoints, FloaterTest,
    WaveCalibrationTest, WindCalibrationTest, Tag, Tags, FloaterConfiguration, FloaterConfigurations, Statistics
)
from .query import create_query_parameters


class BaseAPI:
    """Base API with methods common for all APIs."""

    def __init__(self, client):
        self._resource_path: str = format_class_name(self.__class__.__name__)
        self.client = client

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

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> Campaigns:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

        Returns
        -------
        Campaigns
            Multiple campaigns
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))
        return Campaigns.parse_obj([dict(**item, client=self.client) for item in data])

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

        if len(campaigns) == 0:
            logging.info(f"Did not find a campaign with name='{name}'.")
            return None
        elif len(campaigns) > 1:
            logging.warning(f"Found multiple campaigns with name='{name}'. Returning the first match.")
            return campaigns[0]
        else:
            return campaigns[0]


class TestAPI(BaseAPI):
    def get(self, filter_by: list = None, sort_by: list = None) -> Tests:
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
        Tests
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return Tests.parse_obj([dict(**item, client=self.client) for item in data])

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

        if len(tests) == 0:
            logging.info(f"Did not find a test with number='{test_number}'.")
            return None
        elif len(tests) > 1:
            logging.warning(f"Found multiple tests with number='{test_number}'. Returning the first match.")
            return tests[0]
        else:
            return tests[0]

    def get_by_campaign_id(self, campaign_id: str) -> Tests:
        """"
        Get tests by parent campaign

        Parameters
        ----------
        campaign_id : str
            Campaign identifier

        Returns
        -------
        Sensors
            Multiple sensors
        """
        tests = self.get(filter_by=[self.client.filter.test.campaign_id == campaign_id])
        return tests


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

    def get(self, filter_by: list = None, sort_by: list = None) -> Tests:
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
        Tests
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return Tests.parse_obj([dict(**item, client=self.client) for item in data])

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

        if len(tests) == 0:
            logging.info(f"Did not find a floater test with name='{test_number}'.")
            return None
        elif len(tests) > 1:
            logging.warning(f"Found multiple floater tests with name='{test_number}'. Returning the first match.")
            return tests[0]
        else:
            return tests[0]


class WaveCalibrationAPI(TestAPI):
    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wave_spectrum: str, wave_height: float, wave_period: float, gamma: float,
               wave_direction: float, current_velocity: float, current_direction: float,
               read_only: bool = False) -> WaveCalibrationTest:
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
        WaveCalibrationTest
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
        return WaveCalibrationTest(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> Tests:
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
        Tests
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return Tests.parse_obj([dict(**item, client=self.client) for item in data])

    def get_by_id(self, test_id: str) -> WaveCalibrationTest:
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
        return WaveCalibrationTest(**data, client=self.client)

    def get_by_number(self, test_number: str) -> Union[WaveCalibrationTest, None]:
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

        if len(tests) == 0:
            logging.info(f"Did not find a wave calibration test with name='{test_number}'.")
            return None
        elif len(tests) > 1:
            logging.warning(f"Found multiple wave calibration tests with name='{test_number}'. "
                            f"Returning the first match.")
            return tests[0]
        else:
            return tests[0]


class WindCalibrationAPI(TestAPI):
    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wind_spectrum: str, wind_velocity: float, zref: float, wind_direction: float,
               read_only: bool = False) -> WindCalibrationTest:
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
        WindCalibrationTest
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
        return WindCalibrationTest(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> Tests:
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
        Tests
            Multiple tests
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return Tests.parse_obj([dict(**item, client=self.client) for item in data])

    def get_by_id(self, test_id: str) -> WindCalibrationTest:
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
        return WindCalibrationTest(**data, client=self.client)

    def get_by_number(self, test_number: str) -> Union[WindCalibrationTest, None]:
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

        if len(tests) == 0:
            logging.info(f"Did not find a wind calibration test with name='{test_number}'.")
            return None
        elif len(tests) > 1:
            logging.warning(f"Found multiple wind calibration tests with name='{test_number}'. "
                            f"Returning the first match.")
            return tests[0]
        else:
            return tests[0]


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

    def get(self, filter_by: list = None, sort_by: list = None) -> Sensors:
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
        Sensors
            Multiple sensors
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return Sensors.parse_obj([dict(**item, client=self.client) for item in data])

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
        sensors = self.get(filter_by=[self.client.filter.sensor.name == name])

        if len(sensors) == 0:
            logging.info(f"Did not find a sensor with name='{name}'.")
            return None
        elif len(sensors) > 1:
            logging.warning(f"Found multiple sensors with name='{name}'. Returning the first match.")
            return sensors[0]
        else:
            return sensors[0]

    def get_by_campaign_id(self, campaign_id: str) -> Sensors:
        """"
        Get sensors by parent campaign

        Parameters
        ----------
        campaign_id : str
            Campaign identifier

        Returns
        -------
        Sensors
            Multiple sensors
        """
        sensors = self.get(filter_by=[self.client.filter.sensor.campaign_id == campaign_id])
        return sensors


class TimeseriesAPI(BaseAPI):
    def create(self, sensor_id: str, test_id: str, default_start_time: float, default_end_time: float, fs: float,
               intermittent: bool = False, read_only: bool = False) -> TimeSeries:
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
        return TimeSeries(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> TimeSeriesList:
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
        TimeSeriesList
            Multiple time series
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return TimeSeriesList.parse_obj([dict(**item, client=self.client) for item in data])

    def get_by_id(self, timeseries_id: str) -> TimeSeries:
        """
        Get single time series by id

        Parameters
        ----------
        timeseries_id : str
            Time series identifier

        Returns
        -------
        TimeSeries
            Time series
        """
        data = self.client.get(self._resource_path, timeseries_id)
        return TimeSeries(**data, client=self.client)

    def get_by_sensor_id(self, sensor_id: str) -> TimeSeriesList:
        """"
        Get time series by sensor id

        Parameters
        ----------
        sensor_id : str
            Sensor id

        Returns
        -------
        TimeSeriesList
            Time series
        """
        timeseries = self.get(filter_by=[self.client.filter.timeseries.sensor_id == sensor_id])
        return timeseries

    def get_by_test_id(self, test_id: str) -> TimeSeriesList:
        """"
        Get time series by test id

        Parameters
        ----------
        test_id : str
            Test id

        Returns
        -------
        TimeSeriesList
            Time series
        """
        timeseries = self.get(filter_by=[self.client.filter.timeseries.test_id == test_id])
        return timeseries

    def get_by_sensor_id_and_test_id(self, sensor_id: str, test_id: str) -> TimeSeries:
        """"
        Get single time serie by sensor id and test id

        Parameters
        ----------
        sensor_id : str
            Sensor identifier
        test_id : str
            Test identifier

        Returns
        -------
        TimeSeries
            Time series
        """
        timeseries = self.get(
            filter_by=[
                self.client.filter.timeseries.sensor_id == sensor_id,
                self.client.filter.timeseries.test_id == test_id
            ]
        )
        return timeseries[0]

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
        return DataPoints(**data.get("data"), client=self.client)

    def add_data_points(self, ts_id: str, time: list, values: list, admin_key: str) -> DataPoints:
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
        admin_key : str
            Administrator secret key

        Returns
        -------
        DataPoints
            Data points
        """
        body = dict(data=dict(time=time, value=values))
        data = self.client.post(resource=self._resource_path, endpoint=f"{ts_id}/data", body=body,
                                parameters=dict(secret_key=admin_key))
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

    def get(self, filter_by: list = None, sort_by: list = None) -> Tags:
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
        Tags
            Multiple tags
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return Tags.parse_obj([dict(**item, client=self.client) for item in data])

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

    def get_by_sensor_id(self, sensor_id: str) -> Tags:
        """"
        Get tags by sensor id

        Parameters
        ----------
        sensor_id : str
            Sensor id

        Returns
        -------
        Tags
            Sensor tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.sensor_id == sensor_id])
        return tags

    def get_by_test_id(self, test_id: str) -> Tags:
        """"
        Get tags by test id

        Parameters
        ----------
        test_id : str
            Test id

        Returns
        -------
        Tags
            Test tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.test_id == test_id])
        return tags

    def get_by_timeseries_id(self, ts_id: str) -> Tags:
        """"
        Get tags by time series id

        Parameters
        ----------
        ts_id : str
            Time series id

        Returns
        -------
        Tags
            Time series tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.timeseries_id == ts_id])
        return tags

    def get_by_name(self, name: str) -> Tags:
        """"
        Get tags by name

        Parameters
        ----------
        name : str
            Tag name

        Returns
        -------
        Tags
            Tags
        """
        tags = self.get(filter_by=[self.client.filter.tags.name == name])
        return tags


class FloaterConfigAPI(BaseAPI):
    def create(self, name: str, description: str, campaign_id: str, draft: float, characteristic_length: float,
               read_only: bool = False) -> FloaterConfiguration:
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
        FloaterConfiguration
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
        return FloaterConfiguration(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None) -> FloaterConfigurations:
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
        FloaterConfigurations
            Multiple floater configurations
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=params)
        return FloaterConfigurations.parse_obj([dict(**item, client=self.client) for item in data])

    def get_by_id(self, config_id: str) -> FloaterConfiguration:
        """
        Get single floater configuration by id

        Parameters
        ----------
        config_id : str
            Configuration identifier

        Returns
        -------
        FloaterConfiguration
            Floater configuration
        """
        data = self.client.get(self._resource_path, config_id)
        return FloaterConfiguration(**data, client=self.client)

    def get_by_campaign_id(self, campaign_id: str) -> FloaterConfigurations:
        """"
        Get configuration by parent campaign

        Parameters
        ----------
        campaign_id : str
            Campaign identifier

        Returns
        -------
        FloaterConfigurations
            Floater configurations
        """
        configs = self.get(filter_by=[self.client.filter.campaign.id == campaign_id, ])
        return configs
