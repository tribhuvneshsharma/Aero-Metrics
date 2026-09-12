from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from packages.contracts import HeadlineIndex, QualityMetadata
from datetime import date

app = FastAPI(
    title="Aero-Metrics (APIx) Policy Service",
    version="0.1.0",
    description="High-frequency supplementary airfare-price measurement API for institutional analysis."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "apix-api", "version": "0.1.0"}


@app.get("/v1/index/headline", response_model=HeadlineIndex, tags=["Index"])
def get_headline_index():
    return HeadlineIndex(
        index_date=date.today(),
        headline_apix=104.35,
        one_day_change_pct=0.45,
        seven_day_change_pct=1.82,
        thirty_day_change_pct=4.35,
        quality_metadata=QualityMetadata(
            coverage_ratio=0.985,
            imputed_weight=0.0,
            excluded_weight=0.0,
            quality_status="pass",
            quality_score=0.96,
            methodology_version="0.1.0",
            weight_version="0.1.0",
            source_mode="replay_fixture"
        )
    )
