"""
Weather routes.

- GET /api/weather?city=CityName&units=metric|imperial
- GET /api/forecast?city=CityName&days=N
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.controllers.weather_controller import (
    ForecastQuery,
    ForecastQueryDep,
    WeatherQuery,
    WeatherQueryDep,
    get_forecast_handler,
    get_weather_handler,
)

router = APIRouter(tags=["Weather"])


@router.get("/weather", summary="Get current weather (mock)", operation_id="getWeather")
# PUBLIC_INTERFACE
def get_weather(query: WeatherQuery = Depends(WeatherQueryDep)) -> dict:
    """Current weather endpoint."""
    return get_weather_handler(query)


@router.get("/forecast", summary="Get forecast (mock)", operation_id="getForecast")
# PUBLIC_INTERFACE
def get_forecast(query: ForecastQuery = Depends(ForecastQueryDep)) -> dict:
    """Forecast endpoint."""
    return get_forecast_handler(query)
