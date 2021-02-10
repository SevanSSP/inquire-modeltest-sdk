"""
API methods
"""
import logging
import warnings
from typing import Union
from .utils import format_class_name
from .resources import (Campaign, CampaignList, Test, TestList, Sensor, SensorList, Timeseries, TimeseriesList,
                        FloaterTest, FloaterTestList, WaveCalibration, WaveCalibrationList, WindCalibration,
                        WindCalibrationList, Tag, TagList, FloaterConfig, FloaterConfigList)
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
        body = dict(name=name, description=description, unit=unit, kind=kind, area=area, x=x,
                    y=y, z=z, is_local=is_local, campaign_id=campaign_id, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Sensor.from_dict(data=data, client=self.client)

    def get(self, sensor_id: str) -> Sensor:
        data = self.client.get(self._resource_path, sensor_id)
        return Sensor.from_dict(data=data, client=self.client)

    def get_multiple_by_name(self, ids) -> Sensor:
        return self.client.post(self._resource_path, "ids", body=ids)

    def get_by_name(self, name: str):
        response = self.get_all(filter_by=[self.client.filter.sensor.name == name])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {name}")

    def get_all(self, filter_by: list = None, sort_by: list = None) -> SensorList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def patch(self, body: dict, sensor_id: str) -> Sensor:
        data = self.client.patch(self._resource_path, endpoint=f"{sensor_id}", body=body)
        return Sensor.from_dict(data=data, client=self.client)


class TimeseriesAPI(BaseAPI):

    def create(self, sensor_id: str, test_id: str, default_start_time: float, default_end_time: float, fs: float,
               intermittent: bool = False, read_only: bool = False) -> Timeseries:
        body = dict(sensor_id=sensor_id, test_id=test_id, default_start_time=default_start_time,
                    default_end_time=default_end_time, fs=fs, intermittent=intermittent, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Timeseries.from_dict(data=data, client=self.client)

    def get(self, ts_id: str) -> Timeseries:
        data = self.client.get(self._resource_path, ts_id)
        return Timeseries.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list = None, sort_by: list = None) -> TimeseriesList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        obj_list = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=obj_list, client=None)

    def patch(self, body: dict, ts_id: str):
        return self.client.patch(resource=self._resource_path, endpoint=f"{ts_id}", body=body)

    def get_data_points(self, ts_id: str) -> dict:
        data = self.client.get(resource=self._resource_path, endpoint=f"{ts_id}/data")
        return data

    def post_data_points(self, ts_id, body=None, form_body=None):
        if form_body is None:
            form_body = {'data': {'time': [], 'value': []}}
            for p in body:
                form_body['data']['time'].append(p['time'])
                form_body['data']['value'].append(p['value'])
        self.client.post(resource=self._resource_path, endpoint=f"{ts_id}/data", body=form_body)

    def get_standard_deviation(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats")
        return data['std']

    def get_max_value(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats")
        return data['max']

    def get_min_value(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats=min")
        return data['min']

    def get_mean(self, ts_id: str):
        data = self.client.get(self._resource_path, f"{ts_id}/statistics/?stats")
        return data['mean']


class TagsAPI(BaseAPI):
    def create(self, name: str, comment: str = None, test_id: str = None, sensor_id: str = None,
               timeseries_id: str = None, read_only: bool = False) -> Tag:
        body = dict(name=name, comment=comment, test_id=test_id, sensor_id=sensor_id, timeseries_id=timeseries_id,
                    read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return Tag.from_dict(data=data, client=self.client)

    def get(self, tag_id: str) -> Tag:
        data = self.client.get(self._resource_path, tag_id)
        return Tag.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list = None, sort_by: list = None) -> TagList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        obj_list = [Tag.from_dict(data=obj, client=self.client) for obj in data]
        return TagList(resources=obj_list, client=None)

    def get_by_name(self, name: str) -> Tag:
        response = self.get_all(filter_by=[self.client.filter.campaign.name == name])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {name}")


class FloaterConfigAPI(BaseAPI):
    def create(self, name: str, description: str, campaign_id: str, draft: float, characteristic_length: float = 0,
               read_only: bool = False) -> FloaterConfig:
        body = dict(name=name, description=description, campaign_id=campaign_id,
                    characteristic_length=characteristic_length, draft=draft, read_only=read_only)
        data = self.client.post(self._resource_path, body=body)
        return FloaterConfig.from_dict(data=data, client=self.client)

    def get(self, floater_id: str) -> FloaterConfig:
        data = self.client.get(self._resource_path, floater_id)
        return FloaterConfig.from_dict(data=data, client=self.client)

    def get_all(self, filter_by: list = None, sort_by: list = None) -> FloaterConfigList:
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, "", parameters=params)
        obj_list = [FloaterConfig.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterConfigList(resources=obj_list, client=None)

    def get_by_name(self, name: str) -> FloaterConfig:
        response = self.get_all(filter_by=[self.client.filter.campaign.name == name])
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
                return response[0]
            else:
                return response[0]
        else:
            raise Exception(f"Could not find any object with name {name}")
