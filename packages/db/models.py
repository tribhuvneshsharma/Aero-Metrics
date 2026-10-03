from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float, DateTime, Date, Integer, Boolean, Text
import uuid
from datetime import datetime

Base = declarative_base()


class RouteWeightModel(Base):
    __tablename__ = "route_weights"

    route_code = Column(String(10), primary_key=True)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    weight = Column(Float, nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    weight_source = Column(String(100), default="DGCA traffic proxy")


class LeadTimeWeightModel(Base):
    __tablename__ = "lead_time_weights"

    horizon = Column(String(5), primary_key=True)
    lead_time_days = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    description = Column(String(100), nullable=True)


class RawQuoteModel(Base):
    __tablename__ = "raw_quotes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_run_id = Column(String(36), nullable=False, index=True)
    source = Column(String(50), nullable=False)
    source_mode = Column(String(30), nullable=False)
    collected_at = Column(DateTime, nullable=False)
    origin = Column(String(3), nullable=False, index=True)
    destination = Column(String(3), nullable=False, index=True)
    travel_date = Column(Date, nullable=False, index=True)
    lead_time_days = Column(Integer, nullable=False, index=True)
    carrier = Column(String(50), nullable=False)
    flight_number = Column(String(20), nullable=False)
    departure_local_time = Column(DateTime, nullable=False)
    base_fare = Column(Float, nullable=True)
    airline_surcharge = Column(Float, default=0.0)
    taxes_and_statutory_fees = Column(Float, default=0.0)
    airport_or_udf_fee = Column(Float, default=0.0)
    ota_convenience_fee = Column(Float, default=0.0)
    mandatory_total_fare = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    availability_status = Column(String(20), default="available")
    raw_evidence_uri = Column(String(255), nullable=True)
    parser_version = Column(String(10), default="1.0.0")


class NormalisedQuoteModel(Base):
    __tablename__ = "normalised_quotes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    raw_quote_id = Column(String(36), nullable=True, index=True)
    canonical_key = Column(String(100), nullable=False, index=True)
    collection_run_id = Column(String(36), nullable=False, index=True)
    source = Column(String(50), nullable=False)
    source_mode = Column(String(30), nullable=False)
    collected_at = Column(DateTime, nullable=False)
    origin = Column(String(3), nullable=False, index=True)
    destination = Column(String(3), nullable=False, index=True)
    route_code = Column(String(10), nullable=False, index=True)
    travel_date = Column(Date, nullable=False, index=True)
    lead_time_days = Column(Integer, nullable=False, index=True)
    horizon = Column(String(5), nullable=False, index=True)
    carrier = Column(String(50), nullable=False)
    flight_number = Column(String(20), nullable=False)
    departure_local_time = Column(DateTime, nullable=False)
    base_fare = Column(Float, nullable=True)
    airline_surcharge = Column(Float, default=0.0)
    taxes_and_statutory_fees = Column(Float, default=0.0)
    airport_or_udf_fee = Column(Float, default=0.0)
    ota_convenience_fee = Column(Float, default=0.0)
    mandatory_total_fare = Column(Float, nullable=False)
    validation_status = Column(String(20), default="valid")
    quality_status = Column(String(20), default="pass")
    flags = Column(Text, default="")
    pipeline_version = Column(String(10), default="0.1.0")


class RouteDailyPriceModel(Base):
    __tablename__ = "route_daily_prices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    route_code = Column(String(10), nullable=False, index=True)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    horizon = Column(String(5), nullable=False, index=True)
    lead_time_days = Column(Integer, nullable=False)
    collection_date = Column(Date, nullable=False, index=True)
    median_fare = Column(Float, nullable=False)
    observation_count = Column(Integer, default=1)
    min_fare = Column(Float, nullable=True)
    max_fare = Column(Float, nullable=True)
    imputed = Column(Boolean, default=False)
    imputation_method = Column(String(50), nullable=True)


class RouteIndexModel(Base):
    __tablename__ = "route_indices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    route_code = Column(String(10), nullable=False, index=True)
    index_date = Column(Date, nullable=False, index=True)
    frequency = Column(String(10), default="daily")
    index_value = Column(Float, nullable=False)
    coverage_ratio = Column(Float, nullable=False)
    quality_score = Column(Float, default=1.0)
    computed_at = Column(DateTime, default=datetime.utcnow)


class HeadlineIndexModel(Base):
    __tablename__ = "headline_indices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    index_date = Column(Date, primary_key=True, index=True)
    frequency = Column(String(10), default="daily")
    headline_apix = Column(Float, nullable=False)
    one_day_change_pct = Column(Float, nullable=True)
    seven_day_change_pct = Column(Float, nullable=True)
    thirty_day_change_pct = Column(Float, nullable=True)
    coverage_ratio = Column(Float, nullable=False)
    quality_score = Column(Float, nullable=False)
    quality_status = Column(String(20), default="pass")
    imputed_weight = Column(Float, default=0.0)
    excluded_weight = Column(Float, default=0.0)
    computed_at = Column(DateTime, default=datetime.utcnow)
