import pathlib

import pytest
import shortuuid
from httpx import AsyncClient
from mimesis import Generic

from app.repositories import datasets_repo
from app.utils.storage import storage


@pytest.mark.asyncio
async def test_get_datasets_zero_items(client: AsyncClient):
    """Tests that API responds with empty list of datasets when no records in the database."""
    resp = await client.get("/datasets")
    data = resp.json()

    assert resp.status_code == 200
    assert data["total_count"] == 0
    assert data["datasets"] == []


@pytest.fixture
async def posts_dataset_row():
    g = Generic("en")
    dataset_row = await datasets_repo.insert_row(
        {
            "name": g.business.company(),
            "path": f"{shortuuid.uuid()}/allposts.csv",
        }
    )
    yield dataset_row
    await datasets_repo.delete_row(name=dataset_row["name"])


@pytest.mark.asyncio
async def test_get_datasets_witn_one_item(client: AsyncClient, posts_dataset_row):
    """Tests that API responds with one dataset"""

    resp = await client.get("/datasets")
    data = resp.json()

    assert resp.status_code == 200
    assert data["total_count"] == len(data["datasets"]) == 1
    assert data["page"] == 1
    assert data["max_per_page"] == 10


@pytest.mark.asyncio
async def test_get_datasets_with_one_item_second_page(
    client: AsyncClient, posts_dataset_row
):
    """Tests that API responds with no dataset when requesting second page."""

    resp = await client.get("/datasets?page=2&max_per_page=5")
    data = resp.json()

    assert resp.status_code == 200
    assert data["total_count"] == 1
    assert data["page"] == 2
    assert data["max_per_page"] == 5
    assert len(data["datasets"]) == 0


@pytest.fixture
def upload_request():
    dataset = pathlib.Path.cwd() / "tests/data/heart.csv"

    return {
        "data": {"dataset_name": "Heart"},
        "files": {"dataset_file": open(dataset, "rb")},
        "headers": {"content-md5": "4740fea127fd35cb58a20e2bcc8bf586"},
    }


@pytest.mark.asyncio
async def test_upload_dataset(client: AsyncClient, upload_request, monkeypatch):
    """Tests that API responds with a successful response when file upload is finished."""

    async def mock_upload(bucket_name, object_name, data, metadata, length, part_size):
        return True

    monkeypatch.setattr(storage, "put_object", mock_upload)

    resp = await client.put("/datasets", **upload_request)
    data = resp.json()

    assert resp.status_code == 200
    assert data["detail"] == "File successfully uploaded to the storage."

    dataset_rows = await datasets_repo.get_rows()
    assert len(dataset_rows) == 1

    await datasets_repo.delete_rows()
