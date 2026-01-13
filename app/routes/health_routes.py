"""
Health routes.

GET /health -> { "status": "ok" }
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check", operation_id="getHealth")
# PUBLIC_INTERFACE
def get_health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
