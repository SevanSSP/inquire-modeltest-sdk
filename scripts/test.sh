#!/usr/bin/env bash

set -e
set -x


pytest --cov --cov-report=term-missing modeltestSDK/tests "${@}"

read -rn1