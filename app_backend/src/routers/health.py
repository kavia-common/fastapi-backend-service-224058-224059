from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Lightweight health check endpoint used for uptime monitoring.",
    operation_id="health_check_v1",
)
def health_check() -> dict:
    """Return basic health status."""
    return {"status": "ok"}
