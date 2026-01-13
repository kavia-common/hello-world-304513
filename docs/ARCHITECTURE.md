# Architecture — Mock Weather API (FastAPI)

## Summary
This repository implements a minimal FastAPI service that returns mock weather data. The codebase contains two parallel “entry styles”:

The `main.py` module defines a single-file FastAPI application with endpoints directly on the `app` object and runs Uvicorn using the `PORT` environment variable (defaulting to 3001).

The `app/` package defines a more structured layout with an application factory (`create_app`), route modules, controller modules for validation, and a service layer that generates mock data. This package structure mirrors a typical production-ready FastAPI layout.

In the current repository state, `python main.py` is the documented way to run the service, and it listens on port 3001 by default.

## Service Responsibilities
The service is responsible for the following behaviors.

It provides a health check endpoint used to confirm liveness.

It provides two read-only weather endpoints that accept query parameters and return JSON responses.

It validates query parameters and returns consistent 400 errors for invalid inputs.

It returns JSON 404 payloads for unknown routes (implemented in the application factory variant).

It returns a JSON 500 payload for unhandled errors (implemented in the application factory variant).

## Repository Structure
### Entrypoint
The current runnable entrypoint is:

`hello-world-304513/main.py`

It defines a FastAPI `app` object, registers routes, and starts Uvicorn via `main()`.

### Application Factory (Structured App)
The structured app package is:

`hello-world-304513/app/`

The key modules are the following.

`app/app.py` defines `create_app()` which configures CORS, includes routers, and registers a JSON 404 middleware and a generic exception handler.

`app/routes/health_routes.py` defines `GET /health`.

`app/routes/weather_routes.py` defines `GET /api/weather` and `GET /api/forecast` (by applying an `/api` prefix when included in `create_app()`).

`app/controllers/weather_controller.py` defines Pydantic models and dependency functions that validate and normalize query parameters and call the service layer.

`app/services/weather_service.py` generates deterministic-ish mock weather and forecast data. It does not call external APIs.

### Note on “Which App is Running”
The repository currently contains both `main.py` and `app/create_app()` wiring. The README instructs running `python main.py`, which runs the single-file app.

If you want to run the structured app factory, you would typically add a small runner that imports `create_app()` and passes it to Uvicorn. That runner does not exist as a separate file currently.

## Runtime Configuration
### Port and Environment
The service defaults to port 3001.

In `main.py`, the port is configurable via the `PORT` environment variable:

`port = int(os.getenv("PORT", "3001"))`

`python-dotenv` is used to load environment variables from a local `.env` file if present:

`load_dotenv(override=False)`

No other environment variables are currently required.

### Dependencies
Python dependencies are pinned in:

`requirements.txt`

They include FastAPI, Uvicorn, Pydantic, and python-dotenv.

## API Surface
### Endpoints (as implemented in main.py)
`GET /health` returns `{ "status": "ok" }`.

`GET /api/weather` requires `city` and accepts `units` in `{metric, imperial}`.

`GET /api/forecast` requires `city` and accepts `days` as an integer 1..10.

### Response Shapes
The service returns JSON objects, not wrapped in any additional envelope for success responses.

For errors raised as `HTTPException` in `main.py`, FastAPI returns a JSON payload with a top-level `detail` field.

For example, a 400 error uses the shape:

```json
{
  "detail": {
    "error": "Bad Request",
    "message": "..."
  }
}
```

## Request/Response Flows
### Flow: GET /health
In the single-file app (`main.py`), request handling is straightforward.

The client calls `GET /health`.

FastAPI routes to the `health()` handler.

The handler returns a Python dict `{ "status": "ok" }`, which FastAPI serializes to JSON and returns with HTTP 200.

In the structured app (`app/routes/health_routes.py`), the same response is returned by `get_health()`.

### Flow: GET /api/weather
This section describes the structured flow because it best represents the intended long-term layering.

The client calls `GET /api/weather?city={city}&units={units}`.

The route handler in `app/routes/weather_routes.py` receives a dependency-injected `WeatherQuery` object from `WeatherQueryDep`.

The dependency function `WeatherQueryDep` calls `WeatherQuery.as_query`, which normalizes and validates the inputs. If `city` is blank or `units` is invalid, it raises `HTTPException(status_code=400, detail=...)`.

When valid, the route calls `get_weather_handler(query)`.

The controller `get_weather_handler` calls the service function `get_mock_weather(city=..., units=...)`.

The service computes deterministic values (temperature, description, humidity, windSpeed) and attaches a UTC timestamp string.

The route returns the dict which FastAPI serializes to JSON.

The single-file implementation in `main.py` performs similar validation and mock data computation directly inside the route function rather than going through a controller/service abstraction.

### Flow: GET /api/forecast
In the structured app, the flow mirrors the weather endpoint.

The client calls `GET /api/forecast?city={city}&days={N}`.

The route handler receives a `ForecastQuery` object from `ForecastQueryDep`.

The dependency validates city and days (ensuring days is an integer within 1..10), raising `HTTPException(400, detail=...)` on error.

The controller calls `get_mock_forecast(city=..., days=...)`, which builds a list of day entries with simple variations.

The response is returned as `{ "city": ..., "days": ..., "forecast": [...] }`.

## Error Handling
### Validation Errors (400)
Both implementations produce 400 responses by raising `fastapi.HTTPException` with a structured `detail` payload.

This keeps error messaging explicit and aligned with typical client-side consumption patterns.

### Not Found (404)
The structured app (`app/app.py`) includes middleware that intercepts responses and replaces 404s with a JSON payload:

```json
{
  "error": "Not Found",
  "message": "Route GET /some/path not found"
}
```

The single-file app does not currently add a custom 404 payload; it will use FastAPI’s default 404 response format.

### Unhandled Errors (500)
The structured app registers an exception handler for all `Exception` types and returns:

```json
{
  "error": "Internal Server Error",
  "message": "..."
}
```

The single-file app does not register a global exception handler and will use FastAPI’s default error behavior.

## Operational Notes
### Run Locally
Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the server (default port 3001):

```bash
python main.py
```

Override the port:

```bash
PORT=3001 python main.py
```

### Observability
No explicit logging, metrics, or tracing are currently configured. Uvicorn/FastAPI will emit basic access logs depending on Uvicorn defaults and runtime flags.

## Current State: Mock Data Only
The service does not call any external provider and does not require API keys. All values are derived from deterministic computations in `app/services/weather_service.py` (and similar logic duplicated in `main.py`).

Because the responses are mock, they are suitable for frontend development and integration tests that should not depend on external network calls.

## Plan: Integrate a Real Weather Provider
A clean integration plan is to preserve current routes and response shapes while replacing the internal mock service computation.

A typical approach would include the following steps.

Introduce a provider client module responsible for outbound HTTP calls and provider-specific authentication (for example, API key header or query param).

Add environment variables for provider configuration such as provider name, base URL, API key, request timeouts, and a toggle for mock fallback.

Update the service layer so `get_mock_weather` and `get_mock_forecast` either become `get_weather`/`get_forecast` with a provider-backed implementation or dispatch to either mock or provider based on configuration.

Add basic resilience features such as timeouts, retry policy (bounded), and error mapping to stable internal errors.

Add caching for frequently requested cities if performance or provider quotas require it.

## Security Considerations (Current and Future)
CORS is currently open to all origins, which is convenient for development but should be tightened for production.

If a provider API key is added, it should be sourced from environment variables and never committed to the repository.

The service currently has no authentication or rate limiting; if deployed publicly, rate limiting and request quotas should be added to prevent abuse and control costs.

Input validation is already implemented for key query parameters; additional validation may be needed for unicode normalization and maximum lengths if exposed to the public internet.

## Performance Considerations (Current and Future)
The current mock implementation is CPU-light and should perform well for typical development loads.

When integrating an external provider, performance will be dominated by outbound network latency. Use explicit timeouts and consider caching.

FastAPI’s async support can help concurrency when using an async HTTP client for provider calls, but care should be taken to avoid blocking I/O.

## Example Requests/Responses
### Health
```bash
curl "http://localhost:3001/health"
```

```json
{ "status": "ok" }
```

### Weather
```bash
curl "http://localhost:3001/api/weather?city=London&units=metric"
```

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

### Forecast
```bash
curl "http://localhost:3001/api/forecast?city=London&days=3"
```

```json
{
  "city": "London",
  "days": 3,
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
