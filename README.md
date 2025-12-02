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

### Automated Setup (Recommended)

Run this one-liner from your project root to automatically set up the coding guidelines:

```bash
curl -fsSL https://raw.githubusercontent.com/IshitaTakeshi/CodingGuideline/main/setup.sh | bash
```

Or download and run the script:

```bash
wget https://raw.githubusercontent.com/IshitaTakeshi/CodingGuideline/main/setup.sh
chmod +x setup.sh
./setup.sh
```

The script will:
- Add this repository as a git submodule (or update if already added)
- Copy GitHub workflows, issue templates, PR template, and labels configuration
- Copy CONTRIBUTING.md to your project root

### Manual Setup

If you prefer to set up manually:

```bash
# Add the submodule to your repository
git submodule add git@github.com:IshitaTakeshi/CodingGuideline.git .coding-guideline
git submodule update --init --recursive

# Copy the configurations you need
mkdir -p .github/workflows .github/ISSUE_TEMPLATE
cp .coding-guideline/.github/workflows/* .github/workflows/
cp .coding-guideline/.github/ISSUE_TEMPLATE/* .github/ISSUE_TEMPLATE/
cp .coding-guideline/.github/pull_request_template.md .github/
cp .coding-guideline/.github/labels.yml .github/
cp .coding-guideline/CONTRIBUTING.md ./

# Commit the changes
git add .github/ CONTRIBUTING.md .coding-guideline
git commit -m "chore: add coding guidelines"
```

## Updating the Guidelines

To update to the latest version, simply run the setup script again:

```bash
curl -fsSL https://raw.githubusercontent.com/IshitaTakeshi/CodingGuideline/main/setup.sh | bash
```

Or manually:

```bash
cd .coding-guideline
git pull origin main
cd ..
git add .coding-guideline
git commit -m "chore: update coding guidelines"
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
