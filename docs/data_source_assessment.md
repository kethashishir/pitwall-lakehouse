# PitWall Lakehouse — Phase 0 Data Source Assessment

Date: 2026-06-24

## Decision

Primary source for Phase 1/2:
- TracingInsights RaceData GitHub release archive (`data.zip`)

Fallback source:
- Kaggle Formula 1 World Championship dataset by Rohan Rao

Scoped enrichment source for later phases:
- OpenF1 historical endpoints, limited to selected 2023+ sessions

Optional enrichment source:
- FastF1, only after the CSV lakehouse pipeline is stable

Ergast-style API context/fallback:
- Jolpica-F1, only for small API checks or successor context

## Why TracingInsights first

TracingInsights RaceData is an automated GitHub archive of Kaggle-derived Formula 1 race datasets. It includes a consolidated `data.zip`, a `data/` directory, and data from 1950 through the current season. The README says the datasets are released under CC0/Public Domain and can be used for personal projects, analysis, research, visualization, academic work, and personal applications.

This is better than starting with direct Kaggle access because GitHub release download is easier to reproduce in CI without storing Kaggle credentials.

## Expected base CSV tables

Core source tables expected from the TracingInsights/Rohan Rao-style dataset include:

- circuits.csv
- constructors.csv
- constructor_results.csv
- constructor_standings.csv
- drivers.csv
- driver_standings.csv
- lap_times.csv
- pit_stops.csv
- qualifying.csv
- races.csv
- results.csv
- seasons.csv
- status.csv

Additional files may exist and should be treated as source-discovered, not hardcoded until ingestion inspects the archive.

## Source suitability

### TracingInsights RaceData

Status: Recommended primary source.

Pros:
- Public GitHub repository.
- Consolidated data.zip.
- Kaggle-derived.
- Includes race results, standings, constructors, drivers, lap times, pit stops, and more.
- README states CC0/Public Domain source datasets.
- Easier than Kaggle for reproducible CI.

Risks:
- It is an unofficial archive.
- Current-season updates may change row counts.
- Schema drift must be checked at ingestion time.
- We should store source metadata and checksums.

### Kaggle Formula 1 World Championship

Status: Suitable fallback/manual source.

Pros:
- Canonical and widely used.
- Historical relational F1 CSV structure.

Risks:
- Direct download usually requires Kaggle account/API credentials.
- Kaggle page/license should be rechecked manually before relying on direct Kaggle download.
- CI should not depend on Kaggle credentials.

### OpenF1

Status: Suitable later, scoped enrichment only.

Pros:
- Historical 2023+ data is free and accessible without authentication.
- Provides modern session data including car data, laps, pit, race control, stints, weather, sessions, and drivers.
- JSON and CSV formats are documented.

Risks:
- Real-time data requires paid subscription.
- Telemetry can explode data volume quickly.
- We should cache selected responses under raw storage.
- Use only a tiny session subset.

### FastF1

Status: Optional later.

Pros:
- Mature Python package for F1 timing/session/telemetry analysis.
- Has built-in caching and rate-limit handling.

Risks:
- Adds dependency complexity.
- Not needed for Phase 1.
- Could distract from the lakehouse/data-quality story.

### Jolpica-F1

Status: Useful successor context and small API fallback.

Pros:
- Ergast successor.
- Backwards-compatible Ergast-style endpoints.
- Open-source project.

Risks:
- Unauthenticated limits are 4 requests/second burst and 500 requests/hour sustained.
- API terms and limits may change.
- Not suitable as the main bulk ingestion path.

## Phase 1 scaffold recommendation

Use a local-first lakehouse scaffold:

```text
pitwall-lakehouse/
  README.md
  Makefile
  pyproject.toml
  .gitignore
  .env.example
  docs/
    architecture.md
    data_source_assessment.md
    demo_plan.md
  data/
    raw/
    bronze/
    silver/
    gold/
  metadata/
    ingestion_manifests/
    data_quality_reports/
    run_logs/
  src/
    pitwall/
      __init__.py
      config.py
      ingestion/
        __init__.py
      quality/
        __init__.py
      utils/
        __init__.py
  tests/
    unit/
    integration/
  dbt/
    pitwall_dbt/
  orchestration/
    dagster_project/
  dashboard/
    streamlit_app/
```

## Phase 1 tooling recommendation

Start with:
- Python
- DuckDB
- Parquet
- pytest
- ruff
- Makefile
- README skeleton
- local project structure

Do not install Dagster, dbt, GX, Streamlit, or FastAPI in Phase 1 unless needed for the scaffold. Add them when their phase starts.

## Non-goals for now

- No Kafka.
- No Spark.
- No Kubernetes.
- No paid APIs.
- No LLM/RAG.
- No frontend-first work.
- No full historical telemetry.
