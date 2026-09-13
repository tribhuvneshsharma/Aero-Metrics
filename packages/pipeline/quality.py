def calculate_quality_score(
    weighted_coverage: float,
    source_success_rate: float,
    component_completeness: float,
    freshness_score: float = 1.0
) -> float:
    """
    Computes composite quality score as defined in Section 3.6:
    quality_score = 0.45 * weighted_coverage + 0.25 * source_success_rate
                  + 0.20 * price_component_completeness + 0.10 * freshness_score
    """
    return (
        0.45 * weighted_coverage +
        0.25 * source_success_rate +
        0.20 * component_completeness +
        0.10 * freshness_score
    )

