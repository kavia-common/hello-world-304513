# Product Requirements Document (PRD) — Mock Weather API (FastAPI)

## Overview
This repository contains a minimal Python/FastAPI backend that serves mock (deterministic) weather and forecast data. It is designed as a scaffold that can later be extended to call real external weather providers, while already providing stable endpoints and consistent error payloads for frontend integration.

The service is intended to run on port 3001 by default to match the preview environment.

## Goals
The primary goals of this service are to provide a stable HTTP API surface for a “weather app” frontend and to demonstrate a clean separation of concerns (routes, controllers, services) in a small FastAPI codebase.

Specifically, the API should provide a health check endpoint, a current weather endpoint, and a multi-day forecast endpoint, all returning JSON payloads. The API should also provide consistent validation and error responses for missing or invalid query parameters.

## Users and Use Cases
The main user of this API is a frontend application or developer who needs predictable responses while building UI workflows for searching a city and viewing current conditions and forecast.

A secondary user is a developer extending the service to integrate a real weather provider while maintaining endpoint compatibility and error handling contracts.

## User Stories
A consumer of the API should be able to perform the following tasks.

As a client application, I want to check if the service is up so that I can show an “online/offline” indicator and gate dependent UI actions.

As a client application, I want to request current weather for a city with a units option so that I can display temperature and related metadata in the user’s preferred measurement system.

As a client application, I want to request a multi-day forecast for a city with a days option so that I can display a forecast list in the UI.

As a developer, I want invalid query parameters to return actionable 400 errors so that my client can display useful validation messages.

As a developer, I want unknown routes to return a JSON 404 error so that failures are easier to debug in client integrations.

## Key Features and Requirements
### Health Check
The API must expose a health endpoint.

The endpoint is `GET /health` and it returns JSON `{ "status": "ok" }`.

### Current Weather Endpoint (Mock)
The API must expose a current-weather endpoint.

The endpoint is `GET /api/weather`.

The endpoint requires a query parameter `city` and accepts an optional query parameter `units` whose value must be `metric` or `imperial`.

The response must be JSON and include at least: city, units, temperature, description, humidity, windSpeed, and timestamp.

The current implementation produces deterministic-ish mock values based on the city name and returns an ISO timestamp for when the response was generated.

### Forecast Endpoint (Mock)
The API must expose a forecast endpoint.

The endpoint is `GET /api/forecast`.

The endpoint requires a query parameter `city` and accepts an optional query parameter `days`, which must be an integer between 1 and 10.

The response must be JSON and include the city, the number of days, and a list of forecast day objects.

The current implementation produces deterministic-ish mock values derived from the mock weather for the city and then varies temperature/humidity/windSpeed by day.

### Error Handling and Validation Requirements
If `city` is missing or empty, the API must return a 400 error with a JSON payload that matches the existing structure used by the service.

If `units` is provided but is not `metric` or `imperial`, the API must return a 400 error with a JSON payload that matches the existing structure used by the service.

If `days` is not an integer or is outside 1..10, the API must return a 400 error with a JSON payload that matches the existing structure used by the service.

Unknown routes must return a JSON 404 response with a message identifying the method and path.

Unhandled server errors must return a JSON 500 response with a stable top-level structure.

### CORS
CORS is enabled for all origins in the current implementation to match the prior Express scaffold behavior. This is intended for development compatibility rather than strict production hardening.

## API Examples
### Health
Request:
```bash
curl "http://localhost:3001/health"
```

Response:
```json
{ "status": "ok" }
```

### Current Weather (metric)
Request:
```bash
curl "http://localhost:3001/api/weather?city=London&units=metric"
```

Example response (values vary by city and time):
```json
{
  "city": "London",
  "units": "metric",
  "temperature": 24,
  "description": "Overcast",
  "humidity": 72,
  "windSpeed": 2,
  "timestamp": "2026-01-13T12:34:56Z"
}
```

### Current Weather (invalid units)
Request:
```bash
curl "http://localhost:3001/api/weather?city=London&units=kelvin"
```

Response:
```json
{
  "detail": {
    "error": "Bad Request",
    "message": "Query parameter \"units\" must be \"metric\" or \"imperial\" when provided."
  }
}
```

### Forecast
Request:
```bash
curl "http://localhost:3001/api/forecast?city=London&days=5"
```

Example response (values vary by city):
```json
{
  "city": "London",
  "days": 5,
  "forecast": [
    {
      "date": "2026-01-14",
      "temperature": 25,
      "description": "Breezy",
      "humidity": 77,
      "windSpeed": 3
    }
  ]
}
```

## Assumptions
The service is currently intended for local development and preview environments and therefore defaults to port 3001.

No external API keys are required in the current state because the service uses deterministic mock data generation.

JSON response shapes are intended to remain stable as real provider integration is introduced, with internal implementations changing behind the service layer.

## Non-Goals
This project does not currently implement user authentication, rate limiting, or API keys for consumers.

This project does not currently implement persistence, caching, or background jobs.

This project does not currently guarantee real meteorological correctness; the data is intentionally mock.

This project does not currently expose a formal OpenAPI schema document beyond FastAPI’s default generated schema.

## Success Metrics
A successful implementation should meet the following measurable outcomes.

The service starts reliably and responds on port 3001 (or `$PORT` when provided).

For valid requests, `/health`, `/api/weather`, and `/api/forecast` return HTTP 200 with JSON payloads.

For invalid requests, the API returns HTTP 400 with clear JSON error messages.

For unknown routes, the API returns HTTP 404 with JSON error payloads.

Integration with a frontend client should require no custom parsing logic beyond reading JSON fields described above.

## Current State: Mock Data and Path to Real Data
The current state uses mock data generated in the service layer. To add real weather data, the implementation should be extended so that the service layer calls an external provider and maps provider-specific response shapes into the stable API contract.

A practical next step is to introduce a provider client module, configure an API key and base URL via environment variables, and update the service functions to call the provider when configured, while retaining a mock fallback for local development.
