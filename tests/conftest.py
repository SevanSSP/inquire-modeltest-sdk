import pytest
import os
import time


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join("docker-compose.yml")


# Invoking this fixture: 'function_scoped_container_getter' starts all services
@pytest.fixture(scope="function")
def http_service(docker_ip, docker_services):
    """Ensure that API service is up and responsive."""

    # `docker_services` is a fixture provided by pytest-docker-compose
    # that allows you to interact with your Docker services from your tests.
    # Wait for the API service to be up.
    port = docker_services.port_for("api", 8000)
    api_url = "http://{}:{}".format(docker_ip, port)
    time.sleep(10)
    return api_url
