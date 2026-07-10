# Architecture

PitWall Lakehouse is planned as a local-first lakehouse-style data platform.

## Layers

- Raw: source-preserved files and metadata.
- Bronze: typed source-preserved Parquet.
- Silver: normalized canonical Formula 1 tables.
- Gold: analytics marts for strategy, pace, reliability, and data-quality summaries.

## Principle

Dashboard and API layers must read only from trusted gold outputs.

## dbt transformation layer

The first dbt project lives under:

~~~text
dbt/pitwall_dbt/
~~~

The project uses DuckDB locally and reads bronze Parquet outputs.

Initial model pattern:

~~~text
bronze Parquet files
  -> bronze dbt views
  -> silver canonical dimensions/facts
  -> gold analytics marts
~~~

The first gold marts are:

- mart_race_summary
- mart_driver_pace
- mart_pit_stop_efficiency

## Data-quality evidence

dbt build produces JSON artifacts under the dbt target directory.

The project parses `run_results.json` to generate local data-quality reports under:

~~~text
metadata/data_quality_reports/
~~~

The current report summarizes:

- total dbt results
- status counts
- resource type counts
- failed checks
- source artifact path
- generated timestamp

GX Core remains a later option for richer expectation suites and static Data Docs.

## Orchestration layer

Dagster orchestrates the local lakehouse pipeline.

Initial Dagster assets:

- bronze_racedata_fixture
- dbt_lakehouse_build
- dbt_quality_summary

The first orchestration implementation intentionally uses simple Python assets instead of advanced dbt asset auto-loading. This keeps the workflow understandable while the project is still local and fixture-based.

Current orchestrated flow:

~~~text
bronze_racedata_fixture
  -> dbt_lakehouse_build
  -> dbt_quality_summary
~~~

## Gold mart expansion

Phase 7 expands the trusted gold layer.

Gold marts now cover:

- race summaries
- driver pace
- pit-stop efficiency
- constructor reliability
- pit strategy windows
- inferred stint degradation
- row-count summaries across bronze, silver, and gold

The current marts run against the committed fixture. Full historical analysis requires the production source archive ingestion phase.

## Fixture and production bronze inputs

The dbt bronze models read Parquet from:

~~~text
data/bronze/{{ var("bronze_dataset") }}/
~~~

Supported local values:

- racedata_sample: tiny committed fixture converted to bronze
- racedata_latest: latest downloaded production RaceData archive converted to bronze

This allows the same dbt model graph to run against both a fast test fixture and the real public dataset.

## Production data hardening

The production RaceData build exposed source issues that were not visible in the tiny fixture:

- `\\N` missing-value markers in numeric fields
- duplicate lap-time rows at the race-driver-lap grain

Silver models use safer casting with `try_cast(nullif(..., '\\N'))`.

`fact_lap_time` currently deduplicates repeated race-driver-lap rows deterministically by keeping the lowest lap-time milliseconds value, then lowest available position. A later quality phase should add a dedicated duplicate audit model/report so these source anomalies are visible instead of silently hidden.

## Audit models

The audit layer captures production source anomalies that should not be silently hidden.

Current audit models:

~~~text
audit_lap_time_duplicate_grain
audit_pit_stop_missing_duration
audit_result_nullable_numeric_fields
audit_source_to_silver_row_counts
~~~

These models support the data-quality story:

- duplicate lap-time source rows are visible
- missing pit-stop duration rows are visible
- nullable numeric result fields are measured
- bronze-to-silver row-count differences are explained

The silver layer can clean and deduplicate data while the audit layer preserves evidence of what was changed.

## Dagster dataset modes

The Dagster asset graph is dataset-aware.

The bronze asset checks `PITWALL_BRONZE_DATASET` and materializes either:

- `racedata_sample`
- `racedata_latest`

The dbt asset passes the selected dataset into dbt using:

~~~text
--vars {"bronze_dataset": "<dataset>"}
~~~

This keeps orchestration aligned with both fast fixture builds and real production RaceData builds.

## CI strategy

The CI workflow validates the fast fixture path.

CI runs:

~~~text
make install
make check
make build-fixture-bronze
dbt deps
make dbt-build-fixture
make quality-report
~~~

The production RaceData download path is verified locally, not in CI. This keeps CI reliable, fast, and independent of large public data downloads.

## dbt warning hygiene

dbt relationship tests use the `arguments:` property for generic test arguments.

This keeps CI and local builds cleaner and avoids deprecated top-level generic-test argument syntax.
