# Devpost draft — Finance Data Hub

**Project name:** Finance Data Hub  
**Category:** Frankenstein  
**Builder:** Gong Dafei (solo)  
**License:** MIT  
**Deploy:** Local Docker (no cloud deploy required for the demo)

## Elevator pitch

Finance Data Hub stitches together financial data providers that refuse to speak
the same language. A Yahoo-like nested chart meta payload and an Alpha Vantage-like
flat `GLOBAL_QUOTE` map are forced through one adapter seam into a single
`NormalizedQuote` API — then shown in a tiny HTML demo you can run with Docker.

## Inspiration

Market data vendors each invent their own field names, timestamps, and nesting.
Dashboards end up full of one-off parsers. Frankenstein felt right: take ugly,
incompatible parts and bolt them into one usable creature.

## What it does

- Registers multiple quote adapters behind a common interface
- Normalizes price, currency, and `as_of` into one schema
- Exposes `/api/v1/quotes/{symbol}` and `/api/v1/quotes/{symbol}/all`
- Serves a same-origin demo page at `/`
- Ships with mocks so judges can run offline; live adapters are a deliberate next step

## How we built it

- Spec-first layout under `.kiro/specs/data-hub` (EARS requirements, design, tasks)
- Steering docs for product / tech / structure with `inclusion: always`
- A PostFileSave Ruff lint hook under `.kiro/hooks`
- Python FastAPI + Pydantic v2 + Uvicorn, containerized with a slim Python image

## Challenges

- Keeping provider-specific keys out of route handlers (true adapter boundary)
- Being honest about Kiro usage in docs — only claim artifacts that exist in `/.kiro`
- Designing mocks that are *obviously* incompatible so the stitching is visible

## What’s next

- Live HTTP adapters (same interface) with optional API keys via env
- Simple caching / rate-limit façade
- Public GitHub repo + completed Devpost media (demo GIF / short video)

## Built with

Python, FastAPI, Pydantic, Uvicorn, Docker, pytest, Ruff, Kiro (`.kiro` steering / specs / hooks)

## Try it

See the repository README for `pip` + `uvicorn` and `docker build` / `docker run`
instructions. Demo symbols: `AAPL`, `MSFT`, `BTC-USD` (Yahoo mock), `IBM` (AV mock).
