import json
from pathlib import Path

import pytest

from pitwall.quality.dbt_quality_report import (
    generate_dbt_quality_report,
    render_summary_markdown,
    summarize_dbt_run_results,
)

FIXTURE_ARTIFACT = Path("tests/fixtures/dbt/run_results_sample.json")


def test_summarize_dbt_run_results_counts_statuses_and_resource_types() -> None:
    summary = summarize_dbt_run_results(FIXTURE_ARTIFACT)

    assert summary.total_results == 3
    assert summary.status_counts == {"pass": 2, "success": 1}
    assert summary.resource_type_counts == {"model": 1, "test": 2}
    assert summary.passed is True
    assert summary.failed_results == []


def test_render_summary_markdown_contains_status_table() -> None:
    summary = summarize_dbt_run_results(FIXTURE_ARTIFACT)
    markdown = render_summary_markdown(summary)

    assert "# dbt Data Quality Summary" in markdown
    assert "| pass | 2 |" in markdown
    assert "| success | 1 |" in markdown
    assert "No failed dbt results." in markdown


def test_generate_dbt_quality_report_writes_json_and_markdown(tmp_path: Path) -> None:
    summary = generate_dbt_quality_report(
        artifact_path=FIXTURE_ARTIFACT,
        output_dir=tmp_path,
    )

    json_path = tmp_path / "latest_dbt_quality_summary.json"
    markdown_path = tmp_path / "latest_dbt_quality_summary.md"

    assert summary.passed is True
    assert json_path.exists()
    assert markdown_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert payload["passed"] is True
    assert payload["total_results"] == 3


def test_generate_dbt_quality_report_exits_nonzero_for_failed_result(tmp_path: Path) -> None:
    failed_artifact = tmp_path / "failed_run_results.json"
    failed_artifact.write_text(
        json.dumps(
            {
                "metadata": {
                    "dbt_schema_version": "https://schemas.getdbt.com/dbt/run-results/v6.json"
                },
                "results": [
                    {
                        "status": "fail",
                        "execution_time": 0.01,
                        "unique_id": "test.pitwall_dbt.not_null_dim_driver_driver_id",
                        "message": "1 row failed",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(SystemExit):
        generate_dbt_quality_report(
            artifact_path=failed_artifact,
            output_dir=tmp_path / "reports",
        )
