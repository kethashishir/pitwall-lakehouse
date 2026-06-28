import subprocess
from pathlib import Path

from dagster import AssetExecutionContext, Definitions, asset

from pitwall.ingestion.raw_to_bronze import raw_to_bronze
from pitwall.quality.dbt_quality_report import generate_dbt_quality_report


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "raw" / "racedata_sample"
BRONZE_FIXTURE_DIR = PROJECT_ROOT / "data" / "bronze" / "racedata_sample"
INGESTION_MANIFEST_DIR = PROJECT_ROOT / "metadata" / "ingestion_manifests"
QUALITY_REPORT_DIR = PROJECT_ROOT / "metadata" / "data_quality_reports"
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt" / "pitwall_dbt"
DBT_PROFILES_DIR = DBT_PROJECT_DIR
DBT_RUN_RESULTS_PATH = DBT_PROJECT_DIR / "target" / "run_results.json"


def run_command(command: list[str], cwd: Path = PROJECT_ROOT) -> None:
    """Run a subprocess command and fail loudly if it exits nonzero."""

    subprocess.run(command, cwd=cwd, check=True)


@asset
def bronze_racedata_fixture(context: AssetExecutionContext) -> dict[str, int]:
    """Convert the tiny raw RaceData fixture into bronze Parquet."""

    manifest = raw_to_bronze(
        raw_dir=RAW_FIXTURE_DIR,
        bronze_dir=BRONZE_FIXTURE_DIR,
        manifest_dir=INGESTION_MANIFEST_DIR,
        source_name="racedata_sample",
    )

    context.log.info(
        "Bronze fixture ingestion complete: "
        f"{len(manifest.files)} files, {manifest.total_bronze_rows} rows"
    )

    return {
        "files": len(manifest.files),
        "rows": manifest.total_bronze_rows,
    }


@asset(deps=[bronze_racedata_fixture])
def dbt_lakehouse_build(context: AssetExecutionContext) -> dict[str, str]:
    """Run dbt deps and dbt build for the local DuckDB lakehouse."""

    run_command(
        [
            "dbt",
            "deps",
            "--project-dir",
            str(DBT_PROJECT_DIR),
            "--profiles-dir",
            str(DBT_PROFILES_DIR),
        ]
    )
    run_command(
        [
            "dbt",
            "build",
            "--project-dir",
            str(DBT_PROJECT_DIR),
            "--profiles-dir",
            str(DBT_PROFILES_DIR),
        ]
    )

    if not DBT_RUN_RESULTS_PATH.exists():
        raise FileNotFoundError(f"Expected dbt artifact not found: {DBT_RUN_RESULTS_PATH}")

    context.log.info(f"dbt build completed and artifact exists: {DBT_RUN_RESULTS_PATH}")

    return {
        "run_results_path": str(DBT_RUN_RESULTS_PATH),
    }


@asset(deps=[dbt_lakehouse_build])
def dbt_quality_summary(context: AssetExecutionContext) -> dict[str, object]:
    """Generate readable data-quality reports from dbt run_results.json."""

    summary = generate_dbt_quality_report(
        artifact_path=DBT_RUN_RESULTS_PATH,
        output_dir=QUALITY_REPORT_DIR,
    )

    context.log.info(
        "dbt quality report complete: "
        f"{summary.total_results} results, passed={summary.passed}"
    )

    return {
        "total_results": summary.total_results,
        "passed": summary.passed,
    }


defs = Definitions(
    assets=[
        bronze_racedata_fixture,
        dbt_lakehouse_build,
        dbt_quality_summary,
    ]
)
