from typing import List, Optional, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from .models import (
    RouteWeightModel,
    LeadTimeWeightModel,
    HeadlineIndexModel,
    RouteIndexModel,
    RouteDailyPriceModel,
    NormalisedQuoteModel
)


def get_all_routes(db: Session) -> List[RouteWeightModel]:
    return db.query(RouteWeightModel).order_by(desc(RouteWeightModel.weight)).all()


def get_route_by_code(db: Session, route_code: str) -> Optional[RouteWeightModel]:
    return db.query(RouteWeightModel).filter(RouteWeightModel.route_code == route_code).first()


def get_lead_time_weights(db: Session) -> List[LeadTimeWeightModel]:
    return db.query(LeadTimeWeightModel).order_by(LeadTimeWeightModel.lead_time_days).all()


def get_headline_indices(
    db: Session,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    frequency: str = "daily",
    limit: int = 100
) -> List[HeadlineIndexModel]:
    q = db.query(HeadlineIndexModel).filter(HeadlineIndexModel.frequency == frequency)
    if from_date:
        q = q.filter(HeadlineIndexModel.index_date >= from_date)
    if to_date:
        q = q.filter(HeadlineIndexModel.index_date <= to_date)
    return q.order_by(HeadlineIndexModel.index_date.asc()).limit(limit).all()


def get_latest_headline_index(db: Session) -> Optional[HeadlineIndexModel]:
    return db.query(HeadlineIndexModel).order_by(desc(HeadlineIndexModel.index_date)).first()


def get_route_indices(
    db: Session,
    route_code: str,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    limit: int = 100
) -> List[RouteIndexModel]:
    q = db.query(RouteIndexModel).filter(RouteIndexModel.route_code == route_code)
    if from_date:
        q = q.filter(RouteIndexModel.index_date >= from_date)
    if to_date:
        q = q.filter(RouteIndexModel.index_date <= to_date)
    return q.order_by(RouteIndexModel.index_date.asc()).limit(limit).all()


def get_route_fares(
    db: Session,
    route_code: str,
    horizon: Optional[str] = None,
    limit: int = 50
) -> List[NormalisedQuoteModel]:
    q = db.query(NormalisedQuoteModel).filter(NormalisedQuoteModel.route_code == route_code)
    if horizon:
        q = q.filter(NormalisedQuoteModel.horizon == horizon)
    return q.order_by(desc(NormalisedQuoteModel.collected_at)).limit(limit).all()


def get_heatmap_matrix(db: Session, limit_days: int = 14) -> List[Dict[str, Any]]:
    """
    Returns a matrix of routes × dates with price index changes for frontend heatmaps.
    """
    recent_dates = [
        r[0] for r in db.query(HeadlineIndexModel.index_date)
        .order_by(desc(HeadlineIndexModel.index_date))
        .limit(limit_days).all()
    ]
    recent_dates.reverse()

    routes = db.query(RouteWeightModel).order_by(desc(RouteWeightModel.weight)).all()
    matrix = []

    for r in routes:
        row = {"route_code": r.route_code, "origin": r.origin, "destination": r.destination, "weight": r.weight, "series": []}
        indices = {
            idx.index_date: idx.index_value
            for idx in db.query(RouteIndexModel)
            .filter(RouteIndexModel.route_code == r.route_code)
            .filter(RouteIndexModel.index_date.in_(recent_dates)).all()
        }
        for d in recent_dates:
            row["series"].append({
                "date": d.isoformat(),
                "index_value": indices.get(d, 100.0)
            })
        matrix.append(row)

    return matrix


def get_lead_time_curve(db: Session, route_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns average fare by horizon (T+1 to T+45) for lead-time elasticity analysis.
    """
    q = db.query(
        RouteDailyPriceModel.horizon,
        RouteDailyPriceModel.lead_time_days,
        func.avg(RouteDailyPriceModel.median_fare).label("avg_median_fare"),
        func.count(RouteDailyPriceModel.id).label("sample_size")
    )
    if route_code:
        q = q.filter(RouteDailyPriceModel.route_code == route_code)
    
    results = q.group_by(RouteDailyPriceModel.horizon, RouteDailyPriceModel.lead_time_days)\
               .order_by(RouteDailyPriceModel.lead_time_days.asc()).all()

    return [
        {
            "horizon": r[0],
            "lead_time_days": r[1],
            "average_fare": round(float(r[2]), 2) if r[2] else 0.0,
            "observations": r[3]
        }
        for r in results
    ]


def get_data_quality_summary(db: Session) -> Dict[str, Any]:
    latest = get_latest_headline_index(db)
    total_quotes = db.query(func.count(NormalisedQuoteModel.id)).scalar() or 0
    total_valid = db.query(func.count(NormalisedQuoteModel.id)).filter(NormalisedQuoteModel.validation_status == "valid").scalar() or 0
    imputed_count = db.query(func.count(RouteDailyPriceModel.id)).filter(RouteDailyPriceModel.imputed == True).scalar() or 0

    return {
        "latest_index_date": latest.index_date.isoformat() if latest else None,
        "headline_apix": latest.headline_apix if latest else 100.0,
        "coverage_ratio": latest.coverage_ratio if latest else 1.0,
        "quality_score": latest.quality_score if latest else 1.0,
        "quality_status": latest.quality_status if latest else "pass",
        "imputed_weight": latest.imputed_weight if latest else 0.0,
        "total_quotes_processed": total_quotes,
        "valid_quotes_rate": round(total_valid / total_quotes, 4) if total_quotes > 0 else 1.0,
        "imputed_observations_count": imputed_count,
        "methodology_version": "0.1.0",
        "source_mode": "replay_fixture"
    }
