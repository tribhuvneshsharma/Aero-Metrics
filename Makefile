.PHONY: up down migrate seed-demo collect process compute-index test lint demo help

help:
	@echo "Aero-Metrics (APIx) Monorepo Commands:"
	@echo "  make up            - Start database, object store, API, dashboard"
	@echo "  make down          - Stop local docker services"
	@echo "  make migrate       - Apply database schema migrations"
	@echo "  make seed-demo     - Load deterministic 30-day replay data"
	@echo "  make collect       - Run permitted collection job"
	@echo "  make process       - Clean and normalise pending raw quotes"
	@echo "  make compute-index - Calculate all affected route & headline indices"
	@echo "  make test          - Run full automated test suite"
	@echo "  make lint          - Run formatting, type, and lint checks"
	@echo "  make demo          - Run full vertical demo: seed -> process -> compute -> smoke test"

up:
	docker compose up -d

down:
	docker compose down

migrate:
	python -m packages.db.migrate

seed-demo:
	python -m packages.collector_core.replay --seed-file data/replay-30d/seed.json

collect:
	python -m packages.collector_core.runner

process:
	python -m packages.pipeline.process

compute-index:
	python -m packages.index_engine.calculator

test:
	pytest tests/

lint:
	ruff check .
	mypy packages/ apps/

demo: seed-demo process compute-index test
	@echo "=== Demo verification successful! API & Dashboard are ready. ==="
