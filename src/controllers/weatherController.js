const { getMockWeather, getMockForecast } = require("../services/weatherService");

/**
 * Normalize and validate "units" query param.
 * @param {string|undefined} unitsRaw
 * @returns {"metric"|"imperial"}
 */
function normalizeUnits(unitsRaw) {
  if (!unitsRaw) return "metric";
  const u = String(unitsRaw).toLowerCase();
  if (u === "metric" || u === "imperial") return u;
  return null;
}

/**
 * Parse and validate "days" query param.
 * @param {string|undefined} daysRaw
 * @returns {number|null}
 */
function normalizeDays(daysRaw) {
  if (!daysRaw) return 5;
  const parsed = Number(daysRaw);
  if (!Number.isFinite(parsed) || !Number.isInteger(parsed)) return null;
  if (parsed < 1 || parsed > 10) return null; // small guardrail for mock scaffold
  return parsed;
}

// PUBLIC_INTERFACE
function getWeatherHandler(req, res, next) {
  /** Express handler for current weather endpoint. */
  try {
    const city = req.query.city ? String(req.query.city).trim() : "";
    if (!city) {
      return res.status(400).json({
        error: "Bad Request",
        message: 'Query parameter "city" is required.'
      });
    }

    const units = normalizeUnits(req.query.units);
    if (!units) {
      return res.status(400).json({
        error: "Bad Request",
        message: 'Query parameter "units" must be "metric" or "imperial" when provided.'
      });
    }

    const payload = getMockWeather({ city, units });
    return res.json(payload);
  } catch (err) {
    return next(err);
  }
}

// PUBLIC_INTERFACE
function getForecastHandler(req, res, next) {
  /** Express handler for forecast endpoint. */
  try {
    const city = req.query.city ? String(req.query.city).trim() : "";
    if (!city) {
      return res.status(400).json({
        error: "Bad Request",
        message: 'Query parameter "city" is required.'
      });
    }

    const days = normalizeDays(req.query.days);
    if (days === null) {
      return res.status(400).json({
        error: "Bad Request",
        message: 'Query parameter "days" must be an integer between 1 and 10.'
      });
    }

    const payload = getMockForecast({ city, days });
    return res.json(payload);
  } catch (err) {
    return next(err);
  }
}

module.exports = {
  getWeatherHandler,
  getForecastHandler
};
