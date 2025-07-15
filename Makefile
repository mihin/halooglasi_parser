.PHONY: help install test run schedule clean setup test-env

help:
	@echo "HaloOglasi Parser - Available Commands:"
	@echo "======================================"
	@echo "  setup     - Set up virtual environment and install dependencies"
	@echo "  install   - Install package in development mode"
	@echo "  test      - Run tests"
	@echo "  test-env  - Test environment variable configuration"
	@echo "  run       - Run apartment search"
	@echo "  schedule  - Start the scheduler"
	@echo "  clean     - Clean up build artifacts and cache files"
	@echo ""

setup:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

install:
	venv/bin/pip install -e .

test:
	venv/bin/python -m pytest tests/ -v

test-env:
	venv/bin/python scripts/test_env_config.py

run:
	venv/bin/python scripts/run_search.py

schedule:
	@echo "Starting apartment scheduler..."
	venv/bin/python scripts/scheduler.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Alias for convenience
start: schedule 