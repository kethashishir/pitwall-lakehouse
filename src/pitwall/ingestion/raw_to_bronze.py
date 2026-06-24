import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from pitwall.ingestion.source_contracts import (
    RACEDATA_CONTRACT,
    SourceContract,
    missing_expected_files,
)


@dataclass(frozen=True)
class IngestedFileManifest:
    """Manifest details for one raw CSV converted to bronze Parquet."""

    file_name: str
    raw_path: str
    bronze_path: str
    size_bytes: int
    sha256: str
    raw_row_count: int
    bronze_row_count: int
    columns: list[str]


@dataclass(frozen=True)
class IngestionManifest:
    """Run-level manifest for a raw-to-bronze ingestion."""

    run_id: str
    source_name: str
    source_url: str
    ingested_at_utc: str
    raw_dir: str
    bronze_dir: str
    files: list[IngestedFileManifest]

    @property
    def total_raw_rows(self) -> int:
        return sum(file.raw_row_count for file in self.files)

    @property
    def total_bronze_rows(self) -> int:
        return sum(file.bronze_row_count for file in self.files)


def sha256_file(path: Path) -> str:
    """Return SHA-256 checksum for a file."""

    digest = hashlib.sha256()

    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def read_csv_header(path: Path) -> list[str]:
    """Return a CSV header without loading the full file."""

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        return next(reader)


def count_csv_data_rows(path: Path) -> int:
    """Count CSV data rows excluding the header."""

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        return sum(1 for _ in reader)


def read_raw_csv_as_strings(path: Path) -> pd.DataFrame:
    """Read raw CSV as strings while preserving source-like null markers."""

    return pd.read_csv(path, dtype=str, keep_default_na=False)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write stable pretty JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def raw_to_bronze(
    raw_dir: Path,
    bronze_dir: Path,
    manifest_dir: Path,
    contract: SourceContract = RACEDATA_CONTRACT,
    source_name: str | None = None,
) -> IngestionManifest:
    """Convert expected raw CSV files into bronze Parquet and write a manifest."""

    missing_files = missing_expected_files(raw_dir, contract)

    if missing_files:
        missing_display = ", ".join(sorted(missing_files))
        raise FileNotFoundError(f"Missing expected source files: {missing_display}")

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    ingested_at = datetime.now(UTC).isoformat()

    bronze_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)

    file_manifests: list[IngestedFileManifest] = []

    for file_name in contract.expected_files:
        raw_path = raw_dir / file_name
        bronze_path = bronze_dir / f"{Path(file_name).stem}.parquet"

        raw_df = read_raw_csv_as_strings(raw_path)
        raw_df.to_parquet(bronze_path, index=False)

        bronze_df = pd.read_parquet(bronze_path)
        raw_row_count = count_csv_data_rows(raw_path)
        bronze_row_count = len(bronze_df)

        if raw_row_count != bronze_row_count:
            raise ValueError(
                f"Row-count mismatch for {file_name}: "
                f"raw={raw_row_count}, bronze={bronze_row_count}"
            )

        file_manifests.append(
            IngestedFileManifest(
                file_name=file_name,
                raw_path=str(raw_path),
                bronze_path=str(bronze_path),
                size_bytes=raw_path.stat().st_size,
                sha256=sha256_file(raw_path),
                raw_row_count=raw_row_count,
                bronze_row_count=bronze_row_count,
                columns=read_csv_header(raw_path),
            )
        )

    manifest = IngestionManifest(
        run_id=run_id,
        source_name=source_name or contract.name,
        source_url=contract.source_url,
        ingested_at_utc=ingested_at,
        raw_dir=str(raw_dir),
        bronze_dir=str(bronze_dir),
        files=file_manifests,
    )

    manifest_payload = asdict(manifest)
    manifest_payload["total_raw_rows"] = manifest.total_raw_rows
    manifest_payload["total_bronze_rows"] = manifest.total_bronze_rows

    manifest_path = manifest_dir / f"raw_to_bronze_{run_id}.json"
    write_json(manifest_path, manifest_payload)

    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert raw RaceData CSV files to bronze Parquet."
    )
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--bronze-dir", required=True, type=Path)
    parser.add_argument("--manifest-dir", required=True, type=Path)
    parser.add_argument("--source-name", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    manifest = raw_to_bronze(
        raw_dir=args.raw_dir,
        bronze_dir=args.bronze_dir,
        manifest_dir=args.manifest_dir,
        source_name=args.source_name,
    )

    print(
        "Raw-to-bronze ingestion complete: "
        f"{len(manifest.files)} files, "
        f"{manifest.total_raw_rows} rows"
    )


if __name__ == "__main__":
    main()
