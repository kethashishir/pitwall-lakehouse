# Data Usage Notice

PitWall Lakehouse is a portfolio data-engineering project.

## Project code

The project code is licensed under the MIT License. See:

~~~text
LICENSE
~~~

This license applies to the source code, tests, documentation, orchestration code, dashboard code, and project configuration created for this repository.

## Source data

The project uses public Formula 1 race data from TracingInsights RaceData.

The source data is not owned by this project.

Users are responsible for reviewing and following the upstream data source terms, license, and attribution requirements.

## Generated local artifacts

Generated artifacts are intentionally not committed to Git.

Examples include:

- downloaded raw RaceData archives
- bronze Parquet files
- local DuckDB database files
- dbt target files
- generated quality reports
- local Dagster state

These artifacts are produced locally when running the pipeline.

## Fixture data

The repository includes a tiny fixture dataset for tests, CI, and smoke demos.

The fixture exists only to validate pipeline behavior quickly and should not be treated as a complete Formula 1 dataset.

## No warranty

This project is provided for educational and portfolio purposes.

It should not be treated as an official Formula 1 data product, betting system, race prediction system, or production analytics service.
