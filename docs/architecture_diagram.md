# PitWall Lakehouse Architecture Diagram

## End-to-end flow

~~~mermaid
flowchart TD
    A[Public RaceData CSV archive] --> B[Raw timestamped snapshot]
    B --> C[Bronze Parquet files]

    C --> D[dbt Bronze Views]
    D --> E[dbt Silver Facts and Dimensions]

    E --> F[dbt Audit Models]
    E --> G[dbt Gold Marts]

    F --> H[Audit Evidence]
    G --> I[Trusted Analytics Outputs]

    D --> J[dbt Tests]
    E --> J
    F --> J
    G --> J

    J --> K[Generated Quality Report]
    I --> L[Streamlit Demo]
    H --> L
    K --> L

    M[Dagster Asset Graph] --> C
    M --> D
    M --> K

    N[GitHub Actions CI] --> O[Fixture Pipeline Validation]
    O --> J
    O --> K
    O --> P[CI Quality Artifact]

    Q[Docker] --> R[Linux Fixture Pipeline Validation]
    R --> J
    R --> K
~~~

## Data modes

~~~mermaid
flowchart LR
    A[racedata_sample fixture] --> B[Fast tests]
    A --> C[GitHub Actions CI]
    A --> D[Docker fixture validation]
    A --> E[Smoke demo]

    F[racedata_latest production] --> G[Local full RaceData pipeline]
    G --> H[Production audit evidence]
    G --> I[Production Streamlit demo]

    J[Generated artifacts] --> K[Local only]
    K --> L[Not committed to Git]
~~~

## Layer responsibilities

~~~mermaid
flowchart TD
    A[Raw] -->|Preserve source files| B[Bronze]
    B -->|Column-preserving Parquet| C[Silver]
    C -->|Typed facts and dimensions| D[Audit]
    C -->|Clean trusted entities| E[Gold]
    D -->|Expose source anomalies| F[Quality Evidence]
    E -->|Analytics-ready marts| F
~~~

## Key design decision

The project separates cleaning from observability.

Silver models clean and type the data, while audit models preserve evidence of source anomalies and row-count impact.

This avoids silently hiding production data issues.
