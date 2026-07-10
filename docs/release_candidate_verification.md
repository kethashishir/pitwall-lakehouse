# PitWall Lakehouse Release Candidate Verification

This document records the release-candidate verification status before tagging a portfolio release.

## Verification date

Fill in the date when running final verification.

~~~text
YYYY-MM-DD
~~~

## Release candidate

~~~text
v1.0.0 candidate
~~~

## Local fixture verification

Command:

~~~bash
make format
make verify-fixture
~~~

Expected result:

- formatting passes
- lint passes
- unit tests pass
- fixture bronze ingestion completes
- dbt fixture build completes
- dbt quality report is generated
- project-health completes

Recorded result:

~~~text
PASS
~~~

## Docker fixture verification

Command:

~~~bash
make docker-build
make docker-check
make docker-fixture-pipeline
~~~

Expected result:

- Docker image builds
- tests pass inside Linux container
- fixture pipeline passes inside Linux container
- quality report generation passes inside container

Recorded result:

~~~text
PASS
~~~

## Production local verification

Command:

~~~bash
make download-racedata
make build-latest-racedata-bronze
make dbt-build-latest
make quality-report
make project-health
~~~

Expected result:

- latest public RaceData archive downloads locally
- production bronze build completes
- production dbt build completes
- dbt quality report is generated
- project-health completes

Recorded result:

~~~text
PASS
~~~

## GitHub Actions verification

Expected result:

- latest `main` CI run is green
- quality report artifact is uploaded
- Dagster fixture orchestration passes

Recorded result:

~~~text
PASS
~~~

## Git safety verification

Command:

~~~bash
git status
git ls-files | grep -E 'data/raw|data/bronze|metadata/ingestion_manifests|metadata/data_quality_reports|target|logs|dbt_packages|.dagster|.streamlit|.tmp_dagster' || true
~~~

Expected result:

- working tree is clean before tagging
- generated artifacts are not tracked
- only intentional `.gitkeep` and source files appear from the grep command

Recorded result:

~~~text
PASS
~~~

## Release decision

~~~text
Ready to tag v1.0.0 after final GitHub Actions check.
~~~

## Tag command

Only run after final verification:

~~~bash
git checkout main
git pull
git tag -a v1.0.0 -m "PitWall Lakehouse v1.0.0 portfolio release"
git push origin v1.0.0
~~~
