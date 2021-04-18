from sqlalchemy import (  # isort:skip
    Column,
    DateTime,
    Integer,
    MetaData,
    Table,
    Text,
)

from app.utils.postgres import utcnow


metadata = MetaData()

datasets_table = Table(
    "datasets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, comment="Name of the dataset"),
    # NOTE: https://aws.amazon.com/ru/premiumsupport/knowledge-center/s3-object-key-naming-pattern/
    Column(
        "path",
        Text,
        nullable=False,
        unique=True,
        comment="Relative path to the dataset inside object storage",
    ),
    Column("created_at", DateTime, nullable=False, server_default=utcnow()),
    Column("updated_at", DateTime, server_default=utcnow(), onupdate=utcnow()),
)
