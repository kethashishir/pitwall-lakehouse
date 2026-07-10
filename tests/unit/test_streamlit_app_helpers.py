import json
from pathlib import Path

from dashboard.streamlit_app.app import (
    AUDIT_TABLES,
    GOLD_TABLES,
    format_milliseconds,
    load_quality_report,
)


def test_gold_tables_only_reference_gold_marts() -> None:
    assert GOLD_TABLES
    assert all(table_name.startswith("mart_") for table_name in GOLD_TABLES.values())


def test_audit_tables_only_reference_audit_models() -> None:
    assert AUDIT_TABLES
    assert all(table_name.startswith("audit_") for table_name in AUDIT_TABLES.values())


def test_streamlit_demo_exposes_expected_audit_tables() -> None:
    assert set(AUDIT_TABLES.values()) == {
        "audit_lap_time_duplicate_grain",
        "audit_pit_stop_missing_duration",
        "audit_result_nullable_numeric_fields",
        "audit_source_to_silver_row_counts",
    }


def test_format_milliseconds_handles_numbers_and_missing_values() -> None:
    assert format_milliseconds(1234) == "1,234 ms"
    assert format_milliseconds(None) == "N/A"


def test_load_quality_report_returns_missing_payload_when_file_absent(tmp_path: Path) -> None:
    report = load_quality_report(tmp_path / "missing.json")

    assert report["missing"] is True
    assert report["passed"] is False


def test_load_quality_report_reads_json_payload(tmp_path: Path) -> None:
    report_path = tmp_path / "quality.json"
    report_path.write_text(
        json.dumps(
            {
                "passed": True,
                "total_results": 106,
                "status_counts": {"pass": 77, "success": 29},
            }
        ),
        encoding="utf-8",
    )

    report = load_quality_report(report_path)

    assert report["passed"] is True
    assert report["total_results"] == 106
    assert report["status_counts"]["pass"] == 77
