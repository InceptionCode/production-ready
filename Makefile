.PHONY: run test lint docker-build docker-run

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest tests/ -v

lint:
	ruff check app/ tests/

docker-build:
	docker build -t task-service:latest .

docker-run:
	docker compose up
