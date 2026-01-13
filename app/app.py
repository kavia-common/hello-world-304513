"""
FastAPI application factory and global configuration.

Mirrors the role of the previous Express app wiring.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes.health_routes import router as health_router
from app.routes.weather_routes import router as weather_router


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="Weather App (Mock API)",
        description="A minimal FastAPI backend serving mock weather and forecast data.",
        version="0.1.0",
    )

    # Allow all origins (matches prior Express cors() default).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(weather_router, prefix="/api")

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Convert unhandled exceptions into a JSON 500 response."""
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": str(exc) or "Unexpected error"},
        )

    @app.middleware("http")
    async def not_found_json_middleware(request: Request, call_next):
        """Return a JSON 404 payload similar to the previous Express scaffold."""
        response = await call_next(request)
        if response.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "Not Found",
                    "message": f"Route {request.method} {request.url.path} not found",
                },
            )
        return response

    return app
