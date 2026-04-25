# Coding Standards & Guidelines

> **Philosophy:** "Pure, Atomic, Trivial."
> Every component must be small enough to be understood at a glance. Complexity is managed through composition, not indentation.

## 1. Structure & Size Limits (Strict)

We adhere to **Object Calisthenics** rules to force modularity.

| Scope | Max Size (excluding comments/JSDoc) |
| :--- | :--- |
| **File** | **100 lines** |
| **Class / Module** | **50 lines** |
| **Function** | **15 lines** |

* **File Sizing:** If a file exceeds 100 lines, it must be split. A file should contain only one class or a small set of tightly coupled functions.
* **Function Sizing:** The 15-line limit is absolute.
    * *Exceptions:* None. Even `try...catch` blocks must be concise. If error handling is complex, delegate the logic inside the `try` block to a separate private function.
    * *When a function is too long:* Extract a sub-function. Never bundle parameters into a single "options" object just to shrink the signature. See [Section 7](#7-complexity-reduction-no-artificial-grouping).
* **Parameter Limit:** Functions may accept at most **3 parameters**. When a function needs more, decompose its logic — do not bundle parameters into an "options" object. See [Section 7](#7-complexity-reduction-no-artificial-grouping).

## 2. Control Flow: The "No Else" Rule

**The `else` keyword is forbidden.** Use Guard Clauses (Early Returns) instead.

**Incorrect:**
```javascript
function calculateStatus(value) {
    if (value > 10) {
        return "High";
    } else {
        return "Low";
    }
}

```

**Correct:**

```javascript
function calculateStatus(value) {
    if (value > 10) {
        return "High";
    }
    return "Low";
}

```

## 3. Naming Conventions

* **Style:** `camelCase` for functions, variables, and instances. `PascalCase` for classes, interfaces, and types. `UPPER_SNAKE_CASE` for global constants.
* **Zero Tolerance for Abbreviations:** Names must be fully descriptive. Ambiguity is technical debt.

| Forbidden | Required Replacement |
| --- | --- |
| `idx`, `i` | `index`, `sequenceIndex` |
| `ctx` | `context` |
| `cb` | `callback`, `onComplete` |
| `val` | `value` |
| `req` / `res` | `request` / `response` |
| `err` | `error` |

## 4. Type Safety

* **Strict Mode:** All code must run strictly (`"use strict";` or natively via ES Modules) and pass TypeScript strict checks (or strict JSDoc via `tsc --noEmit`). JavaScript-only projects using JSDoc must add `"allowJs": true` and `"checkJs": true` to their `tsconfig.json` to enable type checking.
* **No `any`:** The use of `any` (or implicit any) is forbidden. If a type is truly dynamic, use `unknown` and narrow it with type guards, or use Generics (`<T>`).
* **Signatures:** Every function (public or private) must have explicit parameter and return types defined via TypeScript or JSDoc.

## 5. Documentation

* **Format:** JSDoc.
* **Requirement:** Mandatory JSDoc blocks for all **Public** (exported) Modules, Classes, and Functions.
* **Content:** Do not just repeat the type information if using TypeScript. Focus on the *purpose*, *behavior*, and *side effects*.

```javascript
/**
 * Establishes the initial connection pool to the database.
 * @param {string} connectionString - The fully qualified database URI.
 * @returns {Promise<void>}
 * @throws {ConnectionError} If the remote host is unreachable.
 */
async function connectToDatabase(connectionString) {
    // ...
}

```

## 6. Imports

* **Sorting:** Can be automated via ESLint (e.g., `eslint-plugin-import` or `simple-import-sort`), but requires an additional plugin — not included in the base rules above.
* **Unused Imports:** Strictly forbidden. The build will fail if detected.
* **Paths:** Prefer absolute alias paths (e.g., `@/components/`) over deep relative paths (`../../../components/`).

## 7. Complexity Reduction: No Artificial Grouping

When a function exceeds size or argument limits, **decompose its logic** into smaller functions — do not bundle its parameters into an "options" object or wrapper type just to bypass the rules.

### The Anti-Pattern

Creating a TypeScript `interface`, `type`, or JSDoc `@typedef` purely to fit a long signature into one argument does not reduce complexity. It displaces it. The same operations still happen on the same data; only the surface area changed.

```javascript
// Wrong: SubplotConfig exists only to hide three arguments.
// The function is no simpler; callers now bear the construction cost.

/**
 * @typedef {Object} SubplotConfig
 * @property {string} ylabel
 * @property {string} title
 * @property {string} color
 */

function _configureSubplot(axis, config) {
    // ...
}

```

```javascript
// Correct: extract a sub-function with a single, nameable responsibility.
// _plotSeries can be understood, tested, and reused independently.
function _plotSeries(axis, label, result) {
    // ...
}

function _configureSubplot(axis, ylabel, title) {
    for (const [label, result] of Object.entries(results)) {
        _plotSeries(axis, label, result);
    }
    _decorateAxis(axis, ylabel, title);
}

```

### Litmus Test for a Legitimate Type / Object

An options object or data structure is legitimate only if **all three** conditions hold:

1. **Domain-named:** Its name comes from the problem domain, not from code structure. Red flags: `Config`, `Options`, `Params`, `Data`, `Info`.
2. **Restriction-independent:** It would exist even with no function size limit.
3. **Single entity:** Its properties describe one holistic thing, not a collection of unrelated arguments that happen to go to the same function.

| ✅ Legitimate | ❌ Artificial |
| --- | --- |
| `SuspensionParameters` — a named concept in vehicle dynamics | `PlotStyle` — two generic args bundled to shrink a signature |
| `SimulationResult` — natural return type shared across module boundaries | `SubplotConfig` — three unrelated fields with only one consumer |

### When a Function Is Still Too Long

Ask: **"What distinct step can I name?"** Extract that named step into a private function. The size limit exists to force you to name every concept — not to encourage hiding concepts inside wrapper objects.

## 8. Tooling

### ESLint (Linter)

Bootstrap ESLint with the official setup tool:

```sh
npm init @eslint/config@latest
```

Then add the following rules to your `eslint.config.js` to enforce this guideline:

```js
rules: {
  // Section 1: Size limits
  "max-lines": ["error", { "max": 100, "skipBlankLines": true, "skipComments": true }],
  "max-lines-per-function": ["error", { "max": 15, "skipBlankLines": true, "skipComments": true }],
  "max-params": ["error", 3],

  // Section 2: No else
  "no-restricted-syntax": [
    "error",
    {
      selector: "IfStatement[alternate]",
      message: "The else keyword is forbidden. Use guard clauses (early returns) instead.",
    },
  ],

  // Section 6: Imports
  "no-duplicate-imports": "error",

  // Section 7: Complexity
  "complexity": ["error", 4],
  "max-depth": ["error", 2],
}
```

For TypeScript files, also disable the base `no-unused-vars` and enable `@typescript-eslint/no-unused-vars: "error"`.

### TypeScript (Type Checker)

Bootstrap TypeScript with:

```sh
npx tsc --init
```

Then enable these compiler options in `tsconfig.json` to satisfy [Section 4](#4-type-safety):

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

> **Minimum version:** `"moduleResolution": "bundler"` requires **TypeScript ≥ 5.0**.

> **Browser projects:** The default `lib` targets ES2020 only. Add `"DOM"` and `"DOM.Iterable"`:
> ```json
> { "compilerOptions": { "lib": ["ES2020", "DOM", "DOM.Iterable"] } }
> ```
