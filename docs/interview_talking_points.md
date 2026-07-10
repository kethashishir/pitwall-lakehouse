# PitWall Lakehouse Interview Talking Points

## One-line pitch

PitWall Lakehouse is a local-first Formula 1 data-engineering platform that ingests public race data, builds a DuckDB/dbt lakehouse, exposes quality and audit evidence, and serves trusted outputs through Streamlit.

## Strongest engineering points

### 1. Real production data issues were discovered

The production dataset exposed issues that the tiny fixture did not:

- duplicate lap-time rows at race-driver-lap grain
- missing pit-stop duration values
- nullable numeric fields encoded as source strings

The project handles these in silver and exposes them through audit models.

### 2. Cleaning is observable

The project does not silently drop or deduplicate data.

Audit models explain:

- what source anomalies exist
- how many rows were affected
- why bronze-to-silver row counts changed

### 3. Fixture and production modes are separated

Fixture mode is used for fast CI and smoke testing.

Production mode is used locally for the full public RaceData archive.

This keeps CI fast while still proving the pipeline works on real data.

### 4. dbt is used for transformation and testing

dbt models cover:

- bronze views over Parquet
- silver facts and dimensions
- audit models
- gold marts

dbt tests validate uniqueness, not-null constraints, relationships, and mart grain.

### 5. Dagster orchestrates the pipeline

Dagster materializes:

- bronze RaceData
- dbt lakehouse build
- dbt quality summary

It supports both fixture and production dataset modes.

### 6. Streamlit is intentionally thin

The dashboard is not the main product.

It exists to make trusted data outputs, quality reports, and audit evidence easy to inspect.

## How to answer “why not use cloud tools?”

This project is intentionally local-first and zero-cost.

The goal was to demonstrate data-engineering fundamentals:

- ingestion
- storage layout
- transformation
- quality checks
- orchestration
- reproducibility
- observability

Cloud deployment can be a later phase, but the core architecture is already visible.

## How to answer “what was the hardest part?”

The hardest part was moving from fixture data to real production RaceData.

The fixture passed, but production exposed source anomalies. I had to harden casting, deduplicate lap-time grain, and then add audit models so those decisions were explainable.

## How to answer “what would you improve next?”

Good next improvements:

- add CI artifact upload for the quality report
- add Great Expectations or Soda only if justified
- add a richer Streamlit summary page
- add Docker for local reproducibility
- add cloud object storage later if cost is acceptable

Avoid saying the next step is random ML. The data foundation should come first.
