/**
 * Express error handling middleware and 404 handler.
 */

// PUBLIC_INTERFACE
function notFoundHandler(req, res, _next) {
  /** Handle unknown routes with a JSON 404 response. */
  res.status(404).json({
    error: "Not Found",
    message: `Route ${req.method} ${req.originalUrl} not found`
  });
}

// PUBLIC_INTERFACE
function errorHandler(err, req, res, _next) {
  /** Handle unexpected errors with a JSON 500 response. */
  // eslint-disable-next-line no-console
  console.error("Unhandled error:", err);

  const status = err.statusCode && Number.isInteger(err.statusCode) ? err.statusCode : 500;

  res.status(status).json({
    error: status === 500 ? "Internal Server Error" : "Error",
    message: err.message || "Unexpected error"
  });
}

module.exports = {
  notFoundHandler,
  errorHandler
};
