from pathlib import Path


def test_career_packaging_doc_exists_and_has_resume_sections() -> None:
    text = Path("docs/career_packaging.md").read_text(encoding="utf-8")

    required_sections = [
        "One-line project description",
        "Resume version",
        "LinkedIn post draft",
        "GitHub repo description",
        "Interview explanation",
        "Recruiter message version",
        "Do not overclaim",
    ]

    for section in required_sections:
        assert section in text


def test_career_packaging_mentions_core_technical_proof() -> None:
    text = Path("docs/career_packaging.md").read_text(encoding="utf-8")

    required_phrases = [
        "DuckDB",
        "dbt",
        "Dagster",
        "Streamlit",
        "Docker",
        "GitHub Actions",
        "audit models",
        "generated quality reports",
        "duplicate lap-time grain rows",
        "missing pit-stop durations",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_career_packaging_avoids_overclaiming() -> None:
    text = Path("docs/career_packaging.md").read_text(encoding="utf-8")

    assert "Do not say:" in text
    assert "this predicts race outcomes" in text
    assert "this is real-time streaming" in text
    assert "local-first data-engineering platform" in text


def test_readme_links_career_packaging_doc() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "docs/career_packaging.md" in text
    assert "Resume bullets" in text
