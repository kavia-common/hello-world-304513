const express = require("express");
const {
  getWeatherHandler,
  getForecastHandler
} = require("../controllers/weatherController");

const router = express.Router();

/**
 * GET /api/weather?city={name}&units=metric|imperial
 */
router.get("/weather", getWeatherHandler);

/**
 * GET /api/forecast?city={name}&days=5
 */
router.get("/forecast", getForecastHandler);

module.exports = router;
