import os
from collections.abc import AsyncGenerator

import aiosqlite

from app.config import settings

DB_PATH: str = settings.database_url


async def init_db() -> None:
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id         TEXT PRIMARY KEY,
                title      TEXT NOT NULL,
                completed  INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.commit()


async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db
