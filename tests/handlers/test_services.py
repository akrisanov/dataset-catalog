import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"detail": "OK"}
