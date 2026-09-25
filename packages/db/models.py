import uuid

from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RawQuoteModel(Base):
    __tablename__ = "raw_quotes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quote_id = Column(String, nullable=True, index=True)
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


class RouteDailyPriceModel(Base):
    __tablename__ = "route_daily_prices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    route_code = Column(String, nullable=False, index=True)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    horizon = Column(String(10), nullable=False)
    lead_time_days = Column(Integer, nullable=False)
    collection_date = Column(Date, nullable=False, index=True)
    median_fare = Column(Float, nullable=False)
    observation_count = Column(Integer, nullable=False)


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


class DGCABenchmarkModel(Base):
    __tablename__ = "dgca_benchmarks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    report_date = Column(Date, nullable=False, index=True)
    route_code = Column(String, nullable=False, index=True)
    dgca_avg_fare = Column(Float, nullable=False)
    apix_route_index = Column(Float, nullable=False)
    passenger_volume = Column(Integer, nullable=True)
