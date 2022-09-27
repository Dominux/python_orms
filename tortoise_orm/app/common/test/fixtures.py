from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from app.app import app
from app import config

DB_URL = "sqlite://:memory:"


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=config.DB_URI,
        modules={"models": ["app.models"]},
        _create_db=create_db,
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture()
async def async_client() -> AsyncGenerator:
    await init()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    await Tortoise._drop_databases()
