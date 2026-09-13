# API Guide

The FastAPI service exposes policy-grade endpoints for macroeconomic researchers, the Reserve Bank of India (RBI), the National Statistical Office (NSO), and the interactive dashboard.

## Endpoints

- `GET /health`: Service health check.
- `GET /v1/index/daily?from=&to=`: Headline APIx daily series with quality metadata.
- `GET /v1/index/weekly`: Weekly aggregated APIx.
- `GET /v1/index/monthly`: Monthly aggregated APIx.
- `GET /v1/routes`: Basket of 16 directional routes with weights and metadata.
- `GET /v1/routes/{route_code}/fares`: Detailed route-level price observations across horizons.
- `GET /v1/routes/{route_code}/index`: Specific route index series.
- `GET /v1/analytics/heatmap`: Matrix of directional routes by date for heatmaps.
- `GET /v1/analytics/lead-time`: Price progression across horizons (T+1 to T+45).
- `GET /v1/data-quality/summary`: Real-time data quality score, coverage ratios, and imputation event logs.
- `GET /v1/methodology`: Active methodology parameters, formulas, and version strings.
- `GET /docs`: Interactive Swagger UI documentation.

