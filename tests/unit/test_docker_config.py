from pathlib import Path


def test_dockerfile_exists_and_uses_python_311() -> None:
    text = Path("Dockerfile").read_text(encoding="utf-8")

    assert "FROM python:3.11-slim" in text
    assert "WORKDIR /app" in text
    assert 'pip install --no-cache-dir -e ".[dev]"' in text
    assert 'CMD ["make", "check"]' in text


def test_dockerignore_excludes_generated_artifacts() -> None:
    text = Path(".dockerignore").read_text(encoding="utf-8")

    ignored_paths = [
        ".venv",
        "data/raw/*",
        "data/bronze/*",
        "metadata/data_quality_reports/*",
        "dbt/pitwall_dbt/target",
        "dbt/pitwall_dbt/logs",
        "dbt/pitwall_dbt/dbt_packages",
    ]

    for ignored_path in ignored_paths:
        assert ignored_path in text


def test_makefile_exposes_docker_targets() -> None:
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "docker-required:" in text
    assert "docker-build: docker-required" in text
    assert "docker-check: docker-required" in text
    assert "docker-fixture-pipeline: docker-required" in text
    assert "Docker is not installed or not on PATH" in text
    assert "docker build -t pitwall-lakehouse:local ." in text
