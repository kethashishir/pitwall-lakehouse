# Ingestion Design

## Phase 2 scope

This phase defines the source contract and creates a tiny committed fixture.

It does not download the full dataset yet.

## Primary historical source

Primary source:

- TracingInsights RaceData GitHub release archive
- Expected artifact: `data.zip`
- Expected contents: Kaggle/Rohan Rao-style Formula 1 CSV files

The full dataset will be downloaded in a later phase into:

~~~text
data/raw/racedata/
~~~

Generated manifests will be written into:

~~~text
metadata/ingestion_manifests/
~~~

## Why not download full data in this phase?

Downloading the full source before writing contracts and tests is risky. It can hide assumptions about schemas, filenames, encodings, and row counts.

This phase creates a small stable fixture first so the project can test ingestion behavior without network access.

## Tiny fixture purpose

The committed sample fixture under `tests/fixtures/raw/racedata_sample/` is intentionally small.

It exists to test:

- expected filenames
- expected CSV headers
- basic foreign-key-like relationships
- basic lap time and pit stop duration input formats
- package import behavior

It is not used for analytics claims.

## Expected source files for the first ingestion pass

Required for the initial historical lakehouse pipeline:

- circuits.csv
- constructors.csv
- drivers.csv
- lap_times.csv
- pit_stops.csv
- qualifying.csv
- races.csv
- results.csv
- seasons.csv
- status.csv

Deferred until needed:

- constructor_results.csv
- constructor_standings.csv
- driver_standings.csv
- sprint_results.csv

## Raw layer rules

Raw ingestion must:

1. Preserve the downloaded archive.
2. Extract source CSVs without modifying cell values.
3. Record source URL, download timestamp, file size, checksum, and extracted filenames.
4. Never overwrite prior raw snapshots silently.
5. Produce a machine-readable manifest.

## Bronze layer rules

Bronze conversion must:

1. Read raw CSVs.
2. Apply source-preserving type normalization.
3. Write Parquet files.
4. Preserve source row counts.
5. Produce row-count reconciliation metadata.

## Current non-goals

- No OpenF1 ingestion yet.
- No FastF1 dependency yet.
- No dbt models yet.
- No Dagster orchestration yet.
- No dashboard yet.
