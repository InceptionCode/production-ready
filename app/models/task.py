from typing import Any

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: str


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    completed: bool | None = None


def task_from_row(row: Any) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        completed=bool(row["completed"]),
        created_at=row["created_at"],
    )
