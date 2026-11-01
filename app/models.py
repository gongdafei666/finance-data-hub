"""Shared Pydantic models for the finance data hub."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class NormalizedQuote(BaseModel):
    """Provider-agnostic quote shape produced by every adapter."""

    symbol: str = Field(..., description="Ticker or instrument id, uppercased")
    price: float = Field(..., description="Last / regular market price")
    currency: str = Field(..., description="ISO-like currency code, e.g. USD")
    as_of: datetime = Field(..., description="Timezone-aware quote timestamp")
    source: str = Field(..., description="Adapter source_id that produced this quote")
    raw_meta: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional provider crumbs kept for debugging / demo",
    )


class SourceInfo(BaseModel):
    source_id: str
    display_name: str


class HealthResponse(BaseModel):
    status: str
    version: str
