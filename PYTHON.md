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

## 7. Tooling

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
