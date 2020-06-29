import os
import sys
import json
import datetime
import urllib.parse

import requests
from requests.exceptions import HTTPError
from .utils import to_snake_case, to_camel_case
from .api_resources import TimeseriesAPI, CampaignAPI, SensorAPI, TestAPI

from .config import Config


class SDKclient:
    '''
    Main entrypoint into modeltest-db SDK.

    Parameters
    ----------
    config : object, optional
        Client configuration (host, base URL)
    '''
    def __init__(self, config=Config):
        self.config = config
        '''Initilize objects for interacting with the API'''
        self.campaign = CampaignAPI(client=self)
        self.timeseries = TimeseriesAPI(client=self)
        self.sensor = SensorAPI(client=self)
        self.test = TestAPI(client=self)


    def do_request(self, method, resource: str, endpoint: str = "", parameters: dict = None, body: dict = None):
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
               """
        url = self.config.host +"/" + "/".join([p for p in [self.config.base_url, resource, endpoint] if p.strip()])

        if parameters is not None and isinstance(parameters, dict):
            parameters = to_camel_case({k: v for k, v in parameters.items() if v is not None})
            enc_parameters = urllib.parse.urlencode(parameters, quote_via=urllib.parse.quote)
        else:
            enc_parameters = ""

        query_url = f"{url}/?{enc_parameters}"

        try:
            response = method(query_url, json=body)
            response.raise_for_status()
            #print(response)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            #print(response.json()) #TODO: parse errors
            raise Exception(http_err) #(response.json()['detail'][0]['msg'])
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise Exception(err)
        else:
            return response.json()

    def get(self, resource: str, endpoint: str = "", parameters: dict = None):
        return self.do_request(requests.get, resource, endpoint, parameters=parameters)

    def post(self, resource: str, endpoint: str = "", body: dict = None):
        return self.do_request(requests.post, resource, endpoint, body=body)

    def patch(self, resource: str, endpoint: str = "", body: dict = None):
        return self.do_request(requests.patch, resource, endpoint, body=body)

    def delete(self, resource: str, endpoint: str):
        return self.do_request(requests.delete, resource, endpoint)