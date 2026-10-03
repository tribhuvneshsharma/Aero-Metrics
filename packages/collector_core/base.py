from abc import ABC, abstractmethod
from datetime import date

from packages.contracts import RawQuote


class BaseFareCollector(ABC):
    """
    Standard interface for all airfare data adapters.
    """

    @abstractmethod
    def fetch_quotes(self, origin: str, destination: str, travel_date: date) -> list[RawQuote]:
        """
        Fetch fares for a given route and date while adhering to rate limits.
        """
