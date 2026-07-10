from pathlib import Path


def test_license_file_exists_and_is_mit() -> None:
    text = Path("LICENSE").read_text(encoding="utf-8")

    assert "MIT License" in text
    assert "Shishir Ketha" in text
    assert "THE SOFTWARE IS PROVIDED" in text


def test_data_usage_notice_distinguishes_code_and_source_data() -> None:
    text = Path("docs/data_usage_notice.md").read_text(encoding="utf-8")

    assert "The project code is licensed under the MIT License" in text
    assert "The source data is not owned by this project" in text
    assert "upstream data source terms" in text
    assert "Generated artifacts are intentionally not committed" in text


def test_data_usage_notice_avoids_overclaiming() -> None:
    text = Path("docs/data_usage_notice.md").read_text(encoding="utf-8")

    assert "not be treated as an official Formula 1 data product" in text
    assert "betting system" in text
    assert "race prediction system" in text


def test_readme_links_license_and_data_notice() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "MIT License" in text
    assert "docs/data_usage_notice.md" in text
    assert "upstream data source terms" in text
