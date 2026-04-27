"""Unit tests for tutorial_specify.charter (T010)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tutorial_specify.charter import parse_chapter_plan, parse_chapter_sources, parse_chapter_tutorial
from tutorial_specify.errors import MissingModeError, PlanDeficiencyError


def _fix(name: str, fixtures_dir: Path) -> Path:
    return fixtures_dir / name


def test_parse_minimal_plan_succeeds(fixtures_dir):
    plan = parse_chapter_plan(_fix("ch_minimal_plan.md", fixtures_dir), "ch99")
    assert plan.mode == "block-focused"
    assert len(plan.files) == 1
    assert plan.files[0].path == "ch99/ch-99-ex-01-minimal.glp"
    assert "single example" in plan.files[0].scope


def test_missing_mode_raises(fixtures_dir):
    with pytest.raises(MissingModeError, match=r"\*\*Mode\*\*"):
        parse_chapter_plan(_fix("ch_missing_mode.md", fixtures_dir), "ch98")


def test_inconsistent_multi_actor_raises(fixtures_dir):
    with pytest.raises(PlanDeficiencyError, match=r"boot\.glp"):
        parse_chapter_plan(_fix("ch_inconsistent.md", fixtures_dir), "ch97")


def test_block_focused_empty_files_raises(tmp_path):
    p = tmp_path / "ch_empty.md"
    p.write_text(
        "# test\n\n**Mode**: block-focused\n\n## Files\n\n## Acceptance\n",
        encoding="utf-8",
    )
    with pytest.raises(PlanDeficiencyError, match=r"no `## Files`"):
        parse_chapter_plan(p, "ch00")


def test_parse_minimal_sources(fixtures_dir):
    src = parse_chapter_sources(_fix("ch_minimal_sources.md", fixtures_dir))
    assert len(src.sources) == 2
    assert src.sources[0][0] == 1
    assert "PDF mock" in src.sources[0][1]


def test_parse_minimal_tutorial(fixtures_dir):
    t = parse_chapter_tutorial(_fix("ch_minimal_tutorial.md", fixtures_dir))
    assert t.title == "Chapter 99 — Minimal Test Fixture"
