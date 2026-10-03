import json
import logging
from datetime import date, timedelta
from sqlalchemy.orm import Session
from packages.db.models import NormalisedQuoteModel, RouteDailyPriceModel, RouteIndexModel, HeadlineIndexModel
from packages.db.repository import get_all_routes, get_lead_time_weights
from packages.pipeline.cleaning import validate_and_normalise

logger = logging.getLogger(__name__)

def run_live_collection(db: Session, api_key: str, route_code: str = None):
    from packages.collectors.live_serpapi_source.adapter import LiveGoogleFlightsAdapter
    
    collector = LiveGoogleFlightsAdapter(api_key=api_key)
    routes = get_all_routes(db)
    if route_code:
        routes = [r for r in routes if r.route_code == route_code]
        
    horizon_days = {"T+1": 1, "T+7": 7, "T+15": 15, "T+30": 30, "T+45": 45}
    today = date.today()
    all_quotes = []
    
    for r in routes:
        for horizon_label, days_out in horizon_days.items():
            travel_date = today + timedelta(days=days_out)
            print(f"Fetching LIVE data for {r.route_code} departing {travel_date}...")
            quotes = collector.fetch_quotes(r.origin, r.destination, travel_date)
            all_quotes.extend([(q, horizon_label) for q in quotes])

    if not all_quotes:
        return {"status": "error", "message": "No live quotes fetched."}

    raw_quotes = [item[0] for item in all_quotes]
    normalised_quotes, _ = validate_and_normalise(raw_quotes)

    db_models = []
    for nq, (rq, horizon_label) in zip(normalised_quotes, all_quotes):
        data = nq.dict()
        db_models.append(NormalisedQuoteModel(
            id=data.get('quote_id'),
            raw_quote_id=data.get('quote_id'),
            canonical_key=data.get('canonical_key'),
            collection_run_id=data.get('collection_run_id'),
            source=data.get('source'),
            source_mode=data.get('source_mode'),
            collected_at=data.get('collected_at'),
            origin=data.get('origin'),
            destination=data.get('destination'),
            route_code=f"{nq.origin}-{nq.destination}",
            travel_date=data.get('travel_date'),
            lead_time_days=data.get('lead_time_days'),
            horizon=horizon_label,
            carrier=data.get('carrier'),
            flight_number=data.get('flight_number'),
            departure_local_time=data.get('departure_local_time'),
            base_fare=data.get('base_fare'),
            airline_surcharge=data.get('airline_surcharge'),
            taxes_and_statutory_fees=data.get('taxes_and_statutory_fees'),
            airport_or_udf_fee=data.get('airport_or_udf_fee'),
            ota_convenience_fee=data.get('ota_convenience_fee'),
            mandatory_total_fare=data.get('mandatory_total_fare'),
            validation_status=data.get('validation_status'),
            quality_status=data.get('quality_status'),
            flags=",".join(data.get('flags', [])),
            pipeline_version=data.get('pipeline_version')
        ))
        
    db.bulk_save_objects(db_models)
    db.commit()
    
    return {
        "status": "success",
        "message": f"Successfully scraped {len(all_quotes)} live quotes.",
        "total_quotes": len(all_quotes)
    }
