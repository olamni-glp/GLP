"""Cohesive-synthesis mode composer.

Multiple short book code blocks woven into one tutorial file with narrative
comments paraphrasing book prose. Typical of chapters with many small
examples (ch 1, ch 3, early sections of ch 5). One user story per chapter
narrative file. Per `contracts/spec-output-format.md` § Mode A.
"""

from __future__ import annotations

from typing import Iterable

from tutorial_specify.charter import ChapterPlan, FileRow
from tutorial_specify.pdf_extract import CodeBlock, format_book_pages_citation


def compose(
    plan: ChapterPlan,
    blocks_for_file: dict[str, list[CodeBlock]],
) -> dict[str, str]:
    user_stories = _user_stories(plan.files)
    requirements = _functional_requirements(plan.files, blocks_for_file)
    success = _success_criteria(plan)
    return {
        "user_scenarios": user_stories,
        "requirements": requirements,
        "success_criteria": success,
        "key_entities": "",
    }


def _user_stories(files: list[FileRow]) -> str:
    if not files:
        return ""
    # cohesive-synthesis chapters typically have one or a few narrative files
    # covering a section group. Each gets its own P1 user story.
    out: list[str] = []
    for i, fr in enumerate(files, start=1):
        priority = "P1" if i == 1 else "P2"
        out.append(
            f"### User Story {i} - Read §X.Y as a single narrative `{fr.path}` "
            f"(Priority: {priority})\n\n"
            f"{fr.scope}\n\n"
            f"**Why this priority**: cohesive-synthesis chapters guide the "
            f"learner through a thematic arc; the narrative file is the unit "
            f"of value.\n\n"
            f"**Independent Test**: load `{fr.path}` into the REPL and step "
            f"through the demo goals named in the chapter plan; each MUST "
            f"succeed (or suspend where declared).\n\n"
            f"**Acceptance Scenarios**:\n\n"
            f"1. **Given** a learner reading the corresponding sections of "
            f"`GLP_ART.pdf` alongside `{fr.path}`, **When** they execute each "
            f"demo goal in turn, **Then** every goal yields the plan's stated "
            f"outcome and the in-file `%%` comments paraphrase the book prose "
            f"surrounding each Program.\n"
        )
    return "\n---\n\n".join(out)


def _functional_requirements(
    files: list[FileRow], blocks_for_file: dict[str, list[CodeBlock]]
) -> str:
    lines: list[str] = ["### Functional Requirements\n"]
    for i, fr in enumerate(files, start=1):
        blocks = blocks_for_file.get(fr.path, [])
        citations = _format_citations(blocks)
        lines.append(
            f"- **FR-{i:03d}**: `{fr.path}` MUST weave the book Programs from "
            f"the corresponding sections into a single coherent narrative file "
            f"({citations}). Every Program preserved verbatim from "
            f"`GLP_ART.pdf`; never from model memory or training. Each Program "
            f"MUST be preceded by a `%%` comment block paraphrasing the matching "
            f"paragraph of book prose."
        )
    lines.append(
        "\n- **FR-VFR**: The narrative file MUST load cleanly in the GLP REPL "
        "(`cd glp_runtime/bin; dart run glp_repl.dart`); every demo goal named in "
        "the chapter plan MUST succeed (or suspend where declared). Tutorial "
        "Charter Compliance per Constitution Principle VI."
    )
    return "\n".join(lines)


def _success_criteria(plan: ChapterPlan) -> str:
    return (
        "### Measurable Outcomes\n\n"
        "- **SC-001**: Loading the chapter's narrative tutorial file(s) into the "
        "GLP REPL succeeds without parse errors.\n"
        "- **SC-002**: Each demo goal stated in the chapter plan, when run after "
        "load, yields the plan's stated outcome.\n"
        "- **SC-003**: A learner reading the corresponding sections of "
        "`GLP_ART.pdf` finds 100% of in-file Programs traceable to a specific "
        "`book p N §A.B[, Program N.N]` citation in the Functional Requirements.\n"
    )


def _format_citations(blocks: Iterable[CodeBlock]) -> str:
    parts: list[str] = []
    for b in blocks:
        parts.append(format_book_pages_citation(b.book_pages, None, b.program_id))
    if not parts:
        return "see chapter plan source references"
    return "; ".join(parts)
