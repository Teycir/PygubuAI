#!/bin/bash

# PygubuAI Trigger Setup Script
# Places .pygubuai marker files to enable auto-detection

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYGUBUAI_ROOT="$(dirname "$SCRIPT_DIR")"

echo "PygubuAI Trigger Setup"
echo "======================"
echo ""

# Function to create marker file
create_marker() {
    local dir="$1"
    local marker="$dir/.pygubuai"
    
    if [ -f "$marker" ]; then
        echo "  Already exists: $marker"
        return
    fi
    
    cat > "$marker" << 'EOF'
# PygubuAI Project Marker
# This file enables automatic PygubuAI context loading
# When you mention "pygubuai" in Amazon Q chat, context is auto-loaded

project_root: .
enabled: true
EOF
    
    echo "  Created: $marker"
}

# Option 1: Mark specific directory
if [ "$1" = "mark" ] && [ -n "$2" ]; then
    TARGET_DIR="$(cd "$2" && pwd)"
    echo "Marking directory: $TARGET_DIR"
    create_marker "$TARGET_DIR"
    echo ""
    echo "Done! Now you can use 'pygubuai' keyword from this directory."
    exit 0
fi

# Option 2: Scan and mark all pygubu projects
if [ "$1" = "scan" ]; then
    SCAN_DIR="${2:-$HOME/Repos}"
    echo "Scanning for pygubu projects in: $SCAN_DIR"
    echo ""
    
    # Find directories with .ui files
    find "$SCAN_DIR" -type f -name "*.ui" 2>/dev/null | while read -r ui_file; do
        project_dir="$(dirname "$ui_file")"
        create_marker "$project_dir"
    done
    
    echo ""
    echo "Done! All pygubu projects are now marked."
    exit 0
fi

# Option 3: Mark PygubuAI repo itself
if [ "$1" = "self" ]; then
    echo "Marking PygubuAI repository: $PYGUBUAI_ROOT"
    create_marker "$PYGUBUAI_ROOT"
    echo ""
    echo "Done!"
    exit 0
fi

# Default: Show usage
cat << 'EOF'
Usage:
  ./setup-trigger.sh mark <directory>    Mark specific directory
  ./setup-trigger.sh scan [directory]    Scan and mark all pygubu projects
  ./setup-trigger.sh self                Mark PygubuAI repo itself

Examples:
  ./setup-trigger.sh mark ~/myproject
  ./setup-trigger.sh scan ~/Repos
  ./setup-trigger.sh scan /home/teycir/Repos
  ./setup-trigger.sh self

After setup, just mention "pygubuai" in Amazon Q chat from any marked directory!
EOF
