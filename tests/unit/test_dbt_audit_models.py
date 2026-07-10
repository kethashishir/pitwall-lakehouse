from pathlib import Path

AUDIT_DIR = Path("dbt/pitwall_dbt/models/audit")


def test_audit_models_exist() -> None:
    expected_models = {
        "audit_lap_time_duplicate_grain.sql",
        "audit_pit_stop_missing_duration.sql",
        "audit_result_nullable_numeric_fields.sql",
        "audit_source_to_silver_row_counts.sql",
    }

    actual_models = {path.name for path in AUDIT_DIR.glob("audit_*.sql")}

    assert expected_models <= actual_models


def test_lap_time_duplicate_audit_preserves_duplicate_grain_evidence() -> None:
    text = (AUDIT_DIR / "audit_lap_time_duplicate_grain.sql").read_text(encoding="utf-8")

    assert "group by" in text.lower()
    assert "race_id" in text
    assert "driver_id" in text
    assert "lap_number" in text
    assert "having count(*) > 1" in text.lower()


def test_source_to_silver_audit_compares_bronze_and_silver_counts() -> None:
    text = (AUDIT_DIR / "audit_source_to_silver_row_counts.sql").read_text(encoding="utf-8")

    assert "bronze_row_count" in text
    assert "silver_row_count" in text
    assert "row_count_difference" in text
    assert "fact_lap_time" in text
    assert "fact_pit_stop" in text
    assert "fact_race_result" in text
