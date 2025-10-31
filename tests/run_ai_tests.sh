#!/bin/bash
# Run complete AI integration test suite

set -e

echo "=========================================="
echo "PygubuAI - AI Integration Test Suite"
echo "=========================================="
echo ""

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest not found. Install with:"
    echo "  pip install -e '.[dev]'"
    exit 1
fi

echo "Running AI Integration Tests..."
echo ""

# Run basic AI tests
echo "1. Basic AI Integration Tests"
echo "------------------------------"
pytest tests/test_ai_integration.py -v --tb=short
echo ""

# Run real-world tests
echo "2. Real-World Application Tests"
echo "--------------------------------"
pytest tests/test_ai_realworld.py -v --tb=short
echo ""

# Run end-to-end workflow tests
echo "3. End-to-End Workflow Tests"
echo "----------------------------"
pytest tests/test_ai_e2e_workflow.py -v --tb=short
echo ""

# Summary
echo "=========================================="
echo "Test Suite Complete!"
echo "=========================================="
echo ""
echo "Coverage Report:"
pytest tests/test_ai_*.py --cov=pygubuai.ai_analyzer --cov=pygubuai.ai_context --cov=pygubuai.ai_query --cov=pygubuai.ai_refactor --cov-report=term-missing
