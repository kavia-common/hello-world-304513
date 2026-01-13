# Weather App (Mock API)

A minimal Node/Express backend scaffolded as a basic weather app. It serves mock weather and forecast data (no external API keys required yet).

## Requirements
- Node.js 18+ recommended

## Install
```bash
npm install
```

## Run (preview uses port 3001)
Production-like:
```bash
npm start
```

Dev (auto-reload):
```bash
npm run dev
```

The server listens on **http://localhost:3001**.

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

## Tooling
- Lint: `npm run lint`
- Format: `npm run format`

Note: linting/formatting are provided for development; they do not affect runtime.