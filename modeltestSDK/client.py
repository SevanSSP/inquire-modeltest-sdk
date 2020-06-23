import os
import sys
import json
import datetime
import requests
from requests.exceptions import HTTPError
from .utils import to_snake_case, to_camel_case

from .config import Config


class SDKclient:

    def __init__(self, config=Config):
        self.config =config

    def printAllCampaignNames(self):
        urls = [self.config.host + "/" + self.config.base_url + "/campaign/all/"]
        for url in urls:
            try:
                response = requests.get(url)

                # If the response was successful, no Exception will be raised
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
            else:
                print('Success!')

        camp_json = response.json()
        for camp in camp_json:
            print(camp['name'])