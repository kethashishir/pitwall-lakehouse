import csv
from pathlib import Path

FIXTURE_DIR = Path("tests/fixtures/raw/racedata_sample")


EXPECTED_HEADERS = {
    "circuits.csv": [
        "circuitId",
        "circuitRef",
        "name",
        "location",
        "country",
        "lat",
        "lng",
        "alt",
        "url",
    ],
    "constructors.csv": ["constructorId", "constructorRef", "name", "nationality", "url"],
    "drivers.csv": [
        "driverId",
        "driverRef",
        "number",
        "code",
        "forename",
        "surname",
        "dob",
        "nationality",
        "url",
    ],
    "lap_times.csv": ["raceId", "driverId", "lap", "position", "time", "milliseconds"],
    "pit_stops.csv": ["raceId", "driverId", "stop", "lap", "time", "duration", "milliseconds"],
    "qualifying.csv": [
        "qualifyId",
        "raceId",
        "driverId",
        "constructorId",
        "number",
        "position",
        "q1",
        "q2",
        "q3",
    ],
    "races.csv": [
        "raceId",
        "year",
        "round",
        "circuitId",
        "name",
        "date",
        "time",
        "url",
        "fp1_date",
        "fp1_time",
        "fp2_date",
        "fp2_time",
        "fp3_date",
        "fp3_time",
        "quali_date",
        "quali_time",
        "sprint_date",
        "sprint_time",
    ],
    "results.csv": [
        "resultId",
        "raceId",
        "driverId",
        "constructorId",
        "number",
        "grid",
        "position",
        "positionText",
        "positionOrder",
        "points",
        "laps",
        "time",
        "milliseconds",
        "fastestLap",
        "rank",
        "fastestLapTime",
        "fastestLapSpeed",
        "statusId",
    ],
    "seasons.csv": ["year", "url"],
    "status.csv": ["statusId", "status"],
}


def read_csv_rows(filename: str) -> list[dict[str, str]]:
    with (FIXTURE_DIR / filename).open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def test_sample_fixture_headers_match_expected_source_shapes() -> None:
    for filename, expected_header in EXPECTED_HEADERS.items():
        with (FIXTURE_DIR / filename).open(newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            actual_header = next(reader)

        assert actual_header == expected_header


def test_sample_fixture_has_no_empty_tables() -> None:
    for filename in EXPECTED_HEADERS:
        assert read_csv_rows(filename), f"{filename} should contain at least one data row"


def test_lap_times_are_positive_milliseconds() -> None:
    rows = read_csv_rows("lap_times.csv")

    assert all(int(row["milliseconds"]) > 0 for row in rows)


def test_pit_stop_durations_are_positive_milliseconds() -> None:
    rows = read_csv_rows("pit_stops.csv")

    assert all(int(row["milliseconds"]) > 0 for row in rows)


def test_result_relationships_exist_in_fixture_dimensions() -> None:
    results = read_csv_rows("results.csv")
    races = {row["raceId"] for row in read_csv_rows("races.csv")}
    drivers = {row["driverId"] for row in read_csv_rows("drivers.csv")}
    constructors = {row["constructorId"] for row in read_csv_rows("constructors.csv")}
    statuses = {row["statusId"] for row in read_csv_rows("status.csv")}

    for result in results:
        assert result["raceId"] in races
        assert result["driverId"] in drivers
        assert result["constructorId"] in constructors
        assert result["statusId"] in statuses


def test_no_duplicate_race_driver_lap_rows_in_fixture() -> None:
    rows = read_csv_rows("lap_times.csv")
    keys = [(row["raceId"], row["driverId"], row["lap"]) for row in rows]

    assert len(keys) == len(set(keys))
