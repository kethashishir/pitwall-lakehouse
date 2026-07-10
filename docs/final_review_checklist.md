# PitWall Lakehouse Final Review Checklist

Use this checklist before adding PitWall Lakehouse to your resume, LinkedIn, portfolio, or job applications.

## 1. Repository state

Run:

~~~bash
git checkout main
git pull
git status
~~~

Expected:

~~~text
On branch main
Your branch is up to date with origin/main
nothing to commit, working tree clean
~~~

## 2. Local checks

Run:

~~~bash
make format
make check
make project-health
~~~

Expected:

- formatting succeeds
- lint succeeds
- unit tests pass
- project-health has no unexpected warnings

## 3. Fixture pipeline

Run:

~~~bash
make build-fixture-bronze
make dbt-build-fixture
make quality-report
~~~

Expected:

- raw-to-bronze fixture ingestion completes
- dbt fixture build passes
- quality report says `passed=True`
- dbt result count is 106

## 4. Dagster fixture orchestration

Run:

~~~bash
make dagster-materialize-fixture
~~~

Expected:

- `bronze_racedata` materializes
- `dbt_lakehouse_build` materializes
- `dbt_quality_summary` materializes
- run completes successfully

## 5. Docker fixture verification

Run:

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

## 6. Production local pipeline

Run:

~~~bash
make download-racedata
make build-latest-racedata-bronze
make dbt-build-latest
make quality-report
~~~

Expected:

- latest public RaceData archive downloads locally
- production bronze build completes
- production dbt build passes
- quality report says `passed=True`

Production data is local-only and should not be committed.

## 7. Streamlit demo

Run:

~~~bash
make demo-fixture
~~~

Check these sections:

- Quality Evidence
- Audit Evidence
- Gold Marts
- Portfolio Proof

Optional production demo:

~~~bash
make demo-latest
~~~

Use production mode only after the production pipeline has been built locally.

## 8. GitHub Actions

On GitHub, confirm:

- latest CI run is green
- fixture pipeline passed
- Dagster fixture orchestration passed
- artifact upload completed

Check the uploaded artifact:

~~~text
pitwall-quality-report
~~~

It should include:

- `latest_dbt_quality_summary.json`
- `latest_dbt_quality_summary.md`
- `run_results.json`

## 9. Screenshots

Use:

~~~text
docs/screenshots_checklist.md
~~~

Capture evidence-focused screenshots:

- README landing page
- Streamlit Quality Evidence
- Streamlit Audit Evidence
- Streamlit Gold Marts
- GitHub Actions green CI
- CI quality artifact
- Dagster materialization
- Docker fixture pipeline

Do not commit large raw screenshots.

## 10. README review

Open the GitHub README and confirm it explains:

- what the project is
- why it exists
- architecture
- tech stack
- data modes
- quick start
- production data issues discovered
- data quality
- CI
- Docker
- limitations

A reviewer should understand the project in under 60 seconds.

## 11. Career packaging

Use:

~~~text
docs/career_packaging.md
~~~

Before applying, copy the appropriate version:

- shorter resume bullets for space-limited resumes
- stronger resume bullets for data-engineering-focused resumes
- LinkedIn post draft for launch
- recruiter message for outreach
- interview explanations for preparation

## 12. Do not overclaim

Do not describe the project as:

- deployed production SaaS
- real-time streaming
- predictive race modeling
- cloud-scale infrastructure
- ML platform

Accurate wording:

- local-first data-engineering platform
- DuckDB/dbt lakehouse
- reproducible fixture pipeline
- production data hardening
- audit and quality evidence
- Dagster-orchestrated workflow
- Docker-verified fixture pipeline

## 13. Final Git safety check

Before sharing, run:

~~~bash
git status
git ls-files | grep -E 'data/raw|data/bronze|metadata/ingestion_manifests|metadata/data_quality_reports|target|logs|dbt_packages|.dagster|.streamlit|.tmp_dagster' || true
~~~

Expected:

Only intentional `.gitkeep`, source files, dashboard files, and orchestration source files should appear.

Generated local data, reports, dbt target files, logs, packages, and temporary Dagster state should not be tracked.

## Final decision

Share the project only when:

- main branch is clean
- CI is green
- local fixture path passes
- Docker fixture path passes
- project-health is clean or explainable
- README is polished
- screenshots are ready
- resume bullets are accurate
