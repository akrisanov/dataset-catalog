#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE dataset_catalog_test;
    GRANT ALL PRIVILEGES ON DATABASE dataset_catalog_test TO dataset_catalog;
EOSQL
