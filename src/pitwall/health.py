from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HealthCheck:
    name: str
    passed: bool
    detail: str


REQUIRED_PATHS = {
    "dbt project": Path("dbt/pitwall_dbt/dbt_project.yml"),
    "CI workflow": Path(".github/workflows/ci.yml"),
    "Dockerfile": Path("Dockerfile"),
    "Docker ignore": Path(".dockerignore"),
    "Streamlit app": Path("dashboard/streamlit_app/app.py"),
    "Dagster definitions": Path("orchestration/dagster_project/definitions.py"),
}

OPTIONAL_ARTIFACTS = {
    "DuckDB database": Path("data/pitwall.duckdb"),
    "quality report json": Path("metadata/data_quality_reports/latest_dbt_quality_summary.json"),
    "quality report markdown": Path("metadata/data_quality_reports/latest_dbt_quality_summary.md"),
}

GENERATED_PATTERN_GROUPS = {
    "data/raw outputs": ["data/raw/*"],
    "data/bronze outputs": ["data/bronze/*"],
    "ingestion manifests": ["metadata/ingestion_manifests/*"],
    "quality reports": ["metadata/data_quality_reports/*"],
    "dbt target": ["dbt/pitwall_dbt/target", "dbt/**/target", "dbt/**/target/"],
    "dbt logs": ["dbt/pitwall_dbt/logs", "dbt/**/logs", "dbt/**/logs/"],
    "dbt packages": [
        "dbt/pitwall_dbt/dbt_packages",
        "dbt/**/dbt_packages",
        "dbt/**/dbt_packages/",
    ],
    "dagster local state": [".dagster"],
    "streamlit local state": [".streamlit"],
    "temporary dagster home": [".tmp_dagster_home*", ".tmp_dagster*"],
}


def check_required_paths() -> list[HealthCheck]:
    checks: list[HealthCheck] = []

    for name, path in REQUIRED_PATHS.items():
        checks.append(
            HealthCheck(
                name=name,
                passed=path.exists(),
                detail=str(path),
            )
        )

    return checks


def check_optional_artifacts() -> list[HealthCheck]:
    checks: list[HealthCheck] = []

    for name, path in OPTIONAL_ARTIFACTS.items():
        checks.append(
            HealthCheck(
                name=name,
                passed=path.exists(),
                detail=str(path),
            )
        )

    return checks


def check_gitignore_patterns() -> list[HealthCheck]:
    gitignore_path = Path(".gitignore")
    text = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""

    checks: list[HealthCheck] = [
        HealthCheck(
            name=".gitignore exists",
            passed=gitignore_path.exists(),
            detail=str(gitignore_path),
        )
    ]

    for name, acceptable_patterns in GENERATED_PATTERN_GROUPS.items():
        matched_patterns = [pattern for pattern in acceptable_patterns if pattern in text]
        checks.append(
            HealthCheck(
                name=f"gitignore coverage: {name}",
                passed=bool(matched_patterns),
                detail=", ".join(matched_patterns) if matched_patterns else "missing",
            )
        )

    return checks


def collect_health_checks() -> list[HealthCheck]:
    return [
        *check_required_paths(),
        *check_optional_artifacts(),
        *check_gitignore_patterns(),
    ]


def format_health_report(checks: list[HealthCheck]) -> str:
    lines = ["PitWall Lakehouse project health", ""]

    required_failures = [check for check in checks if not check.passed]

    for check in checks:
        status = "PASS" if check.passed else "WARN"
        lines.append(f"[{status}] {check.name}: {check.detail}")

    lines.append("")
    lines.append(f"total checks: {len(checks)}")
    lines.append(f"passed: {sum(check.passed for check in checks)}")
    lines.append(f"warnings: {len(required_failures)}")

    return "\n".join(lines)


def main() -> None:
    print(format_health_report(collect_health_checks()))


if __name__ == "__main__":
    main()
