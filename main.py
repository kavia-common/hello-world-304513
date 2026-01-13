"""
Single-file FastAPI mock Weather API.

Endpoints preserved from the original Node/Express scaffold:
- GET /health
- GET /api/weather?city=CityName&units=metric|imperial
- GET /api/forecast?city=CityName&days=N

Server listens on port 3001 by default to match the preview environment.
"""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from typing import Literal, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

Units = Literal["metric", "imperial"]

app = FastAPI(
    title="Weather App (Mock API)",
    description="A minimal FastAPI backend serving mock weather and forecast data.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _compute_mock_temperature(city: str, units: Units) -> int | float:
    base_c = 12
    variance = sum(ord(ch) for ch in city.lower())
    temp_c = base_c + (variance % 15)  # 12..26
    if units == "imperial":
        return round((temp_c * 9) / 5 + 32)
    return temp_c


def _compute_mock_description(seed: str) -> str:
    options = ["Clear sky", "Partly cloudy", "Overcast", "Light rain", "Breezy"]
    idx = sum(ord(ch) for ch in seed.lower()) % len(options)
    return options[idx]


@app.get("/health", tags=["Health"], summary="Health check")
# PUBLIC_INTERFACE
def health() -> dict:
    """Health check endpoint returning `{ "status": "ok" }`."""
    return {"status": "ok"}


@app.get("/api/weather", tags=["Weather"], summary="Get current weather (mock)")
# PUBLIC_INTERFACE
def get_weather(
    city: str = Query(..., description='City name (required). Example: "London".'),
    units: Optional[str] = Query(
        default="metric", description='Units system: "metric" or "imperial".'
    ),
) -> dict:
    """Return mock current weather for a city."""
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

    temperature = _compute_mock_temperature(city_norm, units_norm)  # type: ignore[arg-type]
    humidity = 40 + (len(city_norm) * 7) % 55
    wind_speed_metric = 2 + (len(city_norm) % 6)
    wind_speed = round(wind_speed_metric * 2.237) if units_norm == "imperial" else wind_speed_metric

    return {
        "city": city_norm,
        "units": units_norm,
        "temperature": temperature,
        "description": _compute_mock_description(city_norm),
        "humidity": humidity,
        "windSpeed": wind_speed,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


@app.get("/api/forecast", tags=["Weather"], summary="Get forecast (mock)")
# PUBLIC_INTERFACE
def get_forecast(
    city: str = Query(..., description='City name (required). Example: "London".'),
    days: Optional[str] = Query(default="5", description="Days of forecast (integer 1..10)."),
) -> dict:
    """Return mock multi-day forecast for a city."""
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

    base_temp = _compute_mock_temperature(city_norm, "metric")

    forecast = []
    start = date.today()
    for i in range(days_int):
        d = start + timedelta(days=i + 1)
        temp_c = base_temp + ((1 if i % 2 == 0 else -1) * (i + 1))
        forecast.append(
            {
                "date": d.isoformat(),
                "temperature": temp_c,
                "description": _compute_mock_description(f"{city_norm}-{i}"),
                "humidity": 50,
                "windSpeed": 3,
            }
        )

    return {"city": city_norm, "days": days_int, "forecast": forecast}


# PUBLIC_INTERFACE
def main() -> None:
    """Run the server on port 3001 by default (or PORT env var)."""
    load_dotenv(override=False)
    port = int(os.getenv("PORT", "3001"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
