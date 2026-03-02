# Coding Guideline

A reusable coding guideline repository that provides standardized development practices, CI/CD configurations, and project templates.

## Features

- Conventional Commits format for PR titles
- Semantic Versioning with automatic version management
- Clean history management with Squash & Merge
- Semi-automated release process with Release Drafter
- Issue and PR templates
- Automated labeling and PR title validation

## Quick Start

Run the following command from your project root:

```bash
curl -fsSL https://raw.githubusercontent.com/IshitaTakeshi/CodingGuideline/main/setup.sh | bash
```

Alternatively, you can download and run the script manually:

1. Download the setup script from the [GitHub repository](https://github.com/IshitaTakeshi/CodingGuideline)
2. Run the script from your project root:

```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Add this repository as a git submodule (or update if already added)
- Copy GitHub workflows, issue templates, PR template, labeler and release drafter configurations
- Add comment headers to all copied files indicating they are managed by CodingGuideline
- Create a manifest file (`.coding-guideline-manifest.txt`) to track all copied files

## Managing the Guidelines

### Updating to the Latest Version

To update all guideline files to the latest version:

```bash
./setup.sh update
```

This will:
- Update the submodule to the latest version
- Refresh all tracked files with the latest content
- Update comment headers with the new version

### Setting Up JavaScript/TypeScript Tooling

To bootstrap ESLint and TypeScript in a JavaScript or TypeScript project:

```bash
./setup.sh javascript
```

Prerequisites: `node` and `npm` must be installed. The guideline submodule must already be present (run `./setup.sh install` first).

This will:
- Create `package.json` with `"type": "module"` if one does not exist, or add the field if it does
- Install `typescript-eslint` as a dev dependency
- Create `eslint.config.js` extending the shared ESLint config, if absent
- Create `tsconfig.json` extending the shared TypeScript base config, if absent

`eslint.config.js` and `tsconfig.json` are **user-owned** — they are not tracked in the manifest and will not be touched by `update` or `remove`. Customize them freely.

### Removing the Guidelines

To remove all guideline files from your project:

```bash
./setup.sh remove
```

This will:
- Remove all files tracked in the manifest
- Optionally remove the submodule
- Clean up the manifest file

The script will ask for confirmation before removing files.

### How File Tracking Works

All copied files include comment headers that identify them as managed by CodingGuideline:

**YAML files** (workflows, configs):
```yaml
# Managed by CodingGuideline (version: abc1234)
# Do not edit manually - changes may be overwritten
# To update: run setup.sh update
```

**Markdown files** (templates, documentation):
```markdown
<!-- Managed by CodingGuideline (version: abc1234) -->
<!-- Do not edit manually - changes may be overwritten -->
<!-- To update: run setup.sh update -->
```

The manifest file (`.coding-guideline-manifest.txt`) tracks all copied files:
```
version: abc1234567890...
.github/workflows/labeler.yml
.github/workflows/release-drafter.yml
.github/ISSUE_TEMPLATE/fix.md
.github/ISSUE_TEMPLATE/feature.md
.github/pull_request_template.md
```

### Cloning a Project with This Submodule

When cloning a project that uses this guideline as a submodule:

```bash
# Clone with submodules
git clone --recurse-submodules <your-project-url>

# Or if already cloned without submodules
git submodule update --init --recursive
```

## License

This project is licensed under CC0 1.0 Universal - see the [LICENSE](LICENSE) file for details.
