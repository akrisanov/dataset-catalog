import logging

from app.settings.base import server_settings


app_logger = logging.getLogger("application")
app_logger.setLevel(server_settings.log_level.upper())
