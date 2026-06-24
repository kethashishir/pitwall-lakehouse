.PHONY: help install test lint format check tree clean

help:
	@echo "PitWall Lakehouse commands:"
	@echo "  make install   Install project with dev dependencies"
	@echo "  make test      Run tests"
	@echo "  make lint      Run ruff lint checks"
	@echo "  make format    Format Python code with ruff"
	@echo "  make check     Run lint and tests"
	@echo "  make tree      Show project tree"
	@echo "  make clean     Remove local caches"

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

format:
	ruff format src tests
	ruff check --fix src tests

check: lint test

tree:
	find . -maxdepth 4 \
		-not -path "./.git/*" \
		-not -path "./.venv/*" \
		-not -path "./__pycache__/*" \
		| sort

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
