import os
import sys
import json
import datetime
from .utils import to_snake_case, to_camel_case
from .config import Config
from .exceptions import AuthenticationError, ClientConnectionError, TimeSeriesAPIError

class SDKclient:

    def __init__(self, config=Config):
        self.config =config
        #self.time_series= TimeSeriesAPI(client=self)
