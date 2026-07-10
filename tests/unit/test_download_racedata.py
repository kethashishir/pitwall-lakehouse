import zipfile
from pathlib import Path

import pytest

from pitwall.ingestion.download_racedata import (
    flatten_csvs_from_nested_data_dir,
    safe_extract_zip,
)


def test_safe_extract_zip_extracts_nested_csvs(tmp_path: Path) -> None:
    zip_path = tmp_path / "sample.zip"
    extract_dir = tmp_path / "extracted"

    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("data/drivers.csv", "driverId,driverRef\n1,verstappen\n")
        archive.writestr("data/races.csv", "raceId,year\n1,2023\n")

    extracted_files = safe_extract_zip(zip_path, extract_dir)

    assert extracted_files == ["data/drivers.csv", "data/races.csv"]
    assert (extract_dir / "data" / "drivers.csv").exists()


def test_safe_extract_zip_blocks_path_traversal(tmp_path: Path) -> None:
    zip_path = tmp_path / "unsafe.zip"
    extract_dir = tmp_path / "extracted"

    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("../bad.csv", "bad\n")

    with pytest.raises(ValueError, match="Unsafe zip member path"):
        safe_extract_zip(zip_path, extract_dir)


def test_flatten_csvs_from_nested_data_dir_copies_csvs_only(tmp_path: Path) -> None:
    extract_dir = tmp_path / "extracted"
    flat_csv_dir = tmp_path / "csv"

    (extract_dir / "data").mkdir(parents=True)
    (extract_dir / "data" / "drivers.csv").write_text("driverId\n1\n", encoding="utf-8")
    (extract_dir / "data" / "README.md").write_text("ignore me", encoding="utf-8")

    copied_files = flatten_csvs_from_nested_data_dir(extract_dir, flat_csv_dir)

    assert copied_files == ["drivers.csv"]
    assert (flat_csv_dir / "drivers.csv").exists()
    assert not (flat_csv_dir / "README.md").exists()
