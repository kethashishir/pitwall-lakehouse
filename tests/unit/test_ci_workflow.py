from pathlib import Path


def test_ci_uploads_quality_report_artifacts() -> None:
    text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "actions/upload-artifact@v4" in text
    assert "pitwall-quality-report" in text
    assert "metadata/data_quality_reports/latest_dbt_quality_summary.json" in text
    assert "metadata/data_quality_reports/latest_dbt_quality_summary.md" in text
    assert "dbt/pitwall_dbt/target/run_results.json" in text


def test_ci_validates_fixture_dagster_orchestration() -> None:
    text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "Materialize Dagster fixture assets" in text
    assert "make dagster-materialize-fixture" in text


def test_ci_does_not_download_production_racedata() -> None:
    text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "make download-racedata" not in text
    assert "make build-latest-racedata-bronze" not in text
    assert "make dbt-build-latest" not in text
    assert "make dagster-materialize-latest" not in text
