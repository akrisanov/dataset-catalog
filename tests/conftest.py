import os
import warnings
from typing import AsyncGenerator

import alembic
import pytest
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy_utils import create_database, drop_database


os.environ["TESTING"] = "1"


@pytest.fixture(scope="session")
def create_test_():
    from app.settings.base import db_settings

    drop_database(db_settings.sqlalchemy_database_url)
    create_database(db_settings.sqlalchemy_database_url)


@pytest.fixture
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.application import app as app_instance

    return app_instance


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client
