from pathlib import Path


def test_release_candidate_verification_doc_exists_and_covers_checks() -> None:
    text = Path("docs/release_candidate_verification.md").read_text(encoding="utf-8")

    required_sections = [
        "Local fixture verification",
        "Docker fixture verification",
        "Production local verification",
        "GitHub Actions verification",
        "Git safety verification",
        "Release decision",
        "Tag command",
    ]

    for section in required_sections:
        assert section in text


def test_release_candidate_verification_mentions_v100_candidate() -> None:
    text = Path("docs/release_candidate_verification.md").read_text(encoding="utf-8")

    assert "v1.0.0 candidate" in text
    assert "git tag -a v1.0.0" in text
    assert "PitWall Lakehouse v1.0.0 portfolio release" in text


def test_release_candidate_verification_records_pass_statuses() -> None:
    text = Path("docs/release_candidate_verification.md").read_text(encoding="utf-8")

    assert text.count("PASS") >= 5
    assert "Ready to tag v1.0.0" in text


def test_readme_links_release_candidate_verification() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "docs/release_candidate_verification.md" in text
    assert "Use this before tagging `v1.0.0`." in text
