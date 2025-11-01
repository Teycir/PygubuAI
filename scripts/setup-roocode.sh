#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

show_help() {
    cat << EOF
Usage: $0 <command> [path]

Commands:
    self        - Mark PygubuAI repo for Roo Code
    mark <path> - Mark directory as PygubuAI-enabled
    scan <path> - Scan and mark all pygubu projects

Examples:
    $0 self
    $0 mark /path/to/project
    $0 scan ~/Repos
EOF
}

mark_directory() {
    touch "$1/.pygubuai"
    echo "Marked: $1"
}

scan_and_mark() {
    echo "Scanning: $1"
    local count=0
    while IFS= read -r ui_file; do
        local dir="$(dirname "$ui_file")"
        [ ! -f "$dir/.pygubuai" ] && mark_directory "$dir" && ((count++))
    done < <(find "$1" -name "*.ui" -type f 2>/dev/null)
    echo "Marked $count projects"
}

case "${1:-}" in
    self) mark_directory "$PROJECT_ROOT" ;;
    mark) [ -z "$2" ] && show_help && exit 1; mark_directory "$2" ;;
    scan) [ -z "$2" ] && show_help && exit 1; scan_and_mark "$2" ;;
    *) show_help; exit 1 ;;
esac
