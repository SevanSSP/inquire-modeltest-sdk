import pytest

from modeltestsdk import Client
from modeltestsdk.config import Config


@pytest.fixture(scope="session")
def client(api):
    """A client for the API given with --api, signed in from the INQUIRE_MODELTEST_* settings; skipped without."""
    if not api:
        pytest.skip("functional tests need --api=<host> and Microsoft sign-in settings")
    with Client(Config(api_host=api)) as c:
        yield c


@pytest.fixture(scope="session")
def timeseries_with_data(client):
    """A timeseries with data, from the first page of timeseries."""
    ts = next((t for t in client.timeseries.get(limit=500) if t.datapoints_created_at), None)
    if ts is None:
        pytest.skip("no timeseries with data")
    return ts
