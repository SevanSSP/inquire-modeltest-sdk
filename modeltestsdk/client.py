import os
import sys
import requests
import requests_cache
import logging
import numpy as np
try:
    from datetime import UTC
except ImportError:
    from datetime import timezone
    UTC = timezone.utc
from datetime import datetime
from .api import (TimeseriesAPI, CampaignAPI, SensorAPI, TestAPI, FloaterTestAPI, WindCalibrationAPI,
                  WaveCalibrationAPI, TagsAPI, FloaterConfigAPI)
from .query import Query
from .config import Config
from requests.adapters import HTTPAdapter, Retry

log_levels = dict(debug=logging.DEBUG, info=logging.INFO, error=logging.ERROR)
retries = Retry(total=Config.requests_max_retries,
                backoff_factor=Config.requests_backoff_factor,
                status_forcelist=[500, 502, 503, 504])


class Client:
    """
    Main entrypoint into modeltest-db SDK.

    Parameters
    ----------
    config : object, optional
        Client configuration (host, base URL)

    Notes
    -----
    Using the SDK requires setting the following environmental variables

        INQUIRE_MODELTEST_API_USER - Your username
        INQUIRE_MODELTEST_API_PASSWORD - Your password
        INQUIRE_MODELTEST_API_HOST - Model test API host

    """

    def __init__(self, config=Config):
        """Initialize objects for interacting with the API"""
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

        # check environmental variables
        if os.getenv("INQUIRE_MODELTEST_API_USER") is None:
            raise EnvironmentError("You have to set the INQUIRE_MODELTEST_API_USER environment variable to login.")
        if os.getenv("INQUIRE_MODELTEST_API_PASSWORD") is None:
            raise EnvironmentError("You have to set the INQUIRE_MODELTEST_API_PASSWORD environment variable to login.")
        if os.getenv("INQUIRE_MODELTEST_API_HOST") is None:
            raise EnvironmentError("You have to set the INQUIRE_MODELTEST_API_HOST environment variable to login.")

        # configure logging
        log_levels = dict(debug=logging.DEBUG, info=logging.INFO, error=logging.ERROR)
        level = log_levels.get(self.config.log_level, logging.INFO)
        if self.config.log_level == "debug":
            fmt = "%(levelname)s at line %(lineno)d in %(filename)s - %(message)s"
        else:
            fmt = "%(levelname)s - %(message)s"

        logging.basicConfig(stream=sys.stdout, level=level, format=fmt)

    def __str__(self):
        return f"<Client host:'{self.config.host}'>"

    def _request_token(self) -> str:
        """str: Authenticate and return access token."""
        # check if current access token is still valid
        current_token = os.getenv("INQUIRE_MODELTEST_API_TOKEN")
        token_expires_on = os.getenv("INQUIRE_MODELTEST_API_TOKEN_EXPIRES")
        if current_token is not None and token_expires_on is not None and \
                datetime.now(UTC).timestamp() < float(token_expires_on):
            logging.debug("Your current access token is still valid.")
            return current_token

        # authenticate and get access token
        try:
            logging.info("Authenticating by user impersonation.")
            user = os.getenv("INQUIRE_MODELTEST_API_USER")
            passwd = os.getenv("INQUIRE_MODELTEST_API_PASSWORD")

            s = requests.session()
            s.mount('http://', HTTPAdapter(max_retries=retries))

            r = s.post(
                self._create_url(resource="auth", endpoint="token"),
                data=dict(grant_type=None,
                          username=user,
                          password=passwd,
                          scope=None,
                          client_id=None,
                          client_secret=None)
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:  # pragma: no cover
            raise e
        except requests.exceptions.ConnectionError as e:  # pragma: no cover
            raise e
        except requests.exceptions.Timeout as e:  # pragma: no cover
            raise e
        except requests.exceptions.RequestException as e:  # pragma: no cover
            raise e
        else:
            # update env vars
            data = r.json()
            token = data.get("access_token")
            expires = data.get("expires")
            if token is None and expires is None:
                raise ValueError(f"Unable to acquire a valid access token 'access_token'= {token} and "
                                 f"token expiry 'expires' = {expires}")
            else:
                logging.info("Acquired valid access token.")
                os.environ["INQUIRE_MODELTEST_API_TOKEN"] = token
                os.environ["INQUIRE_MODELTEST_API_TOKEN_EXPIRES"] = str(expires)
                return token

    def _create_url(self, resource: str = None, endpoint: str = None) -> str:
        """
        Create URL for endpoint

        Parameters
        ----------
        resource : str, optiona
            API resource e.g. 'plant/timeseries'
        endpoint : str, optional
           API resource endpoint e.g. 'list' or 'search'

        Returns
        -------
        str
           Request response

        Notes
        -----
        The full request url is like
           '{host}/{base_url}/{version}/{resource}/{endpoint}'

        """
        url = f"{self.config.host}/{self.config.base_url}/{self.config.version}/"
        url += "/".join([p for p in [resource, endpoint] if p is not None])
        return url

    def _do_request(self, method: str, resource: str = None, endpoint: str = None, parameters: dict = None,
                    body: dict = None, cache=False):
        """
        Carry out request.

        Parameters
        ----------
        method : {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}
            Request method.
        resource : str, optional
            API resource e.g. 'plant/timeseries'
        endpoint : str, optional
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response

        """
        # create base url
        url = self._create_url(resource=resource, endpoint=endpoint)

        # authenticate and get access token
        token = self._request_token()

        # create request headers
        headers = {
            "Authorization": f"Bearer {token}",
            "Connection": "keep-alive",
            "Host": self.config.host.split("://")[-1],  # remove leading http/https
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # remove empty values from parameters
        if parameters is not None:
            parameters = {k: v for k, v in parameters.items() if v is not None}

        # do request (also encodes parameters)

        s = requests.session()
        s.mount('http://', HTTPAdapter(max_retries=retries))

        try:
            if cache:
                with requests_cache.enabled(**Config.cache_settings):
                    r = s.request(method, url, params=parameters, json=body, headers=headers)
                r.raise_for_status()
            else:
                r = s.request(method, url, params=parameters, json=body, headers=headers)
                r.raise_for_status()
        except requests.exceptions.HTTPError as e:  # pragma: no cover
            logging.error("Request body:  " + str(body))
            logging.error("Request response: " + r.text)
            raise e
        except requests.exceptions.ConnectionError as e:  # pragma: no cover
            raise e
        except requests.exceptions.Timeout as e:  # pragma: no cover
            raise e
        except requests.exceptions.RequestException as e:  # pragma: no cover
            raise e
        else:
            return r.json()

    @staticmethod
    def _ensure_serializable(body: dict):
        """
        change data types not natively supported by json encoder

        Parameters
        ----------
        body : dict
            Request body.

        Returns
        -------
        dict
            Request body with json encoder supported data types
        """

        serializable_body = dict()
        for key, value in body.items():
            if isinstance(value, np.int64) or isinstance(value, np.int32):
                value = int(value)
            elif isinstance(value, np.float64) or isinstance(value, np.float32):
                value = float(value)

            if (isinstance(value, float) or isinstance(value, int)) and np.isnan(value):
                value = None

            serializable_body[key] = value

        return serializable_body

    def get(self, resource: str = None, endpoint: str = None, parameters: dict = None, cache: bool = False):
        """
        Perform GET request

        Parameters
        ----------
        resource : str, optional
            API resource e.g. 'plant/timeseries'
        endpoint : str, optional
           API resource endpoint e.g. 'list' or 'search'
        parameters : dict, optional
            URL parameters
        cache : bool, optional
            Enable caching of request response

        Returns
        -------
        dict
            Request response

        """
        return self._do_request("GET", resource=resource, endpoint=endpoint, parameters=parameters, cache=cache)

    def post(self, resource: str = None, endpoint: str = None, parameters: dict = None, body: dict = None):
        """
        Perform POST request

        Parameters
        ----------
        resource : str, optional
            API resource e.g. 'plant/timeseries'
        endpoint : str, optional
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response
        """
        body = self._ensure_serializable(body)

        return self._do_request("POST", resource=resource, endpoint=endpoint, parameters=parameters, body=body)

    def patch(self, resource: str = None, endpoint: str = None, parameters: dict = None, body: dict = None):
        """
        Perform PATCH request

        Parameters
        ----------
        resource : str, optional
            API resource e.g. 'plant/timeseries'
        endpoint : str, optional
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response
        """
        return self._do_request("PATCH", resource=resource, endpoint=endpoint, parameters=parameters, body=body)

    def delete(self, resource: str = None, endpoint: str = None, parameters: dict = None):
        """
        Perform DELETE request

        Parameters
        ----------
        resource : str, optional
            API resource e.g. 'plant/timeseries'
        endpoint : str, optional
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.

        Returns
        -------
        dict
            Request response
        """
        return self._do_request("DELETE", resource=resource, endpoint=endpoint, parameters=parameters)

    @staticmethod
    def clear_cache():
        """
        Removes cached datapoints (from mtdb.sqlite at local cache folder)
        """
        with requests_cache.enabled(**Config.cache_settings):  # pragma: no cover
            requests_cache.clear()
