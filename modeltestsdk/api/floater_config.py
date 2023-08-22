from modeltestsdk.resources import (
    FloaterConfig, FloaterConfigs
)
from modeltestsdk.query import create_query_parameters
from pydantic import parse_obj_as
from .base import BaseAPI


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

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None,
            limit: int = None) -> FloaterConfigs:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

        Returns
        -------
        FloaterConfigs
            Multiple floater configurations
        """
        if filter_by is None:
            filter_by = list()
        if sort_by is None:
            sort_by = list()
        params = create_query_parameters(filter_expressions=filter_by, sorting_expressions=sort_by)
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))

        return FloaterConfigs([parse_obj_as(FloaterConfig, dict(**i, client=self.client)) for i in data])

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

    def get_by_campaign_id(self, campaign_id: str, limit=100, skip=0) -> FloaterConfigs:
        """
        Get configuration by parent campaign

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
        FloaterConfigs
            Floater configurations
        """
        configs = self.get(filter_by=[self.client.filter.campaign.id == campaign_id],
                           limit=limit, skip=skip)
        return configs
