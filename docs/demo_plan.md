# Demo Plan

The final demo should show evidence of data-engineering work, not just charts.

Planned demo sections:

1. Data source and ingestion manifest
2. Raw-to-bronze reconciliation
3. Data-quality run summary
4. Race strategy analytics
5. Driver and constructor pace/reliability marts
6. Lineage explanation from source CSVs to gold marts

## Streamlit demo

The first demo UI is intentionally thin.

It reads:

- trusted gold marts from `data/pitwall.duckdb`
- generated quality evidence from `metadata/data_quality_reports/latest_dbt_quality_summary.json`

It does not read raw CSVs.

Demo sections:

1. Quality Evidence
2. Gold Marts
3. Portfolio Proof

The dashboard must avoid fake historical claims while the project is still running on the tiny fixture.

## Audit evidence demo

The Streamlit demo includes an Audit Evidence section.

It reads dbt audit models from DuckDB:

~~~text
audit_lap_time_duplicate_grain
audit_pit_stop_missing_duration
audit_result_nullable_numeric_fields
audit_source_to_silver_row_counts
~~~

This lets reviewers see production source anomalies and the row-count impact of silver cleaning decisions.
