# Aero-Metrics â€” Real-time Airfare Price Index (APIx)

> **Smart India Hackathon (SIH 2026) â€” Problem Statement 56**  
> An automated, high-frequency airfare price measurement platform converting online airfare quotes into transparent, governed, route-level and headline indices for NSO and RBI retail inflation analysis.
## 🚀 Live Prototype Links (For SIH Judges)
* **Frontend Dashboard:** [https://aero-metrics.vercel.app](https://aero-metrics.vercel.app)
* **Backend API Docs:** [https://aero-metrics.onrender.com/docs](https://aero-metrics.onrender.com/docs)
* **Live Scraper Endpoint:** [POST /v1/collect/live](https://aero-metrics.onrender.com/docs#/default/trigger_live_scrape_v1_collect_live_post) (Trigger real-time fetch)
---

## 1. Clean System Architecture

```text
Aero-Metrics/
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ api/                       # FastAPI policy service & OpenAPI docs
â”‚   â””â”€â”€ dashboard/                 # Next.js interactive policy dashboard
â”œâ”€â”€ packages/
â”‚   â”œâ”€â”€ collectors/                # Live Google Flights scraping engine (IndiGo, AI, Akasa)
â”‚   â”‚   â”œâ”€â”€ base.py                # Abstract BaseFareCollector contract
â”‚   â”‚   â””â”€â”€ google_flights.py      # Real-time multi-airline live scraper
â”‚   â”œâ”€â”€ contracts/                 # Pydantic schemas (RawQuote, NormalisedQuote, HeadlineIndex)
â”‚   â”œâ”€â”€ db/                        # SQLAlchemy database models, session & SQLite/Postgres engine
â”‚   â”œâ”€â”€ index_engine/              # Mathematical methodology (Medians, RouteIndex, Headline APIx)
â”‚   â””â”€â”€ pipeline/                  # Outlier cleaning, deduplication & QA scoring
â”œâ”€â”€ data/
â”‚   â””â”€â”€ reference/                 # 16 directional route basket & lead-time weights
â”‚       â”œâ”€â”€ route_basket.csv       # DGCA traffic-weighted 16 domestic city pairs
â”‚       â””â”€â”€ lead_time_weights.csv  # T+1, T+7, T+15, T+30, T+45 booking horizon weights
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ fetch_google_flights.py    # CLI tool to test live airfare extraction for any route
â”‚   â””â”€â”€ seed_30d_history.py        # Generates 30-day historical time-series & DGCA benchmarks
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ e2e/test_smoke.py          # End-to-end API endpoint smoke tests
â”‚   â””â”€â”€ integration/               # Pipeline data validation & QA score tests
â”œâ”€â”€ aerometrics.db                 # Zero-config SQLite database (or PostgreSQL via DATABASE_URL)
â””â”€â”€ pyproject.toml                 # Centralized tooling (Pytest, Ruff, MyPy)
```

---

## 2. Core Capabilities (SIH PS 56 Deliverables)

| Component | Status | Details |
|---|---|---|
| **Multi-Source Scraping** | âœ… Active | Real-time extraction of live Indian airlines (Air India, IndiGo, Akasa, SpiceJet) via Google Flights with rate-limiting safeguards. |
| **Data Cleaning Pipeline** | âœ… Active | Filters negative/zero fares, removes outliers, separates base fare vs statutory taxes/fees, and canonicalises flight keys. |
| **30-Day Historical Database** | âœ… Active | Persistent SQLite/Postgres database seeded with 30 days of daily indices and DGCA benchmark comparisons. |
| **Index Engine (APIx)** | âœ… Active | Computes route-horizon daily medians $P(r,h,t)$, advance-booking aggregates, and weighted National Headline APIx. |
| **Policy API (FastAPI)** | âœ… Active | Typed REST endpoints with Swagger docs at `http://127.0.0.1:8000/docs` ready for NSO/RBI integration. |

---

## 3. Quickstart Guide

### 1. Seed the 30-Day Historical Database
Populate the database with 30 days of continuous daily index observations and official DGCA benchmarks:

```bash
python scripts/seed_30d_history.py
```

### 2. Extract Live Airfares (On-Demand)
Query live flights and prices in native INR (`â‚¹`) for any domestic city pair:

```bash
# E.g., Delhi (DEL) to Mumbai (BOM) departing in 7 days
python scripts/fetch_google_flights.py --origin DEL --destination BOM --lead-days 7

# E.g., Mumbai (BOM) to Bangalore (BLR) departing in 14 days
python scripts/fetch_google_flights.py --origin BOM --destination BLR --lead-days 14
```

### 3. Run the Backend API Service
Start the FastAPI server:

```bash
uvicorn apps.api.main:app --reload
```

Open your browser:
* **Interactive API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Latest Headline APIx:** [http://127.0.0.1:8000/v1/index/headline](http://127.0.0.1:8000/v1/index/headline)
* **30-Day Historical Time-Series:** [http://127.0.0.1:8000/v1/index/timeseries?days=30](http://127.0.0.1:8000/v1/index/timeseries?days=30)
* **Sector-Wise Route Heatmap:** [http://127.0.0.1:8000/v1/routes/heatmap](http://127.0.0.1:8000/v1/routes/heatmap)
* **Lead-Time Elasticity Curves:** [http://127.0.0.1:8000/v1/analytics/elasticity](http://127.0.0.1:8000/v1/analytics/elasticity)
* **DGCA 30-Day Backtest Comparison:** [http://127.0.0.1:8000/v1/backtest/dgca](http://127.0.0.1:8000/v1/backtest/dgca)

---

## 4. Mathematical Methodology

1. **Route-Horizon Median Price:**
   $$P(r,h,t) = \text{median}(\text{valid canonical total fares for route } r, \text{horizon } h, \text{date } t)$$
2. **Price Relative:**
   $$R(r,h,t) = \frac{P(r,h,t)}{P(r,h,0)}$$
3. **Route Price Index Across Horizons:**
   $$\text{RouteIndex}(r,t) = 100 \times \sum_{h} \left[ v(h) \times R(r,h,t) \right]$$
   *(Default weights $v(h)$: T+1: 10%, T+7: 25%, T+15: 30%, T+30: 20%, T+45: 15%)*
4. **Headline National APIx:**
   $$\text{APIx}(t) = \sum_{r} \left[ w(r) \times \text{RouteIndex}(r,t) \right]$$
   *(Weights $w(r)$ derived from DGCA passenger traffic volume proxies).*

---

## 5. Automated Tests & Code Quality

Run tests and linting with zero configuration:

```bash
# Run test suite (10/10 tests passing)
pytest tests/

# Run code linter
ruff check .
```

