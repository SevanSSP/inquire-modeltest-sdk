import pytest
import os
import time


def pytest_addoption(parser):
    parser.addoption("--api", action="store", default="http://127.0.0.1:8000")


@pytest.fixture(scope="session")
def api(pytestconfig):
    return pytestconfig.getoption("api")


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join("tests", "functional", "docker-compose.test.yml")


@pytest.fixture(scope="session")
def http_service(api, request):
    """Ensure that API service is up and responsive."""
    if api == 'build':
        docker_ip = request.getfixturevalue("docker_ip")
        docker_services = request.getfixturevalue("docker_services")

        # `docker_services` is a fixture provided by pytest-docker-compose
        # that allows you to interact with your Docker services from your tests.
        # Wait for the API service to be up.
        port = docker_services.port_for("api", 8000)
        api_url = f"http://{docker_ip}:{port}"
        time.sleep(10)
    else:
        api_url = api

    return api_url


@pytest.fixture(scope="session")
def admin_key(api):
    """collect admin key from environmental variable if testing against localhost, otherwise returns 'administrator'"""
    if api == 'build':
        return 'administrator'
    else:
        return os.environ.get("ADMINISTRATOR_KEY")
