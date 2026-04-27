"""Multi-actor distillation mode composer.

The chapter's multi-process / multi-actor code is distilled into one or more
project-shaped multi-actor plays — `{self, agent, network, actors, boot}.glp`
plus an optional Flutter entry point. Per `contracts/spec-output-format.md`
§ Mode C.
"""

from __future__ import annotations

from typing import Iterable

from tutorial_specify.charter import ChapterPlan, UseCase
from tutorial_specify.pdf_extract import CodeBlock, format_book_pages_citation


REQUIRED_PROJECT_FILES = ("self.glp", "agent.glp", "network.glp", "actors.glp", "boot.glp")


def compose(
    plan: ChapterPlan,
    blocks_for_use_case: dict[str, list[CodeBlock]],
) -> dict[str, str]:
    user_stories = _user_stories(plan.use_cases)
    requirements = _functional_requirements(plan.use_cases, blocks_for_use_case)
    success = _success_criteria(plan.use_cases)
    key_entities = _key_entities(plan.use_cases)
    return {
        "user_scenarios": user_stories,
        "requirements": requirements,
        "success_criteria": success,
        "key_entities": key_entities,
    }


def _user_stories(use_cases: list[UseCase]) -> str:
    out: list[str] = []
    for i, uc in enumerate(use_cases, start=1):
        priority = "P1" if i == 1 else ("P2" if i <= 2 else "P3")
        play_name = uc.name.rstrip("/")
        out.append(
            f"### User Story {i} - Run `play_{play_name}` (Priority: {priority})\n\n"
            f"{uc.scope}\n\n"
            f"**Why this priority**: multi-actor plays are the chapter's "
            f"deliverable; each play stands alone as a runnable demo of the "
            f"chapter's protocol.\n\n"
            f"**Independent Test**: load the project at `chNN/{play_name}/` "
            f"and run `play_{play_name}.` in the GLP REPL; expect "
            f"`→ succeeds` (or `→ suspended` if the chapter plan declares "
            f"open channels are acceptable for this play).\n\n"
            f"**Acceptance Scenarios**:\n\n"
            f"1. **Given** the project loaded with all five files "
            f"({', '.join(REQUIRED_PROJECT_FILES)}), **When** "
            f"`play_{play_name}.` is invoked, **Then** the REPL prints "
            f"`→ succeeds` (or declared `→ suspended`).\n"
        )
    return "\n---\n\n".join(out)


def _functional_requirements(
    use_cases: list[UseCase], blocks_for_use_case: dict[str, list[CodeBlock]]
) -> str:
    lines: list[str] = ["### Functional Requirements\n"]
    fr_n = 1
    for uc in use_cases:
        play_name = uc.name.rstrip("/")
        blocks = blocks_for_use_case.get(uc.name, [])
        citations = _format_citations(blocks)
        lines.append(
            f"- **FR-{fr_n:03d}**: The project at `chNN/{play_name}/` MUST "
            f"contain exactly the five files {REQUIRED_PROJECT_FILES} (no "
            f"additional files; no missing files). Each file's content MUST "
            f"distil the corresponding multi-actor protocol from `GLP_ART.pdf` "
            f"({citations}). Code MUST come from the PDF in source, never from "
            f"model memory or training."
        )
        fr_n += 1
        lines.append(
            f"- **FR-{fr_n:03d}**: `chNN/{play_name}/agent.glp` MUST implement "
            f"the per-actor agent process the book describes for this play; "
            f"`chNN/{play_name}/network.glp` MUST wire the message routing; "
            f"`chNN/{play_name}/actors.glp` MUST contain deterministic GLP-side "
            f"actor scripts so the play runs headless in the REPL; "
            f"`chNN/{play_name}/boot.glp` MUST orchestrate the spawn order."
        )
        fr_n += 1
        if "flutter" in uc.scope.lower() or "main_olamni" in uc.scope.lower():
            lines.append(
                f"- **FR-{fr_n:03d}**: A Flutter entry point at "
                f"`glp_multiagent/lib/main_olamni_chNN_{play_name}.dart` MUST "
                f"orchestrate one Dart isolate per agent and the per-actor UI "
                f"panels, derived from the chapter plan's named template (see "
                f"the chapter plan's [sN] references for the template path)."
            )
            fr_n += 1
    lines.append(
        f"\n- **FR-{fr_n:03d}**: Every project listed above MUST load cleanly "
        f"in the GLP REPL via `dart run bin/glp_repl.dart` followed by "
        f"`load <project-dir>` and the play goal; any failure aborts acceptance "
        f"per Constitution Principle V (Test-First)."
    )
    return "\n".join(lines)


def _success_criteria(use_cases: list[UseCase]) -> str:
    plays = [uc.name.rstrip("/") for uc in use_cases]
    return (
        "### Measurable Outcomes\n\n"
        f"- **SC-001**: All {len(plays)} plays load cleanly in the GLP REPL: "
        f"{', '.join(plays)}.\n"
        f"- **SC-002**: Each play's `play_<name>` goal yields `→ succeeds` "
        f"or declared `→ suspended` per the chapter plan.\n"
        f"- **SC-003**: 100% of the protocol code in each play is traceable "
        f"to a specific `book p N §A.B[, Program N.N]` citation in the "
        f"Functional Requirements.\n"
        f"- **SC-004**: For plays with a declared Flutter entry point, "
        f"`flutter build` in `glp_multiagent/` succeeds.\n"
    )


def _key_entities(use_cases: list[UseCase]) -> str:
    if not use_cases:
        return ""
    out = ["### Key Entities\n"]
    for uc in use_cases:
        play_name = uc.name.rstrip("/")
        out.append(
            f"- **`{play_name}` play**: a multi-actor scenario with project "
            f"shape `{REQUIRED_PROJECT_FILES}`. Typed unions and message types "
            f"MUST be derived from the book's protocol description for this "
            f"play and declared in `self.glp`."
        )
    return "\n".join(out)


def _format_citations(blocks: Iterable[CodeBlock]) -> str:
    parts: list[str] = []
    for b in blocks:
        parts.append(format_book_pages_citation(b.book_pages, None, b.program_id))
    if not parts:
        return "see chapter plan source references"
    return "; ".join(parts)
