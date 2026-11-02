from pathlib import Path
from urllib.parse import quote
from modeltestsdk.resources import (
    Campaign, Campaigns, CampaignDocument
)
from modeltestsdk.query import create_query_parameters
from pydantic import TypeAdapter
from .base import BaseAPI, upsert_body
from typing import List, Union


class CampaignAPI(BaseAPI):
    def create(self, name: str, description: str, location: str, date: str, scale_factor: float, water_depth: float,
               read_only: bool = False, **fields) -> Campaign:
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
            Make the campaign read only.
        **fields
            Further fields of the API's schema (see the API documentation)

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
            read_only=read_only,
            **fields
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

    def documents(self, campaign_id: str) -> List[CampaignDocument]:
        """
        The campaign's documents (reports, test programmes, drawings), by class.

        Parameters
        ----------
        campaign_id : str
            Campaign identifier

        Returns
        -------
        list of CampaignDocument
            The documents; download one with download_document
        """
        data = self.client.get(self._resource_path, f"{campaign_id}/documents")
        return [CampaignDocument(**i) for i in data]

    def download_document(self, campaign_id: str, path: str, destination: Union[str, Path] = ".") -> Path:
        """
        Download a campaign document.

        Parameters
        ----------
        campaign_id : str
            Campaign identifier
        path : str
            The document's path, as in documents()
        destination : str or Path, optional
            Folder to save it in (under its own name), or a file path. Default: the current folder.

        Returns
        -------
        Path
            The file written
        """
        destination = Path(destination)
        if destination.is_dir():
            destination = destination / Path(path).name
        self.client.download(self._resource_path, f"{campaign_id}/documents/{quote(path)}", destination,
                             parameters=dict(download=True))
        return destination

    def upsert(self, item) -> Campaign:
        """
        Create or update a campaign by name (import pipeline).

        Parameters
        ----------
        item : dict or Campaign
            Campaign fields: name, description, date, location, scale_factor, water_depth, and optionally
            main_characteristic_length, data_format, source_workbook, notes, read_only and the coordinate
            definitions (lab_axis_x/y/z, lq, north, z_origin, ...). Fields not given are left as they are.

        Returns
        -------
        Campaign
            The stored campaign; upsert_status is 'created', 'updated' or 'unchanged'

        Notes
        -----
        Creating a campaign requires the Admin role, updating one requires write access to it.
        """
        return self._upserted(self.client.put(self._resource_path, body=upsert_body(item)), Campaign)
