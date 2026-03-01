// Strict JavaScript/TypeScript ESLint Configuration
// Derivative repositories can extend this:
//
//   // eslint.config.js
//   import baseConfig from "./.coding-guideline/eslint.config.js";
//   export default [...baseConfig];

/** @type {import("eslint").Linter.Config[]} */
export default [
  {
    rules: {
      // Section 1: Structure & Size Limits
      "max-lines": ["error", { "max": 100, "skipBlankLines": true, "skipComments": true }],
      "max-lines-per-function": ["error", { "max": 15, "skipBlankLines": true, "skipComments": true }],
      "max-params": ["error", 3],

      // Section 2: Control Flow — No Else
      "no-else-return": "error",

      // Section 6: Imports
      "no-unused-vars": "error",
      "no-duplicate-imports": "error",

      // Section 7: Complexity Reduction
      "complexity": ["error", 4],
      "max-depth": ["error", 2],
    },
  },
];
