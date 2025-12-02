# Contributing Guide

To ensure development transparency and proper version management with Semantic Versioning, please follow these rules.

## 1. Philosophy

* **No Issue, No Code**: All code changes must start with an Issue.
* **Semantic Versioning**: Version (Major.Minor.Patch) is automatically determined based on PR titles and history.
* **Squash & Merge**: The `main` branch history is kept clean with "1 feature/fix = 1 commit". **Commit messages during work are flexible, but PR titles must be strictly managed.**

---

## 2. Development Workflow

### Step 1: Create an Issue
When you find a task or bug, create an Issue. Choose the appropriate template:
* **Feature Request**: For new features/tasks (completion criteria required)
* **Bug Report**: For bug reports (reproduction steps required)

### Step 2: Create a Branch
Create a working branch from `main`.
**Naming convention: `prefix/issue-number-description`**

* **prefix**: Corresponds to the Type (see below): `feature/`, `fix/`, `documentation/`, etc.
* **issue-number**: The corresponding Issue number (required)
* **description**: Brief description in kebab-case (lowercase letters and hyphens)

**Good examples:**
* ✅ `feature/123-login-page` (Login feature for Issue #123)
* ✅ `fix/45-auth-token-bug` (Bug fix for Issue #45)
* ✅ `documentation/67-api-guide` (Documentation update for Issue #67)

### Step 3: Implementation & Push
Develop locally. Since changes will be squash merged, commit messages during work are flexible (e.g., `wip`, `fix`).

### Step 4: Create a Pull Request (PR)
Create a PR on GitHub.
* **Title**: Must strictly follow **[Naming Convention](#3-naming-convention-and-semver-conventional-commits)** (checked by CI).
* **Body**: Include `Closes #123` or `Fixes #45` to link to the Issue. Describe changes, screenshots, and test methods.
* **Labels**: Automatically assigned based on branch name.
    * ⚠️ **For breaking changes**: The `major` label is automatically assigned when the PR title contains `!`.

### Step 5: Review & Merge
* CI (Lint PR, Tests) must pass.
* Reviewer approval is required.
* **Merge responsibility**: The PR creator should merge. Select "Squash and Merge" and **verify that the commit message matches the PR title**.

### Step 6: Post-Merge Process
* **Issue**: Automatically closed if `Closes #xxx` is included.
* **Branch**: Automatically deleted after merge (or delete manually).

---

## 3. Naming Convention and SemVer (Conventional Commits)

Pull Request titles must follow the **Conventional Commits** format.

**Format:**
```text
<type>(<scope>): <description>
```

* **type**: Type of change (required - see table below)
* **scope**: Area of change (optional). Enclosed in parentheses.
    * Examples: `feature(api):`, `fix(ui):`, `chore(deps):`
* **description**: Brief description of the change (required).

### Type List and Version Impact

| Type | Meaning | SemVer Impact | Corresponding Branch Name |
| :--- | :--- | :--- | :--- |
| **feature** | New feature | Minor (0.x.0) | `feature/xxx` |
| **fix** | Bug fix | Patch (0.0.x) | `fix/xxx` |
| **performance** | Performance improvement | Patch | `performance/xxx` |
| **revert** | Revert changes | Patch | `revert/xxx` |
| **documentation** | Documentation changes | None | `documentation/xxx` |
| **style** | Code formatting only | None | `style/xxx` |
| **refactor** | Refactoring | None | `refactor/xxx` |
| **test** | Test additions/modifications | None | `test/xxx` |
| **build** | Build system changes | None | `build/xxx` |
| **ci** | CI configuration changes | None | `ci/xxx` |
| **chore** | Other miscellaneous changes | None | `chore/xxx` |

### ⚠️ Breaking Changes (Major Version)
For changes that break backward compatibility, follow both steps:

1. Add `!` after the Type in the PR title
2. Include `BREAKING CHANGE: details` in the PR body footer

The `major` label will be automatically assigned based on the `!` in the PR title.

**Complete example:**
```
Title: feature!: migrate REST API to GraphQL

Body:
This PR migrates the entire API from REST to GraphQL.

BREAKING CHANGE: All REST endpoints have been removed. Clients must migrate to GraphQL queries.

Closes #123
```
The `major` label will be automatically added when the PR is created.

### ✅ Good PR Title Examples
* `feature(auth): add login page`
* `fix(api): fix null error when fetching user info`
* `feature!: migrate REST API to GraphQL` (breaking change)
* `documentation: update README setup instructions`
* `chore(deps): update eslint to 8.0.0`

### ❌ Bad PR Title Examples
* `add login page` (missing Type)
* `feature:add login` (missing space after colon)
* `feature(auth) add login` (missing colon)
* `update` (no Type or Scope, unclear content)
* `feature(auth): Add login page and fix bug and refactor code` (mixing multiple changes in one PR)

---

## 4. Automation Setup (for Maintainers)

This project uses the following CI configurations to assist with guideline compliance:

* **PR Title Check**: [.github/workflows/check-pr-title.yml](.github/workflows/check-pr-title.yml)
* **Auto Labeling**: [.github/workflows/labeler.yml](.github/workflows/labeler.yml)
* **Labeler Configuration**: [.github/labeler.yml](.github/labeler.yml)

---

## 5. Release Process

This project uses **[Release Drafter](https://github.com/release-drafter/release-drafter)** to semi-automate the release process.

### Configuration Files
* **Release Drafter Configuration**: [.github/release-drafter.yml](.github/release-drafter.yml)
* **Release Drafter Workflow**: [.github/workflows/release-drafter.yml](.github/workflows/release-drafter.yml)

### Label to Version Mapping

The next version is determined based on labels assigned to PRs.

| Label | Version Impact | Notes |
| :--- | :--- | :--- |
| `major` | 🚨 **Major** (x.0.0) | **Automatically assigned when PR title contains `!`** |
| `feature` | 🚀 **Minor** (0.x.0) | Auto-assigned from `feature/*` branches |
| `fix`, `bug`, `performance` | 🐛 **Patch** (0.0.x) | Auto-assigned from `fix/*`, `performance/*` branches, etc. |
| Others (`documentation`, `chore`, etc.) | None | Version number does not increase |

### Release Procedure
1. **Automatic Draft Generation**: Each time a PR is merged to `main`, the release notes draft is automatically updated.
2. **Execute Release**: Maintainers open the GitHub [Releases] page at any time and review the Draft content.
3. **Publish**: If the content is correct, click "Publish release".
    * A Git Tag is created at this point.
    * Published as an official Release Note.
