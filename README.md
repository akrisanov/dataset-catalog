# Dataset Catalog

[![dataset_catalog](https://github.com/akrisanov/dataset-catalog/actions/workflows/dataset-catalog.yml/badge.svg)](https://github.com/akrisanov/dataset-catalog/actions/workflows/dataset-catalog.yml) [![codecov](https://codecov.io/gh/akrisanov/dataset-catalog/branch/main/graph/badge.svg?token=QBMa7gcOBe)](https://codecov.io/gh/akrisanov/dataset-catalog)

A naive web service for uploading datasets to the imaginary data store and retrieving the information about them.

## Documentation

- [System Design](docs/system-design.md)
- [Development Environment](docs/env.md)
- [Tooling](docs/tooling.md)
- [Style Guide](docs/style-guide.md)
- [Testing](docs/testing.md)
- [Building Docker Image](docs/build.md)
- [Deployment](docs/deployment.md)

## Technology Stack

- Python 3.9
- FastAPI
- Uvicorn
- PostgreSQL
- S3-compatible storage
- Containers

## Project Layout

```shell
├── app                 # Application logic
│   ├── handlers        # Request handlers (similar to controllers or views in other frameworks)
│   ├── models          # SQLAlchemy table definitions and additional data types like enums
│   ├── repositories    # Modules containing SQLAlchemy query expressions → DB access interface
│   ├── schemas         # Pydantic schemas validating input and output data
│   ├── settings        # Application settings
│   ├── utils           # Helpers that doesn't contain any business logic and can be extracted
│   ├── application.py  # FastAPI entry point and it's configuration
├── main.py             # Webservice entry point with additional settings
├── migrations          # Alembic migrations
├── pip.conf            # pip config for working with private package registry like Artifactory
├── setup.cfg           # Python environment configs like linters, mypy rules, pytest etc.
├── tests               # Test suite running via Pytest
```

## Run Locally

```shell
make up

cp .env.example .env
make venv
# Check PostgreSQL logs to make sure
# LOG: database system is ready to accept connections
make migrate
make serve
```

[Open](http://localhost:8000/docs) Swagger UI in your favourite browser.

---

© Andrey Krisanov, 2021
