// Strict JavaScript/TypeScript ESLint Configuration
// Derivative repositories can extend this:
//
//   // eslint.config.js
//   import baseConfig from "./.coding-guideline/eslint.config.js";
//   export default [...baseConfig];
//
// Peer dependency required:
//   npm install --save-dev typescript-eslint

import tseslint from "typescript-eslint";

/** @type {Record<string, unknown>} */
const sharedRules = {
  // Section 1: Structure & Size Limits
  "max-lines": ["error", { "max": 100, "skipBlankLines": true, "skipComments": true }],
  "max-lines-per-function": ["error", { "max": 15, "skipBlankLines": true, "skipComments": true }],
  "max-params": ["error", 3],

  // Section 2: Control Flow — No Else (bans all else, including else-if)
  "no-restricted-syntax": [
    "error",
    {
      selector: "IfStatement[alternate]",
      message: "The else keyword is forbidden. Use guard clauses (early returns) instead.",
    },
  ],

  // Section 6: Imports
  "no-duplicate-imports": "error",

  // Section 7: Complexity Reduction
  "complexity": ["error", 4],
  "max-depth": ["error", 2],
};

/** @type {import("eslint").Linter.Config[]} */
export default [
  // JavaScript
  {
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      ...sharedRules,
      "no-unused-vars": "error",
    },
  },

  // TypeScript
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tseslint.parser,
    },
    plugins: {
      "@typescript-eslint": tseslint.plugin,
    },
    rules: {
      ...sharedRules,
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": "error",
    },
  },
];
