"""Unit tests for the per-mode composers (T014)."""

from __future__ import annotations

from pathlib import Path

from tutorial_specify.charter import ChapterPlan, FileRow, UseCase
from tutorial_specify.modes import MODE_REGISTRY, VALID_MODES, compose_block_focused, \
    compose_cohesive_synthesis, compose_multi_actor_distillation
from tutorial_specify.pdf_extract import CodeBlock


def test_mode_registry_has_three():
    assert VALID_MODES == frozenset({
        "cohesive-synthesis",
        "block-focused",
        "multi-actor-distillation",
    })
    assert set(MODE_REGISTRY) == VALID_MODES


def _block_focused_plan() -> ChapterPlan:
    return ChapterPlan(
        path=Path("/dev/null"),
        chapter_id="ch04",
        mode="block-focused",
        files=[FileRow(path="ch04/a.glp", scope="A demo")],
    )


def test_block_focused_emits_one_user_story_per_file():
    plan = _block_focused_plan()
    sections = compose_block_focused(plan, {"ch04/a.glp": [CodeBlock(
        "b1", (37,), (49,), "p(a).", "Program 1.1"
    )]})
    assert "User Story 1" in sections["user_scenarios"]
    assert "ch04/a.glp" in sections["user_scenarios"]
    assert "FR-001" in sections["requirements"]
    assert "Program 1.1" in sections["requirements"]
    assert "Measurable Outcomes" in sections["success_criteria"]


def test_cohesive_synthesis_emits_narrative_user_story():
    plan = ChapterPlan(
        path=Path("/dev/null"),
        chapter_id="ch01",
        mode="cohesive-synthesis",
        files=[FileRow(path="ch01/ch-01-ex-01.glp", scope="merge demo")],
    )
    sections = compose_cohesive_synthesis(plan, {
        "ch01/ch-01-ex-01.glp": [CodeBlock("b1", (5, 6), (17, 18), "merge(...).", None)],
    })
    assert "single narrative" in sections["user_scenarios"]
    assert "weave" in sections["requirements"]
    assert "%%" in sections["requirements"]


def test_multi_actor_distillation_requires_project_files():
    plan = ChapterPlan(
        path=Path("/dev/null"),
        chapter_id="ch12",
        mode="multi-actor-distillation",
        use_cases=[
            UseCase(
                name="play-foo/",
                scope="self.glp agent.glp network.glp actors.glp boot.glp",
                file_paths=[
                    "self.glp", "agent.glp", "network.glp", "actors.glp", "boot.glp"
                ],
            )
        ],
    )
    sections = compose_multi_actor_distillation(plan, {
        "play-foo/": [CodeBlock("b1", (115,), (127,), "agent(...).", None)],
    })
    req = sections["requirements"]
    for required in ("self.glp", "agent.glp", "network.glp", "actors.glp", "boot.glp"):
        assert required in req
    assert "play_play-foo" in sections["user_scenarios"]
    assert "Key Entities" in sections["key_entities"]
