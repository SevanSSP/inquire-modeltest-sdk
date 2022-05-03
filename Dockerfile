FROM python:3.9 as builder

FROM postgres
COPY docker_scripts/install-extensions.sql /docker-entrypoint-initdb.d