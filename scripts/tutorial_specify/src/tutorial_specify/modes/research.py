"""Mode research and interactive selection (spec FR-007, revised 2026-04-28).

When a chapter plan lacks a `**Mode**:` header, the CLI calls `suggest_mode`
to derive a recommended mode from the chapter plan structure plus PDF
evidence in the chapter's page range, then prompts the operator
interactively on stderr.

The previous design (FR-007a aborted on missing mode) was replaced after
the operator pointed out that /tutorial-specify is responsible for
extracting critical chapter detail from the PDF and suggesting it, not for
demanding the human do that work upfront.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass

from tutorial_specify.charter import ChapterPlan
from tutorial_specify.pdf_extract import PdfPage

_VALID_MODES = ("cohesive-synthesis", "block-focused", "multi-actor-distillation")

_CHAPTER_HEADING_RE = re.compile(r"^\s*Chapter\s+([0-9]+)\b", re.IGNORECASE)
_PROGRAM_LABEL_RE = re.compile(r"^\s*Program\s+([0-9]+(?:\.[0-9]+)?)\s*$")
_ACTOR_HINT_RE = re.compile(
    r"\b(agent\s*/\s*4|self\.glp|network\.glp|actors\.glp|boot\.glp)\b"
)


@dataclass
class ModeSuggestion:
    chapter_id: str
    mode: str
    evidence: list[str]


def _chapter_pdf_page_range(pages: list[PdfPage], chapter_num: int) -> tuple[int, int] | None:
    """Estimate the PDF page range of `chapter_num` by scanning for 'Chapter N' headings."""
    starts: dict[int, int] = {}
    for p in pages:
        for raw in (p.text or "").splitlines():
            m = _CHAPTER_HEADING_RE.match(raw.strip())
            if m:
                n = int(m.group(1))
                if n not in starts:
                    starts[n] = p.pdf_page
    if chapter_num not in starts:
        return None
    start = starts[chapter_num]
    next_starts = sorted(s for n, s in starts.items() if n > chapter_num)
    end = (next_starts[0] - 1) if next_starts else len(pages)
    return (start, end)


def _count_evidence_in_range(
    pages: list[PdfPage], pdf_range: tuple[int, int]
) -> tuple[int, int]:
    """Return (program_label_count, actor_hint_count) inside [lo, hi] PDF pages."""
    lo, hi = pdf_range
    program_count = 0
    actor_count = 0
    for p in pages:
        if not (lo <= p.pdf_page <= hi):
            continue
        text = p.text or ""
        for raw in text.splitlines():
            if _PROGRAM_LABEL_RE.match(raw.strip()):
                program_count += 1
        for _ in _ACTOR_HINT_RE.finditer(text):
            actor_count += 1
    return program_count, actor_count


def suggest_mode(plan: ChapterPlan, pages: list[PdfPage]) -> ModeSuggestion:
    """Derive a suggested mode from the plan structure and PDF evidence.

    Returns a `ModeSuggestion` with one of `_VALID_MODES` and an evidence
    list the caller renders to stderr.
    """
    evidence: list[str] = []

    # 1. Plan structural signal (proximate and authoritative when present).
    if plan.use_cases:
        evidence.append(
            f"plan has {len(plan.use_cases)} entries under `## Use cases` "
            f"(multi-actor project shape)"
        )
        plan_signal = "multi-actor-distillation"
    elif plan.files and len(plan.files) >= 4:
        evidence.append(
            f"plan lists {len(plan.files)} `.glp` files under `## Files` "
            f"(suggests multiple weave-into-one or multiple narrow Programs)"
        )
        plan_signal = "cohesive-synthesis"
    elif plan.files and len(plan.files) <= 3:
        evidence.append(
            f"plan lists {len(plan.files)} file(s) under `## File(s)` "
            f"(small file count typical of block-focused)"
        )
        plan_signal = "block-focused"
    else:
        evidence.append("plan has no `## Files` or `## Use cases` section")
        plan_signal = None

    # 2. PDF evidence in the chapter's estimated page range.
    chapter_num: int | None = None
    m = re.match(r"ch0*([0-9]+)$", plan.chapter_id)
    if m:
        chapter_num = int(m.group(1))
    pdf_range = _chapter_pdf_page_range(pages, chapter_num) if chapter_num else None
    if pdf_range is None:
        evidence.append(
            f"could not locate `Chapter {chapter_num}` heading in the PDF; "
            f"PDF-based evidence skipped"
        )
        program_count = 0
        actor_count = 0
    else:
        program_count, actor_count = _count_evidence_in_range(pages, pdf_range)
        evidence.append(
            f"PDF chapter range PDF pp {pdf_range[0]}–{pdf_range[1]}: "
            f"{program_count} `Program N.N` labels, {actor_count} multi-actor hints "
            f"(`agent/4`, `self.glp`, `network.glp`, `actors.glp`, `boot.glp`)"
        )

    # 3. Combine signals. Plan signal wins when present and consistent;
    # PDF can override when the plan is silent or the PDF strongly disagrees.
    if plan_signal is None:
        if actor_count > 0:
            mode = "multi-actor-distillation"
        elif program_count >= 6:
            mode = "cohesive-synthesis"
        else:
            mode = "block-focused"
    else:
        mode = plan_signal
        # If plan says block-focused but PDF chapter has many actor hints,
        # warn and prefer multi-actor-distillation.
        if plan_signal == "block-focused" and actor_count >= 5:
            evidence.append(
                f"PDF actor hints ({actor_count}) override plan signal "
                f"(`block-focused`); switching to `multi-actor-distillation`"
            )
            mode = "multi-actor-distillation"

    return ModeSuggestion(chapter_id=plan.chapter_id, mode=mode, evidence=evidence)


def prompt_for_mode(suggestion: ModeSuggestion) -> str:
    """Print the suggestion to stderr, read operator's decision from stdin.

    Returns the chosen mode (one of `_VALID_MODES`). Raises ValueError on
    an unrecognised reply.
    """
    sys.stderr.write(f"\n[{suggestion.chapter_id}] Mode classification\n")
    for line in suggestion.evidence:
        sys.stderr.write(f"  - {line}\n")
    sys.stderr.write(f"  Suggested mode: {suggestion.mode}\n")
    sys.stderr.write(
        "  Press Enter to accept, or type one of:\n"
        "    cohesive-synthesis | block-focused | multi-actor-distillation\n"
        "  > "
    )
    sys.stderr.flush()
    line = sys.stdin.readline()
    if line == "":  # EOF — non-interactive runs accept the suggestion
        sys.stderr.write(f"  (stdin closed; accepting {suggestion.mode})\n")
        return suggestion.mode
    answer = line.strip().lower()
    if answer == "":
        return suggestion.mode
    if answer in _VALID_MODES:
        return answer
    raise ValueError(
        f"unrecognised mode reply {answer!r}; expected one of {_VALID_MODES} "
        f"or empty line to accept the suggestion"
    )
