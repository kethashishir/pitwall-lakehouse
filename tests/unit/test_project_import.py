from pitwall.config import Settings


def test_settings_defaults_point_to_local_lakehouse_dirs() -> None:
    settings = Settings()

    assert str(settings.raw_dir) == "data/raw"
    assert str(settings.bronze_dir) == "data/bronze"
    assert str(settings.silver_dir) == "data/silver"
    assert str(settings.gold_dir) == "data/gold"
