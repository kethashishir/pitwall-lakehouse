from pathlib import Path


def test_readme_has_portfolio_landing_sections() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    required_sections = [
        "# PitWall Lakehouse",
        "Why this project exists",
        "Architecture",
        "Tech stack",
        "Data modes",
        "Quick start",
        "Core commands",
        "Lakehouse layers",
        "Production data issues discovered",
        "Data quality",
        "CI",
        "Streamlit demo",
        "Documentation",
        "What this project proves",
        "Limitations",
        "Portfolio case study",
    ]

    for section in required_sections:
        assert section in text


def test_readme_mentions_production_anomaly_audit_story() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "duplicate lap-time rows" in text
    assert "missing pit-stop duration" in text
    assert "audit_lap_time_duplicate_grain" in text
    assert "audit_source_to_silver_row_counts" in text
    assert "production data issues are not silently hidden" in text


def test_readme_explains_fixture_vs_production_modes() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "racedata_sample" in text
    assert "racedata_latest" in text
    assert "make demo-fixture" in text
    assert "make download-racedata" in text
    assert "make demo-latest" in text


def test_readme_does_not_overclaim_ml_or_cloud() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "no predictive ML layer" in text
    assert "no cloud object storage yet" in text
    assert "local-first and zero-cost" in text
