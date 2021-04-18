from fastapi import FastAPI

from app.handlers import services_router
from app.settings.base import app_settings, db


tags_metadata = [
    {"name": "services", "description": "Service methods"},
    {"name": "datasets", "description": "Dataset catalog methods"},
]

app = FastAPI(
    title="Dataset Catalog API",
    version="0.1",
    description="Private HTTP API for managing dataset catalog.",
    openapi_tags=tags_metadata,
    docs_url=app_settings.docs_url,
    openapi_url=app_settings.openapi_url,
    redoc_url=None,
)

app.include_router(services_router, tags=["services"])


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
