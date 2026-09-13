from typing import List
from datetime import date
from packages.collector_core.base import BaseFareCollector
from packages.contracts import RawQuote


class PermittedLiveSourceB(BaseFareCollector):
    """
    Adapter for Permitted Live Source B (API / public feed compliant with robots.txt).
    """

    def fetch_quotes(self, origin: str, destination: str, travel_date: date) -> List[RawQuote]:
        # Implement permitted rate-limited fetch
        return []

