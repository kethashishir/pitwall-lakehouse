from pathlib import Path


def test_architecture_diagram_exists_and_mentions_core_layers() -> None:
    text = Path("docs/architecture_diagram.md").read_text(encoding="utf-8")

    required_terms = [
        "Public RaceData CSV archive",
        "Bronze Parquet files",
        "dbt Bronze Views",
        "dbt Silver Facts and Dimensions",
        "dbt Audit Models",
        "dbt Gold Marts",
        "Generated Quality Report",
        "Streamlit Demo",
        "Dagster Asset Graph",
        "GitHub Actions CI",
        "Docker",
    ]

    for term in required_terms:
        assert term in text


def test_architecture_diagram_mentions_data_modes() -> None:
    text = Path("docs/architecture_diagram.md").read_text(encoding="utf-8")

    assert "racedata_sample fixture" in text
    assert "racedata_latest production" in text
    assert "Local only" in text
    assert "Not committed to Git" in text


def test_architecture_diagram_explains_cleaning_observability() -> None:
    text = Path("docs/architecture_diagram.md").read_text(encoding="utf-8")

    assert "separates cleaning from observability" in text
    assert "audit models preserve evidence" in text
    assert "silently hiding production data issues" in text


def test_readme_links_architecture_diagram() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "docs/architecture_diagram.md" in text
    assert "visual architecture diagram" in text
