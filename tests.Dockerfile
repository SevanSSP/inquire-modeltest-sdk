FROM postgres
COPY docker_scripts/install-extensions.sql /docker-entrypoint-initdb.d

FROM python:3.9 as builder

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export --dev --without-hashes -f requirements.txt > requirements.txt

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONUNBUFFERED=1

COPY --from=builder ./requirements.txt .

RUN pip install -r requirements.txt

COPY modeltestSDK ./modeltestSDK
COPY tests ./tests
