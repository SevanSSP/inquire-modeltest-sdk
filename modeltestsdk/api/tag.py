from modeltestsdk.resources import (
    Tag, Tags
)
from modeltestsdk.query import create_query_parameters
from pydantic import parse_obj_as
from .base import BaseAPI


class TagsAPI(BaseAPI):
    def create(self, name: str, comment: str = None, test_id: str = None, sensor_id: str = None,
               timeseries_id: str = None, read_only: bool = False) -> Tag:
        """
        Tag a test, a sensor or a time series.

        Parameters
        ----------
        name : str
            Tag name, allowable types:
            for sensor tag: "comment", "surge", "sway", "heave", "roll", "pitch", "yaw", "quality: bad",
                            "quality: questionable", "coord. system: Sevan - Global",
                            "coord. system: Sevan - Local - globally oriented", "coord. system: Sevan - Local",
                            "reference signal"
            for test tag: "comment", "failed" and "repeated"
            for timeseries tag: "comment", "quality: bad" and "quality: questionable"
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

    def get(self, filter_by: list = None, sort_by: list = None, skip: int = None, limit: int = None) -> Tags:
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
        skip : int, optional
            Skip the first `skip` campaigns.
        limit : int, optional
            Do not return more than `limit` hits.

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
        data = self.client.get(self._resource_path, parameters=dict(**params, skip=skip, limit=limit))
        return Tags([parse_obj_as(Tag, dict(**i, client=self.client)) for i in data])

    def get_by_id(self, tag_id: str) -> Tag:
        """
        Get single tag series by id

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

    def get_by_sensor_id(self, sensor_id: str, limit=100, skip=0) -> Tags:
        """
        Get tags by sensor id

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
        Tags
            Sensor tags
        """
        tags = self.get(filter_by=[self.client.filter.tag.sensor_id == sensor_id],
                        limit=limit, skip=skip)
        return tags

    def get_by_test_id(self, test_id: str, limit=100, skip=0) -> Tags:
        """
        Get tags by test id

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
        Tags
            Test tags
        """
        tags = self.get(filter_by=[self.client.filter.tag.test_id == test_id],
                        limit=limit, skip=skip)
        return tags

    def get_by_timeseries_id(self, ts_id: str, limit=100, skip=0) -> Tags:
        """
        Get tags by time series id

        Parameters
        ----------
        ts_id : str
            Time series id
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        Tags
            Time series tags
        """
        tags = self.get(filter_by=[self.client.filter.tag.timeseries_id == ts_id],
                        limit=limit, skip=skip)
        return tags

    def get_by_name(self, name: str, limit=100, skip=0) -> Tags:
        """
        Get tags by name

        Parameters
        ----------
        name : str
            Tag name
        limit : int, optional
            Limit the number of results, default is 100
        skip : int, optional
            Skip the first `skip` results, default is 0

        Returns
        -------
        Tags
            Tags
        """
        tags = self.get(filter_by=[self.client.filter.tag.name == name],
                        limit=limit, skip=skip)
        return tags