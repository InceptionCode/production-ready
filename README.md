# Production-Ready Task Service

A small, production-minded task management API built with FastAPI and SQLite. Designed as a portfolio project demonstrating clean structure, Docker packaging, health checks, environment-based config, and production engineering basics.

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| Server | Uvicorn |
| Database | SQLite via aiosqlite |
| Config | pydantic-settings |
| Tests | pytest + httpx |
| Container | Docker |

---

## Local Setup

**Requirements:** Python 3.12+

```bash
# Clone and enter the project
cd production-ready

# Copy env file and (optionally) edit
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run the app
make run
# or: uvicorn app.main:app --reload --port 8000
```

The API is now available at `http://localhost:8000`.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | Environment name (development / production) |
| `DATABASE_URL` | `./data/tasks.db` | Path to SQLite database file |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `PORT` | `8000` | Port the server listens on |

---

## Endpoints

| Method | Path | Description | Request Body | Response |
|---|---|---|---|---|
| GET | `/healthz` | Liveness check | — | `{"status": "ok"}` |
| GET | `/readyz` | Readiness check (DB ping) | — | `{"status": "ok"}` |
| GET | `/api/tasks/` | List all tasks | — | `Task[]` |
| POST | `/api/tasks/` | Create a task | `{"title": "..."}` | `Task` (201) |
| PATCH | `/api/tasks/{id}` | Update a task | `{"title"?: "...", "completed"?: bool}` | `Task` |
| DELETE | `/api/tasks/{id}` | Delete a task | — | 204 No Content |

**Task schema:**
```json
{
  "id": "uuid",
  "title": "string",
  "completed": false,
  "created_at": "2025-01-01T00:00:00+00:00"
}
```

**Interactive docs:** `http://localhost:8000/docs`

---

## Running Tests

```bash
make test
# or: pytest tests/ -v
```

Tests use an isolated in-memory SQLite database per test — no shared state.

---

## Docker

**Build:**
```bash
make docker-build
# or: docker build -t task-service:latest .
```

**Run:**
```bash
make docker-run
# or: docker compose up
```

The SQLite database is persisted in a named Docker volume (`db_data`) so data survives container restarts.

**Stop:**
```bash
docker compose down
```

---

## Project Structure

```
production-ready/
├── app/
│   ├── main.py              # App entry point: lifespan, middleware, routes, health
│   ├── config.py            # Environment-based configuration
│   ├── api/
│   │   └── tasks.py         # Task route handlers
│   ├── models/
│   │   └── task.py          # Pydantic request/response models
│   ├── services/
│   │   └── task_service.py  # Business logic and SQL queries
│   ├── db/
│   │   └── database.py      # DB init, connection dependency
│   └── middleware/
│       └── logging.py       # Request logging middleware
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_health.py       # Health endpoint tests
│   └── test_tasks.py        # Task CRUD and validation tests
├── infra/docker/            # Future: nginx, compose overrides
├── docs/                    # Future: ADRs, runbooks
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── .env.example
```

---

## Design Notes

- **Direct SQL over ORM:** The schema is one table. Raw parameterized SQL is clearer and avoids SQLAlchemy session lifecycle complexity.
- **aiosqlite:** Keeps the entire stack async-native. SQLite handles concurrent reads well; writes are serialized at the file level.
- **Non-root Docker user:** The container runs as `appuser` rather than root — a basic but important production security practice.
- **Layer-optimized Dockerfile:** Dependencies are installed before source is copied, so editing app code does not bust the pip cache layer.
- **SQLite write concurrency:** SQLite supports one writer at a time. This is fine for a single-container deployment. If horizontal scaling is needed in a later phase, PostgreSQL would be the upgrade path.

---

## Next Phases (not yet implemented)

- Phase 2: Push to ECR, deploy on ECS Fargate
- Phase 3: Terraform infrastructure
- Phase 4: GitHub Actions CI/CD
- Phase 5: CloudWatch metrics and alerting
