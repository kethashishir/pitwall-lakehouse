# PitWall Lakehouse Career Packaging

Use this document when describing PitWall Lakehouse on a resume, LinkedIn, GitHub, or in interviews.

## One-line project description

PitWall Lakehouse is a local-first Formula 1 data-engineering platform that ingests public race data, builds a DuckDB/dbt lakehouse, exposes data-quality and audit evidence, orchestrates the pipeline with Dagster, validates the fixture path in CI, and serves trusted outputs through Streamlit.

## Resume version

### Strong resume bullet set

- Built a local-first Formula 1 lakehouse pipeline using Python, DuckDB, Parquet, dbt, Dagster, and Streamlit to transform raw public race CSV data into tested analytics marts.
- Designed bronze, silver, audit, and gold layers with dbt models and 100+ data tests covering not-null checks, uniqueness, relationships, and mart grain.
- Hardened the production pipeline after discovering real source anomalies, including duplicate lap-time grain rows, missing pit-stop durations, nullable numeric fields, and bronze-to-silver row-count differences.
- Added audit models and generated dbt quality reports to make cleaning decisions observable instead of silently dropping or transforming problematic records.
- Implemented GitHub Actions CI, Docker fixture validation, and Dagster fixture orchestration to prove the pipeline is reproducible outside the local development environment.

### Shorter resume bullet set

- Built a Python/DuckDB/dbt Formula 1 lakehouse with bronze, silver, audit, and gold layers over public race data.
- Added dbt tests, audit models, and generated quality reports to expose production data anomalies and cleaning impact.
- Orchestrated fixture and production data modes with Dagster and validated the fixture pipeline through GitHub Actions and Docker.

## LinkedIn post draft

I built PitWall Lakehouse, a local-first Formula 1 data-engineering project focused on ingestion, lakehouse modeling, data quality, orchestration, and reproducibility.

The project takes public Formula 1 race data and builds:

- raw-to-bronze Parquet ingestion
- DuckDB/dbt bronze, silver, audit, and gold layers
- dbt tests and generated quality reports
- audit models for real production data issues
- Dagster orchestration
- GitHub Actions CI
- Docker fixture validation
- a Streamlit demo over trusted outputs

The most valuable part was moving from fixture data to real production data. The production dataset exposed issues like duplicate lap-time grain rows, missing pit-stop durations, nullable numeric fields, and row-count differences after cleaning.

Instead of hiding those issues, I added audit models so the pipeline explains what changed and why.

This project helped me practice practical data-engineering fundamentals: ingestion design, reproducible local processing, dbt modeling, quality checks, orchestration, CI, and demo readiness.

GitHub: <add link>
Demo notes: <add link or screenshot>

## GitHub repo description

Local-first Formula 1 lakehouse using Python, DuckDB, Parquet, dbt, Dagster, Streamlit, Docker, and GitHub Actions with audit models and generated data-quality reports.

## Interview explanation

### Tell me about this project.

PitWall Lakehouse is a local-first Formula 1 data-engineering platform. I built it to show the full data platform lifecycle: ingestion, bronze Parquet storage, dbt transformations, silver facts and dimensions, audit models, gold marts, data-quality reporting, Dagster orchestration, CI, Docker validation, and a Streamlit demo.

The project supports two modes. Fixture mode is small and committed to the repo so CI and tests are fast. Production mode downloads the latest public RaceData archive locally and builds the larger pipeline.

### What was technically interesting?

The most interesting part was that fixture data passed easily, but production data exposed real issues. I found duplicate lap-time rows at the race-driver-lap grain, missing pit-stop durations, and numeric columns encoded with nullable source strings.

I hardened the silver models to handle these safely, but I also added audit models so the cleaning decisions stayed visible. That is closer to real data engineering than silently dropping bad records.

### Why DuckDB and dbt?

DuckDB made sense because the project is local-first, zero-cost, and analytical. dbt made the transformation layer testable and easier to document. Together they let me show lakehouse-style modeling without needing paid cloud infrastructure.

### Why Dagster?

Dagster gives the project an orchestration layer. It materializes bronze ingestion, the dbt lakehouse build, and the quality report. It also supports fixture and production dataset modes.

### Why Streamlit?

Streamlit is intentionally thin. It is not the core product. It gives reviewers a simple way to inspect quality evidence, audit evidence, and gold marts without reading raw tables manually.

### What would you improve next?

I would improve the demo UI and add richer summary cards. I would only add cloud storage, APIs, or machine learning if there is a clear use case. The current focus is the trustworthy data foundation.

## Recruiter message version

Hi <Name>, I recently built PitWall Lakehouse, a Formula 1 data-engineering portfolio project using Python, DuckDB, Parquet, dbt, Dagster, Streamlit, Docker, and GitHub Actions.

The project is focused on real data-engineering fundamentals: ingestion, bronze/silver/gold modeling, data-quality checks, audit models for production data issues, orchestration, CI, and reproducibility.

GitHub: <add link>

I would be happy to walk through the architecture or the production data issues I found while building it.

## Do not overclaim

Do not say:

- this is a deployed production system
- this predicts race outcomes
- this uses cloud-scale infrastructure
- this is an ML platform
- this is real-time streaming
- this is a full SaaS product

Better wording:

- local-first data-engineering platform
- lakehouse-style project
- production data hardening
- quality and audit evidence
- reproducible fixture pipeline
- Docker-validated local workflow
