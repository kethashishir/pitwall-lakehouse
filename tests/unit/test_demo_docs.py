from pathlib import Path


def test_demo_walkthrough_exists_and_mentions_audit_evidence() -> None:
    text = Path("docs/demo_walkthrough.md").read_text(encoding="utf-8")

    assert "Audit Evidence" in text
    assert "bronze-to-silver row-count differences" in text
    assert "The data platform is the product" in text


def test_interview_talking_points_cover_production_data_issues() -> None:
    text = Path("docs/interview_talking_points.md").read_text(encoding="utf-8")

    assert "duplicate lap-time rows" in text
    assert "missing pit-stop duration" in text
    assert "Fixture mode" in text
    assert "Production mode" in text


def test_makefile_exposes_demo_targets() -> None:
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "demo-fixture:" in text
    assert "demo-latest:" in text
    assert "$(MAKE) build-fixture-bronze" in text
    assert "$(MAKE) build-latest-racedata-bronze" in text
    assert "$(MAKE) streamlit-demo" in text
