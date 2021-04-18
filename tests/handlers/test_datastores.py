import pytest
import shortuuid
from httpx import AsyncClient
from mimesis import Generic

from app.repositories import datasets_repo


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
            "path": f"/datasets/{shortuuid.uuid()}/allposts.csv",
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
