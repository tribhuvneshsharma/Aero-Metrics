# Aero-Metrics — Real-time Airfare Price Index (APIx)

> **SIH 2026 PS 56:** A high-frequency supplementary airfare-price measurement platform converting online airfare quotes into transparent, governed, route-level and headline indices for NSO/RBI-style policy consumers.

---

## 1. Monorepo Architecture & Directory Layout

```text
Aero-Metrics/
├── apps/
│   ├── api/                       # FastAPI service & OpenAPI documentation
│   ├── dashboard/                 # Next.js dashboard & policy visualizations
│   └── scheduler/                 # Fixed collection & index recomputation jobs
├── packages/
│   ├── contracts/                 # Pydantic schemas, JSON Schema & OpenAPI types
│   ├── collector-core/            # Collector interfaces, rate limiting & replay logic
│   ├── collectors/                # Source adapters
│   │   ├── permitted-live-source-a/
│   │   ├── permitted-live-source-b/
│   │   └── replay-demo-source/
│   ├── pipeline/                  # Normalisation, deduplication, QA & outlier rules
│   ├── index-engine/              # Mathematical methodology, aggregation & backtest
│   ├── db/                        # SQLAlchemy models, migrations & repositories
│   └── ui/                        # Reusable UI component library
├── data/
│   ├── reference/                 # 16 directional route basket, weights, airports
│   ├── fixtures/                  # Sanitised raw responses
│   ├── replay-30d/                # 30 dated snapshots for deterministic judge demo
│   └── synthetic/                 # Clearly-labelled synthetic generator
├── docs/
│   ├── architecture.md            # System architecture and data flow
│   ├── methodology.md             # Aggregation formulas and imputation rules
│   ├── data-dictionary.md         # Field definitions and DB schema
│   ├── source-governance.md       # Ethical web collection and compliance
│   ├── backtest.md                # 30-day replay and DGCA comparison
│   ├── api-guide.md               # Endpoints and payload documentation
│   └── judge-demo.md              # 90-second judging presentation flow
├── infra/
│   ├── postgres/                  # Database container setup & init scripts
│   ├── minio/                     # Object store for raw quotes evidence
│   └── monitoring/                # Service health & metrics
├── tests/
│   ├── integration/               # Pipeline, imputation, and weighting tests
│   └── e2e/                       # End-to-end API and UI smoke tests
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

---

## 2. Six-Person Team Responsibility Matrix

| Member | Role & Mission | Module Ownership |
|---|---|---|
| **Member 1** | Product Lead / Platform Engineer | Repo, Docker, DB, CI/CD, integration, narrative |
| **Member 2** | Collection & Compliance Engineer | Adapter framework, permitted collectors, replay demo |
| **Member 3** | Data Engineer / QA Owner | Cleaning, normalisation, quality score, data dictionary |
| **Member 4** | Economist / Data Scientist | Basket, weights, APIx methodology, 30-day backtest |
| **Member 5** | Backend Engineer | FastAPI, DB repositories, API docs, scheduler wiring |
| **Member 6** | Frontend & Storytelling Engineer | Dashboard, demo UX, charts, presentation assets |

---

## 3. Quickstart

### Prerequisites
- Python 3.12+
- Node.js 20+ & pnpm
- Docker & Docker Compose

### Commands
```bash
# 1. Start database & object store
make up

# 2. Seed deterministic 30-day replay data
make seed-demo

# 3. Clean and normalise quotes
make process

# 4. Compute route and headline indices
make compute-index

# 5. Run test suite
make test

# Full End-to-End Vertical Demo
make demo
```

---

## 4. Methodology Summary
- **Routes**: 16 directional domestic corridors (summing to 1.0).
- **Horizons**: T+1, T+7, T+15, T+30, T+45 booking windows.
- **Route-Horizon Price**: $P(r,h,t) = \text{median}(\text{valid canonical total fares})$.
- **Route Index**: $\text{RouteIndex}(r,t) = 100 \times \sum_h [v(h) \times R(r,h,t)]$.
- **Headline APIx**: $\text{APIx}(t) = \sum_r [w(r) \times \text{RouteIndex}(r,t)]$.
- **Imputation Policy**: Maximum 2 days carry-forward, then dynamic horizon weight re-normalisation with quality status logging.
