from modeltestsdk.resources import (
    Campaign, Campaigns
)
from modeltestsdk.query import create_query_parameters
from pydantic import TypeAdapter
from .base import BaseAPI
from typing import List


class CampaignAPI(BaseAPI):
    def create(self, name: str, description: str, location: str, date: str, scale_factor: float, water_depth: float,
               admin_key: str, read_only: bool = False, ) -> Campaign:
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
        admin_key : str
            admin key required to create a Campaign in MTDB
        read_only : bool, optional
            Make the campaign read only.



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
        data = self.client.post(self._resource_path, parameters=dict(administrator_key=admin_key), body=body)
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

        return Campaigns(TypeAdapter(List[Campaign]).validate_python([dict(**i, client=self.client) for i in data]))

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

    def get_by_name(self, name: str, limit=100, skip=0) -> Campaigns:
        """
        Get single campaign by name

        Parameters
        ----------
        name : str
            Campaign name
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        Campaigns
            Campaigns data
        """
        return self.get(filter_by=[self.client.filter.campaign.name == name],
                        limit=limit, skip=skip)
