from sqlalchemy import Table, and_, select

from app.settings.base import db
from app.utils.query import extract_column


class CrudMixin:
    def __init__(self, table: Table) -> None:
        self.table = table

    async def get_row(self, **where_kwargs):
        """Select a table row matching at least one column value."""
        query = select(self.table.c).where(
            and_(*(extract_column(self.table, k) == v for k, v in where_kwargs.items()))
        )
        return await db.fetch_one(query)
