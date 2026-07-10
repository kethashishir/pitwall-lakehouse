from pathlib import Path


def test_fact_models_use_try_cast_for_nullable_numeric_source_fields() -> None:
    fact_pit_stop = Path("dbt/pitwall_dbt/models/silver/fact_pit_stop.sql").read_text(
        encoding="utf-8"
    )
    fact_race_result = Path("dbt/pitwall_dbt/models/silver/fact_race_result.sql").read_text(
        encoding="utf-8"
    )

    assert "try_cast(nullif(milliseconds" in fact_pit_stop

    nullable_result_fields = [
        "grid",
        "positionOrder",
        "points",
        "laps",
        "milliseconds",
        "fastestLap",
        "rank",
        "fastestLapSpeed",
    ]

    for field in nullable_result_fields:
        assert f"try_cast(nullif({field}" in fact_race_result


def test_fact_lap_time_deduplicates_race_driver_lap_grain() -> None:
    text = Path("dbt/pitwall_dbt/models/silver/fact_lap_time.sql").read_text(encoding="utf-8")

    assert "row_number() over" in text
    assert "partition by race_id, driver_id, lap_number" in text
    assert "where duplicate_rank = 1" in text
