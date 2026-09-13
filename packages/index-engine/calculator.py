import statistics
from typing import List, Dict
from packages.contracts import NormalisedQuote, ValidationStatus


def compute_route_horizon_median(quotes: List[NormalisedQuote]) -> float:
    """
    P(r, h, t) = median(valid canonical total fares for r, h, t)
    """
    valid_fares = [
        q.mandatory_total_fare
        for q in quotes
        if q.validation_status == ValidationStatus.VALID
    ]
    if not valid_fares:
        raise ValueError("No valid fares available for calculation")
    return float(statistics.median(valid_fares))


def aggregate_route_index(
    horizon_relatives: Dict[str, float],
    horizon_weights: Dict[str, float]
) -> float:
    """
    RouteIndex(r, t) = 100 * sum(v(h) * R(r, h, t))
    """
    total = sum(
        horizon_weights[h] * horizon_relatives[h]
        for h in horizon_relatives
        if h in horizon_weights
    )
    return 100.0 * total


def aggregate_headline_apix(
    route_indices: Dict[str, float],
    route_weights: Dict[str, float]
) -> float:
    """
    APIx(t) = sum(w(r) * RouteIndex(r, t))
    """
    return sum(
        route_weights[r] * route_indices[r]
        for r in route_indices
        if r in route_weights
    )

