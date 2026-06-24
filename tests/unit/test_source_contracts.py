from pathlib import Path

from pitwall.ingestion.source_contracts import (
    RACEDATA_CONTRACT,
    list_csv_files,
    missing_expected_files,
)

FIXTURE_DIR = Path("tests/fixtures/raw/racedata_sample")


def test_racedata_contract_has_public_zip_url() -> None:
    assert RACEDATA_CONTRACT.name == "TracingInsights RaceData"
    assert RACEDATA_CONTRACT.source_url.endswith("/data.zip")
    assert RACEDATA_CONTRACT.expected_files


def test_sample_fixture_contains_all_expected_contract_files() -> None:
    assert missing_expected_files(FIXTURE_DIR) == set()


def test_list_csv_files_only_returns_csv_filenames() -> None:
    found_files = list_csv_files(FIXTURE_DIR)

    assert "races.csv" in found_files
    assert "drivers.csv" in found_files
    assert all(file_name.endswith(".csv") for file_name in found_files)
