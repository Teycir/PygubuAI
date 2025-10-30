#!/bin/bash
# Verification script for PygubuAI improvements

set -e

echo "🔍 Verifying PygubuAI Improvements..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0

# Helper function
check_command() {
    if eval "$1" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2"
        ((FAILED++))
    fi
}

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} File exists: $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} File missing: $1"
        ((FAILED++))
    fi
}

echo "📋 Checking new files..."
check_file "tests/test_integration.py"
check_file ".pre-commit-config.yaml"
check_file "docs/USER_GUIDE.md"
check_file "docs/DEVELOPER_GUIDE.md"
check_file "setup-dev.sh"
check_file "IMPROVEMENTS_COMPLETED.md"
check_file "IMPROVEMENTS_SUMMARY.md"

echo ""
echo "📦 Checking package installation..."
check_command "python3 -c 'import pygubuai'" "PygubuAI package importable"
check_command "pygubu-create --version" "pygubu-create command available"
check_command "pygubu-register --help" "pygubu-register command available"
check_command "pygubu-template list" "pygubu-template command available"

echo ""
echo "🔧 Checking development tools..."
check_command "command -v pytest" "pytest installed"
check_command "command -v black" "black installed"
check_command "command -v flake8" "flake8 installed"
check_command "command -v mypy" "mypy installed"
check_command "command -v pre-commit" "pre-commit installed"

echo ""
echo "🧪 Running tests..."
if pytest -v > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} All tests pass"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Some tests failed (check with 'make test')"
    ((FAILED++))
fi

echo ""
echo "📊 Checking coverage configuration..."
check_file ".coveragerc"
check_file "pyproject.toml"
if grep -q "tool.coverage" pyproject.toml; then
    echo -e "${GREEN}✓${NC} Coverage configuration in pyproject.toml"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Coverage configuration missing"
    ((FAILED++))
fi

echo ""
echo "🎨 Checking code style configuration..."
if grep -q "tool.black" pyproject.toml; then
    echo -e "${GREEN}✓${NC} Black configuration in pyproject.toml"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Black configuration missing"
    ((FAILED++))
fi

if grep -q "tool.mypy" pyproject.toml; then
    echo -e "${GREEN}✓${NC} Mypy configuration in pyproject.toml"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Mypy configuration missing"
    ((FAILED++))
fi

echo ""
echo "🔄 Checking CI configuration..."
check_file ".github/workflows/ci.yml"
if grep -q "codecov" .github/workflows/ci.yml; then
    echo -e "${GREEN}✓${NC} Codecov integration in CI"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Codecov integration missing"
    ((FAILED++))
fi

echo ""
echo "📚 Checking documentation..."
if grep -q "USER_GUIDE.md" README.md; then
    echo -e "${GREEN}✓${NC} README references USER_GUIDE.md"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} README doesn't reference USER_GUIDE.md"
    ((FAILED++))
fi

if grep -q "DEVELOPER_GUIDE.md" README.md; then
    echo -e "${GREEN}✓${NC} README references DEVELOPER_GUIDE.md"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} README doesn't reference DEVELOPER_GUIDE.md"
    ((FAILED++))
fi

echo ""
echo "🎯 Checking Makefile targets..."
check_command "grep -q 'format:' Makefile" "make format target exists"
check_command "grep -q 'typecheck:' Makefile" "make typecheck target exists"
check_command "grep -q 'pre-commit-install:' Makefile" "make pre-commit-install target exists"

echo ""
echo "=" | awk '{for(i=0;i<60;i++)printf "="; printf "\n"}'
echo "📊 Results Summary"
echo "=" | awk '{for(i=0;i<60;i++)printf "="; printf "\n"}'
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All improvements verified successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Run 'make test' to run full test suite"
    echo "  2. Run 'make coverage' to check code coverage"
    echo "  3. Run 'pre-commit run --all-files' to verify hooks"
    echo "  4. Read docs/USER_GUIDE.md and docs/DEVELOPER_GUIDE.md"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some checks failed. Review the output above.${NC}"
    echo ""
    echo "To fix issues:"
    echo "  1. Run './setup-dev.sh' to install missing tools"
    echo "  2. Run 'pip install -e \".[dev]\"' to install dev dependencies"
    echo "  3. Check that all files were created correctly"
    exit 1
fi
