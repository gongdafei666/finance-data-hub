"""Yahoo-like mock adapter — nested chart meta shape."""

from __future__ import annotations

from datetime import UTC, datetime

from app.adapters.base import QuoteAdapter
from app.models import NormalizedQuote

# Deliberately Yahoo-ish nested payload (not AV flat keys).
_YAHOO_FIXTURES: dict[str, dict] = {
    "AAPL": {
        "meta": {
            "symbol": "AAPL",
            "currency": "USD",
            "regularMarketPrice": 198.45,
            "regularMarketTime": 1793462400,
            "exchangeName": "NMS",
        }
    },
    "MSFT": {
        "meta": {
            "symbol": "MSFT",
            "currency": "USD",
            "regularMarketPrice": 420.12,
            "regularMarketTime": 1793462400,
            "exchangeName": "NMS",
        }
    },
    "BTC-USD": {
        "meta": {
            "symbol": "BTC-USD",
            "currency": "USD",
            "regularMarketPrice": 67250.0,
            "regularMarketTime": 1793464200,
            "exchangeName": "CCC",
        }
    },
}


class YahooMockAdapter(QuoteAdapter):
    source_id = "yahoo_mock"
    display_name = "Yahoo Finance (mock)"

    async def fetch_quote(self, symbol: str) -> NormalizedQuote | None:
        key = symbol.strip().upper()
        payload = _YAHOO_FIXTURES.get(key)
        if payload is None:
            return None
        meta = payload["meta"]
        as_of = datetime.fromtimestamp(meta["regularMarketTime"], tz=UTC)
        return NormalizedQuote(
            symbol=meta["symbol"],
            price=float(meta["regularMarketPrice"]),
            currency=meta["currency"],
            as_of=as_of,
            source=self.source_id,
            raw_meta={"exchangeName": meta.get("exchangeName"), "shape": "yahoo_meta"},
        )
