from app.models import datasets_table

from .crud_mixin import CrudMixin


class DatasetsRepository(CrudMixin):
    """Database interface to query datasets table."""


datasets_repo = DatasetsRepository(
    table=datasets_table,
)
