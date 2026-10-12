"""
Access tokens for the model test API.

Token sources, all held per client (nothing is written to environment variables):

- ``StaticToken``: a token you already have
- ``ProviderToken``: a function that returns a current token, e.g. from a web app's user session
- ``CredentialToken``: an azure-identity credential (``DefaultAzureCredential``, managed identity, ...)
- ``ClientSecretToken``: a service principal (client id + secret), e.g. the import pipeline
- ``InteractiveToken``: Microsoft sign-in in the browser, remembered in a token cache on disk
"""
import logging
import threading
import time
from pathlib import Path
from typing import Callable, Optional, Protocol

logger = logging.getLogger(__name__)


class TokenSource(Protocol):
    def __call__(self) -> str:
        """Returns a valid access token."""


class _Cached:
    """Keeps a token until shortly before it expires. Thread safe."""

    def __init__(self, margin: float):
        self._margin = margin
        self._token: Optional[str] = None
        self._expires_on = 0.0
        self._lock = threading.Lock()

    def __call__(self) -> str:
        with self._lock:
            if self._token is None or time.time() >= self._expires_on - self._margin:
                self._token, self._expires_on = self._acquire()
            return self._token

    def _acquire(self) -> tuple[str, float]:
        """Returns (token, expiry as unix time)."""
        raise NotImplementedError  # pragma: no cover


class StaticToken:
    def __init__(self, token: str):
        self._token = token

    def __call__(self) -> str:
        return self._token


class ProviderToken:
    """Calls the provider for every request; the provider is responsible for refreshing."""

    def __init__(self, provider: Callable[[], str]):
        self._provider = provider

    def __call__(self) -> str:
        token = self._provider()
        if not token:
            raise RuntimeError("token_provider returned no token")
        return token


class CredentialToken(_Cached):
    """An azure-identity style credential: anything with get_token(scope) -> (token, expires_on)."""

    def __init__(self, credential, scope: str, margin: float = 60):
        super().__init__(margin)
        self._credential = credential
        self._scope = scope

    def _acquire(self):
        token = self._credential.get_token(self._scope)
        return token.token, float(token.expires_on)


def _msal_result(result: Optional[dict]) -> tuple[str, float]:
    if not result or "access_token" not in result:
        error = (result or {}).get("error_description") or (result or {}).get("error") or "no token"
        raise RuntimeError(f"Microsoft sign-in failed: {error}")
    return result["access_token"], time.time() + float(result.get("expires_in", 0))


class ClientSecretToken(_Cached):
    """Service principal sign-in with the client credentials flow."""

    def __init__(self, tenant_id: str, client_id: str, client_secret: str, scope: str, margin: float = 60):
        import msal
        super().__init__(margin)
        self._app = msal.ConfidentialClientApplication(
            client_id, client_credential=client_secret, authority=f"https://login.microsoftonline.com/{tenant_id}")
        self._scope = scope

    def _acquire(self):
        return _msal_result(self._app.acquire_token_for_client(scopes=[self._scope]))


def default_token_cache_path() -> Path:
    return Path.home() / ".inquire-modeltest" / "msal_token_cache.bin"


class InteractiveToken(_Cached):
    """
    Microsoft sign-in in the browser. The sign-in is kept in an encrypted token cache on disk, so later
    sessions refresh silently instead of opening the browser again.
    """

    def __init__(self, tenant_id: str, client_id: str, scope: str, cache_path: Optional[Path] = None,
                 margin: float = 60):
        import msal
        from msal_extensions import PersistedTokenCache, build_encrypted_persistence
        super().__init__(margin)
        cache_path = Path(cache_path or default_token_cache_path())
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache = PersistedTokenCache(build_encrypted_persistence(str(cache_path)))
        self._app = msal.PublicClientApplication(
            client_id, authority=f"https://login.microsoftonline.com/{tenant_id}", token_cache=cache)
        self._scope = scope

    def _acquire(self):
        accounts = self._app.get_accounts()
        if accounts:
            result = self._app.acquire_token_silent([self._scope], account=accounts[0])
            if result and "access_token" in result:
                return _msal_result(result)
        logger.info("Signing in with Microsoft in the browser")
        return _msal_result(self._app.acquire_token_interactive([self._scope]))

