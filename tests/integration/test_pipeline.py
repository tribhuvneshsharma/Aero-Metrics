import pytest
from datetime import datetime, date
from packages.contracts import RawQuote, SourceMode, ValidationStatus
from packages.pipeline.cleaning import validate_and_normalise
from packages.pipeline.quality import calculate_quality_score


def test_quote_validation_positive_fare():
    quote = RawQuote(
        collection_run_id="run-1",
        source="test_source",
        source_mode=SourceMode.REPLAY_FIXTURE,
        collected_at=datetime.utcnow(),
        origin="DEL",
        destination="BOM",
        travel_date=date(2026, 9, 20),
        lead_time_days=7,
        carrier="Air India",
        flight_number="AI-101",
        departure_local_time=datetime.utcnow(),
        mandatory_total_fare=5200.0,
        currency="INR"
    )
    normalised, issues = validate_and_normalise([quote])
    assert len(normalised) == 1
    assert normalised[0].validation_status == ValidationStatus.VALID
    assert normalised[0].canonical_key == "Air India_AI-101_2026-09-20_DEL_BOM"


def test_quote_validation_negative_fare():
    quote = RawQuote(
        collection_run_id="run-2",
        source="test_source",
        source_mode=SourceMode.REPLAY_FIXTURE,
        collected_at=datetime.utcnow(),
        origin="DEL",
        destination="BOM",
        travel_date=date(2026, 9, 20),
        lead_time_days=7,
        carrier="Air India",
        flight_number="AI-101",
        departure_local_time=datetime.utcnow(),
        mandatory_total_fare=-100.0,
        currency="INR"
    )
    normalised, issues = validate_and_normalise([quote])
    assert len(normalised) == 1
    assert normalised[0].validation_status == ValidationStatus.EXCLUDED
    assert "invalid_negative_or_zero_fare" in normalised[0].flags


def test_quality_score_computation():
    score = calculate_quality_score(
        weighted_coverage=1.0,
        source_success_rate=1.0,
        component_completeness=1.0,
        freshness_score=1.0
    )
    assert pytest.approx(score, 0.001) == 1.0
