from modeltestSDK.resources import (
    Sensor, Sensors
)
from modeltestSDK.query import create_query_parameters
from pydantic import parse_obj_as
from .base import BaseAPI


class SensorAPI(BaseAPI):
    def create(self, name: str, description: str, unit: str, kind: str, source: str, x: float, y: float, z: float,
               position_reference: str, position_heading_lock: bool, position_draft_lock: bool,
               positive_direction_definition: str, campaign_id: str, area: float = None,
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
            Kind of sensor: "length", "velocity", "acceleration", "force", "pressure", "volume", "mass", "moment",
            "angle", "angular velocity", "angular acceleration", "slamming force", "slamming pressure", "control signal"
        source : str
            Data source. 'Direct measurement', 'Basin derived', 'Sevan derived' or 'external derived'
        x : float
            Position x-coordinate
        y : float
            Position y-coordinate
        z : float
            Position z-coordinate
        position_reference : str
            position reference, "local" or "global"
        position_heading_lock : bool
            Is the position locked to floater heading
        position_draft_lock: bool
            Is the position locked to floater draft
        positive_direction_definition : str
            Definition of positive directio
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
            unit=unit,
            kind=kind,
            source=source,
            area=area,
            x=x,
            y=y,
            z=z,
            position_reference=position_reference,
            position_heading_lock=position_heading_lock,
            position_draft_lock=position_draft_lock,
            positive_direction_definition=positive_direction_definition,
            campaign_id=campaign_id,
            read_only=read_only
        )
        data = self.client.post(self._resource_path, body=body)
        return Sensor(**data, client=self.client)

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> Sensors:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

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
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))
        return Sensors([parse_obj_as(Sensor, dict(**i, client=self.client)) for i in data])

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

    def get_by_name(self, name: str, limit=100, skip=0) -> Sensors:
        """
        Get sensors by name

        Parameters
        ----------
        name : str
            Sensor name
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        Sensor
            Sensor data
        """
        return self.get(filter_by=[self.client.filter.sensor.name == name],
                        limit=limit, skip=skip)

    def get_by_campaign_id(self, campaign_id: str, limit=100, skip=0) -> Sensors:
        """
        Get sensors by parent campaign

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
        Sensors
            Multiple sensors
        """
        return self.get(filter_by=[self.client.filter.sensor.campaign_id == campaign_id],
                        limit=limit, skip=skip)
