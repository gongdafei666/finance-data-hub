"""FastAPI entrypoint for Finance Data Hub."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.adapters import AlphaVantageMockAdapter, YahooMockAdapter
from app.models import HealthResponse, NormalizedQuote, SourceInfo
from app.services import HubService

STATIC_DIR = Path(__file__).resolve().parent / "static"

hub = HubService(
    adapters=[
        YahooMockAdapter(),
        AlphaVantageMockAdapter(),
    ]
)

app = FastAPI(
    title="Finance Data Hub",
    description=(
        "Frankenstein hub that stitches Yahoo-like and Alpha Vantage-like "
        "mock quote shapes into one NormalizedQuote API."
    ),
    version=__version__,
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def demo_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/v1/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@app.get("/api/v1/sources", response_model=list[SourceInfo])
async def list_sources() -> list[SourceInfo]:
    return hub.list_sources()


@app.get("/api/v1/quotes/{symbol}", response_model=NormalizedQuote)
async def get_quote(
    symbol: str,
    source: str | None = Query(
        default=None,
        description="Adapter source_id; omit to use the first successful adapter",
    ),
) -> NormalizedQuote:
    try:
        quote = await hub.get_quote(symbol, source=source)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if quote is None:
        raise HTTPException(
            status_code=404,
            detail=f"symbol not found: {symbol}"
            + (f" (source={source})" if source else ""),
        )
    return quote


@app.get("/api/v1/quotes/{symbol}/all", response_model=list[NormalizedQuote])
async def get_quote_all(symbol: str) -> list[NormalizedQuote]:
    quotes = await hub.get_all_quotes(symbol)
    if not quotes:
        raise HTTPException(status_code=404, detail=f"symbol not found: {symbol}")
    return quotes
