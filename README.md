# Finance Data Hub

**Kiroween 2026 — Frankenstein category**  
Author: Gong Dafei · License: MIT · Solo

A small chimera that stitches **two incompatible financial quote shapes** into one
usable hub:

| Provider mock | Raw shape | Adapter |
|---------------|-----------|---------|
| Yahoo-like | Nested `meta.regularMarketPrice` + epoch time | `yahoo_mock` |
| Alpha Vantage-like | Flat `"Global Quote"` / `"05. price"` keys | `alphavantage_mock` |

Both map into a single `NormalizedQuote` (`symbol`, `price`, `currency`, `as_of`,
`source`, `raw_meta`) served by FastAPI, with a minimal HTML demo at `/`.

> Mocks ship by default so the demo runs offline. Live HTTP adapters can replace
> the mocks later behind the same `QuoteAdapter` interface.

## Quick start (local Python)

```bash
cd finance-data-hub
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000/ for the demo UI, or try:

```bash
curl -s http://127.0.0.1:8000/api/v1/sources | jq
curl -s http://127.0.0.1:8000/api/v1/quotes/AAPL/all | jq
curl -s 'http://127.0.0.1:8000/api/v1/quotes/AAPL?source=yahoo_mock' | jq
```

## Docker (local)

```bash
docker build -t finance-data-hub .
docker run --rm -p 8000:8000 finance-data-hub
```

Then open http://127.0.0.1:8000/

## Tests

```bash
pytest -q
```

## API sketch

| Method | Path | Notes |
|--------|------|-------|
| GET | `/` | HTML demo |
| GET | `/api/v1/health` | Liveness |
| GET | `/api/v1/sources` | Registered adapters |
| GET | `/api/v1/quotes/{symbol}` | Optional `?source=` |
| GET | `/api/v1/quotes/{symbol}/all` | Multi-source merge |

## Kiro artifacts

This repo keeps `/.kiro` at the root (steering, specs, hooks) and **does not**
gitignore it. See [docs/KIRO_USAGE.md](docs/KIRO_USAGE.md) for an honest inventory
of what is in the tree. Devpost draft notes: [docs/DEVPOST.md](docs/DEVPOST.md).

## Project layout

See `.kiro/steering/structure.md` for the canonical tree and conventions.
