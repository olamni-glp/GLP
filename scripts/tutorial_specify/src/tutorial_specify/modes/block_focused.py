"""Block-focused mode composer.

Each substantial book Program gets its own tutorial file. One user story per
file, one Functional Requirement per file, citing the book Program directly.
Per `contracts/spec-output-format.md` § Mode B.
"""

from __future__ import annotations

from typing import Iterable

from tutorial_specify.charter import ChapterPlan, FileRow
from tutorial_specify.pdf_extract import CodeBlock, format_book_pages_citation


def compose(
    plan: ChapterPlan,
    blocks_for_file: dict[str, list[CodeBlock]],
) -> dict[str, str]:
    """Return spec sections (markdown strings) keyed by section name.

    `blocks_for_file` maps each declared file path to the code blocks the
    extractor associated with it; each block MUST have already passed
    REPL parse-check before this composer is called.
    """
    user_stories = _user_stories(plan.files)
    requirements = _functional_requirements(plan.files, blocks_for_file)
    success = _success_criteria(plan)
    return {
        "user_scenarios": user_stories,
        "requirements": requirements,
        "success_criteria": success,
        "key_entities": "",  # block-focused chapters generally have no domain entities
    }


def _user_stories(files: list[FileRow]) -> str:
    out: list[str] = []
    for i, fr in enumerate(files, start=1):
        priority = "P1" if i == 1 else ("P2" if i <= 3 else "P3")
        out.append(
            f"### User Story {i} - Read and run `{fr.path}` (Priority: {priority})\n\n"
            f"{fr.scope}\n\n"
            f"**Why this priority**: each Program in a block-focused chapter is "
            f"self-contained; learners can succeed on this Program independently of others.\n\n"
            f"**Independent Test**: load `{fr.path}` in the GLP REPL and run the demo "
            f"goal stated in the chapter plan.\n\n"
            f"**Acceptance Scenarios**:\n\n"
            f"1. **Given** the GLP REPL loaded with `{fr.path}`, **When** the demo "
            f"goal is run, **Then** the REPL prints `→ succeeds` (or `→ suspended` "
            f"where the chapter plan declares suspension is acceptable).\n"
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
            f"- **FR-{i:03d}**: `{fr.path}` MUST contain the GLP code corresponding "
            f"to the chapter plan's scope statement, sourced from `GLP_ART.pdf` "
            f"({citations}). Code MUST NOT come from model memory or training; "
            f"every clause MUST be traceable to the cited pages."
        )
    lines.append(
        "\n- **FR-VFR**: Every `.glp` file in this chapter MUST load cleanly in "
        "the GLP REPL (`cd glp_runtime/bin; dart run glp_repl.dart`); the demo "
        "goal in the chapter plan MUST succeed (or suspend, where suspension is "
        "explicitly declared acceptable). Tutorial Charter Compliance per "
        "Constitution Principle VI."
    )
    return "\n".join(lines)


def _success_criteria(plan: ChapterPlan) -> str:
    return (
        "### Measurable Outcomes\n\n"
        f"- **SC-001**: Loading any of the {len(plan.files)} chapter files into "
        "the GLP REPL succeeds without parse errors.\n"
        "- **SC-002**: Running each file's stated demo goal yields the chapter "
        "plan's stated outcome (`→ succeeds` or declared `→ suspended`).\n"
        "- **SC-003**: 100% of code lines in each tutorial file are traceable "
        "to a `book p N §A.B[, Program N.N]` citation in the Functional "
        "Requirements above.\n"
    )


def _format_citations(blocks: Iterable[CodeBlock]) -> str:
    parts: list[str] = []
    for b in blocks:
        cite = format_book_pages_citation(b.book_pages, None, b.program_id)
        parts.append(cite)
    if not parts:
        return "see chapter plan source references"
    return "; ".join(parts)
