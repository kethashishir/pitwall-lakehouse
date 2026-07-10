from pathlib import Path


def test_readme_has_project_badges() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    required_badges = [
        "actions/workflows/ci.yml/badge.svg",
        "python-3.11",
        "dbt-duckdb",
        "storage-DuckDB",
        "orchestration-Dagster",
        "docker-fixture--validated",
        "status-portfolio--ready",
    ]

    for badge in required_badges:
        assert badge in text


def test_readme_badges_are_near_top() -> None:
    lines = Path("README.md").read_text(encoding="utf-8").splitlines()
    first_twenty_lines = "\n".join(lines[:20])

    assert "# PitWall Lakehouse" in first_twenty_lines
    assert "![CI]" in first_twenty_lines
    assert "![Python]" in first_twenty_lines
    assert "![Docker]" in first_twenty_lines
