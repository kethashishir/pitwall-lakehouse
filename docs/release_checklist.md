# PitWall Lakehouse Release Checklist

Use this checklist before tagging a portfolio-ready release such as `v1.0.0`.

## Release goal

A release means the project is ready to share publicly as a data-engineering portfolio project.

It does not mean the project is a deployed production service.

## Required checks before tagging

### 1. Main branch is clean

~~~bash
git checkout main
git pull
git status
~~~

Expected:

~~~text
nothing to commit, working tree clean
~~~

### 2. GitHub Actions is green

On GitHub, verify the latest CI workflow is passing.

CI should validate:

- Python linting
- unit tests
- fixture raw-to-bronze ingestion
- dbt fixture build
- quality report generation
- Dagster fixture orchestration
- quality artifact upload

### 3. Local fixture verification passes

~~~bash
make format
make verify-fixture
~~~

Expected:

- tests pass
- fixture bronze build passes
- dbt fixture build passes
- quality report says `passed=True`
- project-health has no unexpected warnings

### 4. Docker fixture verification passes

~~~bash
make docker-build
make docker-check
make docker-fixture-pipeline
~~~

Expected:

- Docker image builds
- tests pass inside Linux container
- fixture pipeline passes inside Linux container
- quality report generation passes inside container

### 5. Production local path passes

~~~bash
make download-racedata
make build-latest-racedata-bronze
make dbt-build-latest
make quality-report
make project-health
~~~

Expected:

- latest source archive downloads locally
- production bronze build completes
- production dbt build passes
- quality report says `passed=True`

Production source data and generated artifacts should remain untracked.

### 6. Final review checklist is complete

Use:

~~~text
docs/final_review_checklist.md
~~~

### 7. Screenshot checklist is complete

Use:

~~~text
docs/screenshots_checklist.md
~~~

At minimum, capture:

- README landing page
- Streamlit Quality Evidence
- Streamlit Audit Evidence
- Streamlit Gold Marts
- GitHub Actions green CI
- CI quality artifact
- Docker fixture pipeline

### 8. Career packaging is ready

Use:

~~~text
docs/career_packaging.md
~~~

Confirm resume bullets and LinkedIn wording are accurate.

### 9. License and data notice exist

Confirm:

~~~text
LICENSE
docs/data_usage_notice.md
~~~

The repo should clearly distinguish project code from upstream public source data.

### 10. Known limitations are documented

The README and case study should honestly state:

- local-first project
- no cloud object storage yet
- no real-time streaming
- no predictive ML layer
- no deployed production dashboard
- production RaceData is local-only

## Optional release tag

After all checks pass, create a release tag:

~~~bash
git checkout main
git pull
git tag -a v1.0.0 -m "PitWall Lakehouse v1.0.0 portfolio release"
git push origin v1.0.0
~~~

## Optional GitHub release notes

Suggested title:

~~~text
PitWall Lakehouse v1.0.0
~~~

Suggested notes:

~~~markdown
PitWall Lakehouse is a local-first Formula 1 data-engineering platform using Python, DuckDB, Parquet, dbt, Dagster, Streamlit, Docker, and GitHub Actions.

This release includes:

- raw CSV to bronze Parquet ingestion
- dbt bronze, silver, audit, and gold models
- 100+ dbt data tests
- generated dbt quality reports
- audit models for production data anomalies
- fixture and production dataset modes
- Dagster orchestration
- GitHub Actions CI with uploaded quality artifacts
- Docker fixture validation
- Streamlit demo over trusted outputs
- portfolio case study and career packaging docs

Known limitations:

- local-first only
- no cloud deployment
- no real-time streaming
- no predictive ML layer
- production source data is downloaded locally and not committed
~~~

## Do not tag if

Do not create a release if:

- CI is failing
- `make verify-fixture` fails
- Docker fixture pipeline fails
- production path has not been recently tested
- README has stale claims
- generated artifacts are accidentally tracked
- the repo has unresolved TODOs that affect demo correctness
