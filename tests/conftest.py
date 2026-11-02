import pytest


def pytest_addoption(parser):
    parser.addoption("--api", action="store", default=None,
                     help="host of a model test API v2 to run the functional tests against, e.g. "
                          "https://inquire-modeltest-staging.azurewebsites.net (sign-in from INQUIRE_MODELTEST_*)")


@pytest.fixture(scope="session")
def api(pytestconfig):
    return pytestconfig.getoption("api")
