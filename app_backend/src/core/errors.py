from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.logging import get_logger
from src.schemas.errors import ErrorResponse

log = get_logger(__name__)


def _error_payload(
    *,
    code: str,
    message: str,
    request_id: Optional[str],
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return ErrorResponse(
        code=code,
        message=message,
        request_id=request_id,
        details=details,
    ).model_dump()


def register_exception_handlers(app: FastAPI) -> None:
    """Register centralized exception handlers for consistent error responses."""

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        payload = _error_payload(
            code="http_error",
            message=str(exc.detail) if exc.detail else "HTTP error",
            request_id=request_id,
            details={"status_code": exc.status_code},
        )
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        payload = _error_payload(
            code="validation_error",
            message="Request validation failed",
            request_id=request_id,
            details={"errors": exc.errors()},
        )
        return JSONResponse(status_code=422, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        log.exception("Unhandled exception", extra={"request_id": request_id})
        payload = _error_payload(
            code="internal_error",
            message="Internal server error",
            request_id=request_id,
        )
        return JSONResponse(status_code=500, content=payload)
