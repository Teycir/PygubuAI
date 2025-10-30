.PHONY: install test clean help

help:
	@echo "PygubuAI Development Commands"
	@echo ""
	@echo "  make install    - Install PygubuAI tools"
	@echo "  make test       - Run test suite"
	@echo "  make clean      - Remove generated files"
	@echo "  make lint       - Run code linters"

install:
	./install.sh

test:
	python -m unittest discover tests -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

lint:
	@command -v flake8 >/dev/null 2>&1 && flake8 *.py || echo "flake8 not installed"
	@command -v black >/dev/null 2>&1 && black --check *.py || echo "black not installed"
