import math
from datetime import date, datetime, timedelta
from typing import Dict
from sqlalchemy.orm import Session
from packages.db.models import (
    RouteWeightModel,
    LeadTimeWeightModel,
    RawQuoteModel,
    NormalisedQuoteModel,
    RouteDailyPriceModel,
    RouteIndexModel,
    HeadlineIndexModel
)
from packages.db.session import SessionLocal, init_db

CARRIERS = ["IndiGo", "Air India", "SpiceJet", "Akasa Air", "Air India Express"]
CARRIER_FLIGHT_PREFIX = {
    "IndiGo": "6E",
    "Air India": "AI",
    "SpiceJet": "SG",
    "Akasa Air": "QP",
    "Air India Express": "IX"
}

BASE_ROUTE_MEDIANS = {
    "DEL-BOM": 4800.0, "BOM-DEL": 4850.0,
    "DEL-BLR": 5400.0, "BLR-DEL": 5350.0,
    "BOM-BLR": 3600.0, "BLR-BOM": 3650.0,
    "DEL-CCU": 4600.0, "CCU-DEL": 4550.0,
    "BLR-HYD": 2800.0, "HYD-BLR": 2850.0,
    "MAA-DEL": 5100.0, "DEL-MAA": 5050.0,
    "BOM-HYD": 3100.0, "HYD-BOM": 3150.0,
    "DEL-PNQ": 4200.0, "PNQ-DEL": 4250.0,
}

HORIZON_MULTIPLIERS = {
    "T+1": 1.65,   # Last-minute surge
    "T+7": 1.18,   # 1 week ahead
    "T+15": 1.00,  # Baseline 2-week
    "T+30": 0.88,  # Early booking discount
    "T+45": 0.82   # Advance purchase
}


def generate_and_seed_30d_replay(db: Session = None, days_count: int = 30, force_reseed: bool = True):
    """
    Generates a deterministic 30-day replay dataset and runs the complete
    cleaning, normalisation, median calculation, and index aggregation pipeline.
    """
    init_db(db)
    close_after = False
    if db is None:
        db = SessionLocal()
        close_after = True

    try:
        # Check if already seeded and not force_reseed
        if not force_reseed and db.query(HeadlineIndexModel).count() >= days_count:
            return {"status": "already_seeded", "days": db.query(HeadlineIndexModel).count()}

        # Wipe old dynamic tables
        db.query(HeadlineIndexModel).delete()
        db.query(RouteIndexModel).delete()
        db.query(RouteDailyPriceModel).delete()
        db.query(NormalisedQuoteModel).delete()
        db.query(RawQuoteModel).delete()
        db.commit()

        routes = db.query(RouteWeightModel).all()
        horizons = db.query(LeadTimeWeightModel).all()
        h_weights = {h.horizon: h.weight for h in horizons}
        r_weights = {r.route_code: r.weight for r in routes}

        # Initialize canonical base reference prices P(r, h, 0)
        base_prices: Dict[str, Dict[str, float]] = {}
        for r in routes:
            base_prices[r.route_code] = {}
            r_median = BASE_ROUTE_MEDIANS.get(r.route_code, 4500.0)
            for h in horizons:
                base_prices[r.route_code][h.horizon] = round(r_median * HORIZON_MULTIPLIERS.get(h.horizon, 1.0), 2)

        start_date = date.today() - timedelta(days=days_count - 1)

        # Seed day by day
        for day_idx in range(days_count):
            cur_date = start_date + timedelta(days=day_idx)
            run_id = f"replay-run-{cur_date.isoformat()}"
            
            # Trend factor: day 0 is 1.0 (exact base 100), peaks around day 18-22 (+5-7%)
            demand_shock = 1.0 + 0.03 * math.sin(day_idx / 4.5) + (0.035 if 16 <= day_idx <= 22 else 0.0)

            daily_route_medians: Dict[str, Dict[str, float]] = {}

            # Generate quotes for each route × horizon
            for r in routes:
                daily_route_medians[r.route_code] = {}
                base_cell_price = base_prices[r.route_code]

                for h in horizons:
                    target_median = base_cell_price[h.horizon] * demand_shock

                    # Generate 3 realistic quotes for this cell
                    quotes_for_cell = []
                    for q_idx in range(3):
                        carrier = CARRIERS[(day_idx + q_idx) % len(CARRIERS)]
                        prefix = CARRIER_FLIGHT_PREFIX[carrier]
                        flight_num = f"{prefix}-{100 + (day_idx * 7 + q_idx * 13) % 899}"
                        
                        # Controlled variance around target median
                        quote_total = round(target_median * (0.97 + 0.06 * ((q_idx * 37 + day_idx * 11) % 10) / 10.0), 2)
                        base_fare = round(quote_total * 0.72, 2)
                        taxes = round(quote_total * 0.12, 2)
                        udf = round(quote_total * 0.11, 2)
                        convenience = round(quote_total - (base_fare + taxes + udf), 2)

                        # Raw Quote
                        raw_q = RawQuoteModel(
                            collection_run_id=run_id,
                            source="replay_demo_feed",
                            source_mode="replay_fixture",
                            collected_at=datetime.combine(cur_date, datetime.min.time()) + timedelta(hours=9),
                            origin=r.origin,
                            destination=r.destination,
                            travel_date=cur_date + timedelta(days=h.lead_time_days),
                            lead_time_days=h.lead_time_days,
                            carrier=carrier,
                            flight_number=flight_num,
                            departure_local_time=datetime.combine(cur_date + timedelta(days=h.lead_time_days), datetime.min.time()) + timedelta(hours=10),
                            base_fare=base_fare,
                            airline_surcharge=0.0,
                            taxes_and_statutory_fees=taxes,
                            airport_or_udf_fee=udf,
                            ota_convenience_fee=convenience,
                            mandatory_total_fare=quote_total,
                            currency="INR",
                            availability_status="available",
                            raw_evidence_uri=f"object://raw-quotes/{cur_date}/{run_id}/{flight_num}.json",
                            parser_version="1.0.0"
                        )
                        db.add(raw_q)

                        # Normalised Quote
                        canonical_key = f"{carrier}_{flight_num}_{raw_q.travel_date}_{r.origin}_{r.destination}"
                        norm_q = NormalisedQuoteModel(
                            raw_quote_id=raw_q.id,
                            canonical_key=canonical_key,
                            collection_run_id=run_id,
                            source="replay_demo_feed",
                            source_mode="replay_fixture",
                            collected_at=raw_q.collected_at,
                            origin=r.origin,
                            destination=r.destination,
                            route_code=r.route_code,
                            travel_date=raw_q.travel_date,
                            lead_time_days=h.lead_time_days,
                            horizon=h.horizon,
                            carrier=carrier,
                            flight_number=flight_num,
                            departure_local_time=raw_q.departure_local_time,
                            base_fare=base_fare,
                            airline_surcharge=0.0,
                            taxes_and_statutory_fees=taxes,
                            airport_or_udf_fee=udf,
                            ota_convenience_fee=convenience,
                            mandatory_total_fare=quote_total,
                            validation_status="valid",
                            quality_status="pass",
                            flags="clean",
                            pipeline_version="0.1.0"
                        )
                        db.add(norm_q)
                        quotes_for_cell.append(quote_total)

                    # Compute route-horizon median P(r, h, t)
                    quotes_for_cell.sort()
                    med_fare = quotes_for_cell[1]  # Median of 3 quotes
                    daily_route_medians[r.route_code][h.horizon] = med_fare

                    rdp = RouteDailyPriceModel(
                        route_code=r.route_code,
                        origin=r.origin,
                        destination=r.destination,
                        horizon=h.horizon,
                        lead_time_days=h.lead_time_days,
                        collection_date=cur_date,
                        median_fare=med_fare,
                        observation_count=len(quotes_for_cell),
                        min_fare=quotes_for_cell[0],
                        max_fare=quotes_for_cell[-1],
                        imputed=False
                    )
                    db.add(rdp)

            # Compute Route Indices: RouteIndex(r, t) = 100 * sum(v(h) * P(r,h,t)/P(r,h,0))
            route_indices = {}
            for r in routes:
                route_sum = 0.0
                for h in horizons:
                    p_rt = daily_route_medians[r.route_code][h.horizon]
                    p_r0 = base_prices[r.route_code][h.horizon]
                    price_relative = p_rt / p_r0
                    route_sum += h_weights[h.horizon] * price_relative

                r_idx_val = round(100.0 * route_sum, 2)
                route_indices[r.route_code] = r_idx_val

                rim = RouteIndexModel(
                    route_code=r.route_code,
                    index_date=cur_date,
                    frequency="daily",
                    index_value=r_idx_val,
                    coverage_ratio=1.0,
                    quality_score=0.98
                )
                db.add(rim)

            # National Headline APIx(t) = sum(w(r) * RouteIndex(r, t))
            headline_val = round(sum(r_weights[r.route_code] * route_indices[r.route_code] for r in routes), 2)
            
            him = HeadlineIndexModel(
                index_date=cur_date,
                frequency="daily",
                headline_apix=headline_val,
                one_day_change_pct=0.0,
                seven_day_change_pct=0.0,
                thirty_day_change_pct=0.0,
                coverage_ratio=1.0,
                quality_score=0.98,
                quality_status="pass"
            )
            db.add(him)

        db.commit()

        # Update percentage changes
        all_headlines = db.query(HeadlineIndexModel).order_by(HeadlineIndexModel.index_date.asc()).all()
        for i, h in enumerate(all_headlines):
            if i >= 1:
                prev = all_headlines[i - 1].headline_apix
                h.one_day_change_pct = round(((h.headline_apix - prev) / prev) * 100.0, 2)
            if i >= 7:
                prev7 = all_headlines[i - 7].headline_apix
                h.seven_day_change_pct = round(((h.headline_apix - prev7) / prev7) * 100.0, 2)
            if i >= 29:
                prev30 = all_headlines[i - 29].headline_apix
                h.thirty_day_change_pct = round(((h.headline_apix - prev30) / prev30) * 100.0, 2)
        db.commit()

        return {
            "status": "success",
            "message": f"Seeded {days_count} days of reproducible replay data across 16 routes and 5 horizons.",
            "total_headlines": len(all_headlines)
        }
    finally:
        if close_after:
            db.close()
