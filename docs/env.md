# Development Environment

## Python

Create Python virtual environment with the command:

```shell
make venv
```

Activate it when necessary:

```shell
source .venv/bin/activate
```

If you have any problems with installing binary dependencies like openssl on macOS, execute:

```shell
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

### Updating Packages

All Python packages have pinned versions in their requirements-*.txt files.
It helps to avoid messing up with resolving dependency conflicts but requires developers to remember
about manual upgrades from time to time. For checking new package versions during the pre-commit
and CI pipeline I use the tool called [pur](https://pypi.org/project/pur/).

```shell
$ make update-deps
All requirements up-to-date.
```

Pur doesn't install updated dependencies automatically. It just changes requirements-*.txt files.
To actually install new versions of dependencies, run the following command:

```shell
make install-deps
```

## Environment Variables

For the production environment, you can use environment variables for the web service configuration.
It's common practice of [12-factor apps](https://12factor.net/).

### Application Server

| Name           | Comments                                            | Default Value         |
|----------------|-----------------------------------------------------|-----------------------|
| HOST           | Use 0.0.0.0 for accessing outside of the machine    | 127.0.0.1             |
| PORT           |                                                     | 8000                  |
| ROOT_PATH      | If you use reverse-proxy, set web service url path  |                       |
| LOG_LEVEL      | Logging level                                       | info                  |
| DEBUG          | Debug mode                                          | false                 |
| RELOAD         | Reload application server when code files change    | false                 |
| RELOAD_DIRS    | Dirs to watch                                       | app                   |
| WORKERS        | Number of worker processes                          | $WEB_CONCURRENCY or 1 |

### Web Service

| Name           | Comments                                            | Default Value         |
|----------------|-----------------------------------------------------|-----------------------|
| SENTRY_DSN     | Error monitoring                                    |                       |
| DOCS_URL       | Where to find Swagger UI                            | /docs                 |
| OPENAPI_URL    | Where to find the Open API schema                   | /openapi.json         |

### Database Connection

| Name           | Comments                                            | Default Value         |
|----------------|-----------------------------------------------------|-----------------------|
| DB_USER        | Owner of the web service database                   | dataset_catalog       |
| DB_PASS        | User's Password                                     | pswd00                |
| DB_HOST        | Database Host                                       | localhost             |
| DB_PORT        | Database Port                                       | 15432                 |
| DB_NAME        | Database Name                                       | dataset_catalog       |

### File Storage

| Name           | Comments                                            | Default Value         |
|----------------|-----------------------------------------------------|-----------------------|
| S3_ENDPOINT    | URL endpoint with host and port                     | localhost:9000        |
| S3_REGION      | Bucket's region                                     |                       |
| S3_ACCESS_KEY  | API access key                                      | LOCAL_ACCESS_KEY      |
| S3_SECRET_KEY  | API secret key                                      | LOCAL_SECRET_KEY      |
| S3_BUCKET_NAME | Bucket's name                                       | datasets              |
| S3_SECURE      | Whether or not to use an SSL connection             | False                 |

For the development environment, create a copy of the example file and change the values of
environment variables according to your needs:

```shell
cp .env.example .env
```

## Creating a Database

_You don't need to create a database manually if you use Docker compose._

```shell
psql postgres
> CREATE DATABASE dataset_catalog;
```

### Running Database Migrations

```shell
PYTHONPATH=. alembic revision --autogenerate -m "[Migration Message]"  # creates a new migration
PYTHONPATH=. alembic upgrade head  # or → make migrate
```

## Starting an Application Server

```shell
make serve
```

For debugging purposes:

```shell
python main.py
```

or use Visual Studio Code "Run and Debug" command.

## Docker Environment

```shell
docker-compose -f docker-compose.local.yml up  # or → make up
```
