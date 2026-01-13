const { createApp } = require("./app");

/**
 * Server entrypoint.
 *
 * Starts the HTTP server on port 3001 to match the preview environment.
 */
function startServer() {
  const app = createApp();

  const port = Number(process.env.PORT) || 3001;

  app.listen(port, () => {
    // Minimal boot log
    // eslint-disable-next-line no-console
    console.log(`Weather API server listening on port ${port}`);
  });
}

// Start immediately when executed as a script.
startServer();
