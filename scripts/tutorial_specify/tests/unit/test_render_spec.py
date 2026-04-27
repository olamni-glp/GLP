"""Unit tests for tutorial_specify.render_spec (T013)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tutorial_specify.charter import (
    ChapterPlan,
    ChapterSources,
    ChapterTutorial,
    FileRow,
    TutorialInputs,
    UseCase,
)
from tutorial_specify.pdf_extract import CodeBlock
from tutorial_specify.render_spec import render_spec


def _make_inputs(tmp_path: Path) -> TutorialInputs:
    charter = tmp_path / "charter.md"
    plan = tmp_path / "ch04_plan.md"
    sources = tmp_path / "ch04-sources.md"
    tutorial = tmp_path / "ch04_tutorial.md"
    for p in (charter, plan, sources, tutorial):
        p.write_text("placeholder", encoding="utf-8")
    return TutorialInputs(charter=charter, plan=plan, sources=sources, tutorial=tutorial)


def _block_focused_plan(plan_path: Path) -> ChapterPlan:
    return ChapterPlan(
        path=plan_path,
        chapter_id="ch04",
        mode="block-focused",
        files=[
            FileRow(path="ch04/ch-04-ex-01.glp", scope="example one"),
            FileRow(path="ch04/ch-04-ex-02.glp", scope="example two"),
        ],
        raw="...",
    )


def test_block_focused_renders_canonical_citations(tmp_path):
    inputs = _make_inputs(tmp_path)
    plan = _block_focused_plan(inputs.plan)
    sources = ChapterSources(path=inputs.sources, sources=[(1, "PDF book pp 25–36")])
    tutorial = ChapterTutorial(path=inputs.tutorial, title="Chapter 4", raw="...")

    blocks = {
        "ch04/ch-04-ex-01.glp": [CodeBlock("b1", (37,), (49,), "p(a).\n", "Program 1.1")],
        "ch04/ch-04-ex-02.glp": [CodeBlock("b2", (38, 40), (50, 52), "q(b).\n", None)],
    }

    body = render_spec(
        feature_dir_name="002-tutorial-ch04",
        chapter_id="ch04",
        plan=plan,
        sources=sources,
        tutorial=tutorial,
        inputs=inputs,
        blocks_for_target=blocks,
        inputs_hashes={"ch04_plan.md": "abc"},
    )

    # Canonical citation present
    assert "book p 37" in body
    assert "Program 1.1" in body
    assert "book pp 38–40" in body
    # FR-003: no PDF page numbers
    assert "PDF p" not in body
    assert "PDF pp" not in body
    # Spec sections present
    assert "## User Scenarios & Testing" in body
    assert "## Requirements" in body
    assert "## Success Criteria" in body
    assert "## Assumptions" in body
    assert "Tutorial Mode" in body and "block-focused" in body


def test_render_refuses_pdf_pages(tmp_path):
    inputs = _make_inputs(tmp_path)
    plan = _block_focused_plan(inputs.plan)
    sources = ChapterSources(path=inputs.sources, sources=[])
    tutorial = ChapterTutorial(path=inputs.tutorial, title="Chapter 4", raw="...")
    body = render_spec(
        feature_dir_name="002-tutorial-ch04",
        chapter_id="ch04",
        plan=plan,
        sources=sources,
        tutorial=tutorial,
        inputs=inputs,
        blocks_for_target={
            "ch04/ch-04-ex-01.glp": [CodeBlock("b1", (37,), (49,), "p(a).\n", None)],
            "ch04/ch-04-ex-02.glp": [CodeBlock("b2", (38,), (50,), "q(b).\n", None)],
        },
        inputs_hashes={},
    )
    assert re.search(r"\bPDF\s+pp?\s+\d", body) is None


def test_multi_actor_distillation_renders_use_cases(tmp_path):
    inputs = _make_inputs(tmp_path)
    plan = ChapterPlan(
        path=inputs.plan,
        chapter_id="ch12",
        mode="multi-actor-distillation",
        use_cases=[
            UseCase(
                name="blocklace-consensus/",
                scope="self.glp agent.glp network.glp actors.glp boot.glp",
                file_paths=[
                    "self.glp", "agent.glp", "network.glp", "actors.glp", "boot.glp",
                ],
            )
        ],
        raw="...",
    )
    sources = ChapterSources(path=inputs.sources, sources=[])
    tutorial = ChapterTutorial(path=inputs.tutorial, title="Chapter 12", raw="...")
    body = render_spec(
        feature_dir_name="003-tutorial-ch12",
        chapter_id="ch12",
        plan=plan,
        sources=sources,
        tutorial=tutorial,
        inputs=inputs,
        blocks_for_target={
            "blocklace-consensus/": [
                CodeBlock("b1", (115, 123), (127, 135), "agent(...).", None)
            ]
        },
        inputs_hashes={},
    )
    assert "blocklace-consensus" in body
    assert "Key Entities" in body
    # Required project-shape FR text
    assert "self.glp" in body
    assert "boot.glp" in body
