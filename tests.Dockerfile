FROM python:3.9 as builder

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export --dev -f requirements.txt > requirements.txt

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONUNBUFFERED=1

COPY --from=builder ./requirements.txt .

RUN pip install -r requirements.txt

COPY modeltestSDK ./modeltestSDK
COPY tests ./tests
