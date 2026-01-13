const express = require("express");
const cors = require("cors");
const morgan = require("morgan");

const healthRoutes = require("./routes/healthRoutes");
const weatherRoutes = require("./routes/weatherRoutes");

const { notFoundHandler, errorHandler } = require("./middleware/errorHandlers");

/**
 * Create and configure the Express application.
 * Split from server.js so it can be imported by tests later if needed.
 */
function createApp() {
  const app = express();

  // Basic middleware
  app.use(cors()); // allow all origins
  app.use(express.json());
  app.use(morgan("dev"));

  // Routes
  app.use(healthRoutes);
  app.use("/api", weatherRoutes);

  // 404 + error handling
  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
}

module.exports = { createApp };
