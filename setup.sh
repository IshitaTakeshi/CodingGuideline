#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SUBMODULE_PATH=".coding-guideline"
REPO_URL="git@github.com:IshitaTakeshi/CodingGuideline.git"
MANIFEST_FILE=".coding-guideline-manifest.txt"

# Get current commit hash of the submodule
get_submodule_version() {
    cd "$SUBMODULE_PATH"
    git rev-parse HEAD
    cd ..
}

# Add header comment to a file based on its extension
add_header_to_file() {
    local file_path="$1"
    local version="$2"
    local temp_file="${file_path}.tmp"

    # Determine file extension
    local ext="${file_path##*.}"

    if [[ "$ext" == "yml" || "$ext" == "yaml" ]]; then
        # YAML files use # for comments
        echo "# Managed by CodingGuideline (version: ${version})" > "$temp_file"
        echo "# Do not edit manually - changes may be overwritten" >> "$temp_file"
        echo "# To update: run setup.sh update" >> "$temp_file"
        cat "$file_path" >> "$temp_file"
    elif [[ "$ext" == "md" ]]; then
        # Markdown files use HTML comments
        echo "<!-- Managed by CodingGuideline (version: ${version}) -->" > "$temp_file"
        echo "<!-- Do not edit manually - changes may be overwritten -->" >> "$temp_file"
        echo "<!-- To update: run setup.sh update -->" >> "$temp_file"
        cat "$file_path" >> "$temp_file"
    else
        # For other files, just copy as-is
        cp "$file_path" "$temp_file"
    fi

    mv "$temp_file" "$file_path"
}

# Initialize or update manifest file
init_manifest() {
    local version="$1"
    echo "version: ${version}" > "$MANIFEST_FILE"
}

# Add a file to the manifest
add_to_manifest() {
    local file_path="$1"
    echo "$file_path" >> "$MANIFEST_FILE"
}

# Copy file with header and tracking
copy_with_tracking() {
    local src="$1"
    local dest="$2"
    local version="$3"

    cp "$src" "$dest"
    add_header_to_file "$dest" "$version"
    add_to_manifest "$dest"
}

# Install/setup command
install_files() {
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

    # Get version and initialize manifest
    VERSION=$(get_submodule_version)
    init_manifest "$VERSION"
    echo -e "${GREEN}✓ Initialized manifest (version: ${VERSION:0:7})${NC}"

    # Create .github directory if it doesn't exist
    mkdir -p .github

    # Copy GitHub workflows
    if [ -d "$SUBMODULE_PATH/.github/workflows" ]; then
        echo -e "${YELLOW}Copying GitHub workflows...${NC}"
        mkdir -p .github/workflows
        for file in "$SUBMODULE_PATH/.github/workflows/"*; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                copy_with_tracking "$file" ".github/workflows/$filename" "$VERSION"
            fi
        done
        echo -e "${GREEN}✓ Workflows copied${NC}"
    fi

    # Copy issue templates
    if [ -d "$SUBMODULE_PATH/.github/ISSUE_TEMPLATE" ]; then
        echo -e "${YELLOW}Copying issue templates...${NC}"
        mkdir -p .github/ISSUE_TEMPLATE
        for file in "$SUBMODULE_PATH/.github/ISSUE_TEMPLATE/"*; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                copy_with_tracking "$file" ".github/ISSUE_TEMPLATE/$filename" "$VERSION"
            fi
        done
        echo -e "${GREEN}✓ Issue templates copied${NC}"
    fi

    # Copy PR template
    if [ -f "$SUBMODULE_PATH/.github/pull_request_template.md" ]; then
        echo -e "${YELLOW}Copying PR template...${NC}"
        copy_with_tracking "$SUBMODULE_PATH/.github/pull_request_template.md" ".github/pull_request_template.md" "$VERSION"
        echo -e "${GREEN}✓ PR template copied${NC}"
    fi

    # Copy labeler configuration
    if [ -f "$SUBMODULE_PATH/.github/labeler.yml" ]; then
        echo -e "${YELLOW}Copying labeler configuration...${NC}"
        copy_with_tracking "$SUBMODULE_PATH/.github/labeler.yml" ".github/labeler.yml" "$VERSION"
        echo -e "${GREEN}✓ Labeler configuration copied${NC}"
    fi

    # Copy release drafter configuration
    if [ -f "$SUBMODULE_PATH/.github/release-drafter.yml" ]; then
        echo -e "${YELLOW}Copying release drafter configuration...${NC}"
        copy_with_tracking "$SUBMODULE_PATH/.github/release-drafter.yml" ".github/release-drafter.yml" "$VERSION"
        echo -e "${GREEN}✓ Release drafter configuration copied${NC}"
    fi

    # Copy CONTRIBUTING.md
    if [ -f "$SUBMODULE_PATH/CONTRIBUTING.md" ]; then
        echo -e "${YELLOW}Copying CONTRIBUTING.md...${NC}"
        copy_with_tracking "$SUBMODULE_PATH/CONTRIBUTING.md" "CONTRIBUTING.md" "$VERSION"
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
    echo "   git add .github/ CONTRIBUTING.md $SUBMODULE_PATH $MANIFEST_FILE"
    echo "   git commit -m 'chore: add coding guidelines'"
    echo ""
    echo "To update guidelines: ./setup.sh update"
    echo "To remove guidelines: ./setup.sh remove"
}

# Update command - refresh all tracked files
update_files() {
    echo -e "${GREEN}Updating Coding Guidelines${NC}"
    echo "================================"

    if [ ! -f "$MANIFEST_FILE" ]; then
        echo -e "${RED}Error: Manifest file not found. Run './setup.sh' first.${NC}"
        exit 1
    fi

    # Update submodule
    echo -e "${YELLOW}Updating submodule...${NC}"
    git submodule update --init --recursive "$SUBMODULE_PATH"
    cd "$SUBMODULE_PATH"
    git pull origin main
    cd ..
    echo -e "${GREEN}✓ Submodule updated${NC}"

    # Get new version
    VERSION=$(get_submodule_version)
    echo -e "${GREEN}New version: ${VERSION:0:7}${NC}"

    # Read files from manifest (skip the version line)
    echo -e "${YELLOW}Updating tracked files...${NC}"
    updated_count=0
    while IFS= read -r line; do
        # Skip version line
        if [[ "$line" == version:* ]]; then
            continue
        fi

        if [ -n "$line" ]; then
            dest_file="$line"
            # Determine source file in submodule
            src_file="$SUBMODULE_PATH/$line"

            if [ -f "$src_file" ]; then
                cp "$src_file" "$dest_file"
                add_header_to_file "$dest_file" "$VERSION"
                echo "  Updated: $dest_file"
                updated_count=$((updated_count + 1))
            else
                echo -e "  ${YELLOW}Warning: Source file not found: $src_file${NC}"
            fi
        fi
    done < "$MANIFEST_FILE"

    # Update version in manifest
    {
        echo "version: ${VERSION}"
        tail -n +2 "$MANIFEST_FILE"
    } > "${MANIFEST_FILE}.tmp"
    mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"

    echo ""
    echo -e "${GREEN}✓ Updated $updated_count files${NC}"
    echo -e "${GREEN}================================${NC}"
    echo "Don't forget to commit the changes!"
}

# Remove command - delete all tracked files
remove_files() {
    echo -e "${YELLOW}Removing Coding Guidelines${NC}"
    echo "================================"

    if [ ! -f "$MANIFEST_FILE" ]; then
        echo -e "${RED}Error: Manifest file not found. Nothing to remove.${NC}"
        exit 1
    fi

    # Confirm with user
    echo -e "${RED}This will remove all files tracked in the manifest.${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi

    # Remove tracked files
    echo -e "${YELLOW}Removing tracked files...${NC}"
    removed_count=0
    while IFS= read -r line; do
        # Skip version line
        if [[ "$line" == version:* ]]; then
            continue
        fi

        if [ -n "$line" ] && [ -f "$line" ]; then
            rm "$line"
            echo "  Removed: $line"
            removed_count=$((removed_count + 1))
        fi
    done < "$MANIFEST_FILE"

    # Remove manifest itself
    rm "$MANIFEST_FILE"
    echo "  Removed: $MANIFEST_FILE"

    # Optionally remove submodule
    echo ""
    read -p "Do you also want to remove the submodule? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git submodule deinit -f "$SUBMODULE_PATH"
        git rm -f "$SUBMODULE_PATH"
        rm -rf ".git/modules/$SUBMODULE_PATH"
        echo -e "${GREEN}✓ Submodule removed${NC}"
    fi

    echo ""
    echo -e "${GREEN}✓ Removed $removed_count files${NC}"
    echo -e "${GREEN}================================${NC}"
    echo "Don't forget to commit the changes!"
}

# Main command dispatcher
case "${1:-install}" in
    install)
        install_files
        ;;
    update)
        update_files
        ;;
    remove)
        remove_files
        ;;
    *)
        echo "Usage: $0 {install|update|remove}"
        echo ""
        echo "Commands:"
        echo "  install (default) - Install coding guidelines"
        echo "  update            - Update tracked files to latest version"
        echo "  remove            - Remove all tracked files"
        exit 1
        ;;
esac
