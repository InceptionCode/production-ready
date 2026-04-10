from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import aiosqlite

from app.models.task import Task, TaskCreate, TaskUpdate, task_from_row


async def get_all_tasks(db: aiosqlite.Connection) -> list[Task]:
    async with db.execute(
        "SELECT id, title, completed, created_at FROM tasks ORDER BY created_at DESC"
    ) as cursor:
        rows = await cursor.fetchall()
    return [task_from_row(row) for row in rows]


async def create_task(db: aiosqlite.Connection, data: TaskCreate) -> Task:
    task_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT INTO tasks (id, title, completed, created_at) VALUES (?, ?, 0, ?)",
        (task_id, data.title, created_at),
    )
    await db.commit()
    return Task(id=task_id, title=data.title, completed=False, created_at=created_at)


async def update_task(
    db: aiosqlite.Connection, task_id: str, data: TaskUpdate
) -> Task | None:
    async with db.execute(
        "SELECT id, title, completed, created_at FROM tasks WHERE id = ?", (task_id,)
    ) as cursor:
        row = await cursor.fetchone()

    if row is None:
        return None

    updates: dict[str, Any] = {}
    if data.title is not None:
        updates["title"] = data.title
    if data.completed is not None:
        updates["completed"] = int(data.completed)

    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [task_id]
        await db.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
        await db.commit()

    # Re-fetch updated row
    async with db.execute(
        "SELECT id, title, completed, created_at FROM tasks WHERE id = ?", (task_id,)
    ) as cursor:
        updated_row = await cursor.fetchone()

    return task_from_row(updated_row)


async def delete_task(db: aiosqlite.Connection, task_id: str) -> bool:
    async with db.execute(
        "SELECT id FROM tasks WHERE id = ?", (task_id,)
    ) as cursor:
        row = await cursor.fetchone()

    if row is None:
        return False

    await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    await db.commit()
    return True


async def check_db(db: aiosqlite.Connection) -> bool:
    async with db.execute("SELECT 1") as cursor:
        await cursor.fetchone()
    return True
