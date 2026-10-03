.PHONY: run seed scrape test lint help

help:
	@echo "Aero-Metrics (APIx) Clean Commands:"
	@echo "  make run    - Start the FastAPI service & interactive dashboard"
	@echo "  make seed   - Seed database with 30-day historical index & DGCA benchmarks"
	@echo "  make scrape - Fetch real-time live flight prices from Google Flights"
	@echo "  make test   - Run automated test suite (Pytest)"
	@echo "  make lint   - Run code linter and quality checks (Ruff)"

run:
	uvicorn apps.api.main:app --reload

seed:
	python scripts/seed_30d_history.py

scrape:
	python scripts/fetch_google_flights.py --origin DEL --destination BOM --lead-days 7

test:
	pytest tests/

lint:
	ruff check .
