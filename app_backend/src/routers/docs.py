from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Docs"])


@router.get(
    "/docs/help",
    summary="API usage help",
    description="Human-friendly usage notes for this backend scaffold.",
    operation_id="docs_help_v1",
)
def docs_help() -> dict:
    """Return usage guidance for interacting with this API."""
    return {
        "message": "FastAPI backend scaffold",
        "docs": "/docs",
        "openapi_json": "/openapi.json",
        "api_base": "/api/v1",
        "endpoints": {
            "health": "/api/v1/health",
            "meta": "/api/v1/meta",
        },
        "notes": [
            "All endpoints return X-Request-ID header for log correlation.",
            "CORS is configurable via environment variables.",
        ],
    }
