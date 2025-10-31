.PHONY: test test-fast test-unit test-integration test-security test-coverage clean help

help:
	@echo "PygubuAI Test Commands"
	@echo "======================"
	@echo "make test          - Run all tests"
	@echo "make test-fast     - Run fast unit tests only"
	@echo "make test-unit     - Run all unit tests"
	@echo "make test-integration - Run integration tests"
	@echo "make test-security - Run security tests"
	@echo "make test-coverage - Run tests with HTML coverage report"
	@echo "make clean         - Remove test artifacts"

test:
	pytest -v

test-fast:
	pytest -m "unit and not slow" -v

test-unit:
	pytest -m unit -v

test-integration:
	pytest -m integration -v

test-security:
	pytest -m security -v

test-coverage:
	pytest --cov=pygubuai --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
