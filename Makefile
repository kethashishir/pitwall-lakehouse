.PHONY: help install test lint format check dbt-debug dbt-build quality-report dagster-list dagster-materialize dagster-dev streamlit-demo build-fixture-bronze tree clean

help:
	@echo "PitWall Lakehouse commands:"
	@echo "  make install   Install project with dev dependencies"
	@echo "  make test      Run tests"
	@echo "  make lint      Run ruff lint checks"
	@echo "  make format    Format Python code with ruff"
	@echo "  make check     Run lint and tests"
	@echo "  make build-fixture-bronze  Build bronze Parquet from test fixture"
	@echo "  make dbt-debug Run dbt debug against local DuckDB profile"
	@echo "  make dbt-build Run dbt build against local DuckDB profile"
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

build-fixture-bronze:
	python -m pitwall.ingestion.raw_to_bronze \
		--raw-dir tests/fixtures/raw/racedata_sample \
		--bronze-dir data/bronze/racedata_sample \
		--manifest-dir metadata/ingestion_manifests \
		--source-name racedata_sample

dbt-debug:
	dbt debug --project-dir dbt/pitwall_dbt --profiles-dir dbt/pitwall_dbt

dbt-build:
	dbt build --project-dir dbt/pitwall_dbt --profiles-dir dbt/pitwall_dbt

quality-report:
	python -m pitwall.quality.dbt_quality_report \
		--artifact-path dbt/pitwall_dbt/target/run_results.json \
		--output-dir metadata/data_quality_reports

dagster-list:
	dagster asset list -m orchestration.dagster_project.definitions

dagster-materialize:
	dagster asset materialize --select "*" -m orchestration.dagster_project.definitions

dagster-dev:
	dagster dev -m orchestration.dagster_project.definitions

streamlit-demo:
	python -m streamlit run dashboard/streamlit_app/app.py


tree:
	find . -maxdepth 4 \
		-not -path "./.git/*" \
		-not -path "./.venv/*" \
		-not -path "./__pycache__/*" \
		| sort

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
