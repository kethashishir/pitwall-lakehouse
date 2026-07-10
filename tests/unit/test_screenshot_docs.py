from pathlib import Path


def test_screenshot_checklist_exists_and_covers_core_evidence() -> None:
    text = Path("docs/screenshots_checklist.md").read_text(encoding="utf-8")

    required_items = [
        "Streamlit Quality Evidence",
        "Streamlit Audit Evidence",
        "Streamlit Gold Marts",
        "GitHub Actions green CI",
        "CI quality artifact",
        "Dagster materialization",
        "Docker fixture pipeline",
        "pitwall-quality-report",
    ]

    for item in required_items:
        assert item in text


def test_readme_links_screenshot_checklist() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "docs/screenshots_checklist.md" in text
    assert "Streamlit quality evidence" in text
    assert "Docker fixture pipeline" in text
    assert "Dagster materialization" in text
