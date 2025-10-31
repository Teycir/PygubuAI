#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./run_example.sh <example_name>"
    echo ""
    echo "Available examples:"
    echo "  calculator      - Calculator with number pad"
    echo "  todo_app        - Todo list manager"
    echo "  login_form      - Login form with validation"
    echo "  settings_dialog - Settings with tabs"
    echo "  data_viewer     - Data table viewer"
    echo "  number_game     - Number guessing game"
    echo ""
    echo "Example: ./run_example.sh calculator"
    exit 1
fi

EXAMPLE=$1
EXAMPLE_DIR="examples/$EXAMPLE"

if [ ! -d "$EXAMPLE_DIR" ]; then
    echo "Error: Example '$EXAMPLE' not found"
    exit 1
fi

cd "$EXAMPLE_DIR"
python3 ${EXAMPLE}.py
