import json
import os
import subprocess
from pathlib import Path

from dagster import AssetExecutionContext, Definitions, MetadataValue, asset

from pitwall.ingestion.build_latest_racedata_bronze import build_latest_racedata_bronze
from pitwall.ingestion.raw_to_bronze import raw_to_bronze
from pitwall.quality.dbt_quality_report import generate_dbt_quality_report


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt" / "pitwall_dbt"
DBT_PROFILES_DIR = PROJECT_ROOT / "dbt" / "pitwall_dbt"
DBT_RUN_RESULTS_PATH = DBT_PROJECT_DIR / "target" / "run_results.json"
QUALITY_REPORT_DIR = PROJECT_ROOT / "metadata" / "data_quality_reports"

SUPPORTED_BRONZE_DATASETS = {"racedata_sample", "racedata_latest"}


def get_bronze_dataset() -> str:
    """Return the bronze dataset Dagster should materialize."""

    dataset = os.getenv("PITWALL_BRONZE_DATASET", "racedata_sample")

    if dataset not in SUPPORTED_BRONZE_DATASETS:
        supported = ", ".join(sorted(SUPPORTED_BRONZE_DATASETS))
        raise ValueError(
            f"Unsupported PITWALL_BRONZE_DATASET={dataset!r}. Supported values: {supported}"
        )

    return dataset


def dbt_vars_for_dataset(dataset: str) -> str:
    """Return dbt vars JSON for a bronze dataset."""

    return json.dumps({"bronze_dataset": dataset})


def run_command(command: list[str]) -> None:
    """Run a subprocess command from the project root."""

    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


@asset
def bronze_racedata(context: AssetExecutionContext) -> str:
    """Build bronze Parquet for the selected RaceData dataset."""

    dataset = get_bronze_dataset()

    if dataset == "racedata_sample":
        manifest = raw_to_bronze(
            raw_dir=PROJECT_ROOT / "tests" / "fixtures" / "raw" / "racedata_sample",
            bronze_dir=PROJECT_ROOT / "data" / "bronze" / "racedata_sample",
            manifest_dir=PROJECT_ROOT / "metadata" / "ingestion_manifests",
            source_name="racedata_sample",
        )

        context.add_output_metadata(
            {
                "dataset": dataset,
                "files": len(manifest.files),
                "rows": manifest.total_bronze_rows,
            }
        )
    else:
        build_latest_racedata_bronze(
            raw_root_dir=PROJECT_ROOT / "data" / "raw" / "racedata",
            bronze_dir=PROJECT_ROOT / "data" / "bronze" / "racedata_latest",
            manifest_dir=PROJECT_ROOT / "metadata" / "ingestion_manifests",
        )

        context.add_output_metadata(
            {
                "dataset": dataset,
                "note": MetadataValue.text(
                    "Built latest RaceData bronze from the newest downloaded raw snapshot."
                ),
            }
        )

    return dataset


@asset(deps=[bronze_racedata])
def dbt_lakehouse_build(context: AssetExecutionContext, bronze_racedata: str) -> str:
    """Run dbt build for the selected bronze dataset."""

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
            "--vars",
            dbt_vars_for_dataset(bronze_racedata),
        ]
    )

    if not DBT_RUN_RESULTS_PATH.exists():
        raise FileNotFoundError(f"Missing dbt run results: {DBT_RUN_RESULTS_PATH}")

    context.add_output_metadata(
        {
            "dataset": bronze_racedata,
            "run_results": MetadataValue.path(str(DBT_RUN_RESULTS_PATH)),
        }
    )

    return str(DBT_RUN_RESULTS_PATH)


@asset(deps=[dbt_lakehouse_build])
def dbt_quality_summary(context: AssetExecutionContext) -> str:
    """Generate a data-quality summary from dbt run_results.json."""

    report = generate_dbt_quality_report(
        artifact_path=DBT_RUN_RESULTS_PATH,
        output_dir=QUALITY_REPORT_DIR,
    )

    markdown_report_path = QUALITY_REPORT_DIR / "latest_dbt_quality_summary.md"
    json_report_path = QUALITY_REPORT_DIR / "latest_dbt_quality_summary.json"

    context.add_output_metadata(
        {
            "passed": report.passed,
            "total_results": report.total_results,
            "markdown_report": MetadataValue.path(str(markdown_report_path)),
            "json_report": MetadataValue.path(str(json_report_path)),
        }
    )

    return str(json_report_path)


defs = Definitions(
    assets=[
        bronze_racedata,
        dbt_lakehouse_build,
        dbt_quality_summary,
    ]
)
