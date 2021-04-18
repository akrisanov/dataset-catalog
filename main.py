from sentry_sdk import init as initialize_sentry
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.application import app
from app.settings.base import app_settings, server_settings


if app_settings.sentry_dsn:
    initialize_sentry(
        dsn=app_settings.sentry_dsn,
        integrations=[SqlalchemyIntegration()],
    )
    app.add_middleware(SentryAsgiMiddleware)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=server_settings.host,
        port=server_settings.port,
        root_path=server_settings.root_path,
        log_level=server_settings.log_level,
        log_config="logging.yaml",
        debug=server_settings.debug,
        reload=server_settings.reload,
        reload_dirs=server_settings.reload_dirs,
        workers=server_settings.workers,
    )
