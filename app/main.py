import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

import aiosqlite

from app.config import settings
from app.db.database import get_db, init_db
from app.api.tasks import router as tasks_router
from app.middleware.logging import RequestLoggingMiddleware
from app.services.task_service import check_db

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    logging.getLogger("app").info("Database initialized")
    yield
    logging.getLogger("app").info("Shutting down")


app = FastAPI(title="Task Service", version="1.0.0", lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(tasks_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logging.getLogger("app").exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/healthz", tags=["health"])
async def healthz() -> dict:
    return {"status": "ok"}


@app.get("/readyz", tags=["health"])
async def readyz(db: aiosqlite.Connection = Depends(get_db)) -> dict:
    await check_db(db)
    return {"status": "ok"}
