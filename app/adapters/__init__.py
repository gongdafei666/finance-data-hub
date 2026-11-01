"""Provider adapters that map vendor-shaped payloads into NormalizedQuote."""

from app.adapters.base import QuoteAdapter
from app.adapters.mock_alphavantage import AlphaVantageMockAdapter
from app.adapters.mock_yahoo import YahooMockAdapter

__all__ = [
    "AlphaVantageMockAdapter",
    "QuoteAdapter",
    "YahooMockAdapter",
]
