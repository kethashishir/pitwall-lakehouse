import argparse
import json
import shutil
import urllib.request
import zipfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pitwall.ingestion.raw_to_bronze import sha256_file
from pitwall.ingestion.source_contracts import RACEDATA_CONTRACT


@dataclass(frozen=True)
class RaceDataDownloadManifest:
    """Manifest for a downloaded and extracted RaceData archive."""

    run_id: str
    source_name: str
    source_url: str
    downloaded_at_utc: str
    archive_path: str
    extract_dir: str
    archive_size_bytes: int
    archive_sha256: str
    extracted_files: list[str]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write stable pretty JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def safe_extract_zip(zip_path: Path, extract_dir: Path) -> list[str]:
    """Extract a zip file while blocking path traversal."""

    extracted_files: list[str] = []
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            member_path = extract_dir / member.filename
            resolved_member_path = member_path.resolve()
            resolved_extract_dir = extract_dir.resolve()

            if not str(resolved_member_path).startswith(str(resolved_extract_dir)):
                raise ValueError(f"Unsafe zip member path: {member.filename}")

            archive.extract(member, extract_dir)

            if not member.is_dir():
                extracted_files.append(member.filename)

    return sorted(extracted_files)


def flatten_csvs_from_nested_data_dir(extract_dir: Path, flat_csv_dir: Path) -> list[str]:
    """Copy extracted CSVs into one flat directory for the raw-to-bronze converter."""

    flat_csv_dir.mkdir(parents=True, exist_ok=True)

    copied_files: list[str] = []

    for csv_path in sorted(extract_dir.rglob("*.csv")):
        target_path = flat_csv_dir / csv_path.name
        shutil.copy2(csv_path, target_path)
        copied_files.append(target_path.name)

    return copied_files


def download_file(source_url: str, destination_path: Path) -> None:
    """Download a file from a URL."""

    destination_path.parent.mkdir(parents=True, exist_ok=True)

    with urllib.request.urlopen(source_url) as response:
        destination_path.write_bytes(response.read())


def download_racedata_archive(
    raw_root_dir: Path,
    manifest_dir: Path,
    source_url: str = RACEDATA_CONTRACT.source_url,
) -> RaceDataDownloadManifest:
    """Download RaceData data.zip, extract it, flatten CSVs, and write a manifest."""

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    downloaded_at = datetime.now(UTC).isoformat()

    snapshot_dir = raw_root_dir / run_id
    archive_path = snapshot_dir / "archive" / "data.zip"
    extract_dir = snapshot_dir / "extracted"
    flat_csv_dir = snapshot_dir / "csv"

    download_file(source_url=source_url, destination_path=archive_path)
    extracted_files = safe_extract_zip(zip_path=archive_path, extract_dir=extract_dir)
    flattened_csvs = flatten_csvs_from_nested_data_dir(
        extract_dir=extract_dir,
        flat_csv_dir=flat_csv_dir,
    )

    manifest = RaceDataDownloadManifest(
        run_id=run_id,
        source_name=RACEDATA_CONTRACT.name,
        source_url=source_url,
        downloaded_at_utc=downloaded_at,
        archive_path=str(archive_path),
        extract_dir=str(flat_csv_dir),
        archive_size_bytes=archive_path.stat().st_size,
        archive_sha256=sha256_file(archive_path),
        extracted_files=flattened_csvs or extracted_files,
    )

    write_json(
        manifest_dir / f"racedata_download_{run_id}.json",
        asdict(manifest),
    )

    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and extract TracingInsights RaceData.")
    parser.add_argument("--raw-root-dir", required=True, type=Path)
    parser.add_argument("--manifest-dir", required=True, type=Path)
    parser.add_argument("--source-url", default=RACEDATA_CONTRACT.source_url)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    manifest = download_racedata_archive(
        raw_root_dir=args.raw_root_dir,
        manifest_dir=args.manifest_dir,
        source_url=args.source_url,
    )

    print(
        "RaceData download complete: "
        f"{len(manifest.extracted_files)} CSV files, "
        f"snapshot={manifest.run_id}"
    )
    print(f"raw_csv_dir={manifest.extract_dir}")


if __name__ == "__main__":
    main()
