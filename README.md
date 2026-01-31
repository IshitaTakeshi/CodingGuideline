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
- Copy CONTRIBUTING.md to your project root
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
CONTRIBUTING.md
```

### Cloning a Project with This Submodule

When cloning a project that uses this guideline as a submodule:

```bash
# Clone with submodules
git clone --recurse-submodules <your-project-url>

# Or if already cloned without submodules
git submodule update --init --recursive
```

### Claude Configuration for Derivative Repositories

If you use Claude Code in your derivative repository, you can add a `CLAUDE.md` file to automatically fetch the submodule when it's missing. Create a `CLAUDE.md` file in your project root with the following content:

~~~markdown
If the `.coding-guideline` directory is missing or empty, run:
```bash
git submodule update --init --recursive
```
~~~

This instructs Claude to check for the submodule and initialize it if needed, which handles the common case of cloning without `--recursive`.

## License

This project is licensed under CC0 1.0 Universal - see the [LICENSE](LICENSE) file for details.
