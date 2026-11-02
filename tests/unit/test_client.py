import logging
import os
import sys
import time
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import requests

from modeltestsdk import Client
from modeltestsdk.config import Config

HOST = "https://modeltest.example"


def config(**kwargs):
    return Config(api_host=HOST, **kwargs)


def response(json_body, status=200):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_body
    r.raise_for_status.return_value = None
    return r


def test_token_is_sent_and_kept_per_client():
    client = Client(config(), token="abc")
    client.session.request = MagicMock(return_value=response({"ok": True}))
    assert client.get("campaign") == {"ok": True}
    args, kwargs = client.session.request.call_args
    assert args == ("GET", f"{HOST}/api/v1/campaign")
    assert kwargs["headers"]["Authorization"] == "Bearer abc"
    assert kwargs["timeout"] == 60.0
    assert not any(k.startswith("INQUIRE_MODELTEST_API_TOKEN") for k in os.environ)

    other = Client(config(), token="xyz")
    assert other._request_token() == "xyz" and client._request_token() == "abc"


def test_token_provider_is_called_for_every_request():
    tokens = iter(["t1", "t2"])
    client = Client(config(), token_provider=lambda: next(tokens))
    assert [client._request_token(), client._request_token()] == ["t1", "t2"]
    with pytest.raises(RuntimeError):
        Client(config(), token_provider=lambda: None)._request_token()


def test_only_one_token_source():
    with pytest.raises(ValueError):
        Client(config(), token="a", token_provider=lambda: "b")


def test_credential_tokens_are_cached_until_shortly_before_expiry():
    credential = MagicMock()
    credential.get_token.side_effect = [SimpleNamespace(token="c1", expires_on=time.time() + 3600),
                                        SimpleNamespace(token="c2", expires_on=time.time() + 3600)]
    client = Client(config(api_client_id="api-id"), credential=credential)
    assert client._request_token() == client._request_token() == "c1"
    credential.get_token.assert_called_once_with("api://api-id/.default")

    client._token_source._expires_on = time.time() + 30  # within the 60 s margin
    assert client._request_token() == "c2"


def test_retries_on_https_and_http():
    client = Client(config(requests_max_retries=3), token="abc")
    for prefix in ("https://", "http://"):
        retries = client.session.get_adapter(prefix + "x").max_retries
        assert retries.total == 3
        assert 429 in retries.status_forcelist and 503 in retries.status_forcelist


def test_service_principal_sign_in(monkeypatch):
    app = MagicMock()
    app.acquire_token_for_client.return_value = {"access_token": "sp", "expires_in": 3600}
    msal = MagicMock()
    msal.ConfidentialClientApplication.return_value = app
    monkeypatch.setitem(sys.modules, "msal", msal)

    client = Client(config(tenant_id="tenant", client_id="app", client_secret="secret", api_client_id="api-id"))
    assert client._request_token() == "sp"
    msal.ConfidentialClientApplication.assert_called_once_with(
        "app", client_credential="secret", authority="https://login.microsoftonline.com/tenant")
    app.acquire_token_for_client.assert_called_once_with(scopes=["api://api-id/.default"])

    app.acquire_token_for_client.return_value = {"error": "invalid_client", "error_description": "bad secret"}
    client._token_source._token = None
    with pytest.raises(RuntimeError, match="bad secret"):
        client._request_token()


def test_interactive_sign_in_uses_the_token_cache(monkeypatch, tmp_path):
    app = MagicMock()
    app.get_accounts.side_effect = [[], [{"username": "alice"}]]
    app.acquire_token_interactive.return_value = {"access_token": "browser", "expires_in": 3600}
    app.acquire_token_silent.return_value = {"access_token": "silent", "expires_in": 3600}
    msal = MagicMock()
    msal.PublicClientApplication.return_value = app
    extensions = MagicMock()
    monkeypatch.setitem(sys.modules, "msal", msal)
    monkeypatch.setitem(sys.modules, "msal_extensions", extensions)

    client = Client(config(tenant_id="tenant", client_id="public", api_client_id="api-id",
                           token_cache_path=str(tmp_path / "cache.bin")))
    assert client._request_token() == "browser"
    app.acquire_token_interactive.assert_called_once_with(["api://api-id/data.read"])
    extensions.build_encrypted_persistence.assert_called_once_with(str(tmp_path / "cache.bin"))

    client._token_source._token = None  # e.g. a later session: signed-in account in the cache
    assert client._request_token() == "silent"
    assert app.acquire_token_interactive.call_count == 1


def test_no_sign_in_configured():
    with pytest.raises(ValueError, match="No way to sign in"):
        Client(config())


def test_library_does_not_configure_logging():
    handlers = list(logging.getLogger().handlers)
    Client(config(log_level="debug"), token="abc")
    assert logging.getLogger().handlers == handlers
    assert logging.getLogger("modeltestsdk").level == logging.DEBUG


def test_context_manager_closes_sessions():
    with Client(config(), token="abc") as client:
        client.session = MagicMock(wraps=client.session)
    client.session.close.assert_called_once()


def test_put_and_errors():
    client = Client(config(), token="abc")
    client.session.request = MagicMock(return_value=response([{"status": "created"}]))
    assert client.put("campaign", "1/sensors", body=[{"name": "A"}]) == [{"status": "created"}]
    assert client.session.request.call_args.kwargs["json"] == [{"name": "A"}]

    failing = response({"detail": "no"}, status=403)
    failing.raise_for_status.side_effect = requests.exceptions.HTTPError("403")
    client.session.request = MagicMock(return_value=failing)
    with pytest.raises(requests.exceptions.HTTPError):
        client.get("campaign")


def test_cached_requests_use_their_own_session(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    client = Client(config(cache_settings={"cache_name": "test_cache", "use_cache_dir": False}), token="abc")
    cached = client._session_for(cache=True)
    assert cached is not client.session and cached is client._session_for(cache=True)
    assert cached.get_adapter("https://x").max_retries.total == client.retries.total
    client.clear_cache()
    client.close()
