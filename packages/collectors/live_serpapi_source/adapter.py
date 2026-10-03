import uuid
import requests
from datetime import date, datetime
from typing import List
from packages.collector_core.base import BaseFareCollector
from packages.contracts import RawQuote, SourceMode, AvailabilityStatus

class LiveGoogleFlightsAdapter(BaseFareCollector):
    """
    Fetches REAL-TIME flight prices using the Google Flights engine via SerpApi.
    Requires a free API key from serpapi.com.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search.json"

    def fetch_quotes(self, origin: str, destination: str, travel_date: date) -> List[RawQuote]:
        if not self.api_key or self.api_key == "YOUR_SERPAPI_KEY":
            print("⚠️ WARNING: No real API key provided. Skipping live fetch.")
            return []

        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": travel_date.isoformat(),
            "currency": "INR",
            "hl": "en",
            "type": "2", # 2 = one way
            "api_key": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            quotes = []
            run_id = f"live-{datetime.now().isoformat()}"
            
            # Google flights returns "best_flights" and "other_flights"
            flights = data.get("best_flights", []) + data.get("other_flights", [])
            
            for f in flights:
                # Extract first segment details (assuming direct flights for simplest index)
                flight_info = f.get("flights", [{}])[0]
                carrier = flight_info.get("airline", "Unknown")
                flight_num = flight_info.get("flight_number", "000")
                
                # Fares in SerpApi Google Flights are returned in the "price" field
                total_fare = float(f.get("price", 0))
                if total_fare <= 0:
                    continue

                lead_time = (travel_date - date.today()).days

                quotes.append(RawQuote(
                    quote_id=str(uuid.uuid4()),
                    collection_run_id=run_id,
                    source="serpapi_google_flights",
                    source_mode=SourceMode.PERMITTED_LIVE,
                    collected_at=datetime.now(),
                    origin=origin,
                    destination=destination,
                    travel_date=travel_date,
                    lead_time_days=lead_time,
                    carrier=carrier,
                    flight_number=f"{carrier[:2]}-{flight_num}",
                    departure_local_time=datetime.now(), # simplified for hackathon
                    fare_class="ECONOMY",
                    base_fare=round(total_fare * 0.8, 2), # Approximate decomposition
                    taxes_and_statutory_fees=round(total_fare * 0.1, 2),
                    airport_or_udf_fee=round(total_fare * 0.05, 2),
                    ota_convenience_fee=round(total_fare * 0.05, 2),
                    mandatory_total_fare=total_fare,
                    currency="INR",
                    availability_status=AvailabilityStatus.AVAILABLE
                ))
            return quotes
        except Exception as e:
            print(f"Live fetch failed for {origin}-{destination}: {str(e)}")
            return []
