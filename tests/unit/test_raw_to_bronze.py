import json
from pathlib import Path

import pandas as pd
import pytest

from pitwall.ingestion.raw_to_bronze import raw_to_bronze

FIXTURE_DIR = Path("tests/fixtures/raw/racedata_sample")


def test_raw_to_bronze_writes_parquet_and_manifest(tmp_path: Path) -> None:
    bronze_dir = tmp_path / "bronze"
    manifest_dir = tmp_path / "manifests"

    manifest = raw_to_bronze(
        raw_dir=FIXTURE_DIR,
        bronze_dir=bronze_dir,
        manifest_dir=manifest_dir,
        source_name="test_racedata_sample",
    )

    assert manifest.source_name == "test_racedata_sample"
    assert len(manifest.files) == 10
    assert manifest.total_raw_rows == manifest.total_bronze_rows
    assert manifest.total_raw_rows > 0

    expected_bronze_files = {
        "circuits.parquet",
        "constructors.parquet",
        "drivers.parquet",
        "lap_times.parquet",
        "pit_stops.parquet",
        "qualifying.parquet",
        "races.parquet",
        "results.parquet",
        "seasons.parquet",
        "status.parquet",
    }

    actual_bronze_files = {path.name for path in bronze_dir.glob("*.parquet")}

    assert actual_bronze_files == expected_bronze_files


def test_raw_to_bronze_preserves_fixture_row_counts(tmp_path: Path) -> None:
    bronze_dir = tmp_path / "bronze"
    manifest_dir = tmp_path / "manifests"

    manifest = raw_to_bronze(
        raw_dir=FIXTURE_DIR,
        bronze_dir=bronze_dir,
        manifest_dir=manifest_dir,
    )

    rows_by_file = {file.file_name: file.raw_row_count for file in manifest.files}

    assert rows_by_file["drivers.csv"] == 2
    assert rows_by_file["lap_times.csv"] == 4
    assert rows_by_file["pit_stops.csv"] == 2
    assert len(pd.read_parquet(bronze_dir / "lap_times.parquet")) == 4


def test_raw_to_bronze_manifest_json_contains_reconciliation_totals(tmp_path: Path) -> None:
    bronze_dir = tmp_path / "bronze"
    manifest_dir = tmp_path / "manifests"

    manifest = raw_to_bronze(
        raw_dir=FIXTURE_DIR,
        bronze_dir=bronze_dir,
        manifest_dir=manifest_dir,
    )

    manifest_files = list(manifest_dir.glob("raw_to_bronze_*.json"))

    assert len(manifest_files) == 1

    payload = json.loads(manifest_files[0].read_text(encoding="utf-8"))

    assert payload["source_name"] == manifest.source_name
    assert payload["total_raw_rows"] == payload["total_bronze_rows"]
    assert payload["total_raw_rows"] == manifest.total_raw_rows
    assert len(payload["files"]) == 10
    assert all(file_payload["sha256"] for file_payload in payload["files"])


def test_raw_to_bronze_fails_when_expected_file_is_missing(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    for source_file in FIXTURE_DIR.glob("*.csv"):
        if source_file.name != "drivers.csv":
            (raw_dir / source_file.name).write_text(source_file.read_text(encoding="utf-8"))

    with pytest.raises(FileNotFoundError, match="drivers.csv"):
        raw_to_bronze(
            raw_dir=raw_dir,
            bronze_dir=tmp_path / "bronze",
            manifest_dir=tmp_path / "manifests",
        )
