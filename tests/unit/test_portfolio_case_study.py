from pathlib import Path


def test_portfolio_case_study_exists_and_has_core_sections() -> None:
    text = Path("docs/portfolio_case_study.md").read_text(encoding="utf-8")

    required_sections = [
        "One-line summary",
        "Why I built this",
        "Data source",
        "Architecture",
        "Bronze layer",
        "Silver layer",
        "Audit layer",
        "Gold layer",
        "Data quality",
        "Orchestration",
        "CI strategy",
        "Streamlit demo",
        "What made this project difficult",
        "What I would improve next",
        "Key takeaway",
    ]

    for section in required_sections:
        assert section in text


def test_portfolio_case_study_mentions_real_production_data_issues() -> None:
    text = Path("docs/portfolio_case_study.md").read_text(encoding="utf-8")

    assert "duplicate lap-time rows" in text
    assert "missing pit-stop duration" in text
    assert "safer numeric casting" in text
    assert "row-count reconciliation" in text


def test_portfolio_case_study_does_not_overclaim_ml() -> None:
    text = Path("docs/portfolio_case_study.md").read_text(encoding="utf-8")

    assert (
        "I would not add machine learning until the data foundation and use case justify it."
        in text
    )
