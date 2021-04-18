# TODO: Using Asyncio with Alembic
# https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.settings.base import db_settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USER", db_settings.db_user)
config.set_section_option(section, "DB_PASS", db_settings.db_pass)
config.set_section_option(section, "DB_HOST", db_settings.db_host)
config.set_section_option(section, "DB_PORT", db_settings.db_port)
config.set_section_option(section, "DB_NAME", db_settings.db_name)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

target_metadata = [  # type: ignore
    # TODO: add your model's MetaData object here for 'autogenerate' support
]


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=db_settings.sqlalchemy_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def process_revision_directives(context, revision, directives):
        """
        Don’t Generate Empty Migrations with Autogenerate
        https://alembic.sqlalchemy.org/en/latest/cookbook.html#don-t-generate-empty-migrations-with-autogenerate
        """
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=db_settings.sqlalchemy_database_url,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
