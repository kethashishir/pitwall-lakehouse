from pathlib import Path


def test_makefile_exposes_verify_fixture_command() -> None:
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "verify-fixture:" in text
    assert "make verify-fixture" in text


def test_verify_fixture_command_runs_expected_steps() -> None:
    text = Path("Makefile").read_text(encoding="utf-8")

    required_steps = [
        "$(MAKE) check",
        "$(MAKE) build-fixture-bronze",
        "dbt deps --project-dir dbt/pitwall_dbt --profiles-dir dbt/pitwall_dbt",
        "$(MAKE) dbt-build-fixture",
        "$(MAKE) quality-report",
        "$(MAKE) project-health",
    ]

    for step in required_steps:
        assert step in text
