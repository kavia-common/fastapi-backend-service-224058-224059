"""
FastAPI application entrypoint.

This module wires together:
- Environment-based configuration (settings)
- Middleware (CORS, request-id, structured request logging)
- Versioned API routers (/api/v1)
- Error handling (HTTP + validation + unexpected errors)
- OpenAPI metadata/tags

The resulting app is suitable as a production-ready scaffold to build on.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.errors import register_exception_handlers
from src.core.logging import configure_logging, get_logger
from src.middleware.request_context import RequestContextMiddleware
from src.routers import api_v1_router

settings = get_settings()

# Configure logging as early as possible so imports/initialization can log.
configure_logging(settings)
log = get_logger(__name__)

openapi_tags = [
    {
        "name": "Health",
        "description": "Service health and readiness endpoints.",
    },
    {
        "name": "Meta",
        "description": "Service metadata endpoints (version, build info, etc.).",
    },
    {
        "name": "Docs",
        "description": "Human-friendly API usage documentation endpoints.",
    },
]

app = FastAPI(
    title=settings.app_name,
    description=(
        "Production-ready FastAPI scaffold with versioned APIs, structured logging, "
        "centralized error handling, and testable routing."
    ),
    version=settings.app_version,
    openapi_tags=openapi_tags,
)

# Middleware: request context (request id), logging, etc.
app.add_middleware(RequestContextMiddleware)

# CORS (env-based). Default remains permissive for early development, but can be tightened.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Routers
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

# Error handlers
register_exception_handlers(app)

log.info(
    "App initialized",
    extra={
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "api_v1_prefix": settings.api_v1_prefix,
    },
)
