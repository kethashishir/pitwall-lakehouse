import json
from pathlib import Path

from dashboard.streamlit_app.app import GOLD_TABLES, format_milliseconds, load_quality_report


def test_gold_tables_only_reference_gold_marts() -> None:
    assert GOLD_TABLES
    assert all(table_name.startswith("mart_") for table_name in GOLD_TABLES.values())


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
                "total_results": 63,
                "status_counts": {"pass": 42, "success": 21},
            }
        ),
        encoding="utf-8",
    )

    report = load_quality_report(report_path)

    assert report["passed"] is True
    assert report["total_results"] == 63
    assert report["status_counts"]["pass"] == 42
