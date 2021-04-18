# Tooling

## Writing Logs

When you need to write to stdout, use the following wrapper:

```python
from app.utils.logging import app_logger

app_logger.debug("Some useful information...")
```

Check out [logging.yaml](../logging.yaml). Uvicorn relies on this config file.

## Linters

- isort
- black
- flake8
- bandit

Their settings are placed in `setup.cfg` and `.bandit`.

Running all linters one by one:

```shell
make lint
```

I also recommend using a pre-commit hook to make sure your changes follow the project rules:

```shell
pre-commit install
pre-commit run
```
