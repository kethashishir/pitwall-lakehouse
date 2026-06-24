from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the local PitWall Lakehouse project."""

    model_config = SettingsConfigDict(env_prefix="PITWALL_", env_file=".env", extra="ignore")

    env: str = "local"
    project_root: Path = Path(".")
    data_dir: Path = Path("data")
    metadata_dir: Path = Path("metadata")

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def bronze_dir(self) -> Path:
        return self.data_dir / "bronze"

    @property
    def silver_dir(self) -> Path:
        return self.data_dir / "silver"

    @property
    def gold_dir(self) -> Path:
        return self.data_dir / "gold"

    @property
    def ingestion_manifest_dir(self) -> Path:
        return self.metadata_dir / "ingestion_manifests"

    @property
    def data_quality_report_dir(self) -> Path:
        return self.metadata_dir / "data_quality_reports"

    @property
    def run_log_dir(self) -> Path:
        return self.metadata_dir / "run_logs"


settings = Settings()
