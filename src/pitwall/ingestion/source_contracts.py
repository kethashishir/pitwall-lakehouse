from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceContract:
    """Documented expectations for an external data source."""

    name: str
    source_url: str
    expected_files: tuple[str, ...]
    license_note: str
    access_note: str


RACEDATA_CONTRACT = SourceContract(
    name="TracingInsights RaceData",
    source_url="https://github.com/TracingInsights/RaceData/releases/latest/download/data.zip",
    expected_files=(
        "circuits.csv",
        "constructors.csv",
        "drivers.csv",
        "lap_times.csv",
        "pit_stops.csv",
        "qualifying.csv",
        "races.csv",
        "results.csv",
        "seasons.csv",
        "status.csv",
    ),
    license_note="Repository currently describes the dataset as CC0-1.0/Public Domain.",
    access_note="Public GitHub release asset; no Kaggle credentials required for this path.",
)


def list_csv_files(directory: Path) -> set[str]:
    """Return CSV filenames found directly inside a directory."""

    return {path.name for path in directory.glob("*.csv") if path.is_file()}


def missing_expected_files(
    directory: Path,
    contract: SourceContract = RACEDATA_CONTRACT,
) -> set[str]:
    """Return expected source files missing from a directory."""

    found_files = list_csv_files(directory)
    return set(contract.expected_files) - found_files
