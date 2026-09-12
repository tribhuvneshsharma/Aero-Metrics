from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class QualityMetadata(BaseModel):
    coverage_ratio: float = Field(..., description="Proportion of weighted basket successfully observed")
    imputed_weight: float = Field(default=0.0, description="Weight of routes/horizons currently using imputed prices")
    excluded_weight: float = Field(default=0.0, description="Weight of routes/horizons excluded due to missingness > 2 days")
    quality_status: str = Field(default="pass", description="pass, partial_coverage, or degraded")
    quality_score: float = Field(default=1.0, description="Composite statistical quality score [0.0 - 1.0]")
    methodology_version: str = "0.1.0"
    weight_version: str = "0.1.0"
    source_mode: str = "replay_fixture"


class RouteDailyPrice(BaseModel):
    """
    Daily median price for a specific route and booking horizon.
    P(r, h, t)
    """
    route_code: str
    origin: str
    destination: str
    horizon: str
    lead_time_days: int
    collection_date: date
    median_fare: float
    observation_count: int
    min_fare: Optional[float] = None
    max_fare: Optional[float] = None
    imputed: bool = False
    imputation_method: Optional[str] = None


class RouteIndex(BaseModel):
    """
    Aggregated price index for a specific route across horizons.
    RouteIndex(r, t) = 100 * sum(v(h) * R(r, h, t))
    """
    route_code: str
    index_date: date
    frequency: Frequency = Frequency.DAILY
    index_value: float
    coverage_ratio: float
    quality_metadata: QualityMetadata
    computed_at: datetime = Field(default_factory=datetime.utcnow)


class HeadlineIndex(BaseModel):
    """
    National Headline APIx (Airfare Price Index).
    APIx(t) = sum(w(r) * RouteIndex(r, t))
    """
    index_date: date
    frequency: Frequency = Frequency.DAILY
    headline_apix: float
    one_day_change_pct: Optional[float] = None
    seven_day_change_pct: Optional[float] = None
    thirty_day_change_pct: Optional[float] = None
    quality_metadata: QualityMetadata
    computed_at: datetime = Field(default_factory=datetime.utcnow)
