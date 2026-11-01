"""Alpha Vantage-like mock adapter — flat GLOBAL_QUOTE shape."""

from __future__ import annotations

from datetime import UTC, datetime

from app.adapters.base import QuoteAdapter
from app.models import NormalizedQuote

# Deliberately AV-ish flat keys (not Yahoo nested meta).
_AV_FIXTURES: dict[str, dict] = {
    "AAPL": {
        "Global Quote": {
            "01. symbol": "AAPL",
            "05. price": "197.88",
            "08. previous close": "196.50",
            "07. latest trading day": "2026-10-31",
            "09. change": "1.3800",
        }
    },
    "MSFT": {
        "Global Quote": {
            "01. symbol": "MSFT",
            "05. price": "419.55",
            "08. previous close": "418.00",
            "07. latest trading day": "2026-10-31",
            "09. change": "1.5500",
        }
    },
    "IBM": {
        "Global Quote": {
            "01. symbol": "IBM",
            "05. price": "221.40",
            "08. previous close": "220.10",
            "07. latest trading day": "2026-10-31",
            "09. change": "1.3000",
        }
    },
}


class AlphaVantageMockAdapter(QuoteAdapter):
    source_id = "alphavantage_mock"
    display_name = "Alpha Vantage (mock)"

    async def fetch_quote(self, symbol: str) -> NormalizedQuote | None:
        key = symbol.strip().upper()
        payload = _AV_FIXTURES.get(key)
        if payload is None:
            return None
        gq = payload["Global Quote"]
        day = gq["07. latest trading day"]
        # Treat trading day as UTC noon for a deterministic as_of.
        as_of = datetime.fromisoformat(f"{day}T12:00:00+00:00").astimezone(UTC)
        return NormalizedQuote(
            symbol=gq["01. symbol"],
            price=float(gq["05. price"]),
            currency="USD",  # AV GLOBAL_QUOTE omits currency; hub normalizes it in
            as_of=as_of,
            source=self.source_id,
            raw_meta={
                "previous_close": gq.get("08. previous close"),
                "change": gq.get("09. change"),
                "shape": "alphavantage_global_quote",
            },
        )
