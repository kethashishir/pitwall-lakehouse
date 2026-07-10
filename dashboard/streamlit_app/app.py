import json
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DUCKDB_PATH = PROJECT_ROOT / "data" / "pitwall.duckdb"
QUALITY_REPORT_PATH = (
    PROJECT_ROOT / "metadata" / "data_quality_reports" / "latest_dbt_quality_summary.json"
)


GOLD_TABLES = {
    "Race Summary": "mart_race_summary",
    "Driver Pace": "mart_driver_pace",
    "Pit Stop Efficiency": "mart_pit_stop_efficiency",
    "Constructor Reliability": "mart_constructor_reliability",
    "Strategy Windows": "mart_strategy_windows",
    "Stint Degradation": "mart_stint_degradation",
    "Data Quality Row Summary": "mart_data_quality_run_summary",
}


AUDIT_TABLES = {
    "Duplicate Lap-Time Grain": "audit_lap_time_duplicate_grain",
    "Missing Pit-Stop Duration": "audit_pit_stop_missing_duration",
    "Nullable Result Numeric Fields": "audit_result_nullable_numeric_fields",
    "Bronze-to-Silver Row Counts": "audit_source_to_silver_row_counts",
}


def format_milliseconds(value: float | int | None) -> str:
    """Format milliseconds for display."""

    if value is None or pd.isna(value):
        return "N/A"

    return f"{float(value):,.0f} ms"


def load_quality_report(path: Path = QUALITY_REPORT_PATH) -> dict:
    """Load the latest generated data-quality report."""

    if not path.exists():
        return {
            "passed": False,
            "total_results": 0,
            "status_counts": {},
            "resource_type_counts": {},
            "missing": True,
        }

    return json.loads(path.read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def query_table(table_name: str, limit: int = 500) -> pd.DataFrame:
    """Read a trusted mart or audit table from DuckDB."""

    allowed_tables = set(GOLD_TABLES.values()) | set(AUDIT_TABLES.values())

    if table_name not in allowed_tables:
        raise ValueError(f"Unsupported table requested: {table_name}")

    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(
            "DuckDB database not found. Run `make dagster-materialize` or `make dbt-build-latest` first."
        )

    with duckdb.connect(str(DUCKDB_PATH), read_only=True) as con:
        return con.execute(f"select * from {table_name} limit ?", [limit]).fetchdf()


def render_quality_summary(report: dict) -> None:
    """Render data-quality report metrics."""

    missing = report.get("missing", False)
    passed = report.get("passed", False)
    total_results = report.get("total_results", 0)
    status_counts = report.get("status_counts", {})

    col1, col2, col3 = st.columns(3)
    col1.metric("Quality report present", "No" if missing else "Yes")
    col2.metric("Overall passed", "Yes" if passed else "No")
    col3.metric("dbt results", total_results)

    if status_counts:
        status_df = pd.DataFrame(
            [{"status": status, "count": count} for status, count in status_counts.items()]
        )
        st.dataframe(status_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No dbt status counts found. Generate the quality report first.")


def render_table_section(label: str, table_name: str, caption_prefix: str) -> None:
    """Render a table preview."""

    st.subheader(label)

    try:
        df = query_table(table_name)
    except FileNotFoundError as exc:
        st.error(str(exc))
        return

    st.caption(f"{caption_prefix}: `{table_name}`")
    st.dataframe(df, use_container_width=True, hide_index=True)

    if df.empty:
        st.warning("This table is empty for the current dataset.")


def render_audit_overview() -> None:
    """Render audit evidence summary cards."""

    st.markdown("### What the audit layer proves")
    st.write(
        "The silver layer can clean and deduplicate production source data, "
        "while the audit layer preserves evidence of what was changed."
    )

    try:
        row_counts = query_table("audit_source_to_silver_row_counts")
    except FileNotFoundError as exc:
        st.error(str(exc))
        return

    st.dataframe(row_counts, use_container_width=True, hide_index=True)


def main() -> None:
    st.set_page_config(
        page_title="PitWall Lakehouse",
        page_icon="🏁",
        layout="wide",
    )

    st.title("PitWall Lakehouse")
    st.caption(
        "Local-first Formula 1 lakehouse demo. "
        "This app reads trusted gold marts, audit models, and generated quality evidence."
    )

    st.warning(
        "If you are using fixture data, the numbers prove pipeline behavior only. "
        "Run `make dbt-build-latest` to inspect production RaceData outputs."
    )

    report = load_quality_report()

    with st.sidebar:
        st.header("Demo controls")
        selected_section = st.radio(
            "Section",
            ["Quality Evidence", "Gold Marts", "Audit Evidence", "Portfolio Proof"],
        )
        selected_gold_label = st.selectbox("Gold mart", list(GOLD_TABLES.keys()))
        selected_audit_label = st.selectbox("Audit table", list(AUDIT_TABLES.keys()))

    if selected_section == "Quality Evidence":
        st.header("Data-quality evidence")
        render_quality_summary(report)

        st.markdown("### What this proves")
        st.write(
            "The pipeline generated dbt artifacts, parsed them into a readable quality report, "
            "and exposes that evidence to the demo layer."
        )

    elif selected_section == "Gold Marts":
        st.header("Trusted gold outputs")
        render_table_section(
            selected_gold_label,
            GOLD_TABLES[selected_gold_label],
            "Trusted gold table",
        )

    elif selected_section == "Audit Evidence":
        st.header("Source anomaly audit evidence")
        render_audit_overview()
        render_table_section(
            selected_audit_label,
            AUDIT_TABLES[selected_audit_label],
            "Audit table",
        )

    else:
        st.header("Portfolio proof")
        st.markdown(
            """
This project currently demonstrates:

- raw-to-bronze ingestion with manifests and checksums
- production RaceData archive download
- row-count reconciliation
- DuckDB + Parquet local lakehouse storage
- dbt bronze, silver, gold, and audit transformations
- dbt tests for keys, uniqueness, relationships, and mart grain
- generated data-quality reports
- explicit audit evidence for production data anomalies
- Dagster orchestration
- a Streamlit demo that reads trusted outputs only

The dashboard is intentionally thin. The data platform is the product.
"""
        )


if __name__ == "__main__":
    main()
