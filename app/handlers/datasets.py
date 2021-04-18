import shortuuid

from app.repositories import datasets_repo
from app.schemas import DatasetList, Message, page_data, paginator_params
from app.utils.logging import app_logger
from app.utils.storage import S3Exception, bucket_name, storage


from fastapi import (  # isort: skip
    APIRouter,
    Body,
    Depends,
    File,
    Header,
    HTTPException,
    UploadFile,
    status,
)


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


@datasets_router.put(
    "/datasets",
    response_model=Message,
    status_code=status.HTTP_200_OK,  # Follows AWS convention
    summary="Upload dataset to the storage",
    description="This API endpoint uses "
    "the [UploadFile](https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile) "
    "interface to deal with memory consumption issues during big file uploads. "
    "It's based on Python's `tempfile.SpooledTemporaryFile` which writes upload file to disk "
    "whether it exceeds the buffer size limit or we ask for a file descriptor. "
    "Also, keep in mind that there is no async/non-blocking way to work with the Linux file "
    "system yet, and FastAPI will spawn a new thread for file upload. ",
)
async def upload_dataset(
    dataset_name: str = Body(..., description="Dataset name", max_length=255),
    dataset_file: UploadFile = File(..., description="Dataset file"),
    content_md5: str = Header(
        ...,
        description="This value is used to check that dataset data is not corrupted "
        "traversing the network.",
    ),
):
    storage_path = f"{shortuuid.uuid()}/{dataset_file.filename}"
    metadata = {"md5chksum": content_md5}

    try:
        # Uploads a stream of bytes to the storage using ThreadPool with num_parallel_uploads=3
        storage.put_object(
            bucket_name=bucket_name,
            object_name=storage_path,
            # Unfortunately, FastAPI doesn't provide direct access to the upload multipart body.
            # Therefore, we can't iterate over body parts, and upload chunks directly.
            data=dataset_file.file,
            metadata=metadata,
            length=-1,
            part_size=1024 * 1024 * 10,  # 10 MB
        )
    except S3Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dataset can not be uploaded. Please try again.",
        )

    dataset_row = await datasets_repo.insert_row(
        {
            "name": dataset_name,
            "path": storage_path,
        }
    )
    app_logger.debug(
        f"Dataset `{dataset_row['name']}` successfully uploaded to `{dataset_row['path']}`"
    )

    return {"detail": "File successfully uploaded to the storage."}
