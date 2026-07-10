.PHONY: help install test lint format check docker-required docker-build docker-check docker-fixture-pipeline dbt-debug dbt-build dbt-build-fixture dbt-build-latest quality-report dagster-list dagster-materialize dagster-materialize-fixture dagster-materialize-latest dagster-dev streamlit-demo demo-fixture demo-latest build-fixture-bronze download-racedata build-latest-racedata-bronze tree clean

help:
	@echo "PitWall Lakehouse commands:"
	@echo "  make install   Install project with dev dependencies"
	@echo "  make test      Run tests"
	@echo "  make lint      Run ruff lint checks"
	@echo "  make format    Format Python code with ruff"
	@echo "  make check     Run lint and tests"
	@echo "  make docker-build Build Docker image"
	@echo "  make docker-check Run checks in Docker"
	@echo "  make docker-fixture-pipeline Run fixture pipeline in Docker"
	@echo "  make build-fixture-bronze  Build bronze Parquet from test fixture"
	@echo "  make dbt-debug Run dbt debug against local DuckDB profile"
	@echo "  make dbt-build Run dbt build against local DuckDB profile"
	@echo "  make dbt-build-fixture Run dbt build against fixture bronze data"
	@echo "  make dbt-build-latest Run dbt build against latest production bronze data"
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

dbt-build-fixture:
	dbt build --project-dir dbt/pitwall_dbt --profiles-dir dbt/pitwall_dbt --vars '{"bronze_dataset": "racedata_sample"}'

dbt-build-latest:
	dbt build --project-dir dbt/pitwall_dbt --profiles-dir dbt/pitwall_dbt --vars '{"bronze_dataset": "racedata_latest"}'

quality-report:
	python -m pitwall.quality.dbt_quality_report \
		--artifact-path dbt/pitwall_dbt/target/run_results.json \
		--output-dir metadata/data_quality_reports

dagster-list:
	dagster asset list -m orchestration.dagster_project.definitions

dagster-materialize:
	dagster asset materialize --select "*" -m orchestration.dagster_project.definitions

dagster-materialize-fixture:
	PITWALL_BRONZE_DATASET=racedata_sample dagster asset materialize --select "*" -m orchestration.dagster_project.definitions

dagster-materialize-latest:
	PITWALL_BRONZE_DATASET=racedata_latest dagster asset materialize --select "*" -m orchestration.dagster_project.definitions

dagster-dev:
	dagster dev -m orchestration.dagster_project.definitions

streamlit-demo:
	python -m streamlit run dashboard/streamlit_app/app.py

demo-fixture:
	$(MAKE) build-fixture-bronze
	$(MAKE) dbt-build-fixture
	$(MAKE) quality-report
	$(MAKE) streamlit-demo

demo-latest:
	$(MAKE) build-latest-racedata-bronze
	$(MAKE) dbt-build-latest
	$(MAKE) quality-report
	$(MAKE) streamlit-demo


tree:
	find . -maxdepth 4 \
		-not -path "./.git/*" \
		-not -path "./.venv/*" \
		-not -path "./__pycache__/*" \
		| sort

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +

download-racedata:
	python -m pitwall.ingestion.download_racedata \
		--raw-root-dir data/raw/racedata \
		--manifest-dir metadata/ingestion_manifests

build-latest-racedata-bronze:
	python -m pitwall.ingestion.build_latest_racedata_bronze

docker-required:
	@command -v docker >/dev/null 2>&1 || { echo "Docker is not installed or not on PATH. Install/start Docker Desktop, then rerun this target."; exit 127; }

docker-build: docker-required
	docker build -t pitwall-lakehouse:local .

docker-check: docker-required
	docker run --rm pitwall-lakehouse:local make check

docker-fixture-pipeline: docker-required
	docker run --rm pitwall-lakehouse:local sh -c "make check && make build-fixture-bronze && dbt deps --project-dir dbt/pitwall_dbt --profiles-dir dbt/pitwall_dbt && make dbt-build-fixture && make quality-report"

