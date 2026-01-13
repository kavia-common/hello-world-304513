const globals = require("globals");

/**
 * ESLint flat config for Node.js (CommonJS) project.
 * Kept intentionally lightweight for a small scaffold.
 */
module.exports = [
  {
    files: ["**/*.js"],
    ignores: ["node_modules/**", "coverage/**", "dist/**", "build/**"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "commonjs",
      globals: {
        ...globals.node
      }
    },
    rules: {
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "no-undef": "error",
      "no-console": "off"
    }
  }
];
