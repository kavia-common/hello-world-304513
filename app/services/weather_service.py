"""
Mock weather service (dependency-free).

Mirrors src/services/weatherService.js.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from typing import Literal


Units = Literal["metric", "imperial"]


def _compute_mock_temperature(city: str, units: Units) -> int | float:
    """Deterministic-ish mock temperature based on city name."""
    base_c = 12
    variance = sum(ord(ch) for ch in city.lower())
    temp_c = base_c + (variance % 15)  # 12..26

    if units == "imperial":
        return round((temp_c * 9) / 5 + 32)
    return temp_c


def _compute_mock_description(seed: str) -> str:
    """Return a simple mock weather description."""
    options = ["Clear sky", "Partly cloudy", "Overcast", "Light rain", "Breezy"]
    idx = sum(ord(ch) for ch in seed.lower()) % len(options)
    return options[idx]


@dataclass(frozen=True)
class MockWeather:
    city: str
    units: Units
    temperature: int | float
    description: str
    humidity: int
    windSpeed: int | float
    timestamp: str


@dataclass(frozen=True)
class MockForecastDay:
    date: str
    temperature: int | float
    description: str
    humidity: int
    windSpeed: int | float


# PUBLIC_INTERFACE
def get_mock_weather(*, city: str, units: Units) -> dict:
    """Get mock current weather payload for a city."""
    temperature = _compute_mock_temperature(city, units)

    humidity = 40 + (len(city) * 7) % 55  # 40..94
    wind_speed_metric = 2 + (len(city) % 6)  # 2..7 m/s
    wind_speed = round(wind_speed_metric * 2.237) if units == "imperial" else wind_speed_metric

    payload = MockWeather(
        city=city,
        units=units,
        temperature=temperature,
        description=_compute_mock_description(city),
        humidity=humidity,
        windSpeed=wind_speed,
        timestamp=datetime.utcnow().isoformat(timespec="seconds") + "Z",
    )
    return asdict(payload)


# PUBLIC_INTERFACE
def get_mock_forecast(*, city: str, days: int) -> dict:
    """Get mock multi-day forecast payload for a city."""
    base = get_mock_weather(city=city, units="metric")

    start = date.today()
    forecast: list[dict] = []

    for i in range(days):
        d = start + timedelta(days=i + 1)

        temp_c = base["temperature"] + ((1 if i % 2 == 0 else -1) * (i + 1))
        humidity = max(25, min(95, base["humidity"] + (5 if i % 3 == 0 else -3)))
        wind_speed = max(1, base["windSpeed"] + (1 if i % 2 == 0 else -1))

        day_payload = MockForecastDay(
            date=d.isoformat(),
            temperature=temp_c,
            description=_compute_mock_description(f"{city}-{i}"),
            humidity=humidity,
            windSpeed=wind_speed,
        )
        forecast.append(asdict(day_payload))

    return {"city": city, "days": days, "forecast": forecast}
