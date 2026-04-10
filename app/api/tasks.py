from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

import aiosqlite

from app.db.database import get_db
from app.models.task import Task, TaskCreate, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=list[Task])
async def list_tasks(db: aiosqlite.Connection = Depends(get_db)) -> list[Task]:
    return await task_service.get_all_tasks(db)


@router.post("/", response_model=Task, status_code=201)
async def create_task(
    body: TaskCreate, db: aiosqlite.Connection = Depends(get_db)
) -> Task:
    return await task_service.create_task(db, body)


@router.patch("/{task_id}", response_model=Task)
async def update_task(
    task_id: str, body: TaskUpdate, db: aiosqlite.Connection = Depends(get_db)
) -> Task:
    result = await task_service.update_task(db, task_id, body)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str, db: aiosqlite.Connection = Depends(get_db)
) -> Response:
    deleted = await task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
