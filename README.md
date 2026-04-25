# Coding Guideline

A reusable coding guideline repository providing development standards, GitHub workflow automation, and project templates.

## Features

- Conventional Commits format for PR titles
- Semantic Versioning with automatic version management
- Clean history management with Squash & Merge
- Semi-automated release process with Release Drafter
- Issue and PR templates
- Automated labeling and PR title validation

## Setup

Add this repository as a submodule to your project:

```bash
git submodule add git@github.com:IshitaTakeshi/CodingGuideline.git .coding-guideline
git submodule update --init --recursive
```

When cloning a project that already has this submodule:

```bash
git clone --recurse-submodules <your-project-url>
# Or if already cloned without submodules:
git submodule update --init --recursive
```

## GitHub Workflows

The workflows in this repository support [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows). Reference them directly from your project without copying — they always run the version currently on `main` of this repository, independent of the submodule revision. To pin to a specific version, replace `@main` with a tag or commit SHA.

> **Permissions:** GitHub Actions tokens default to read-only in many repos. Each example below includes the required `permissions:` block so the workflow has write access where needed.

### PR Title Check

Create `.github/workflows/check-pr-title.yml` in your project:

```yaml
name: "Lint PR"
on:
  pull_request_target:
    types: [opened, edited, synchronize]
jobs:
  lint-pr:
    uses: IshitaTakeshi/CodingGuideline/.github/workflows/check-pr-title.yml@main
    permissions:
      pull-requests: write
      statuses: read
```

### Pull Request Labeler

Create `.github/workflows/labeler.yml` in your project:

```yaml
name: "Pull Request Labeler"
on:
  pull_request_target:
    types: [opened, synchronize, reopened]
jobs:
  label:
    uses: IshitaTakeshi/CodingGuideline/.github/workflows/labeler.yml@main
    permissions:
      contents: read
      pull-requests: write
```

Also copy the labeler configuration to your project (this file stays in your repo and can be customized):

```bash
cp .coding-guideline/.github/labeler.yml .github/labeler.yml
```

### Auto Major Label

Create `.github/workflows/auto-label-major.yml` in your project:

```yaml
name: "Auto-assign Major Label"
on:
  pull_request_target:
    types: [opened, edited, synchronize]
jobs:
  assign-major-label:
    uses: IshitaTakeshi/CodingGuideline/.github/workflows/auto-label-major.yml@main
    permissions:
      pull-requests: write
      issues: write
```

### Release Drafter

Create `.github/workflows/release-drafter.yml` in your project:

```yaml
name: Release Drafter
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  draft:
    uses: IshitaTakeshi/CodingGuideline/.github/workflows/release-drafter.yml@main
    permissions:
      contents: write
      pull-requests: read
```

Also copy the release drafter configuration to your project:

```bash
cp .coding-guideline/.github/release-drafter.yml .github/release-drafter.yml
```

## Copy-Once Files

These files are best copied once and owned by your project. After copying, customize them freely:

```bash
# Issue templates
cp -r .coding-guideline/.github/ISSUE_TEMPLATE .github/

# PR template
cp .coding-guideline/.github/pull_request_template.md .github/pull_request_template.md
```

## License

This project is licensed under CC0 1.0 Universal - see the [LICENSE](LICENSE) file for details.
