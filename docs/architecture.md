# Architecture

PitWall Lakehouse is planned as a local-first lakehouse-style data platform.

## Layers

- Raw: source-preserved files and metadata.
- Bronze: typed source-preserved Parquet.
- Silver: normalized canonical Formula 1 tables.
- Gold: analytics marts for strategy, pace, reliability, and data-quality summaries.

## Principle

Dashboard and API layers must read only from trusted gold outputs.
