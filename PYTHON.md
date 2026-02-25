# Coding Standards & Guidelines

> **Philosophy:** "Pure, Atomic, Trivial."
> Every component must be small enough to be understood at a glance. Complexity is managed through composition, not indentation.

## 1. Structure & Size Limits (Strict)

We adhere to **Object Calisthenics** rules to force modularity.

| Scope | Max Size (excluding comments/docstrings) |
| :--- | :--- |
| **File** | **100 lines** |
| **Class** | **50 lines** |
| **Function** | **15 lines** |

* **File Sizing:** If a file exceeds 100 lines, it must be split. A file should contain only one class or a small set of tightly coupled functions.
* **Function Sizing:** The 15-line limit is absolute.
    * *Exceptions:* None. Even `try-except` blocks must be concise. If error handling is complex, delegate the logic inside the `try` block to a separate private function.
    * *When a function is too long:* Extract a sub-function. Never bundle parameters into a wrapper type to shrink the signature. See [Section 7](#7-complexity-reduction-no-artificial-grouping).

## 2. Control Flow: The "No Else" Rule

**The `else` keyword is forbidden.** Use Guard Clauses (Early Returns) instead.

**Incorrect:**
```python
def calculate_status(value: int) -> str:
    if value > 10:
        return "High"
    else:
        return "Low"

```

**Correct:**

```python
def calculate_status(value: int) -> str:
    if value > 10:
        return "High"
    return "Low"

```

## 3. Naming Conventions

* **Style:** Follow PEP8 (Snake case for functions/variables, PascalCase for classes).
* **Zero Tolerance for Abbreviations:** Names must be fully descriptive. Ambiguity is technical debt.

| Forbidden | Required Replacement |
| --- | --- |
| `idx`, `i` | `index`, `sequence_index` |
| `ctx` | `context` |
| `repo` | `repository` |
| `val` | `value` |
| `params` | `parameters` |
| `func` | `function` |

## 4. Type Safety

* **Strict Mode:** All code must pass `mypy --strict`.
* **No `Any`:** The use of `Any` is forbidden. If a type is truly dynamic, use `TypeVar` or specific `Protocol`.
* **Signatures:** Every function (public or private) must have type hints.

## 5. Documentation

* **Format:** Sphinx (ReStructuredText).
* **Requirement:** Mandatory docstrings for all **Public** Modules, Classes, and Functions.
* **Content:** Do not repeat type information in the docstring (the type hint is the source of truth). Focus on the *purpose* and *behavior*.

```python
def connect_to_database(connection_string: str) -> None:
    """
    Establishes the initial connection pool to the database.

    Raises:
        ConnectionError: If the remote host is unreachable.
    """
    ...

```

## 6. Imports

* **Sorting:** Automated via Ruff/Isort.
* **Unused Imports:** Strictly forbidden. The build will fail if detected.

## 7. Complexity Reduction: No Artificial Grouping

When a function exceeds size or argument limits, **decompose its logic** into
smaller functions — do not bundle its parameters into a wrapper type.

### The Anti-Pattern

Creating a `TypedDict`, `dataclass`, or `NamedTuple` purely to fit a long
signature into one argument does not reduce complexity. It displaces it. The
same operations still happen on the same data; only the surface area changed.

```python
# Wrong: SubplotConfig exists only to hide three arguments.
# The function is no simpler; callers now bear the construction cost.
@dataclass
class SubplotConfig:
    accessor: Callable[[Result], NDArray[np.float64]]
    ylabel: str
    title: str

def _configure_subplot(axis: Axes, config: SubplotConfig, ...) -> None:
    ...
```

```python
# Correct: extract a sub-function with a single, nameable responsibility.
# _plot_series can be understood, tested, and reused independently.
def _plot_series(
    axis: Axes, label: str, accessor: Callable[...], result: Result
) -> None:
    ...

def _configure_subplot(
    axis: Axes, accessor: Callable[...], ylabel: str, title: str, ...
) -> None:
    for label, result in results.items():
        _plot_series(axis, label, accessor, result)
    _decorate_axis(axis, ylabel, title)
```

### Litmus Test for a Legitimate Type

A `TypedDict`, `dataclass`, or `NamedTuple` is legitimate only if **all three**
conditions hold:

1. **Domain-named:** Its name comes from the problem domain, not from code
   structure. Red flags: `Config`, `Options`, `Params`, `Data`, `Info`.
2. **Restriction-independent:** It would exist even with no function size limit.
3. **Single entity:** Its fields describe one thing, not a collection of
   unrelated arguments that happen to go to the same function.

| ✅ Legitimate | ❌ Artificial |
| :--- | :--- |
| `SuspensionParameters` — a named concept in vehicle dynamics | `PlotStyle` — two matplotlib kwargs bundled to shrink a signature |
| `SimulationResult` — natural return type shared across module boundaries | `SubplotConfig` — three unrelated fields with only one consumer |

### When a Function Is Still Too Long

Ask: **"What distinct step can I name?"** Extract that named step into a private
function. The size limit exists to force you to name every concept — not to
encourage hiding concepts inside wrapper types.

## 8. Tooling

This repository provides configuration files for automated enforcement.

### Ruff (Linter & Formatter)

Derivative repositories can extend the ruff configuration:

```toml
# In your pyproject.toml
[tool.ruff]
extend = ".coding-guideline/ruff.toml"

# Or in a standalone ruff.toml
extend = ".coding-guideline/ruff.toml"
```

### MyPy (Type Checker)

MyPy does not support configuration inheritance. Copy the settings from [`mypy.toml`](mypy.toml) to your project's `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_any_explicit = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```
