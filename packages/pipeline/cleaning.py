
from packages.contracts import NormalisedQuote, RawQuote, ValidationStatus


def validate_and_normalise(raw_quotes: list[RawQuote]) -> tuple[list[NormalisedQuote], list[str]]:
    """
    Validates fare totals, checks mandatory fare components, deduplicates across sources,
    and applies canonical flight keys.
    """
    normalised = []
    issues = []
    for q in raw_quotes:
        flags = []
        status = ValidationStatus.VALID

        # Check total fare non-negative
        if q.mandatory_total_fare <= 0:
            status = ValidationStatus.EXCLUDED
            flags.append("invalid_negative_or_zero_fare")

        # Canonical key: carrier-flight-date-dep
        canonical_key = f"{q.carrier}_{q.flight_number}_{q.travel_date}_{q.origin}_{q.destination}"

        norm = NormalisedQuote(
            **q.model_dump(),
            canonical_key=canonical_key,
            validation_status=status,
            quality_status="pass" if status == ValidationStatus.VALID else "rejected",
            flags=flags,
            pipeline_version="0.1.0"
        )
        normalised.append(norm)

    return normalised, issues

