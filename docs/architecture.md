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
