import json
from pathlib import Path

import pytest
from orchestration.dagster_project.definitions import (
    SUPPORTED_BRONZE_DATASETS,
    dbt_vars_for_dataset,
    defs,
    get_bronze_dataset,
)


def test_dagster_definitions_load_assets() -> None:
    asset_graph = defs.resolve_asset_graph()
    asset_keys = {asset_key.to_user_string() for asset_key in asset_graph.get_all_asset_keys()}

    assert asset_keys == {
        "bronze_racedata",
        "dbt_lakehouse_build",
        "dbt_quality_summary",
    }


def test_dagster_quality_asset_depends_on_dbt_build() -> None:
    asset_graph = defs.resolve_asset_graph()

    quality_key = next(
        asset_key
        for asset_key in asset_graph.get_all_asset_keys()
        if asset_key.to_user_string() == "dbt_quality_summary"
    )

    quality_node = asset_graph.get(quality_key)
    parent_keys = {parent_key.to_user_string() for parent_key in quality_node.parent_keys}

    assert parent_keys == {"dbt_lakehouse_build"}


def test_supported_bronze_datasets_are_explicit() -> None:
    assert SUPPORTED_BRONZE_DATASETS == {"racedata_sample", "racedata_latest"}


def test_get_bronze_dataset_defaults_to_sample(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PITWALL_BRONZE_DATASET", raising=False)

    assert get_bronze_dataset() == "racedata_sample"


def test_get_bronze_dataset_rejects_unknown_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PITWALL_BRONZE_DATASET", "bad_dataset")

    with pytest.raises(ValueError, match="Unsupported PITWALL_BRONZE_DATASET"):
        get_bronze_dataset()


def test_dbt_vars_for_dataset_returns_json_payload() -> None:
    payload = json.loads(dbt_vars_for_dataset("racedata_latest"))

    assert payload == {"bronze_dataset": "racedata_latest"}


def test_dagster_quality_asset_uses_latest_quality_report_paths() -> None:
    definitions_text = Path("orchestration/dagster_project/definitions.py").read_text(
        encoding="utf-8"
    )

    assert "latest_dbt_quality_summary.md" in definitions_text
    assert "latest_dbt_quality_summary.json" in definitions_text
    assert "report.markdown_path" not in definitions_text
    assert "report.json_path" not in definitions_text
