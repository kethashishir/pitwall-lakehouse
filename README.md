# PitWall Lakehouse

PitWall Lakehouse is a local-first Formula 1 data-engineering platform that ingests historical race data, validates and transforms it into trusted analytics marts, and exposes strategy, reliability, pace, and data-quality evidence through a polished demo.

## Project pitch

Build an F1 analytics lakehouse that ingests historical race data plus selected modern telemetry/session data, validates and transforms it into trusted race-strategy marts, and exposes analytics, lineage, and data-quality evidence through a polished demo.

## Why this project exists

This project is designed to demonstrate serious data-engineering skills:

- reproducible ingestion
- raw, bronze, silver, and gold lakehouse layers
- typed Parquet outputs
- dbt transformations
- data quality checks
- orchestration
- tests and CI
- analytics marts
- a small polished demo reading trusted gold outputs

This is not intended to be a generic Formula 1 dashboard or CRUD app.

## Current status

Phase 8: Streamlit demo over trusted gold outputs.

Implemented:

- project structure
- Python package skeleton
- local configuration object
- test/lint tooling
- lakehouse directory layout
- source assessment documentation
- ingestion design documentation
- tiny RaceData-style raw CSV fixture
- source contract tests
- raw-to-bronze Parquet conversion
- JSON ingestion manifest generation
- raw-to-bronze row-count reconciliation tests
- dbt project using DuckDB
- bronze views over Parquet
- silver canonical dimensions and facts
- first gold analytics marts
- generated dbt data-quality summary reports
- Dagster assets for bronze ingestion, dbt build, and quality reporting
- expanded gold marts for reliability, strategy windows, stint degradation, and row-count summaries
- Streamlit demo reading trusted gold outputs and quality reports

Not implemented yet:

- full data download
- full production ingestion from downloaded source archive
- Parquet conversion
- dbt models
- data quality checks
- Dagster orchestration
- Streamlit dashboard

## Planned architecture

~~~text
data/
  raw/      source-preserved files and cached API responses
  bronze/   typed source-preserved Parquet
  silver/   normalized canonical F1 tables
  gold/     analytics marts for strategy, pace, reliability, and quality

metadata/
  ingestion_manifests/
  data_quality_reports/
  run_logs/
~~~

## Initial data-source decision

The project starts with TracingInsights RaceData as the primary historical CSV source because it is easier to reproduce locally and in CI than direct Kaggle access.

See:

~~~text
docs/data_source_assessment.md

~~~text
docs/ingestion_design.md
~~~
~~~

## Local development

Create and activate a virtual environment:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

Install development dependencies:

~~~bash
make install
~~~

Run checks:

~~~bash
make check
~~~

## Project layout

~~~text
src/pitwall/          Python package code
tests/                unit and integration tests
docs/                 architecture and source documentation
data/                 local lakehouse storage, ignored except .gitkeep files
metadata/             generated manifests, quality reports, and logs
dbt/                  future dbt project
orchestration/        future Dagster project
dashboard/            future Streamlit app
~~~

## Scope control

Non-goals for the early phases:

- no Kafka
- no Spark
- no Kubernetes
- no paid APIs
- no LLM/RAG
- no frontend-first development
- no full historical telemetry

## Raw-to-bronze fixture ingestion

Run fixture raw-to-bronze ingestion:

~~~bash
python -m pitwall.ingestion.raw_to_bronze \
  --raw-dir tests/fixtures/raw/racedata_sample \
  --bronze-dir data/bronze/racedata_sample \
  --manifest-dir metadata/ingestion_manifests \
  --source-name racedata_sample
~~~

The generated Parquet files are local artifacts and are not committed.

## dbt transformation layer

Build fixture bronze files first:

~~~bash
make build-fixture-bronze
~~~

Install dbt packages:

~~~bash
dbt deps --project-dir dbt/pitwall_dbt --profiles-dir dbt/pitwall_dbt
~~~

Validate the dbt profile:

~~~bash
make dbt-debug
~~~

Run dbt models and tests:

~~~bash
make dbt-build
~~~

## Data-quality report

After running dbt build, generate a readable quality summary:

~~~bash
make quality-report
~~~

Generated reports are written locally under:

~~~text
metadata/data_quality_reports/
~~~

These reports are generated artifacts and are not committed.

## Dagster orchestration

List local Dagster assets:

~~~bash
make dagster-list
~~~

Materialize the local lakehouse pipeline:

~~~bash
make dagster-materialize
~~~

Launch the local Dagster UI:

~~~bash
make dagster-dev
~~~

The Dagster UI is for local development and observability only. Generated Dagster artifacts are not committed.

## Gold analytics marts

Current gold marts include:

~~~text
mart_race_summary
mart_driver_pace
mart_pit_stop_efficiency
mart_constructor_reliability
mart_strategy_windows
mart_stint_degradation
mart_data_quality_run_summary
~~~

These marts are currently validated against the tiny fixture. They prove the transformation structure, not full historical F1 conclusions yet.

## Streamlit demo

Before launching the demo, materialize the local pipeline:

~~~bash
make dagster-materialize
~~~

Then launch Streamlit:

~~~bash
make streamlit-demo
~~~

The demo reads only trusted gold tables and generated quality reports. It does not read raw CSVs directly.

## Fixture vs production dbt builds

The dbt bronze layer is parameterized with a `bronze_dataset` variable.

Build against the committed tiny fixture:

~~~bash
make build-fixture-bronze
make dbt-build-fixture
~~~

Build against the latest downloaded production RaceData bronze files:

~~~bash
make download-racedata
make build-latest-racedata-bronze
make dbt-build-latest
~~~

The default dbt project variable is:

~~~text
bronze_dataset: racedata_sample
~~~

This keeps local smoke tests fast while still supporting real public-data builds.

## Audit models

The project includes dbt audit models for production data anomalies:

~~~text
audit_lap_time_duplicate_grain
audit_pit_stop_missing_duration
audit_result_nullable_numeric_fields
audit_source_to_silver_row_counts
~~~

These models make cleaning decisions explainable instead of silent.

## Streamlit audit evidence

The Streamlit demo includes an Audit Evidence section that reads dbt audit models from DuckDB.

This makes production source anomalies visible in the demo instead of hiding them in the transformation logic.

## Dagster dataset modes

Dagster can materialize either the tiny fixture dataset or the latest downloaded production RaceData snapshot.

Fixture mode:

~~~bash
make dagster-materialize-fixture
~~~

Production mode:

~~~bash
make download-racedata
make dagster-materialize-latest
~~~

The selected dataset is controlled by:

~~~text
PITWALL_BRONZE_DATASET
~~~

Supported values:

~~~text
racedata_sample
racedata_latest
~~~

## Continuous integration

GitHub Actions runs the fixture pipeline on pushes and pull requests.

CI validates:

~~~text
Python linting
unit tests
fixture raw-to-bronze ingestion
dbt fixture build
dbt tests
quality report generation
~~~

Production RaceData download is intentionally not run in CI because it depends on external network/data size and should remain a local production-mode workflow.
