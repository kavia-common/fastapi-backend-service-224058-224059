from __future__ import annotations

import logging
import sys
from typing import Optional

from src.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """
    Configure root logging for the service.

    Uses a simple, production-friendly format that remains readable in local dev.
    """
    level_name = (settings.log_level or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    # Avoid duplicate handlers in some reload/test scenarios
    root = logging.getLogger()
    if root.handlers:
        root.setLevel(level)
        return

    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a standard library logger."""
    return logging.getLogger(name if name else "app")
