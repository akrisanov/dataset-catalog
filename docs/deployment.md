# Deployment

## Running Migrations

Please, run the migrations via `./prestart.sh` when a new version of the service (pod) is successfully up.

## Python Shell Inside a Container

You can use IPython and work with async code directly from the shell:

```shell
$ ipython

>>> from app.settings.base import db
>>> await db.connect()
>>> from app.repositories import datasets_repo
>>> u = await datasets_repo.get_row(id=1)
```

## Infra

- If you decide going with Nginx as reverse proxy, don't forget about configuring:
  - CORS headers
  - The `client_max_body_size` setting to limit a size of uploads
- Use something like Prometheus and Grafana for monitoring application health and resource utilization.
- Helm package to deploy all the resources in one shot.
