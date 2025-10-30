#!/bin/bash
# Development environment setup script for PygubuAI

set -e

echo "🚀 Setting up PygubuAI development environment..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Install package with dev dependencies
echo ""
echo "📦 Installing PygubuAI with dev dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo ""
echo "🔧 Installing pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "   ✓ Pre-commit hooks installed"
else
    echo "   ⚠️  pre-commit not found, skipping hooks installation"
fi

# Run tests to verify setup
echo ""
echo "🧪 Running tests to verify setup..."
if command -v pytest &> /dev/null; then
    pytest -v
    echo "   ✓ Tests passed"
else
    python3 run_tests.py
fi

# Run linters
echo ""
echo "🔍 Running linters..."
if command -v flake8 &> /dev/null; then
    flake8 src/pygubuai --max-line-length=120 --extend-ignore=E203,W503 || echo "   ⚠️  Linting issues found"
fi

if command -v black &> /dev/null; then
    black --check src/pygubuai || echo "   ⚠️  Formatting issues found (run 'make format' to fix)"
fi

# Verify CLI commands
echo ""
echo "✅ Verifying CLI commands..."
pygubu-create --version
pygubu-register --help > /dev/null
pygubu-template list > /dev/null

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  make test              - Run tests"
echo "  make coverage          - Run tests with coverage"
echo "  make lint              - Run linters"
echo "  make format            - Format code"
echo "  make typecheck         - Run type checking"
echo "  pre-commit run --all-files - Run all pre-commit hooks"
echo ""
echo "📚 Documentation:"
echo "  docs/USER_GUIDE.md      - User documentation"
echo "  docs/DEVELOPER_GUIDE.md - Developer documentation"
echo ""
