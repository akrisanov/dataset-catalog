# Testing

## How to Test

- Because the dataset catalog service is built around IO and doesn't have much business logic, it makes sense to write integration or even stress tests checking the web service behavior.
- Utility methods like helpers can be covered by unit tests by isolating (mocking) external dependencies.
- Tests for request handlers only require covering logic responsible for assembling responses,
but not the response objects themselves — that part should be covered by Pydantic.

## Test Database

If somehow the `init-database.sh` script doesn't work for you, run the following commands manually:

```shell
PGPASSWORD='pswd00' docker exec -it [CONTAINER_ID] psql -U dataset_catalog -c "CREATE DATABASE dataset_catalog_test;"

PGPASSWORD='pswd00' docker exec -it [CONTAINER_ID] psql -U dataset_catalog -c "GRANT ALL PRIVILEGES ON DATABASE dataset_catalog_test TO dataset_catalog;"
```

## Test Runner

Please check out the `setup.cfg` file.

## Running Tests

```shell
make test
```

## Test Coverage

When pytest runs tests, test coverage is available in HTML and XML formats.
The `htmlcov` directory is added into `.gitignore` and only accessible either locally or in CI artifacts.

→ Check the [test coverage](../htmlcov/index.html).
