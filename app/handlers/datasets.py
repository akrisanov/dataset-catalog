from fastapi import APIRouter, Depends

from app.repositories import datasets_repo
from app.schemas import DatasetList, page_data, paginator_params


datasets_router = APIRouter()


@datasets_router.get(
    "/datasets",
    response_model=DatasetList,
    summary="Get list of uploaded datasets",
)
async def get_datasets(paginator: dict = Depends(paginator_params)):
    total_count = await datasets_repo.get_rows_count()

    if total_count > 0:
        dataset_rows = await datasets_repo.get_rows(
            paginator["page"], paginator["max_per_page"]
        )
    else:
        dataset_rows = []

    return {
        **page_data(total_count, paginator),
        "datasets": dataset_rows,
    }
