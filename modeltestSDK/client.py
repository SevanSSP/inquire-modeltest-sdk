import os
import sys
import json
import datetime
import urllib.parse

import requests
from requests.exceptions import HTTPError
from .utils import to_snake_case, to_camel_case

from .config import Config


class SDKclient:

    def __init__(self, config=Config):
        self.config = config

    def do_request(self, method, resource: str, endpoint: str = "", parameters: dict = None, body: dict = None):
        url = self.config.host +"/" + "/".join([p for p in [self.config.base_url, resource, endpoint] if p.strip()])

        if parameters is not None and isinstance(parameters, dict):
            parameters = to_camel_case({k: v for k, v in parameters.items() if v is not None})
            enc_parameters = urllib.parse.urlencode(parameters, quote_via=urllib.parse.quote)
        else:
            enc_parameters = ""

        query_url= f"{url}/?{enc_parameters}"

        try:
            response = method(query_url,json=body)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return err
        except Exception as err:
            print(f'Other error occurred: {err}')
            return err
        else:
            return response.json()

    def get(self,resource: str, endpoint: str = "", parameters: dict = None):
        return self.do_request(requests.get, resource, endpoint, parameters=parameters)

    def post(self,resource: str, endpoint: str = "", body: dict = None):
        return self.do_request(requests.post, resource, endpoint, body=body)

    #def delete(self, resource: str, endpoint: str, parameters: dict = None):
    #    return self.do_request(requests.delete,resource,)