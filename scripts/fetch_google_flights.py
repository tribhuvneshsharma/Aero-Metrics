"""
CLI Script to fetch live airfares from Google Flights using GoogleFlightsCollector.

Usage:
  python scripts/fetch_google_flights.py --origin DEL --destination BOM --lead-days 7
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from packages.collectors.google_flights import GoogleFlightsCollector
from packages.pipeline.cleaning import validate_and_normalise


def main():
    parser = argparse.ArgumentParser(description="Fetch real-time airfares from Google Flights")
    parser.add_argument("--origin", default="DEL", help="Origin IATA code (e.g. DEL)")
    parser.add_argument("--destination", default="BOM", help="Destination IATA code (e.g. BOM)")
    parser.add_argument(
        "--lead-days",
        type=int,
        default=7,
        help="Lead time days from today (default: 7)",
    )
    parser.add_argument(
        "--save-json",
        action="store_true",
        help="Save raw quotes to data/fixtures/google_flights_quotes.json",
    )

    args = parser.parse_args()

    travel_date = datetime.now(timezone.utc).date() + timedelta(days=args.lead_days)
    print(f"\n🛫 Querying Google Flights: {args.origin} ➔ {args.destination}")
    print(f"📅 Travel Date: {travel_date} (T+{args.lead_days} days)")
    print("⏳ Fetching real-time domestic fares (Air India, IndiGo, Akasa, etc.)...\n")

    collector = GoogleFlightsCollector(currency="INR")
    quotes = collector.fetch_quotes(
        origin=args.origin,
        destination=args.destination,
        travel_date=travel_date,
    )

    if not quotes:
        print("⚠️ No flights found for this route and date.")
        return

    print(f"✅ Retrieved {len(quotes)} flight quotes directly from Google Flights!\n")

    # Pass through Aero-Metrics pipeline validation
    normalised_quotes, _issues = validate_and_normalise(quotes)

    # Show top 15 quotes
    print(f"{'Carrier':<16} {'Flight No':<14} {'Travel Date':<14} {'Base Fare':<12} {'Total (INR)':<14} {'Status':<10}")
    print("-" * 84)
    for nq in normalised_quotes[:20]:
        base_str = f"₹{nq.base_fare:,.2f}" if nq.base_fare else "N/A"
        total_str = f"₹{nq.mandatory_total_fare:,.2f}"
        print(f"{nq.carrier:<16} {nq.flight_number:<14} {nq.travel_date!s:<14} {base_str:<12} {total_str:<14} {nq.validation_status.value:<10}")

    if len(normalised_quotes) > 20:
        print(f"... and {len(normalised_quotes) - 20} more flights.")

    if args.save_json:
        output_dir = Path("data/fixtures")
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / "google_flights_quotes.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump([q.model_dump(mode="json") for q in quotes], f, indent=2)
        print(f"\n💾 Saved {len(quotes)} quotes to {out_file}")


if __name__ == "__main__":
    main()
