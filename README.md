# Weather App (Mock API) — Python/FastAPI

A minimal **Python/FastAPI** backend scaffolded as a basic weather app. It serves **mock** weather and forecast data (no external API keys required yet).

## Requirements
- Python 3.11+ recommended

## Install
Create and activate a virtual environment (recommended), then install dependencies:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Run (preview uses port 3001)
The server listens on **http://localhost:3001** by default.

```bash
python main.py
```

You may also override the port via environment variable:

```bash
PORT=3001 python main.py
```

## Documentation
- [Product Requirements Document (PRD)](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)

## API

### Health
`GET /health`

Response:
```json
{ "status": "ok" }
```

### Current weather (mock)
`GET /api/weather?city={name}&units=metric|imperial`

Example:
```bash
curl "http://localhost:3001/api/weather?city=London&units=metric"
```

### Forecast (mock)
`GET /api/forecast?city={name}&days=5`

Example:
```bash
curl "http://localhost:3001/api/forecast?city=London&days=5"
```

## Tooling (suggested)
- Lint/format (ruff):
  ```bash
  pip install ruff
  ruff check .
  ruff format .
  ```

Notes:
- No external weather API integration is implemented yet; responses are mock/deterministic.
- CORS is enabled for all origins to match the previous Express scaffold.
