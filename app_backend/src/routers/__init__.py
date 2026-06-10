from __future__ import annotations

from fastapi import APIRouter

from src.routers.docs import router as docs_router
from src.routers.health import router as health_router
from src.routers.meta import router as meta_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(meta_router)
api_v1_router.include_router(docs_router)
