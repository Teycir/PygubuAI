.PHONY: install test clean help lint coverage uninstall dev

help:
	@echo "PygubuAI Development Commands"
	@echo ""
	@echo "  make dev        - Install in development mode"
	@echo "  make install    - Install PygubuAI (legacy shell script)"
	@echo "  make test       - Run test suite"
	@echo "  make coverage   - Run tests with coverage"
	@echo "  make lint       - Run code linters"
	@echo "  make clean      - Remove generated files"
	@echo "  make uninstall  - Uninstall PygubuAI"

dev:
	pip install -e ".[dev]"

install:
	./install.sh

uninstall:
	./uninstall.sh

test:
	@command -v pytest >/dev/null 2>&1 && pytest -v || python3 run_tests.py

coverage:
	@command -v pytest >/dev/null 2>&1 && pytest --cov=src/pygubuai --cov-report=html --cov-report=term-missing || ./run_coverage.sh
	@echo "Coverage report: htmlcov/index.html"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage

lint:
	@command -v flake8 >/dev/null 2>&1 && flake8 src/pygubuai || echo "⚠️  flake8 not installed"
	@command -v black >/dev/null 2>&1 && black --check src/pygubuai || echo "⚠️  black not installed"
