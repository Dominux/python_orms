import pytest
from httpx import AsyncClient
from fastapi import status

from tortoise_orm.common.test.fixtures import async_client as client
from tortoise_orm.models import User, UserSchema


pytestmark = pytest.mark.asyncio


async def test_create_user(client: AsyncClient):
    # Creating user via API
    username = "lol"
    response = await client.post("/users", json={"username": username})

    # Checking response
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["username"] == username
    assert (user_id := data.get("id"))

    # Checking in db
    user = await UserSchema.from_queryset_single(User.get(id=user_id))
    assert user.username == username
