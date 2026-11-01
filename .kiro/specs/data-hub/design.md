# Design — Data Hub

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│ HTML demo / │────▶│ FastAPI      │────▶│ HubService          │
│ curl client │     │ /api/v1/*    │     │  - list sources     │
└─────────────┘     └──────────────┘     │  - get quote        │
                                         │  - get all quotes   │
                                         └──────────┬──────────┘
                              ┌─────────────────────┼─────────────────────┐
                              ▼                     ▼                     ▼
                     YahooMockAdapter      AlphaVantageMockAdapter   (future live)
                     (chart/meta shape)    (GLOBAL_QUOTE shape)
                              │                     │
                              └──────────┬──────────┘
                                         ▼
                                 NormalizedQuote
```

## Frankenstein stitching

Two deliberately incompatible mock payloads:

1. **Yahoo-like** — nested `meta.regularMarketPrice`, `meta.currency`, `meta.symbol`,
   epoch `regularMarketTime`.
2. **Alpha Vantage-like** — flat `"Global Quote"` map with keys like `05. price`,
   `08. previous close`, `07. latest trading day`.

Each adapter implements `QuoteAdapter`:

- `source_id: str`
- `display_name: str`
- `async def fetch_quote(symbol: str) -> NormalizedQuote | None`

Mapping lives only inside adapters. The hub never reads vendor keys directly.

## Data model

```python
class NormalizedQuote(BaseModel):
    symbol: str
    price: float
    currency: str
    as_of: datetime  # timezone-aware
    source: str
    raw_meta: dict[str, Any] = {}
```

## API surface

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/` | Static demo HTML |
| GET | `/api/v1/health` | Liveness |
| GET | `/api/v1/sources` | Registered adapters |
| GET | `/api/v1/quotes/{symbol}` | One normalized quote (`?source=`) |
| GET | `/api/v1/quotes/{symbol}/all` | Multi-source merge |

## Error handling

- Unknown source → 404 `{ "detail": "..." }`
- Symbol miss → 404
- Adapter exceptions → logged; treated as miss for `/all`, 502 for single-source if adapter raises unexpectedly

## Testing strategy

- Unit: adapter mapping from fixture payloads → `NormalizedQuote`
- API: `TestClient` for sources, quote, all, 404 paths
- Manual: open `/` after `uvicorn` or Docker run

## Deployment

- `Dockerfile`: install deps, copy `app/`, `CMD uvicorn app.main:app --host 0.0.0.0 --port 8000`
- No external services required for the mock scaffold
