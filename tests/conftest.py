# import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from app.main import app as fastapi_app
from app.db import database


@pytest_asyncio.fixture
async def client(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "DB_PATH", db_path)
    await database.init_db()

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac
