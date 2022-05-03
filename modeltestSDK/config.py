"""
Configurations
"""
import os
from datetime import timedelta

class Config:
    """
    Client configuration
    """
    host: str = os.environ.get("INQUIRE_MODELTEST_API_HOST")
    base_url: str = "api"
    version: str = "v1"
    log_level: str = "info"
    cache_settings = {'cache_name': 'mtdb',
                      'backend': 'sqlite',
                      'use_cache_dir': True,
                      'expire_after': timedelta(days=7)}


class LocalConfig(Config):
    """
    Local context configuration
    """
    host: str = os.environ.get("INQUIRE_MODELTEST_API_HOST", "http://localhost:8080/")


class GitHubConfig(LocalConfig):
    DOCKER_USERNAME: str = 'snorrefjellvang'
    DOCKER_PASSWORD: str = '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'
    DOCKER_REGISTRY: str = "https://ghcr.io"


"""
#docker login "https://ghcr.io" -u "snorrefjellvang"
#docker pull ghcr.io/sevanssp/inquire_modeltest:latest
#docker pull postgres
#docker run --name db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test -p 5432:5432 -d postgres:10
#docker run -e INQUIRE_MODELTEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost/inquire_test --name test ghcr.io/sevanssp/inquire_modeltest

#docker run -e INQUIRE_MODELTEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/postgres --name test ghcr.io/sevanssp/inquire_modeltest
postgresql+psycopg2://postgres:postgres@db:5432/

docker run -e INQUIRE_MODELTEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/test --name test -d --network testnetwork ghcr.io/sevanssp/inquire_modeltest

docker run -e INQUIRE_MODELTEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/postgres --name test -d --network testnetwork ghcr.io/sevanssp/inquire_modeltest

docker run -e INQUIRE_MODELTEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/postgres --name test -d ghcr.io/sevanssp/inquire_modeltest

#docker run --name db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test -d postgres
docker run -e INQUIRE_MODELTEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:80/postgres --name test -p 80:80 -d --network testnetwork ghcr.io/sevanssp/inquire_modeltest
"""
