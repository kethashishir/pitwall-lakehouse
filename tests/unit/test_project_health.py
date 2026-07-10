from pitwall.health import (
    GENERATED_PATTERNS,
    HealthCheck,
    collect_health_checks,
    format_health_report,
)


def test_generated_patterns_cover_core_artifact_paths() -> None:
    assert "data/raw/*" in GENERATED_PATTERNS
    assert "data/bronze/*" in GENERATED_PATTERNS
    assert "metadata/data_quality_reports/*" in GENERATED_PATTERNS
    assert "dbt/pitwall_dbt/target" in GENERATED_PATTERNS
    assert ".tmp_dagster_home*" in GENERATED_PATTERNS


def test_collect_health_checks_returns_expected_checks() -> None:
    checks = collect_health_checks()
    names = {check.name for check in checks}

    assert "dbt project" in names
    assert "CI workflow" in names
    assert "Dockerfile" in names
    assert "Streamlit app" in names
    assert "Dagster definitions" in names
    assert "quality report json" in names
    assert ".gitignore exists" in names


def test_format_health_report_contains_summary() -> None:
    checks = [
        HealthCheck(name="example pass", passed=True, detail="ok"),
        HealthCheck(name="example warn", passed=False, detail="missing"),
    ]

    report = format_health_report(checks)

    assert "PitWall Lakehouse project health" in report
    assert "[PASS] example pass: ok" in report
    assert "[WARN] example warn: missing" in report
    assert "total checks: 2" in report
    assert "passed: 1" in report
    assert "warnings: 1" in report
