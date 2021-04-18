from typing import List

from sqlalchemy import Column, Table, and_, func, select

from app.settings.base import db
from app.utils.query import extract_column


class CrudMixin:
    def __init__(self, table: Table) -> None:
        self.table = table

    async def get_rows_count(self):
        """Retrieve rows count."""
        query = select([func.count()]).select_from(self.table)
        return await db.fetch_val(query)

    async def get_rows(
        self,
        page: int = 1,
        max_per_page: int = 10,
        columns: List[Column] = None,
    ):
        """Select all rows from a table."""
        if not columns:
            columns = self.table.c

        offset_ = (page - 1) * max_per_page
        query = (
            select(columns).select_from(self.table).limit(max_per_page).offset(offset_)
        )

        return await db.fetch_all(query)

    async def get_row(self, **where_kwargs):
        """Select a table row matching at least one column value."""
        query = select(self.table.c).where(
            and_(*(extract_column(self.table, k) == v for k, v in where_kwargs.items()))
        )
        return await db.fetch_one(query)

    async def insert_row(self, data: dict):
        """Insert a table row and returns inserted values."""
        query = self.table.insert().values(**data).returning(*self.table.c)
        return await db.fetch_one(query)

    async def delete_row(self, **where_kwargs):
        """Delete a table row matching at least one column value."""
        query = self.table.delete().where(
            and_(*(extract_column(self.table, k) == v for k, v in where_kwargs.items()))
        )
        return await db.execute(query)

    async def delete_rows(self, **where_kwargs):
        """Delete all the rows in a table."""
        query = self.table.delete()
        return await db.execute(query)
