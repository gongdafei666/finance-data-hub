# Requirements — Data Hub (Feature Spec)

## Overview

Build a minimal financial data hub that integrates at least two incompatible
provider response shapes into one normalized API and a simple HTML demo.

## User Stories

### US-1: List available data sources

As a developer exploring the hub,
I want to see which providers are registered,
so that I know which sources I can query.

#### Acceptance Criteria

WHEN a client calls `GET /api/v1/sources`
THE SYSTEM SHALL return a JSON list of registered source identifiers and display names.

WHEN no adapters are configured
THE SYSTEM SHALL return an empty list with HTTP 200.

### US-2: Fetch a normalized quote

As a dashboard builder,
I want a single quote shape regardless of provider,
so that my UI does not special-case vendor fields.

#### Acceptance Criteria

WHEN a client calls `GET /api/v1/quotes/{symbol}?source={source}`
THE SYSTEM SHALL return a `NormalizedQuote` with fields: `symbol`, `price`, `currency`, `as_of`, `source`, and optional `raw_meta`.

WHEN the requested source is unknown
THE SYSTEM SHALL return HTTP 404 with a clear error message.

WHEN the symbol is not found for that source
THE SYSTEM SHALL return HTTP 404 with a clear error message.

WHEN `source` is omitted
THE SYSTEM SHALL attempt the default / first available adapter and still return a `NormalizedQuote` on success.

### US-3: Multi-source merge view

As a Frankenstein demo reviewer,
I want to see the same symbol from multiple providers side by side,
so that the stitching is obvious.

#### Acceptance Criteria

WHEN a client calls `GET /api/v1/quotes/{symbol}/all`
THE SYSTEM SHALL return an array of `NormalizedQuote` objects, one per adapter that successfully resolves the symbol.

WHEN an adapter fails for the symbol
THE SYSTEM SHALL omit that adapter's entry and continue with others (partial success).

WHEN no adapter can resolve the symbol
THE SYSTEM SHALL return HTTP 404.

### US-4: Demo HTML page

As a judge or new contributor,
I want a browser page that exercises the API,
so that I can verify the hub without a separate client.

#### Acceptance Criteria

WHEN a client opens `GET /`
THE SYSTEM SHALL serve a static HTML page that can query quotes and display results.

WHEN the demo page loads
THE SYSTEM SHALL be able to call the JSON API from the same origin without CORS setup for local use.

### US-5: Containerized local run

As a solo developer,
I want to run the hub via Docker,
so that I do not fight host Python environments.

#### Acceptance Criteria

WHEN an operator builds the provided Dockerfile and runs the image exposing port 8000
THE SYSTEM SHALL serve the API and demo page at the mapped host port.
