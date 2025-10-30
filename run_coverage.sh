#!/bin/bash
# Run tests with coverage

echo "Running tests with coverage..."
python3 -m coverage run --source=. -m unittest discover -s tests -p "test_*.py"

echo ""
echo "Coverage Report:"
python3 -m coverage report

echo ""
echo "Generating HTML report..."
python3 -m coverage html

echo ""
echo "✅ Coverage report generated in htmlcov/index.html"
