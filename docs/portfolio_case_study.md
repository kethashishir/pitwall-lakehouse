# PitWall Lakehouse Portfolio Case Study

## One-line summary

PitWall Lakehouse is a local-first Formula 1 data-engineering platform that ingests public race data, builds a DuckDB/dbt lakehouse, exposes data-quality and audit evidence, orchestrates the pipeline with Dagster, and serves trusted outputs through Streamlit.

## Why I built this

I wanted a portfolio project that demonstrates real data-engineering fundamentals instead of only a dashboard or CRUD app.

The goal was to show:

- reproducible ingestion
- bronze/silver/gold lakehouse modeling
- data-quality checks
- source anomaly auditing
- orchestration
- CI validation
- a simple demo over trusted outputs

## Data source

The project uses public Formula 1 race data from TracingInsights RaceData.

The pipeline supports two data modes:

- `racedata_sample`: a tiny committed fixture for fast tests and CI
- `racedata_latest`: the latest locally downloaded production RaceData archive

Production data is downloaded locally and is not committed to Git.

## Architecture

~~~text
Public RaceData archive
  -> raw timestamped snapshot
  -> bronze Parquet files
  -> dbt bronze views
  -> dbt silver facts and dimensions
  -> dbt audit models
  -> dbt gold marts
  -> dbt quality report
  -> Streamlit demo
~~~

Dagster orchestrates the main local asset graph:

~~~text
bronze_racedata
  -> dbt_lakehouse_build
  -> dbt_quality_summary
~~~

## Bronze layer

The bronze layer converts source CSVs into Parquet.

The ingestion step records:

- source file names
- raw row counts
- bronze row counts
- checksums
- manifest metadata

This makes ingestion reproducible and auditable.

## Silver layer

The silver layer creates typed facts and dimensions.

Examples:

- `dim_driver`
- `dim_constructor`
- `dim_circuit`
- `dim_race`
- `fact_race_result`
- `fact_lap_time`
- `fact_pit_stop`

Production data required hardening for missing values encoded as source strings.

## Audit layer

The audit layer exposes source anomalies instead of hiding them.

Current audit models include:

- `audit_lap_time_duplicate_grain`
- `audit_pit_stop_missing_duration`
- `audit_result_nullable_numeric_fields`
- `audit_source_to_silver_row_counts`

The production dataset exposed:

- duplicate lap-time rows at the race-driver-lap grain
- missing pit-stop duration values
- nullable numeric fields requiring safer casting

The silver layer cleans these issues, while the audit layer preserves evidence of what changed.

## Gold layer

The gold layer contains analytics-ready marts.

Examples:

- `mart_race_summary`
- `mart_driver_pace`
- `mart_pit_stop_efficiency`
- `mart_constructor_reliability`
- `mart_strategy_windows`
- `mart_stint_degradation`
- `mart_data_quality_run_summary`

These marts support the Streamlit demo and portfolio walkthrough.

## Data quality

dbt tests validate:

- not-null constraints
- uniqueness
- relationships
- fact table grain
- mart grain

The project also generates a quality report from dbt artifacts.

The report is available locally and uploaded as a GitHub Actions artifact in CI.

## Orchestration

Dagster materializes:

- bronze RaceData
- dbt lakehouse build
- dbt quality summary

The same Dagster asset graph supports:

- fixture mode for fast validation
- production mode for the latest downloaded RaceData snapshot

## CI strategy

GitHub Actions validates the fixture pipeline.

CI runs:

- Python checks
- unit tests
- fixture raw-to-bronze ingestion
- dbt fixture build
- quality report generation
- Dagster fixture orchestration

Production RaceData download is intentionally local-only so CI remains fast and reliable.

## Streamlit demo

The Streamlit demo is intentionally thin.

It reads:

- trusted gold marts
- audit models
- generated quality reports

It does not read raw CSVs directly.

The demo sections are:

- Quality Evidence
- Gold Marts
- Audit Evidence
- Portfolio Proof

## What made this project difficult

The hardest part was moving from fixture data to real production data.

The fixture pipeline passed easily, but production RaceData exposed issues that required:

- safer numeric casting
- deterministic lap-time deduplication
- explicit audit models
- row-count reconciliation

That is the main engineering value of the project.

## What I would improve next

Good next improvements:

- add Docker for local reproducibility
- add richer summary cards to Streamlit
- add CI artifact previews in documentation
- add a small FastAPI layer only if there is a real consumer
- add cloud object storage only if cost is acceptable

I would not add machine learning until the data foundation and use case justify it.

## Key takeaway

PitWall Lakehouse is not just a dashboard.

It is a reproducible, tested, orchestrated local lakehouse that turns messy public race data into trusted analytics outputs with visible quality and audit evidence.
