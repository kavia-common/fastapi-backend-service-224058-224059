from __future__ import annotations

from fastapi import APIRouter

from src.core.config import get_settings

router = APIRouter(tags=["Meta"])


@router.get(
    "/meta",
    summary="Service metadata",
    description="Returns service name, version, and environment metadata.",
    operation_id="service_meta_v1",
)
def service_meta() -> dict:
    """Return basic service metadata."""
    settings = get_settings()
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
