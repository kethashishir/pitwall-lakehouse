import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DbtNodeResult:
    """A compact dbt node result for reporting."""

    unique_id: str
    resource_type: str
    status: str
    execution_time_seconds: float | None
    message: str | None


@dataclass(frozen=True)
class DbtQualitySummary:
    """A compact quality summary derived from dbt run_results.json."""

    generated_at_utc: str
    artifact_path: str
    dbt_schema_version: str | None
    total_results: int
    status_counts: dict[str, int]
    resource_type_counts: dict[str, int]
    failed_results: list[DbtNodeResult]

    @property
    def passed(self) -> bool:
        bad_statuses = {"error", "fail", "failed"}
        return not any(status in bad_statuses for status in self.status_counts)


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file."""

    return json.loads(path.read_text(encoding="utf-8"))


def extract_resource_type(unique_id: str) -> str:
    """Extract dbt resource type from a unique_id like model.project.name."""

    return unique_id.split(".", maxsplit=1)[0] if "." in unique_id else "unknown"


def summarize_dbt_run_results(artifact_path: Path) -> DbtQualitySummary:
    """Summarize dbt run_results.json into a compact quality report."""

    payload = load_json(artifact_path)
    results = payload.get("results", [])

    status_counter: Counter[str] = Counter()
    resource_type_counter: Counter[str] = Counter()
    failed_results: list[DbtNodeResult] = []

    for result in results:
        unique_id = result.get("unique_id", "unknown")
        status = result.get("status", "unknown")
        resource_type = extract_resource_type(unique_id)
        execution_time = result.get("execution_time")
        message = result.get("message")

        status_counter[status] += 1
        resource_type_counter[resource_type] += 1

        node_result = DbtNodeResult(
            unique_id=unique_id,
            resource_type=resource_type,
            status=status,
            execution_time_seconds=execution_time,
            message=message,
        )

        if status in {"error", "fail", "failed"}:
            failed_results.append(node_result)

    return DbtQualitySummary(
        generated_at_utc=datetime.now(UTC).isoformat(),
        artifact_path=str(artifact_path),
        dbt_schema_version=payload.get("metadata", {}).get("dbt_schema_version"),
        total_results=len(results),
        status_counts=dict(sorted(status_counter.items())),
        resource_type_counts=dict(sorted(resource_type_counter.items())),
        failed_results=failed_results,
    )


def write_summary_json(summary: DbtQualitySummary, output_path: Path) -> None:
    """Write summary as JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(summary) | {"passed": summary.passed}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render_summary_markdown(summary: DbtQualitySummary) -> str:
    """Render summary as human-readable Markdown."""

    status_lines = [
        f"| {status} | {count} |" for status, count in sorted(summary.status_counts.items())
    ]
    resource_lines = [
        f"| {resource_type} | {count} |"
        for resource_type, count in sorted(summary.resource_type_counts.items())
    ]

    failed_section = "No failed dbt results."

    if summary.failed_results:
        failed_lines = [
            "| unique_id | resource_type | status | message |",
            "| --- | --- | --- | --- |",
        ]
        for result in summary.failed_results:
            failed_lines.append(
                f"| {result.unique_id} | {result.resource_type} | "
                f"{result.status} | {result.message or ''} |"
            )
        failed_section = "\n".join(failed_lines)

    return f"""# dbt Data Quality Summary

Generated at UTC: `{summary.generated_at_utc}`

Artifact path: `{summary.artifact_path}`

Overall passed: `{summary.passed}`

Total dbt results: `{summary.total_results}`

## Status counts

| status | count |
| --- | --- |
{chr(10).join(status_lines)}

## Resource type counts

| resource_type | count |
| --- | --- |
{chr(10).join(resource_lines)}

## Failed results

{failed_section}
"""


def write_summary_markdown(summary: DbtQualitySummary, output_path: Path) -> None:
    """Write summary as Markdown."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_summary_markdown(summary), encoding="utf-8")


def generate_dbt_quality_report(
    artifact_path: Path,
    output_dir: Path,
) -> DbtQualitySummary:
    """Generate JSON and Markdown quality reports from dbt run_results.json."""

    summary = summarize_dbt_run_results(artifact_path)

    write_summary_json(summary, output_dir / "latest_dbt_quality_summary.json")
    write_summary_markdown(summary, output_dir / "latest_dbt_quality_summary.md")

    if not summary.passed:
        raise SystemExit("dbt quality report contains failed results")

    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a dbt data-quality summary report.")
    parser.add_argument("--artifact-path", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = generate_dbt_quality_report(
        artifact_path=args.artifact_path,
        output_dir=args.output_dir,
    )

    print(f"dbt quality report generated: {summary.total_results} results, passed={summary.passed}")


if __name__ == "__main__":
    main()
