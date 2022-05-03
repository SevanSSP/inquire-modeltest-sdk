COPY poetry.lock ./
COPY pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY modeltestSDK ./modeltestSDK
COPY tests ./tests

FROM postgres
COPY docker_scripts/install-extensions.sql /docker-entrypoint-initdb.d