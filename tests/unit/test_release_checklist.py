from pathlib import Path


def test_release_checklist_exists_and_covers_required_checks() -> None:
    text = Path("docs/release_checklist.md").read_text(encoding="utf-8")

    required_sections = [
        "Main branch is clean",
        "GitHub Actions is green",
        "Local fixture verification passes",
        "Docker fixture verification passes",
        "Production local path passes",
        "Final review checklist is complete",
        "Screenshot checklist is complete",
        "Career packaging is ready",
        "License and data notice exist",
        "Known limitations are documented",
    ]

    for section in required_sections:
        assert section in text


def test_release_checklist_includes_tag_instructions() -> None:
    text = Path("docs/release_checklist.md").read_text(encoding="utf-8")

    assert "git tag -a v1.0.0" in text
    assert "git push origin v1.0.0" in text
    assert "PitWall Lakehouse v1.0.0" in text


def test_release_checklist_prevents_bad_release() -> None:
    text = Path("docs/release_checklist.md").read_text(encoding="utf-8")

    assert "Do not tag if" in text
    assert "CI is failing" in text
    assert "Docker fixture pipeline fails" in text
    assert "generated artifacts are accidentally tracked" in text


def test_readme_links_release_checklist() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "docs/release_checklist.md" in text
    assert "Use it before tagging" in text
