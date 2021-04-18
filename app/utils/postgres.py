from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    """Build a PostgreSQL specific data type for SQLAlchemy expressions."""
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
