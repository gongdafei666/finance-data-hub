---
inclusion: always
---

# Technology Stack — Finance Data Hub

## Runtime

- **Language:** Python 3.12+
- **Web framework:** FastAPI + Uvicorn
- **Validation:** Pydantic v2 models for request/response and normalized quotes
- **HTTP client (future live adapters):** `httpx` (async-ready; unused by default mocks)

## Packaging & deploy

- **Deps:** `requirements.txt` (pinned ranges acceptable for scaffold)
- **Container:** official `python:3.12-slim` based `Dockerfile`
- **Local run:** `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Testing & quality

- **Tests:** `pytest` against hub normalization and API routes via FastAPI `TestClient`
- **Lint (hook):** `ruff check` on saved `*.py` files via `.kiro/hooks`

## Conventions Kiro should prefer

- Prefer adapter pattern over hard-coding provider logic in route handlers
- Keep provider-specific field mapping inside `app/adapters/*`
- Return ISO-8601 UTC timestamps in normalized models (`...Z` or offset-aware)
- Do not invent live API keys; mocks are the default path
- Avoid adding databases in v0 — in-memory / deterministic mock responses only
