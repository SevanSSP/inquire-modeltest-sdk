import pytest
from modeltestSDK import SDKclient


@pytest.fixture(scope="module")
def client():
    """
    Expose an SDK API client configured for testing
    """
    client = SDKclient()  # TODO: Konfigurer en test API (lokalt?)
    return client
