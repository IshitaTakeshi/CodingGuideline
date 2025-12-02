#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SUBMODULE_PATH=".coding-guideline"
REPO_URL="git@github.com:IshitaTakeshi/CodingGuideline.git"

echo -e "${GREEN}Coding Guideline Setup${NC}"
echo "================================"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository. Please run this script from your project root.${NC}"
    exit 1
fi

# Add or update submodule
if [ -d "$SUBMODULE_PATH" ]; then
    echo -e "${YELLOW}Submodule already exists. Updating...${NC}"
    git submodule update --init --recursive "$SUBMODULE_PATH"
    cd "$SUBMODULE_PATH"
    git pull origin main
    cd ..
    git add "$SUBMODULE_PATH"
    echo -e "${GREEN}✓ Submodule updated${NC}"
else
    echo -e "${YELLOW}Adding submodule...${NC}"
    git submodule add "$REPO_URL" "$SUBMODULE_PATH"
    git submodule update --init --recursive
    echo -e "${GREEN}✓ Submodule added${NC}"
fi

# Create .github directory if it doesn't exist
mkdir -p .github

# Copy GitHub workflows
if [ -d "$SUBMODULE_PATH/.github/workflows" ]; then
    echo -e "${YELLOW}Copying GitHub workflows...${NC}"
    mkdir -p .github/workflows
    cp -r "$SUBMODULE_PATH/.github/workflows/"* .github/workflows/
    echo -e "${GREEN}✓ Workflows copied${NC}"
fi

# Copy issue templates
if [ -d "$SUBMODULE_PATH/.github/ISSUE_TEMPLATE" ]; then
    echo -e "${YELLOW}Copying issue templates...${NC}"
    mkdir -p .github/ISSUE_TEMPLATE
    cp -r "$SUBMODULE_PATH/.github/ISSUE_TEMPLATE/"* .github/ISSUE_TEMPLATE/
    echo -e "${GREEN}✓ Issue templates copied${NC}"
fi

# Copy PR template
if [ -f "$SUBMODULE_PATH/.github/pull_request_template.md" ]; then
    echo -e "${YELLOW}Copying PR template...${NC}"
    cp "$SUBMODULE_PATH/.github/pull_request_template.md" .github/pull_request_template.md
    echo -e "${GREEN}✓ PR template copied${NC}"
fi

# Copy labeler configuration
if [ -f "$SUBMODULE_PATH/.github/labeler.yml" ]; then
    echo -e "${YELLOW}Copying labeler configuration...${NC}"
    cp "$SUBMODULE_PATH/.github/labeler.yml" .github/labeler.yml
    echo -e "${GREEN}✓ Labeler configuration copied${NC}"
fi

# Copy release drafter configuration
if [ -f "$SUBMODULE_PATH/.github/release-drafter.yml" ]; then
    echo -e "${YELLOW}Copying release drafter configuration...${NC}"
    cp "$SUBMODULE_PATH/.github/release-drafter.yml" .github/release-drafter.yml
    echo -e "${GREEN}✓ Release drafter configuration copied${NC}"
fi

# Copy CONTRIBUTING.md
if [ -f "$SUBMODULE_PATH/CONTRIBUTING.md" ]; then
    echo -e "${YELLOW}Copying CONTRIBUTING.md...${NC}"
    cp "$SUBMODULE_PATH/CONTRIBUTING.md" ./CONTRIBUTING.md
    echo -e "${GREEN}✓ CONTRIBUTING.md copied${NC}"
fi

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review the copied files in .github/ and CONTRIBUTING.md"
echo "2. Customize them for your project if needed"
echo "3. Commit the changes:"
echo "   git add .github/ CONTRIBUTING.md $SUBMODULE_PATH"
echo "   git commit -m 'chore: add coding guidelines'"
echo ""
echo "To update guidelines in the future, run this script again."
