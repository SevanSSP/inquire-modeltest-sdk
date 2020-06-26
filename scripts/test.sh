#!/usr/bin/env bash

set -e
set -x


pytest --cov=app --cov-report=term-missing modeltestSDK/tests "${@}"

read -rn1