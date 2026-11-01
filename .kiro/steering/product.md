---
inclusion: always
---

# Product Overview — Finance Data Hub

## Purpose

Finance Data Hub is a Frankenstein-style chimera that stitches together multiple
heterogeneous financial market data providers into one usable hub. Each provider
speaks a different dialect (field names, timestamps, currency codes, quote shapes).
The hub normalizes those dialects into a single quote model and exposes them through
one FastAPI surface plus a minimal HTML demo.

## Target users

- Solo builders and hobby quants who want a local, Docker-friendly data façade
- Developers prototyping dashboards without wiring each vendor SDK by hand
- Hackathon judges evaluating Frankenstein integration (not a production trading desk)

## Key features

1. **Provider adapters** — pluggable adapters for at least two mock/provider shapes
   (Yahoo-like and Alpha Vantage-like) that can later be swapped for live HTTP clients.
2. **Normalized quotes** — a single `NormalizedQuote` schema (symbol, price, currency,
   as_of, source, raw_meta).
3. **Hub API** — REST endpoints to list sources, fetch a quote by symbol, and merge
   multi-source views for the same ticker.
4. **Demo UI** — a simple HTML page that calls the API and renders JSON/table output.
5. **Local Docker deploy** — one `Dockerfile` for reproducible runs.

## Non-goals (v0)

- Real brokerage execution or order routing
- Authentication / multi-tenant SaaS
- Guaranteed live market data (mocks ship by default; live keys are optional later)
- High-frequency streaming (polling/REST only in the scaffold)

## Business / hackathon objectives

- Demonstrate clear Frankenstein stitching of incompatible data shapes
- Keep the repo Kiro-friendly (steering, specs, hooks committed under `/.kiro`)
- Ship something judges can `docker build` and hit in a browser within minutes
