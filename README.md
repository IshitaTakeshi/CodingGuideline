# Coding Guideline

A reusable coding guideline repository that provides standardized development practices, CI/CD configurations, and project templates.

## Features

- Conventional Commits format for PR titles
- Semantic Versioning with automatic version management
- Clean history management with Squash & Merge
- Semi-automated release process with Release Drafter
- Issue and PR templates
- Automated labeling and PR title validation

## Usage as Git Submodule

### Adding to Your Project

To use this coding guideline in your project, add it as a git submodule:

```bash
# Add the submodule to your repository
git submodule add git@github.com:IshitaTakeshi/CodingGuideline.git .coding-guideline

# Initialize and update the submodule
git submodule update --init --recursive
```

### Using the Guidelines

Once added as a submodule, you can reference and copy the configurations you need:

1. **GitHub Workflows**: Copy workflows from `.coding-guideline/.github/workflows/` to `.github/workflows/`
2. **Issue Templates**: Copy templates from `.coding-guideline/.github/ISSUE_TEMPLATE/` to `.github/ISSUE_TEMPLATE/`
3. **PR Template**: Copy `.coding-guideline/.github/pull_request_template.md` to `.github/pull_request_template.md`
4. **Contributing Guide**: Reference or adapt `.coding-guideline/CONTRIBUTING.md`
5. **Labels Configuration**: Copy `.coding-guideline/.github/labels.yml` to `.github/labels.yml`

### Updating the Guidelines

To update to the latest version of the coding guidelines:

```bash
# Navigate to the submodule directory
cd .coding-guideline

# Pull the latest changes
git pull origin main

# Navigate back to your project root
cd ..

# Commit the submodule update
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
