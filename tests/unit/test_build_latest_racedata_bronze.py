from pathlib import Path

import pytest

from pitwall.ingestion.build_latest_racedata_bronze import find_latest_racedata_csv_dir


def test_find_latest_racedata_csv_dir_returns_latest_snapshot(tmp_path: Path) -> None:
    older = tmp_path / "20260101T000000Z" / "csv"
    newer = tmp_path / "20260102T000000Z" / "csv"

    older.mkdir(parents=True)
    newer.mkdir(parents=True)

    assert find_latest_racedata_csv_dir(tmp_path) == newer


def test_find_latest_racedata_csv_dir_fails_when_no_snapshots_exist(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="No RaceData snapshots found"):
        find_latest_racedata_csv_dir(tmp_path)
