from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables (and optionally .env).

    Note: the platform provides a .env; this code only reads from environment.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="FastAPI Backend Service", description="Human-readable service name.")
    app_version: str = Field(default="0.1.0", description="Service version for OpenAPI and metadata.")
    environment: str = Field(default="development", description="Runtime environment (development/staging/production).")

    api_v1_prefix: str = Field(default="/api/v1", description="Prefix for versioned API endpoints.")

    # CORS configuration
    cors_allow_origins_raw: str = Field(
        default="*",
        description=(
            "Comma-separated list of allowed origins. Use '*' for permissive development mode. "
            "Example: 'https://example.com,https://app.example.com'"
        ),
    )
    cors_allow_credentials: bool = Field(default=True, description="Whether to allow cookies/credentials in CORS.")
    cors_allow_methods_raw: str = Field(default="*", description="Comma-separated methods or '*'.")
    cors_allow_headers_raw: str = Field(default="*", description="Comma-separated headers or '*'.")

    # Logging
    log_level: str = Field(default="INFO", description="Python logging level (DEBUG, INFO, WARNING, ERROR).")

    def _split_csv_or_star(self, raw: str) -> List[str]:
        raw = (raw or "").strip()
        if raw == "" or raw == "*":
            return ["*"]
        return [part.strip() for part in raw.split(",") if part.strip()]

    @property
    def cors_allow_origins(self) -> List[str]:
        """Parsed list for FastAPI CORS middleware."""
        return self._split_csv_or_star(self.cors_allow_origins_raw)

    @property
    def cors_allow_methods(self) -> List[str]:
        """Parsed list for FastAPI CORS middleware."""
        return self._split_csv_or_star(self.cors_allow_methods_raw)

    @property
    def cors_allow_headers(self) -> List[str]:
        """Parsed list for FastAPI CORS middleware."""
        return self._split_csv_or_star(self.cors_allow_headers_raw)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get a cached Settings instance."""
    # Allow overriding app version from env at runtime without code changes (optional convenience).
    # If APP_VERSION is set it will be picked up by pydantic automatically; keep this hook minimal.
    _ = os.getenv("APP_VERSION")
    return Settings()
