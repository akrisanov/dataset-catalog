from sqlalchemy import Column, Table


class ColumnNotExists(Exception):
    """A specific exception for debugging purposes."""


def extract_column(table: Table, column_name: str) -> Column:
    """Return a table column or raise an exception with a readable stacktrace."""
    try:
        return table.c[column_name]
    except KeyError:
        raise ColumnNotExists(f"There is no column {column_name} in the {table} table.")
