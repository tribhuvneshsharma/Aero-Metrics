from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float, DateTime, Date, Integer, Boolean
import uuid

Base = declarative_base()


class RawQuoteModel(Base):
    __tablename__ = "raw_quotes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_run_id = Column(String, nullable=False, index=True)
    source = Column(String, nullable=False)
    source_mode = Column(String, nullable=False)
    collected_at = Column(DateTime, nullable=False)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    travel_date = Column(Date, nullable=False)
    lead_time_days = Column(Integer, nullable=False)
    carrier = Column(String, nullable=False)
    flight_number = Column(String, nullable=False)
    departure_local_time = Column(DateTime, nullable=False)
    base_fare = Column(Float, nullable=True)
    mandatory_total_fare = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    availability_status = Column(String, default="available")
    raw_evidence_uri = Column(String, nullable=True)


class RouteIndexModel(Base):
    __tablename__ = "route_indices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    route_code = Column(String, nullable=False, index=True)
    index_date = Column(Date, nullable=False, index=True)
    frequency = Column(String, default="daily")
    index_value = Column(Float, nullable=False)
    coverage_ratio = Column(Float, nullable=False)
    computed_at = Column(DateTime, nullable=False)


class HeadlineIndexModel(Base):
    __tablename__ = "headline_indices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    index_date = Column(Date, primary_key=True, index=True)
    frequency = Column(String, default="daily")
    headline_apix = Column(Float, nullable=False)
    one_day_change_pct = Column(Float, nullable=True)
    seven_day_change_pct = Column(Float, nullable=True)
    thirty_day_change_pct = Column(Float, nullable=True)
    coverage_ratio = Column(Float, nullable=False)
    quality_score = Column(Float, nullable=False)
    computed_at = Column(DateTime, nullable=False)
