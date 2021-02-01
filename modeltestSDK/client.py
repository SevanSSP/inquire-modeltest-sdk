import os
import sys
import requests
import logging
from datetime import datetime
from .api import (TimeseriesAPI, CampaignAPI, SensorAPI, TestAPI, FloaterTestAPI, WindCalibrationAPI,
                  WaveCalibrationAPI, TagsAPI, FloaterConfigAPI)
from .query import Query
from .config import Config


log_levels = dict(debug=logging.DEBUG, info=logging.INFO, error=logging.ERROR)


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

        logging.basicConfig(
            stream=sys.stdout,
            level=log_levels.get(self.config.log_level, logging.INFO),
            format="%(levelname)s at line %(lineno)d in %(filename)s - %(message)s"
        )

    def _request_token(self) -> str:
        """str: Authenticate and return access token."""
        # check if current access token is still valid
        current_token = os.getenv("INQUIRE_MODELTEST_API_TOKEN")
        token_expires_on = os.getenv("INQUIRE_MODELTEST_API_TOKEN_EXPIRES")
        if current_token is not None and token_expires_on is not None and \
                datetime.utcnow().timestamp() < float(token_expires_on):
            logging.debug("Your current access token has not yet expired.")
            return current_token

        # authenticate and get access token
        try:
            logging.info("Authenticating by user impersonation.")
            user = os.getenv("INQUIRE_MODELTEST_API_USER")
            passwd = os.getenv("INQUIRE_MODELTEST_API_PASSWORD")
            assert user is not None and passwd is not None, "You have to set the following two environment variables " \
                                                            "to login and acquire an access token\n" \
                                                            "\n\t'INQUIRE_MODELTEST_API_USER'" \
                                                            "\n\t'INQUIRE_MODELTEST_API_PASSWORD'."

            r = requests.post(
                self._create_url(resource="auth", endpoint="token"),
                data=dict(
                    username=user,
                    password=passwd
                )
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        except requests.exceptions.ConnectionError as e:
            raise e
        except requests.exceptions.Timeout as e:
            raise e
        except requests.exceptions.RequestException as e:
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
                logging.info("Authentication successful. Acquired valid access token.")
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
           'https://{host}/{base_url}/{version}/{resource}/{endpoint}'

        """
        url = f"https://{self.config.host}/{self.config.base_url}/{self.config.version}/"
        url += "/".join([p for p in [resource, endpoint] if p is not None])
        return url

    def _do_request(self, method: str, resource: str = None, endpoint: str = None, parameters: dict = None,
                    body: dict = None):
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
            "Host": self.config.host,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        # do request (also encodes parameters)
        try:
            r = requests.request(method, url, params=parameters, data=body, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        except requests.exceptions.ConnectionError as e:
            raise e
        except requests.exceptions.Timeout as e:
            raise e
        except requests.exceptions.RequestException as e:
            raise e
        else:
            return r.json()

    def get(self, resource: str = None, endpoint: str = None, parameters: dict = None):
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

        Returns
        -------
        dict
            Request response

        """
        return self._do_request("GET", resource=resource, endpoint=endpoint, parameters=parameters)

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

    def delete(self, resource: str = None, endpoint: str = None, parameters: str = None):
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
