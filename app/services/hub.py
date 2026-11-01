"""Orchestrates multiple quote adapters into one hub façade."""

from __future__ import annotations

import logging

from app.adapters.base import QuoteAdapter
from app.models import NormalizedQuote, SourceInfo

logger = logging.getLogger(__name__)


class HubService:
    def __init__(self, adapters: list[QuoteAdapter]) -> None:
        if not adapters:
            raise ValueError("HubService requires at least one adapter")
        self._adapters = adapters
        self._by_id = {a.source_id: a for a in adapters}

    def list_sources(self) -> list[SourceInfo]:
        return [
            SourceInfo(source_id=a.source_id, display_name=a.display_name)
            for a in self._adapters
        ]

    def get_adapter(self, source_id: str) -> QuoteAdapter | None:
        return self._by_id.get(source_id)

    async def get_quote(
        self, symbol: str, source: str | None = None
    ) -> NormalizedQuote | None:
        if source:
            adapter = self._by_id.get(source)
            if adapter is None:
                raise KeyError(f"unknown source: {source}")
            return await adapter.fetch_quote(symbol)

        # Default: first adapter that resolves the symbol.
        for adapter in self._adapters:
            try:
                quote = await adapter.fetch_quote(symbol)
            except Exception:
                logger.exception("adapter %s failed for %s", adapter.source_id, symbol)
                continue
            if quote is not None:
                return quote
        return None

    async def get_all_quotes(self, symbol: str) -> list[NormalizedQuote]:
        results: list[NormalizedQuote] = []
        for adapter in self._adapters:
            try:
                quote = await adapter.fetch_quote(symbol)
            except Exception:
                logger.exception("adapter %s failed for %s", adapter.source_id, symbol)
                continue
            if quote is not None:
                results.append(quote)
        return results
