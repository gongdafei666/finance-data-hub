"""Adapter interface for quote providers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import NormalizedQuote


class QuoteAdapter(ABC):
    """Frankenstein seam: each provider implements this small contract."""

    source_id: str
    display_name: str

    @abstractmethod
    async def fetch_quote(self, symbol: str) -> NormalizedQuote | None:
        """Return a normalized quote or None when the symbol is unknown."""
