#!/bin/sh

# You could probably do this fancier and have an array of extensions
# to create, but this is mostly an illustration of what can be done

psql -v ON_ERROR_STOP=1 --username postgres --dbname test_modeltest_db <<EOF
create extension "UUID-OSSP";
EOF