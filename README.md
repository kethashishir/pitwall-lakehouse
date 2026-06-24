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

Phase 2: source contract and tiny raw fixture.

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

Not implemented yet:

- full data download
- production ingestion
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
