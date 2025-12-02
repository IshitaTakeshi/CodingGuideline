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

## Updating the Guidelines

To update to the latest version, download the latest setup script from the [GitHub repository](https://github.com/IshitaTakeshi/CodingGuideline) and run it again:

```bash
./setup.sh
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
