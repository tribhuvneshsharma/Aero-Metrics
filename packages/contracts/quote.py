from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid


class SourceMode(str, Enum):
    LIVE_PERMITTED = "live_permitted"
    REPLAY_FIXTURE = "replay_fixture"
    SYNTHETIC_DEMO = "synthetic_demo"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "available"
    SOLD_OUT = "sold_out"
    CANCELLED = "cancelled"
    NO_RESULT = "no_result"


class ValidationStatus(str, Enum):
    VALID = "valid"
    EXCLUDED = "excluded"
    FLAGGED = "flagged"


class RawQuote(BaseModel):
    """
    Immutable raw quote schema representing a direct parse from a collection run.
    Section 4.1 of SIH PS 56 Blueprint.
    """
    quote_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    collection_run_id: str
    source: str
    source_mode: SourceMode
    collected_at: datetime
    origin: str
    destination: str
    travel_date: date
    lead_time_days: int
    carrier: str
    flight_number: str
    departure_local_time: datetime
    fare_class: str = "ECONOMY"
    base_fare: Optional[float] = None
    airline_surcharge: Optional[float] = 0.0
    taxes_and_statutory_fees: Optional[float] = 0.0
    airport_or_udf_fee: Optional[float] = 0.0
    ota_convenience_fee: Optional[float] = 0.0
    mandatory_total_fare: float
    currency: str = "INR"
    availability_status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    raw_evidence_uri: Optional[str] = None
    parser_version: str = "1.0.0"


class NormalisedQuote(RawQuote):
    """
    Normalised, verified quote with canonical flight keys and QA flags.
    """
    canonical_key: str
    validation_status: ValidationStatus = ValidationStatus.VALID
    quality_status: str = "pass"
    flags: List[str] = Field(default_factory=list)
    pipeline_version: str = "0.1.0"
    normalised_at: datetime = Field(default_factory=datetime.utcnow)

