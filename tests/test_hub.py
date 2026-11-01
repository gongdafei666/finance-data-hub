"""Tests for adapter normalization and API routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.adapters import AlphaVantageMockAdapter, YahooMockAdapter
from app.main import app
from app.services import HubService


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.asyncio
async def test_yahoo_adapter_maps_nested_meta() -> None:
    adapter = YahooMockAdapter()
    quote = await adapter.fetch_quote("aapl")
    assert quote is not None
    assert quote.symbol == "AAPL"
    assert quote.price == 198.45
    assert quote.currency == "USD"
    assert quote.source == "yahoo_mock"
    assert quote.raw_meta.get("shape") == "yahoo_meta"


@pytest.mark.asyncio
async def test_alphavantage_adapter_maps_flat_global_quote() -> None:
    adapter = AlphaVantageMockAdapter()
    quote = await adapter.fetch_quote("AAPL")
    assert quote is not None
    assert quote.symbol == "AAPL"
    assert quote.price == 197.88
    assert quote.currency == "USD"
    assert quote.source == "alphavantage_mock"
    assert quote.raw_meta.get("shape") == "alphavantage_global_quote"


@pytest.mark.asyncio
async def test_hub_merge_returns_both_sources_for_aapl() -> None:
    hub = HubService([YahooMockAdapter(), AlphaVantageMockAdapter()])
    quotes = await hub.get_all_quotes("AAPL")
    sources = {q.source for q in quotes}
    assert sources == {"yahoo_mock", "alphavantage_mock"}
    # Prices differ on purpose — Frankenstein stitching, not reconciliation.
    assert quotes[0].price != quotes[1].price


def test_api_sources(client: TestClient) -> None:
    res = client.get("/api/v1/sources")
    assert res.status_code == 200
    ids = {row["source_id"] for row in res.json()}
    assert ids == {"yahoo_mock", "alphavantage_mock"}


def test_api_quote_all(client: TestClient) -> None:
    res = client.get("/api/v1/quotes/AAPL/all")
    assert res.status_code == 200
    body = res.json()
    assert len(body) == 2


def test_api_quote_unknown_symbol(client: TestClient) -> None:
    res = client.get("/api/v1/quotes/NOPE/all")
    assert res.status_code == 404


def test_api_unknown_source(client: TestClient) -> None:
    res = client.get("/api/v1/quotes/AAPL?source=no_such_provider")
    assert res.status_code == 404


def test_health_and_demo(client: TestClient) -> None:
    assert client.get("/api/v1/health").json()["status"] == "ok"
    home = client.get("/")
    assert home.status_code == 200
    assert "Finance Data Hub" in home.text
