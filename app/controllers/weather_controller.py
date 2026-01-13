"""
Weather controllers: validation + service layer calls.
"""

from __future__ import annotations

from typing import Literal, Optional

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field

from app.services.weather_service import get_mock_forecast, get_mock_weather


class WeatherQuery(BaseModel):
    """Validated query parameters for current weather."""

    city: str = Field(..., description='City name (required).', min_length=1)
    units: Optional[Literal["metric", "imperial"]] = Field(
        default="metric",
        description='Units system: "metric" or "imperial".',
    )

    @classmethod
    def as_query(cls, city: str, units: Optional[str]) -> "WeatherQuery":
        """Build WeatherQuery with Express-like error messaging."""
        city_norm = (city or "").strip()
        if not city_norm:
            raise HTTPException(
                status_code=400,
                detail={"error": "Bad Request", "message": 'Query parameter "city" is required.'},
            )

        units_norm = (units or "metric").strip().lower()
        if units_norm not in ("metric", "imperial"):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Bad Request",
                    "message": 'Query parameter "units" must be "metric" or "imperial" when provided.',
                },
            )
        return cls(city=city_norm, units=units_norm)  # type: ignore[arg-type]


class ForecastQuery(BaseModel):
    """Validated query parameters for forecast."""

    city: str = Field(..., description='City name (required).', min_length=1)
    days: int = Field(default=5, description="Days (1..10).", ge=1, le=10)

    @classmethod
    def as_query(cls, city: str, days: Optional[str]) -> "ForecastQuery":
        """Build ForecastQuery with Express-like error messaging."""
        city_norm = (city or "").strip()
        if not city_norm:
            raise HTTPException(
                status_code=400,
                detail={"error": "Bad Request", "message": 'Query parameter "city" is required.'},
            )

        try:
            days_int = int(days) if days not in (None, "") else 5
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Bad Request",
                    "message": 'Query parameter "days" must be an integer between 1 and 10.',
                },
            ) from exc

        if days_int < 1 or days_int > 10:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Bad Request",
                    "message": 'Query parameter "days" must be an integer between 1 and 10.',
                },
            )

        return cls(city=city_norm, days=days_int)


# PUBLIC_INTERFACE
def WeatherQueryDep(
    city: str = Query(...),
    units: Optional[str] = Query(default="metric"),
) -> WeatherQuery:
    """Dependency that validates query params for /api/weather."""
    return WeatherQuery.as_query(city=city, units=units)


# PUBLIC_INTERFACE
def ForecastQueryDep(
    city: str = Query(...),
    days: Optional[str] = Query(default="5"),
) -> ForecastQuery:
    """Dependency that validates query params for /api/forecast."""
    return ForecastQuery.as_query(city=city, days=days)


# PUBLIC_INTERFACE
def get_weather_handler(query: WeatherQuery) -> dict:
    """Controller for current weather endpoint."""
    return get_mock_weather(city=query.city, units=query.units or "metric")


# PUBLIC_INTERFACE
def get_forecast_handler(query: ForecastQuery) -> dict:
    """Controller for forecast endpoint."""
    return get_mock_forecast(city=query.city, days=query.days)
