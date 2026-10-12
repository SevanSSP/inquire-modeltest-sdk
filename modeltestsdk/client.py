import logging
from typing import Callable, Optional

import numpy as np
import requests
import requests_cache
from requests.adapters import HTTPAdapter, Retry

from .api import (TimeseriesAPI, CampaignAPI, SensorAPI, TestAPI, FloaterTestAPI, WindCalibrationAPI,
                  WaveCalibrationAPI, TagsAPI, FloaterConfigAPI)
from .auth import ClientSecretToken, CredentialToken, InteractiveToken, ProviderToken, StaticToken, TokenSource
from .config import Config
from .query import Query

logger = logging.getLogger("modeltestsdk")
log_levels = dict(debug=logging.DEBUG, info=logging.INFO, error=logging.ERROR)


class Client:
    """
    Main entrypoint into modeltest-db SDK.

    Parameters
    ----------
    config : Config, optional
        Client configuration. By default read from INQUIRE_MODELTEST_* environment variables.
    token : str, optional
        Access token to use for every request.
    token_provider : callable, optional
        Function returning a current access token, called for every request (e.g. a web app's user session).
    credential : object, optional
        azure-identity credential (anything with get_token(scope)), e.g. DefaultAzureCredential.

    Notes
    -----
    Give at most one of token, token_provider and credential. Without them the client signs in with Microsoft
    from the configuration: as a service principal if client_secret is set, otherwise in the browser (kept in a
    token cache on disk).
    The token is kept by this client only, so clients for different users can run in one process.

    Use the client as a context manager, or call close(), to release its connections.
    """

    def __init__(self, config: Optional[Config] = None, *, token: Optional[str] = None,
                 token_provider: Optional[Callable[[], str]] = None, credential=None):
        """Initialize objects for interacting with the API"""
        if sum(x is not None for x in (token, token_provider, credential)) > 1:
            raise ValueError("Give at most one of token, token_provider and credential")
        self.config: Config = config if config is not None else Config(_env_file="../.env")
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

        logger.setLevel(log_levels.get(self.config.log_level, logging.INFO))

        # One session per client, retrying failed connections, throttling (honouring Retry-After) and server errors
        self.retries = Retry(total=self.config.requests_max_retries,
                             backoff_factor=self.config.requests_backoff_factor,
                             status_forcelist=[429, 500, 502, 503, 504], raise_on_status=False)
        self.session = self._new_session(requests.Session())
        self._cached_session: Optional[requests_cache.CachedSession] = None

        if token is not None:
            self._token_source: TokenSource = StaticToken(token)
        elif token_provider is not None:
            self._token_source = ProviderToken(token_provider)
        elif credential is not None:
            self._token_source = CredentialToken(credential, self._app_scope(), self.config.token_expiry_margin)
        else:
            self._token_source = self._token_source_from_config()

    def __str__(self):
        return f"<Client host:'{self.config.api_host}'>"

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        """Releases the client's connections."""
        self.session.close()
        if self._cached_session is not None:
            self._cached_session.close()

    def _new_session(self, session: requests.Session) -> requests.Session:
        adapter = HTTPAdapter(max_retries=self.retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({"Accept": "application/json"})
        return session

    def _app_scope(self) -> str:
        if not self.config.api_client_id:
            raise ValueError("Microsoft sign-in needs api_client_id (INQUIRE_MODELTEST_API_CLIENT_ID)")
        return f"api://{self.config.api_client_id}/.default"

    def _token_source_from_config(self) -> TokenSource:
        c = self.config
        margin = c.token_expiry_margin
        if c.tenant_id and c.client_id and c.client_secret:
            return ClientSecretToken(c.tenant_id, c.client_id, c.client_secret, self._app_scope(), margin)
        if c.tenant_id and c.client_id and c.api_client_id:
            return InteractiveToken(c.tenant_id, c.client_id, f"api://{c.api_client_id}/data.read",
                                    c.token_cache_path, margin)
        raise ValueError("No way to sign in: give a token, token_provider or credential, or configure Microsoft "
                         "sign-in (tenant_id, api_client_id and client_id, plus client_secret for a service principal)")

    def _request_token(self) -> str:
        """str: A valid access token for this client."""
        return self._token_source()

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
        url = f"{self.config.api_host}/{self.config.base_url}/{self.config.version}/"
        url += "/".join([p for p in [resource, endpoint] if p is not None])
        return url

    def _session_for(self, cache: bool) -> requests.Session:
        if not cache:
            return self.session
        if self._cached_session is None:
            self._cached_session = self._new_session(
                requests_cache.CachedSession(**self.config.cache_settings.model_dump()))
        return self._cached_session

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
        cache : bool, optional
            Use the on-disk response cache.

        Returns
        -------
        dict
            Request response

        """
        url = self._create_url(resource=resource, endpoint=endpoint)
        headers = {"Authorization": f"Bearer {self._request_token()}"}
        if parameters is not None:
            parameters = {k: v for k, v in parameters.items() if v is not None}

        r = self._session_for(cache).request(method, url, params=parameters, json=body, headers=headers,
                                             timeout=self.config.request_timeout)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            logger.error("Request body:  " + str(body))
            logger.error("Request response: " + r.text)
            raise
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

    def put(self, resource: str = None, endpoint: str = None, parameters: dict = None, body=None):
        """
        Perform PUT request

        Parameters
        ----------
        resource : str, optional
            API resource e.g. 'campaign'
        endpoint : str, optional
            API resource endpoint e.g. '{id}/sensors'
        parameters : dict, optional
            Request parameters.
        body : dict or list, optional
            Request body.

        Returns
        -------
        dict or list
            Request response
        """
        return self._do_request("PUT", resource=resource, endpoint=endpoint, parameters=parameters, body=body)

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

    def clear_cache(self):
        """
        Removes cached responses (from mtdb.sqlite in the local cache folder)
        """
        self._session_for(cache=True).cache.clear()
