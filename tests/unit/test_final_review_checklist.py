from pathlib import Path


def test_final_review_checklist_exists_and_covers_readiness_areas() -> None:
    text = Path("docs/final_review_checklist.md").read_text(encoding="utf-8")

    required_sections = [
        "Repository state",
        "Local checks",
        "Fixture pipeline",
        "Dagster fixture orchestration",
        "Docker fixture verification",
        "Production local pipeline",
        "Streamlit demo",
        "GitHub Actions",
        "Screenshots",
        "README review",
        "Career packaging",
        "Do not overclaim",
        "Final Git safety check",
    ]

    for section in required_sections:
        assert section in text


def test_final_review_checklist_mentions_quality_and_artifacts() -> None:
    text = Path("docs/final_review_checklist.md").read_text(encoding="utf-8")

    required_phrases = [
        "pitwall-quality-report",
        "latest_dbt_quality_summary.json",
        "run_results.json",
        "passed=True",
        "dbt result count is 106",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_final_review_checklist_prevents_overclaiming() -> None:
    text = Path("docs/final_review_checklist.md").read_text(encoding="utf-8")

    assert "Do not describe the project as:" in text
    assert "real-time streaming" in text
    assert "predictive race modeling" in text
    assert "local-first data-engineering platform" in text


def test_readme_links_final_review_checklist() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "docs/final_review_checklist.md" in text
    assert "overclaim prevention" in text
