import os
from typing import Optional, Set

import databases
from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    """
    A full list of Uvicorn configs can be found here:
    https://www.uvicorn.org/#command-line-options
    """

    host: str = "127.0.0.1"
    port: int = 8000
    root_path: str = ""  # e.g. "/api/datasets"
    log_level: str = "info"
    debug: bool = False
    reload: bool = False
    reload_dirs: Set[str] = {"app"}  # в yaml: '["app"]'
    workers: Optional[int] = None


# NOTE: Instead of defining global configs and import those variables, we can use the FastAPI
# [dependency mechanism](https://fastapi.tiangolo.com/advanced/settings/#settings-in-a-dependency).
# It can be useful in tests.


class AppSettings(BaseSettings):
    sentry_dsn: Optional[str] = None
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"


class DatabaseSettings(BaseSettings):
    db_user: str = "dataset_catalog"
    db_pass: str = "pswd00"
    db_host: str = "localhost"
    db_port: str = "15432"
    db_name: str = "dataset_catalog"

    @property
    def sqlalchemy_database_url(self) -> str:
        db_name = f"{self.db_name}_test" if os.environ.get("TESTING") else self.db_name
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{db_name}"  # noqa: E501


class MinioSettings(BaseSettings):
    s3_endpoint: str = "localhost:9000"
    s3_region: Optional[str] = None
    s3_access_key: str = "LOCAL_ACCESS_KEY"
    s3_secret_key: str = "LOCAL_SECRET_KEY"
    s3_bucket_name: str = "datasets"
    s3_secure: bool = False


server_settings = ServerSettings()
app_settings = AppSettings()

db_settings = DatabaseSettings()
db = databases.Database(db_settings.sqlalchemy_database_url)

minio_settings = MinioSettings()
