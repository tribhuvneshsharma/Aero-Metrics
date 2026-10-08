# Aero-Metrics — Real-time Airfare Price Index (APIx)

> **Smart India Hackathon (SIH 2026) — Problem Statement 56**  
> An automated, high-frequency airfare price measurement platform converting online airfare quotes into transparent, governed, route-level and headline indices for NSO and RBI retail inflation analysis.

## 🚀 Live Prototype Links (For SIH Judges)
* **Frontend Dashboard (Vercel):** [https://aero-metrics-jet.vercel.app/](https://aero-metrics-jet.vercel.app/)
* **Backend API Docs (Render):** [https://aero-metrics.onrender.com/dashboard](https://aero-metrics.onrender.com/dashboard)
* **Live Scraper Endpoint:** [POST /v1/collect/live](https://aero-metrics.onrender.com/docs#/default/trigger_live_scrape_v1_collect_live_post) (Trigger real-time fetch)

---

## 1. Clean System Architecture

```text
Aero-Metrics/
├── apps/
│   ├── api/                       # FastAPI policy service & OpenAPI docs
│   └── dashboard/                 # Next.js interactive policy dashboard
├── packages/
│   ├── collectors/                # Live Google Flights scraping engine (IndiGo, AI, Akasa)
│   │   ├── base.py                # Abstract BaseFareCollector contract
│   │   └── google_flights.py      # Real-time multi-airline live scraper
│   ├── contracts/                 # Pydantic schemas (RawQuote, NormalisedQuote, HeadlineIndex)
│   ├── db/                        # SQLAlchemy database models, session & SQLite/Postgres engine
│   ├── index_engine/              # Mathematical methodology (Medians, RouteIndex, Headline APIx)
│   └── pipeline/                  # Outlier cleaning, deduplication & QA scoring
├── data/
│   └── reference/                 # 16 directional route basket & lead-time weights
│       ├── route_basket.csv       # DGCA traffic-weighted 16 domestic city pairs
│       └── lead_time_weights.csv  # T+1, T+7, T+15, T+30, T+45 booking horizon weights
├── scripts/
│   ├── fetch_google_flights.py    # CLI tool to test live airfare extraction for any route
│   └── seed_30d_history.py        # Generates 30-day historical time-series & DGCA benchmarks
├── tests/
│   ├── e2e/test_smoke.py          # End-to-end API endpoint smoke tests
│   └── integration/               # Pipeline data validation & QA score tests
├── aerometrics.db                 # Zero-config SQLite database (or PostgreSQL via DATABASE_URL)
└── pyproject.toml                 # Centralized tooling (Pytest, Ruff, MyPy)
```

---

## 2. Core Capabilities (SIH PS 56 Deliverables)

| Component | Status | Details |
|---|---|---|
| **Multi-Source Scraping** | ✅ Active | Real-time extraction of live Indian airlines (Air India, IndiGo, Akasa, SpiceJet) via Google Flights with rate-limiting safeguards. |
| **Data Cleaning Pipeline** | ✅ Active | Filters negative/zero fares, removes outliers, separates base fare vs statutory taxes/fees, and canonicalises flight keys. |
| **30-Day Historical Database** | ✅ Active | Persistent SQLite/Postgres database seeded with 30 days of daily indices and DGCA benchmark comparisons. |
| **Index Engine (APIx)** | ✅ Active | Computes route-horizon daily medians $P(r,h,t)$, advance-booking aggregates, and weighted National Headline APIx. |
| **Policy API (FastAPI)** | ✅ Active | Typed REST endpoints with Swagger docs at `https://aero-metrics.onrender.com/docs` ready for NSO/RBI integration. |

---

## 3. Quickstart Guide

### 1. Seed the 30-Day Historical Database
Populate the database with 30 days of continuous daily index observations and official DGCA benchmarks:

```bash
python scripts/seed_30d_history.py
```

### 2. Extract Live Airfares (On-Demand)
Query live flights and prices in native INR (`₹`) for any domestic city pair:

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
* **Interactive API Documentation:** [https://aero-metrics.onrender.com/docs](https://aero-metrics.onrender.com/docs)
* **Latest Headline APIx:** [https://aero-metrics.onrender.com/v1/index/headline](https://aero-metrics.onrender.com/v1/index/headline)
* **30-Day Historical Time-Series:** [https://aero-metrics.onrender.com/v1/index/timeseries?days=30](https://aero-metrics.onrender.com/v1/index/timeseries?days=30)
* **Sector-Wise Route Heatmap:** [https://aero-metrics.onrender.com/v1/routes/heatmap](https://aero-metrics.onrender.com/v1/routes/heatmap)
* **Lead-Time Elasticity Curves:** [https://aero-metrics.onrender.com/v1/analytics/elasticity](https://aero-metrics.onrender.com/v1/analytics/elasticity)
* **DGCA 30-Day Backtest Comparison:** [https://aero-metrics.onrender.com/v1/backtest/dgca](https://aero-metrics.onrender.com/v1/backtest/dgca)

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
