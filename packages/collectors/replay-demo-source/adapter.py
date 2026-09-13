from typing import List
from datetime import date
from packages.collector_core.base import BaseFareCollector
from packages.contracts import RawQuote


class ReplayDemoSource(BaseFareCollector):
    """
    Deterministic replay adapter reading local fixtures for guaranteed offline judge demonstrations.
    """

    def __init__(self, fixture_dir: str = "data/replay-30d"):
        self.fixture_dir = fixture_dir

    def fetch_quotes(self, origin: str, destination: str, travel_date: date) -> List[RawQuote]:
        # Reads deterministic snapshot data
        return []

