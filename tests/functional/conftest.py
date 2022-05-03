import pytest
from modeltestSDK import Client
import requests

@pytest.fixture(scope="module")
def client():
    """
    Expose an SDK API client configured for testing
    """
    client = Client()  # TODO: Konfigurer en test API (lokalt?)
    return client
