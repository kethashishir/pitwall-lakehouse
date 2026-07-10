from pathlib import Path

from pitwall.ingestion.raw_to_bronze import raw_to_bronze


def find_latest_racedata_csv_dir(raw_root_dir: Path) -> Path:
    """Find the latest downloaded RaceData CSV snapshot directory."""

    snapshots = sorted(raw_root_dir.glob("*/csv"))

    if not snapshots:
        raise FileNotFoundError("No RaceData snapshots found. Run `make download-racedata` first.")

    return snapshots[-1]


def build_latest_racedata_bronze(
    raw_root_dir: Path = Path("data/raw/racedata"),
    bronze_dir: Path = Path("data/bronze/racedata_latest"),
    manifest_dir: Path = Path("metadata/ingestion_manifests"),
) -> None:
    """Convert the latest downloaded RaceData CSV snapshot to bronze Parquet."""

    latest_csv_dir = find_latest_racedata_csv_dir(raw_root_dir)

    manifest = raw_to_bronze(
        raw_dir=latest_csv_dir,
        bronze_dir=bronze_dir,
        manifest_dir=manifest_dir,
        source_name="racedata_latest",
    )

    print(
        "Latest RaceData bronze build complete: "
        f"{len(manifest.files)} files, {manifest.total_bronze_rows} rows"
    )


def main() -> None:
    build_latest_racedata_bronze()


if __name__ == "__main__":
    main()
