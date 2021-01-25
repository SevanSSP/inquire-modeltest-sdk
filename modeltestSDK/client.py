import urllib.parse
import requests
import logging
from datetime import datetime
from requests.auth import AuthBase
from .api import (TimeseriesAPI, CampaignAPI, SensorAPI, TestAPI, FloaterTestAPI, WindCalibrationAPI,
                  WaveCalibrationAPI, TagsAPI, FloaterConfigAPI)
from .query import Query
from .config import Config
from .exceptions import ClientException


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


class Client:
    """
    Main entrypoint into modeltest-db SDK.

    Parameters
    ----------
    config : object, optional
        Client configuration (host, base URL)
    """
    def __init__(self, config=Config):
        """Initilize objects for interacting with the API"""
        self.config = config
        self.filter = Query(method_spec='filter')
        self.sort = Query(method_spec='sort')
        self.campaign = CampaignAPI(client=self)
        self.timeseries = TimeseriesAPI(client=self)
        self.sensor = SensorAPI(client=self)
        self.test = TestAPI(client=self)
        self.floater_test = FloaterTestAPI(client=self)
        self.wind_calibration = WindCalibrationAPI(client=self)
        self.wave_calibration = WaveCalibrationAPI(client=self)
        self.tag = TagsAPI(client=self)
        self.floater_config = FloaterConfigAPI(client=self)

    def do_request(self, method, resource: str, endpoint: str = "", parameters: dict = None, enc_parameters: str = None,
                   body: dict = None):
        """
        Carry out request.
        Parameters
        ----------
        method : {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}
            Request method.
        resource : str
            API resource e.g. 'plant/timeseries'
            version : str
                 API version e.g. 'v1.3'
               endpoint : str
                   API resource endpoint e.g.
               parameters : dict, optional
                   Request parameters.
               body : dict, optional
                   Request body.
               Returns
               -------
               dict
                   Request response
               Notes
               -----
               The full request url is like
                   'https://{host}/{base_url}/{resource}/{endpoint}?firstparameter=value&anotherparameter=value
                   :param enc_parameters:
                   :param body:
                   :param parameters:
                   :param resource:
                   :param method:
                   :param endpoint:
               """
        if not isinstance(endpoint, str):
            endpoint = str(endpoint)

        url = self.config.host + "/"
        url = url + "/".join([p for p in [self.config.base_url, self.config.version, resource, endpoint] if p.strip()])
        if enc_parameters is None:
            if parameters is not None and isinstance(parameters, dict):
                # parameters = to_camel_case({k: v for k, v in parameters.items() if v is not None})
                enc_parameters = urllib.parse.urlencode(parameters, quote_via=urllib.parse.quote)
            else:
                enc_parameters = ""

        query_url = f"{url}/?{enc_parameters}"

        response = None
        try:
            response = method(query_url, json=body)
            response.raise_for_status()
        except Exception as inst:
            ClientException(exception=inst, response=response)
        else:
            return response.json()

    def get(self, resource: str, endpoint: str = "", parameters: dict = None, enc_parameters: str = None):
        """
        Method to retrieve resource from db
        :param enc_parameters:
        :param resource:
        :param endpoint:
        :param parameters:
        :return:
        """
        return self.do_request(requests.get, resource, endpoint, parameters=parameters, enc_parameters=enc_parameters)

    def post(self, resource: str, endpoint: str = "", body: dict = None):
        """
        Method to create resource in db
        :param resource:
        :param endpoint:
        :param body:
        :return:
        """
        return self.do_request(requests.post, resource, endpoint, body=body)

    def patch(self, resource: str, endpoint: str = "", body: dict = None):
        """
        Method to update resource in db
        :param resource:
        :param endpoint:
        :param body:
        :return:
        """
        return self.do_request(requests.patch, resource, endpoint, body=body)

    def delete(self, resource: str, endpoint: str, parameters: str = None):
        """
        Method for deleting a resource from db
        WARNING: Not working in a intuitive way
        :param parameters: Query string for admin-delete
        :param resource:
        :param endpoint:
        :return:
        """
        return self.do_request(requests.delete, resource=resource, endpoint=endpoint, parameters=parameters)
