/**
 * Mock weather service.
 *
 * This layer is intentionally dependency-free and does not call external APIs yet.
 * Later, it can be replaced by a real provider integration (e.g., OpenWeather).
 */

/**
 * Deterministic-ish mock temperature based on city name so different cities look different.
 * @param {string} city
 * @param {"metric"|"imperial"} units
 * @returns {number}
 */
function computeMockTemperature(city, units) {
  const baseC = 12;
  const variance = city
    .toLowerCase()
    .split("")
    .reduce((acc, ch) => acc + ch.charCodeAt(0), 0);

  const tempC = baseC + (variance % 15); // 12..26
  if (units === "imperial") {
    return Math.round((tempC * 9) / 5 + 32);
  }
  return tempC;
}

/**
 * Return a simple mock weather description.
 * @param {string} city
 * @returns {string}
 */
function computeMockDescription(city) {
  const options = ["Clear sky", "Partly cloudy", "Overcast", "Light rain", "Breezy"];
  const idx =
    city
      .toLowerCase()
      .split("")
      .reduce((acc, ch) => acc + ch.charCodeAt(0), 0) % options.length;
  return options[idx];
}

/**
 * @param {object} input
 * @param {string} input.city
 * @param {"metric"|"imperial"} input.units
 * @returns {{city:string, units:"metric"|"imperial", temperature:number, description:string, humidity:number, windSpeed:number, timestamp:string}}
 */
// PUBLIC_INTERFACE
function getMockWeather({ city, units }) {
  /** Get mock current weather payload for a city. */
  const temperature = computeMockTemperature(city, units);

  const humidity = 40 + (city.length * 7) % 55; // 40..94
  const windSpeedMetric = 2 + (city.length % 6); // 2..7 m/s
  const windSpeed = units === "imperial" ? Math.round(windSpeedMetric * 2.237) : windSpeedMetric;

  return {
    city,
    units,
    temperature,
    description: computeMockDescription(city),
    humidity,
    windSpeed,
    timestamp: new Date().toISOString()
  };
}

/**
 * @param {object} input
 * @param {string} input.city
 * @param {number} input.days
 * @returns {{city:string, days:number, forecast:Array<{date:string, temperature:number, description:string, humidity:number, windSpeed:number}>}}
 */
// PUBLIC_INTERFACE
function getMockForecast({ city, days }) {
  /** Get mock multi-day forecast payload for a city. */
  const today = new Date();
  const base = getMockWeather({ city, units: "metric" });

  const forecast = Array.from({ length: days }, (_, i) => {
    const date = new Date(today);
    date.setDate(today.getDate() + i + 1);

    // Simple variation day-by-day
    const tempC = base.temperature + ((i % 2 === 0 ? 1 : -1) * (i + 1));
    const humidity = Math.max(25, Math.min(95, base.humidity + (i % 3 === 0 ? 5 : -3)));
    const windSpeed = Math.max(1, base.windSpeed + (i % 2 === 0 ? 1 : -1));

    return {
      date: date.toISOString().slice(0, 10),
      temperature: tempC,
      description: computeMockDescription(`${city}-${i}`),
      humidity,
      windSpeed
    };
  });

  return {
    city,
    days,
    forecast
  };
}

module.exports = {
  getMockWeather,
  getMockForecast
};
