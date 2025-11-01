#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
KILOCODE_DIR="$PROJECT_ROOT/.kilocode"

echo "PygubuAI Kilo Code Setup"
echo "========================"
echo ""

show_help() {
    cat << EOF
Usage: $0 <command> [path]

Commands:
    self        - Mark PygubuAI repo itself for Kilo Code
    mark <path> - Mark a specific directory as PygubuAI-enabled
    scan <path> - Scan directory tree for pygubu projects and mark them
    status      - Show current Kilo Code configuration

Examples:
    $0 self
    $0 mark /path/to/my/project
    $0 scan ~/Repos
    $0 status
EOF
}

mark_directory() {
    local target_dir="$1"
    
    if [ ! -d "$target_dir" ]; then
        echo "Error: Directory does not exist: $target_dir"
        exit 1
    fi
    
    touch "$target_dir/.pygubuai"
    echo "Marked: $target_dir"
}

scan_and_mark() {
    local scan_dir="$1"
    
    if [ ! -d "$scan_dir" ]; then
        echo "Error: Directory does not exist: $scan_dir"
        exit 1
    fi
    
    echo "Scanning for pygubu projects in: $scan_dir"
    echo ""
    
    local count=0
    while IFS= read -r ui_file; do
        local project_dir="$(dirname "$ui_file")"
        if [ ! -f "$project_dir/.pygubuai" ]; then
            mark_directory "$project_dir"
            ((count++))
        fi
    done < <(find "$scan_dir" -name "*.ui" -type f 2>/dev/null)
    
    echo ""
    echo "Marked $count new pygubu projects"
}

show_status() {
    echo "Kilo Code Configuration Status"
    echo "==============================="
    echo ""
    echo "Configuration directory: $KILOCODE_DIR"
    
    if [ -d "$KILOCODE_DIR" ]; then
        echo "Status: Configured"
        echo ""
        echo "Files:"
        ls -lh "$KILOCODE_DIR/prompts/" 2>/dev/null || echo "  No prompts found"
        ls -lh "$KILOCODE_DIR/rules/" 2>/dev/null || echo "  No rules found"
    else
        echo "Status: Not configured"
        echo ""
        echo "Run setup first to create configuration"
    fi
    
    echo ""
    echo "Marked projects:"
    find /home/teycir/Repos -name ".pygubuai" -type f 2>/dev/null | while read marker; do
        echo "  $(dirname "$marker")"
    done
}

case "${1:-}" in
    self)
        echo "Marking PygubuAI repository for Kilo Code..."
        mark_directory "$PROJECT_ROOT"
        echo ""
        echo "Done! PygubuAI is now available in Kilo Code."
        echo "Just say 'pygubuai' in any chat from this directory."
        ;;
    
    mark)
        if [ -z "${2:-}" ]; then
            echo "Error: Please provide a directory path"
            echo ""
            show_help
            exit 1
        fi
        mark_directory "$2"
        echo ""
        echo "Done! Directory marked for PygubuAI in Kilo Code."
        ;;
    
    scan)
        if [ -z "${2:-}" ]; then
            echo "Error: Please provide a directory path to scan"
            echo ""
            show_help
            exit 1
        fi
        scan_and_mark "$2"
        echo ""
        echo "Done! All pygubu projects are now available in Kilo Code."
        ;;
    
    status)
        show_status
        ;;
    
    *)
        show_help
        exit 1
        ;;
esac
