from typing import Union
from modeltestSDK.resources import (
    Test, Tests, FloaterTest, WaveCalibration, WindCalibration,
)
from modeltestSDK.query import create_query_parameters
from pydantic import parse_obj_as
from .base import BaseAPI


class TestAPI(BaseAPI):
    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> Tests:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

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
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))
        data_out = []
        for i in data:
            if i['type'] == 'Wave Calibration':
                data_out.append(self.client.wave_calibration.get_by_id(i['id']))
            elif i['type'] == 'Wind Calibration':
                data_out.append(self.client.wind_calibration.get_by_id(i['id']))
            else:
                data_out.append(self.client.floater_test.get_by_id(i['id']))
        return Tests(data_out)

    def get_by_id(self, test_id: str) -> Union[FloaterTest, WaveCalibration, WindCalibration, Test, None]:
        """
        Get single test by id

        Parameters
        ----------
        test_id : str
            test identifier

        Returns
        -------
        Union[FloaterTest, WaveCalibration, WindCalibration, Test, None]:
            Test data
        """
        return self.get(filter_by=[self.client.filter.test.id == test_id])[0]

    def get_by_number(self, test_number: str, limit=100, skip=0) -> Tests:
        """
        Get tests by number

        Parameters
        ----------
        test_number : str
            Test number
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        Union[FloaterTest, WaveCalibration, WindCalibration, Test, None]
            Test data
        """
        return self.get(filter_by=[self.client.filter.test.number == test_number],
                        limit=limit, skip=skip)

    def get_by_campaign_id(self, campaign_id: str, limit=100, skip=0) -> Tests:
        """
        Get tests by parent campaign

        Parameters
        ----------
        campaign_id : str
            Campaign identifier
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        Tests
            Multiple tests
        """
        return self.get(filter_by=[self.client.filter.test.campaign_id == campaign_id],
                        limit=limit, skip=skip)


class FloaterTestAPI(TestAPI):
    def create(self, number: str, description: str, test_date: str, campaign_id: str, category: str, orientation: float,
               floaterconfig_id: str = None, wave_id: str = None, wind_id: str = None,
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
            The kind of test, "current force", "wind force", "decay", "regular wave", "irregular wave" or "pull out"
        orientation : float
            Orientation (degrees)
        floaterconfig_id : id
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
            type='Floater Test',
            test_date=test_date,
            campaign_id=campaign_id,
            category=category,
            orientation=orientation,
            wave_id=wave_id,
            wind_id=wind_id,
            floaterconfig_id=floaterconfig_id,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return FloaterTest(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> Tests:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

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
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))

        return Tests([parse_obj_as(FloaterTest, dict(**i, client=self.client)) for i in data])

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


class WaveCalibrationAPI(TestAPI):
    def create(self, number: str, description: str, test_date: str, campaign_id: str,
               wave_spectrum: Union[str, None], wave_height: float, wave_period: float, gamma: float,
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
        wave_spectrum : Union[str, None]
            Wave spectrum type, "jonswap", "torsethaugen", "broad band", "regular", None
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

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> Tests:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

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
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))

        return Tests([parse_obj_as(WaveCalibration, dict(**i, client=self.client)) for i in data])

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
            Vertical reference height (m)
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

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> Tests:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

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
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))

        return Tests([parse_obj_as(WindCalibration, dict(**i, client=self.client)) for i in data])

    def get_by_id(self, test_id: str) -> WindCalibration:
        """
        Get single wind calibration test by id

        Parameters
        ----------
        test_id : str
            Test identifier

        Returns
        -------
        WindCalibration
            Test data
        """
        data = self.client.get(self._resource_path, test_id)
        return WindCalibration(**data, client=self.client)
