# Data Dictionary

## 1. Tables Overview

| Table | Description |
|---|---|
| `collection_runs` | Records execution time, source, status, query count, and error reasons. |
| `raw_quotes` | Append-only raw parsed flight quotes with pointer to stored evidence. |
| `normalised_quotes` | Validated, canonical observations with QA anomaly flags. |
| `route_weights` | Directional route weights with validity windows and source notes. |
| `lead_time_weights` | Horizon booking window weights with rationale. |
| `route_daily_prices` | Daily median price $P(r,h,t)$ and coverage metrics. |
| `route_indices` | Daily/weekly/monthly index series for individual routes. |
| `headline_indices` | National composite APIx series. |
| `quality_events` | Log of imputation, exclusion, and outlier suppression events. |
| `benchmark_observations` | Official comparator data (DGCA passenger traffic and fares). |

## 2. Fare Component Decomposition Fields
- `base_fare`: Core airline tariff before statutory charges.
- `airline_surcharge`: Fuel, booking fees, or airline convenience fees.
- `taxes_and_statutory_fees`: GST, User Development Fee (UDF), Passenger Service Fee (PSF).
- `mandatory_total_fare`: Final payable price for ticket issuance without optional ancillaries.
- `currency`: ISO-4217 code (INR).

