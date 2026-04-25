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
* **Title**: Must strictly follow **[Naming Convention](#7-naming-convention-and-semver-conventional-commits)** (checked by CI).
* **Body**: Use the PR template to provide complete context. See **[PR Description Best Practices](#5-pr-description-best-practices)** below.
* **Labels**: Automatically assigned based on branch name.
    * ⚠️ **For breaking changes**: The `major` label is automatically assigned when the PR title contains `!`.
* **Draft PRs**: If your work is not ready for review, create a Draft PR. This signals to reviewers that the code is still in progress and allows early feedback without formal review.

### Step 5: Review & Merge
* CI (Lint PR, Tests) must pass.
* Reviewer approval is required.
* Select "Squash and Merge" and **verify that the commit message matches the PR title**.

### Step 6: Post-Merge Process
* **Issue**: Automatically closed if `Closes #xxx` is included.
* **Branch**: Automatically deleted after merge (or delete manually).

---

## 3. Milestone Branch Workflow

For projects with multiple independent concepts or large feature sets, use **milestone branches** to group related work under a single GitHub Milestone.

### Structure

```
main
└── milestone/<milestone-number>-<description>       ← one per GitHub Milestone
    ├── feature/<issue-number>-<description>
    └── fix/<issue-number>-<description>
```

* **`milestone-number`** is the **GitHub Milestone number**.
* The concept or goal is written in the **GitHub Milestone's description** — not in any file on the branch.
* Feature/fix branch naming follows the existing convention (`feature/<issue-number>-<description>`). Issue numbers are unique project-wide and are independent of milestone numbers.
* **Exception to [Section 2](#2-development-workflow)**: when using a milestone branch, feature/fix branches are created from the milestone branch — not from `main`.

### Lifecycle

1. **Open** a GitHub Milestone and describe the concept/goal in its description.
2. **Create** `milestone/<milestone-number>-<description>` from `main`.
3. **Work**: open Issues under the Milestone, create `feature/<issue-number>-...` branches from the milestone branch, and PR back into it.
4. **Close**: when all Issues are resolved, merge the milestone branch into `main` via a PR, then close the GitHub Milestone.
    * ⚠️ The `milestone/...` branch prefix is not matched by the auto-labeler. Add the appropriate SemVer label manually (`major`, `feature`, `fix`, etc.) before merging so release automation works correctly.

---

## 4. Issue Description Best Practices

A good issue is **self-documenting**: anyone should be able to understand it without prior context, even the author returning months later.

### Key Principles

* **Standalone Comprehension**: Write as if the reader knows nothing about your project. Include enough background that the issue makes sense on its own.
* **Answer the 5 Ws + H**: Who is affected? What is the problem/feature? When did it start/when is it needed? Where does it occur? Why does it matter? How will we verify success?
* **Be Specific**: Vague issues lead to misunderstandings. Use concrete examples, exact error messages, and measurable criteria.
* **Preserve Decision Context**: Document alternatives considered and why they were rejected. This prevents revisiting the same decisions later.

### Bug Report Sections

| Section | Purpose | Required |
| :--- | :--- | :---: |
| **Bug Description** | Clear summary of what's broken | Yes |
| **Impact / Severity** | Who is affected and how badly | Yes |
| **Steps to Reproduce** | Exact steps to trigger the bug | Yes |
| **Expected Behavior** | What should happen | Yes |
| **Current Behavior** | What actually happens | Yes |
| **First Occurrence** | When the bug started (helps identify cause) | Yes |
| **Frequency** | How often it occurs | Yes |
| **Workaround** | Temporary solution if any | Yes |
| **Environment** | OS, browser, version details | Yes |
| **Error Logs / Screenshots** | Evidence for debugging | If applicable |
| **Related Issues** | Links to similar or blocking issues | If applicable |

### Feature Request Sections

| Section | Purpose | Required |
| :--- | :--- | :---: |
| **User Story / Problem Statement** | Who needs this and why (persona-based) | Yes |
| **Purpose / Background** | Context and motivation for the feature | Yes |
| **Acceptance Criteria** | Measurable conditions for completion | Yes |
| **Out of Scope** | What is explicitly NOT included | Yes |
| **Success Metrics** | How to measure if the feature works | Yes |
| **Dependencies** | What must exist first | Yes |
| **Alternatives Considered** | Other approaches and why rejected | Yes |
| **Risks / Concerns** | Potential problems or challenges | Yes |
| **Implementation Overview** | Technical approach suggestions | Optional |
| **References** | Links to designs, docs, related issues | If applicable |

### Writing Tips

* **For bugs**: Include exact error messages, not paraphrased versions. Screenshots are worth a thousand words.
* **For features**: A clear user story prevents building the wrong thing. "As a user, I want X so that Y" forces you to articulate the real need.
* **For both**: Link to related issues liberally. Future readers will thank you for the context trail.

---

## 5. PR Description Best Practices

A good PR tells the story of your change: not just *what* changed, but *why* it changed and *how* to verify it.

### Key Principles

* **Keep PRs Focused**: Each PR should address a single concern. Don't mix unrelated changes (e.g., a bug fix with a large refactor). Smaller PRs are easier to review and less risky to merge.
* **Provide Context**: Explain the problem you're solving. The Issue link provides tracking, but reviewers benefit from understanding the "why" directly in the PR.
* **Be Specific with Test Steps**: Write exact steps that a reviewer can follow to verify your changes. Avoid vague instructions like "test the feature."

### PR Template Sections

| Section | Purpose | Required |
| :--- | :--- | :---: |
| **Related Issue** | Links PR to the tracking Issue for traceability | Yes |
| **Context** | Explains why this change is needed | Yes |
| **Changes** | High-level summary of what was modified | Yes |
| **Type of Change** | Helps reviewers understand the scope and risk | Yes |
| **Test Steps** | Step-by-step verification instructions | Yes |
| **Screenshots** | Visual proof for UI changes (Before/After) | If applicable |
| **Checklist** | Self-review confirmation | Yes |
| **Review Focus** | Guides reviewers to areas needing attention | Optional |

### Breaking Changes

When your PR title includes `!` (indicating a breaking change), provide additional context in the PR body:
* What existing behavior will change
* Migration steps for users
* Why the breaking change is necessary

---

## 6. Commit Message Best Practices

While this project uses **Squash & Merge** (making PR titles the final commit message), writing descriptive commit messages during development helps reviewers understand your changes and makes debugging easier.

### Structure

```text
<type>(<scope>): <subject>

<body>

<footer>
```

* **Subject line**: What changed (≤50 characters, imperative mood, no period)
* **Body**: Why it changed and what impact it has (wrap at 72 characters)
* **Footer**: Issue references (`Closes #123`) and co-author attribution

### The "Why" Is Essential

Every commit should answer these questions:

| Question | Purpose |
| :--- | :--- |
| **What problem existed?** | The motivation for the change |
| **What did you change?** | The subject line (what) |
| **Why this approach?** | Alternatives considered, trade-offs made |
| **What is the impact?** | Before vs. after behavior |

### Examples from This Repository

**❌ Missing context (actual commit):**
```text
fix: update workflow to use renamed issue template files (#65)

Closes #64
```
*Problem: Doesn't explain why files were renamed or what broke.*

**✅ With proper context:**
```text
fix: update workflow to use renamed issue template files (#65)

The issue template files were renamed from bug_report.md to fix.md
and feature_request.md to feature.md to align with the Conventional
Commits type names. The GitHub workflow still referenced the old
filenames, causing template validation to fail.

Closes #64
```

**❌ Missing motivation (actual commit):**
```text
ci: remove paths filter from test workflow for reliable status checks (#67)

Closes #66
```
*Problem: Doesn't explain what was unreliable or why.*

**✅ With proper context:**
```text
ci: remove paths filter from test workflow for reliable status checks (#67)

The paths filter skipped test runs when only documentation files
changed. However, GitHub requires all status checks to run before
merging. Skipped checks were blocking PRs because they never
reported a status.

Removing the filter ensures tests always run and report status,
even if the test itself has nothing new to verify.

Closes #66
```

### Quick Checklist

Before committing, verify your message answers:
- [ ] What problem does this solve?
- [ ] Why was this change necessary?
- [ ] What is different now compared to before?

---

## 7. Naming Convention and SemVer (Conventional Commits)

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
For changes that break backward compatibility, add `!` before the colon (after type or scope if present) in the PR title. The `major` label will be automatically assigned.

**Example:**
```
Title: feature!: migrate REST API to GraphQL

Body:
This PR migrates the entire API from REST to GraphQL.

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

## 8. Automation Setup (for Maintainers)

This project uses the following CI configurations to assist with guideline compliance:

* **PR Title Check**: [.github/workflows/check-pr-title.yml](.github/workflows/check-pr-title.yml)
* **Auto Labeling**: [.github/workflows/labeler.yml](.github/workflows/labeler.yml)
* **Labeler Configuration**: [.github/labeler.yml](.github/labeler.yml)

---

## 9. Release Process

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
| `fix`, `performance`, `revert` | 🐛 **Patch** (0.0.x) | Auto-assigned from `fix/*`, `performance/*`, `revert/*` branches |
| Others (`documentation`, `chore`, etc.) | None | Version number does not increase |

### Release Procedure
1. **Automatic Draft Generation**: Each time a PR is merged to `main`, the release notes draft is automatically updated.
2. **Execute Release**: Maintainers open the GitHub [Releases] page at any time and review the Draft content.
3. **Publish**: If the content is correct, click "Publish release".
    * A Git Tag is created at this point.
    * Published as an official Release Note.
