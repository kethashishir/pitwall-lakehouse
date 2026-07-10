from pathlib import Path

BRONZE_MODEL_DIR = Path("dbt/pitwall_dbt/models/bronze")


def test_bronze_models_use_bronze_dataset_variable() -> None:
    bronze_sql_files = sorted(BRONZE_MODEL_DIR.glob("bronze__*.sql"))

    assert bronze_sql_files

    for sql_file in bronze_sql_files:
        text = sql_file.read_text(encoding="utf-8")

        assert 'var("bronze_dataset")' in text
        assert "data/bronze/racedata_sample" not in text
        assert "data/bronze/racedata_latest" not in text


def test_dbt_project_declares_default_bronze_dataset_variable() -> None:
    text = Path("dbt/pitwall_dbt/dbt_project.yml").read_text(encoding="utf-8")

    assert "vars:" in text
    assert "bronze_dataset: racedata_sample" in text
