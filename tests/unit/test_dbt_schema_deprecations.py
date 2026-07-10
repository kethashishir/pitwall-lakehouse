from pathlib import Path


def test_relationship_tests_use_arguments_property() -> None:
    text = Path("dbt/pitwall_dbt/models/silver/schema.yml").read_text(encoding="utf-8")
    lines = text.splitlines()

    for index, line in enumerate(lines):
        if line.strip() == "- relationships:":
            following_lines = lines[index + 1 : index + 4]
            following_text = "\n".join(following_lines)

            assert "arguments:" in following_text


def test_relationship_tests_do_not_use_top_level_to_field_arguments() -> None:
    text = Path("dbt/pitwall_dbt/models/silver/schema.yml").read_text(encoding="utf-8")

    deprecated_patterns = [
        "- relationships:\n              to:",
        "- relationships:\n              field:",
    ]

    for pattern in deprecated_patterns:
        assert pattern not in text


def test_gold_unique_combination_tests_use_arguments_property() -> None:
    text = Path("dbt/pitwall_dbt/models/gold/schema.yml").read_text(encoding="utf-8")
    lines = text.splitlines()

    for index, line in enumerate(lines):
        if line.strip() == "- dbt_utils.unique_combination_of_columns:":
            following_lines = lines[index + 1 : index + 4]
            following_text = "\n".join(following_lines)

            assert "arguments:" in following_text
            assert "combination_of_columns:" in following_text


def test_gold_unique_combination_tests_do_not_use_top_level_arguments() -> None:
    text = Path("dbt/pitwall_dbt/models/gold/schema.yml").read_text(encoding="utf-8")

    deprecated_pattern = (
        "- dbt_utils.unique_combination_of_columns:\n          combination_of_columns:"
    )

    assert deprecated_pattern not in text
