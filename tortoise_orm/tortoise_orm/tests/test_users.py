import pytest
from httpx import AsyncClient
from fastapi import status

from tortoise_orm.common.test.fixtures import async_client as client
from tortoise_orm.models import User


pytestmark = pytest.mark.asyncio


async def test_create_user(client: AsyncClient):
    username = "lol"
    response = await client.post("/users", json={"username": username})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["username"] == username
    assert "id" == data["id"]
    user_id = data["id"]
