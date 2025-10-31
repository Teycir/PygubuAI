.PHONY: help install test test-fast test-integration test-performance test-coverage lint clean

help:
	@echo "PygubuAI Development Commands"
	@echo ""
	@echo "  make install           - Install package in development mode"
	@echo "  make test              - Run all tests"
	@echo "  make test-fast         - Run fast tests only"
	@echo "  make test-integration  - Run integration tests"
	@echo "  make test-performance  - Run performance tests"
	@echo "  make test-coverage     - Run tests with coverage report"
	@echo "  make lint              - Run linters"
	@echo "  make clean             - Clean build artifacts"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-fast:
	pytest tests/ -v -m "not slow and not integration and not performance"

test-integration:
	pytest tests/test_integration.py -v

test-performance:
	pytest tests/test_performance.py -v

test-coverage:
	pytest tests/ -v --cov=src/pygubuai --cov-report=html --cov-report=term

lint:
	flake8 src/pygubuai --max-line-length=120 --extend-ignore=E203,W503
	black --check src/pygubuai

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf htmlcov/ .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
