from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard API error envelope returned by exception handlers."""

    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error message.")
    request_id: Optional[str] = Field(default=None, description="Request id for correlating logs.")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Optional structured error details.")
