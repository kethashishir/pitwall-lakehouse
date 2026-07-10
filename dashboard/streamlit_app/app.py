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
    """Read a trusted gold table from DuckDB."""

    if table_name not in GOLD_TABLES.values():
        raise ValueError(f"Unsupported table requested: {table_name}")

    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(
            "DuckDB database not found. Run `make dagster-materialize` or `make dbt-build` first."
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


def render_table_section(label: str, table_name: str) -> None:
    """Render a gold table preview."""

    st.subheader(label)

    try:
        df = query_table(table_name)
    except FileNotFoundError as exc:
        st.error(str(exc))
        return

    st.caption(f"Trusted gold table: `{table_name}`")
    st.dataframe(df, use_container_width=True, hide_index=True)

    if df.empty:
        st.warning("This mart is empty for the current fixture data.")


def main() -> None:
    st.set_page_config(
        page_title="PitWall Lakehouse",
        page_icon="🏁",
        layout="wide",
    )

    st.title("PitWall Lakehouse")
    st.caption(
        "Local-first Formula 1 lakehouse demo. "
        "This app reads trusted gold marts and generated quality evidence only."
    )

    st.warning(
        "Current demo uses the tiny committed fixture. "
        "The numbers prove pipeline behavior and model structure, not full historical F1 conclusions."
    )

    report = load_quality_report()

    with st.sidebar:
        st.header("Demo controls")
        selected_section = st.radio(
            "Section",
            ["Quality Evidence", "Gold Marts", "Portfolio Proof"],
        )
        selected_table_label = st.selectbox("Gold mart", list(GOLD_TABLES.keys()))

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
        render_table_section(selected_table_label, GOLD_TABLES[selected_table_label])

    else:
        st.header("Portfolio proof")
        st.markdown(
            """
This project currently demonstrates:

- raw-to-bronze ingestion with manifests and checksums
- row-count reconciliation
- DuckDB + Parquet local lakehouse storage
- dbt bronze, silver, and gold transformations
- dbt tests for keys, uniqueness, relationships, and mart grain
- generated data-quality reports
- Dagster orchestration
- a Streamlit demo that reads only trusted gold outputs

The dashboard is intentionally thin. The data platform is the product.
"""
        )


if __name__ == "__main__":
    main()
