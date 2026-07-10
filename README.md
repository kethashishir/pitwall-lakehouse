# PitWall Lakehouse

![CI](https://github.com/kethashishir/pitwall-lakehouse/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![dbt](https://img.shields.io/badge/dbt-duckdb-orange)
![DuckDB](https://img.shields.io/badge/storage-DuckDB-yellow)
![Dagster](https://img.shields.io/badge/orchestration-Dagster-purple)
![Docker](https://img.shields.io/badge/docker-fixture--validated-blue)
![Status](https://img.shields.io/badge/status-portfolio--ready-brightgreen)

PitWall Lakehouse is a local-first Formula 1 data-engineering platform.

It ingests public race data, builds a DuckDB/dbt lakehouse, exposes quality and audit evidence, orchestrates the pipeline with Dagster, validates the fixture path in CI, and serves trusted outputs through a Streamlit demo.

The goal is not to build a flashy dashboard first. The goal is to prove a serious data platform:

~~~text
raw ingestion -> bronze Parquet -> silver cleaning -> audit evidence -> gold marts -> quality reports -> orchestration -> demo
~~~

## Why this project exists

Most portfolio projects stop at a dashboard or a CRUD app.

PitWall Lakehouse is built to show data-engineering fundamentals:

- reproducible ingestion
- local lakehouse storage
- bronze/silver/gold modeling
- source anomaly auditing
- dbt tests and quality reporting
- Dagster orchestration
- CI validation
- a thin demo over trusted outputs

## Architecture

A visual architecture diagram is available at:

~~~text
docs/architecture_diagram.md
~~~

~~~text
Public RaceData archive
  -> timestamped raw snapshot
  -> bronze Parquet files
  -> dbt bronze views
  -> dbt silver facts and dimensions
  -> dbt audit models
  -> dbt gold marts
  -> generated dbt quality report
  -> Streamlit demo
~~~

Dagster materializes:

~~~text
bronze_racedata
  -> dbt_lakehouse_build
  -> dbt_quality_summary
~~~

## Tech stack

- Python 3.11
- DuckDB
- Parquet
- pandas
- dbt-duckdb
- Dagster
- Streamlit
- pytest
- ruff
- GitHub Actions

## Data modes

The project supports two local data modes.

### Fixture mode

`racedata_sample` is a tiny committed fixture used for fast tests, CI, and smoke demos.

~~~bash
make demo-fixture
~~~

### Production mode

`racedata_latest` is built from the latest locally downloaded public RaceData archive.

~~~bash
make download-racedata
make demo-latest
~~~

Production data and generated artifacts are intentionally not committed.

## Quick start

Create and activate a virtual environment, then install the project.

~~~bash
python3.11 -m venv .venv
source .venv/bin/activate
make install
~~~

Run checks:

~~~bash
make check
~~~

Run the fast fixture demo:

~~~bash
make demo-fixture
~~~

Run the production local demo:

~~~bash
make download-racedata
make demo-latest
~~~

## Core commands

~~~bash
make verify-fixture                # run full fixture validation
make check                         # lint and unit tests
make build-fixture-bronze          # convert fixture raw CSVs to bronze Parquet
make dbt-build-fixture             # build dbt models using fixture bronze data
make download-racedata             # download latest public RaceData archive locally
make build-latest-racedata-bronze  # convert latest RaceData snapshot to bronze Parquet
make dbt-build-latest              # build dbt models using production bronze data
make quality-report                # generate dbt quality report
make dagster-materialize-fixture   # orchestrate fixture pipeline with Dagster
make dagster-materialize-latest    # orchestrate production pipeline with Dagster
make streamlit-demo                # launch Streamlit demo
~~~

## Lakehouse layers

### Bronze

The bronze layer stores source CSV data as Parquet and records ingestion metadata.

It tracks:

- source files
- raw row counts
- bronze row counts
- checksums
- manifest metadata

### Silver

The silver layer creates typed facts and dimensions.

Examples:

- `dim_driver`
- `dim_constructor`
- `dim_circuit`
- `dim_race`
- `fact_race_result`
- `fact_lap_time`
- `fact_pit_stop`

### Audit

The audit layer exposes source anomalies and cleaning impact.

Current audit models:

- `audit_lap_time_duplicate_grain`
- `audit_pit_stop_missing_duration`
- `audit_result_nullable_numeric_fields`
- `audit_source_to_silver_row_counts`

This is one of the most important parts of the project: production data issues are not silently hidden.

### Gold

The gold layer contains analytics-ready marts.

Current gold marts:

- `mart_race_summary`
- `mart_driver_pace`
- `mart_pit_stop_efficiency`
- `mart_constructor_reliability`
- `mart_strategy_windows`
- `mart_stint_degradation`
- `mart_data_quality_run_summary`

## Production data issues discovered

Moving from fixture data to production RaceData exposed issues that required hardening:

- duplicate lap-time rows at the race-driver-lap grain
- missing pit-stop duration values
- nullable numeric fields encoded as source strings
- bronze-to-silver row-count differences caused by cleaning decisions

The silver layer handles these issues. The audit layer preserves evidence of them.

## Data quality

dbt tests validate:

- not-null constraints
- uniqueness
- relationships
- fact table grain
- mart grain

The project generates a quality report from dbt artifacts:

~~~text
metadata/data_quality_reports/latest_dbt_quality_summary.json
metadata/data_quality_reports/latest_dbt_quality_summary.md
~~~

Generated metadata stays local and is not committed.

## CI

GitHub Actions validates the fixture pipeline.

CI runs:

- Python linting
- unit tests
- fixture raw-to-bronze ingestion
- dbt fixture build
- quality report generation
- Dagster fixture orchestration
- quality artifact upload

Production RaceData download is intentionally not run in CI because it depends on external data and should remain a local production-mode workflow.

## Streamlit demo

The Streamlit demo reads trusted outputs only.

Sections:

- Quality Evidence
- Gold Marts
- Audit Evidence
- Portfolio Proof

The app does not read raw CSVs directly.

## Documentation

Useful docs:

~~~text
docs/portfolio_case_study.md
docs/demo_walkthrough.md
docs/interview_talking_points.md
docs/architecture.md
docs/ingestion_design.md
docs/data_source_assessment.md
~~~

## What this project proves

PitWall Lakehouse demonstrates:

- source ingestion design
- reproducible local data processing
- lakehouse-style layering
- dbt modeling and testing
- production data hardening
- auditability
- orchestration
- CI hygiene
- demo readiness

## Limitations

This is intentionally local-first and zero-cost.

Current limitations:

- no cloud object storage yet
- no Docker image yet
- no deployed production dashboard
- no predictive ML layer
- production RaceData is local-only
- Streamlit is intentionally thin

These are tradeoffs, not accidental gaps. The project focuses first on a trustworthy data foundation.

## Portfolio case study

A recruiter/interviewer-friendly case study is available at:

~~~text
docs/portfolio_case_study.md
~~~

## Docker

Build the local Docker image:

~~~bash
make docker-build
~~~

Run checks inside Docker:

~~~bash
make docker-check
~~~

Run the fixture pipeline inside Docker:

~~~bash
make docker-fixture-pipeline
~~~

Docker mode validates the reproducible fixture path. Production RaceData download remains a local workflow.

Docker Desktop or another Docker runtime must be installed and available on `PATH` before running Docker targets.

## dbt warning cleanup

Silver relationship tests and gold mart grain tests use dbt's current `arguments:` syntax for generic test arguments.

This keeps local, Docker, and CI dbt output free of avoidable generic-test deprecation warnings.

## Screenshots

A screenshot checklist is available at:

~~~text
docs/screenshots_checklist.md
~~~

Recommended screenshots include Streamlit quality evidence, audit evidence, gold marts, GitHub Actions CI, CI artifacts, Dagster materialization, Docker fixture pipeline, and the README landing page.

## Project health check

Run a quick local project readiness check:

~~~bash
make project-health
~~~

This reports whether core project files, optional generated artifacts, and generated-artifact ignore rules are present.

## Career packaging

Resume bullets, LinkedIn copy, recruiter messaging, and interview talking points are available at:

~~~text
docs/career_packaging.md
~~~

## Final review checklist

Before sharing the project publicly, use:

~~~text
docs/final_review_checklist.md
~~~

It covers local checks, CI, Docker, Dagster, Streamlit, production mode, screenshots, resume packaging, and overclaim prevention.

## License and data usage

Project code is licensed under the MIT License.

Data usage details are documented at:

~~~text
docs/data_usage_notice.md
~~~

Public source data remains subject to the upstream data source terms. Generated local data artifacts are intentionally not committed.

## One-command verification

Run the full local fixture validation path:

~~~bash
make verify-fixture
~~~

This runs Python checks, fixture bronze ingestion, dbt fixture build, quality report generation, and project-health.

## Release checklist

A v1.0-style release checklist is available at:

~~~text
docs/release_checklist.md
~~~

Use it before tagging or publicly launching the project.
