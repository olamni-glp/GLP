"""Tutorial-Specify CLI entry point.

Per `contracts/cli-interface.md`:

    /tutorial-specify <chapter> [--resume | --restart]

Where chapter is `ch01`..`ch13` or `all`.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from tutorial_specify.charter import (
    ChapterPlan,
    ChapterSources,
    ChapterTutorial,
    TutorialInputs,
    parse_chapter_plan,
    parse_chapter_sources,
    parse_chapter_tutorial,
    resolve_inputs,
)
from tutorial_specify.checkpoint import (
    Checkpoint,
    ExtractedBlock,
    ReplResult,
    checkpoint_path,
    hash_inputs,
    read_checkpoint,
    verify_inputs_unchanged,
    write_checkpoint,
)
from tutorial_specify.errors import (
    CheckpointMismatchError,
    ConcurrentInvocationError,
    InternalError,
    MissingModeError,
    PdfMissingError,
    PlanDeficiencyError,
    ReplParseError,
    TutorialSpecifyError,
    UserCancelledError,
)
from tutorial_specify.lock import acquire_spec_dir_lock
from tutorial_specify.pdf_extract import (
    CodeBlock,
    build_book_page_map,
    collect_code_blocks,
    extract_pages,
)
from tutorial_specify.render_spec import (
    render_spec,
    render_sync_impact_report,
    write_atomic,
)
from tutorial_specify.repl_parse import parse_block as repl_parse_block

CHAPTER_IDS = tuple(f"ch{n:02d}" for n in range(1, 14))


# ---------------- environment / paths ----------------


def discover_repo_root() -> Path:
    env = os.environ.get("TUTORIAL_SPECIFY_ROOT")
    if env:
        return Path(env).resolve()
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        return Path(out).resolve()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd().resolve()


def discover_pdf_path(repo_root: Path) -> Path:
    env = os.environ.get("TUTORIAL_SPECIFY_PDF")
    if env:
        return Path(env).resolve()
    return repo_root / "GLP_ART.pdf"


def discover_specs_dir(repo_root: Path) -> Path:
    return repo_root / "specs"


def find_or_assign_spec_dir(specs_dir: Path, chapter_id: str) -> Path:
    """Return the spec dir for this chapter; assign next sequential NNN if absent.

    Per Q3/A in /speckit-analyze: sequential numeric prefix.
    """
    suffix = f"-tutorial-{chapter_id}"
    if specs_dir.exists():
        for child in sorted(specs_dir.iterdir()):
            if child.is_dir() and child.name.endswith(suffix):
                return child
    next_num = _next_seq(specs_dir)
    return specs_dir / f"{next_num:03d}-tutorial-{chapter_id}"


def _next_seq(specs_dir: Path) -> int:
    if not specs_dir.exists():
        return 2  # 001 is the tool's own feature; chapters start at 002
    max_n = 1
    for child in specs_dir.iterdir():
        if not child.is_dir():
            continue
        m = re.match(r"^(\d{3,})-", child.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return max_n + 1


# ---------------- chapter pipeline ----------------


def process_chapter(
    chapter_id: str,
    repo_root: Path,
    *,
    resume: bool,
    restart: bool,
) -> int:
    """Process one chapter end-to-end. Returns CLI exit code."""
    if resume and restart:
        sys.stderr.write("error: --resume and --restart are mutually exclusive\n")
        return 2

    specs_dir = discover_specs_dir(repo_root)
    spec_dir = find_or_assign_spec_dir(specs_dir, chapter_id)
    spec_dir.mkdir(parents=True, exist_ok=True)

    inputs = resolve_inputs(repo_root, chapter_id)
    pdf_path = discover_pdf_path(repo_root)

    try:
        with acquire_spec_dir_lock(spec_dir):
            return _run_chapter(
                chapter_id=chapter_id,
                repo_root=repo_root,
                spec_dir=spec_dir,
                inputs=inputs,
                pdf_path=pdf_path,
                resume=resume,
                restart=restart,
            )
    except TutorialSpecifyError as exc:
        sys.stderr.write(f"[{chapter_id}] {exc}\n")
        return exc.exit_code


def _run_chapter(
    *,
    chapter_id: str,
    repo_root: Path,
    spec_dir: Path,
    inputs: TutorialInputs,
    pdf_path: Path,
    resume: bool,
    restart: bool,
) -> int:
    cp_path = checkpoint_path(spec_dir)
    existing = read_checkpoint(spec_dir)

    if existing and not resume and not restart:
        sys.stderr.write(
            f"error: existing checkpoint at {cp_path}; pass --resume to "
            f"continue or --restart to wipe and rerun\n"
        )
        return 2

    if restart:
        if not _confirm_restart(spec_dir):
            raise UserCancelledError("user cancelled --restart")
        if cp_path.exists():
            cp_path.unlink()
        existing = None

    # Compute current input hashes
    for inp in inputs.all():
        if not inp.exists():
            raise PlanDeficiencyError(
                f"required input file missing: {inp} (chapter {chapter_id})"
            )
    if not pdf_path.exists():
        raise PdfMissingError(
            f"GLP_ART.pdf not found at {pdf_path}; the tool MUST NOT fall back "
            f"to memory or training as a substitute"
        )

    current_hashes = hash_inputs(list(inputs.all()) + [pdf_path])

    if resume:
        if existing is None:
            raise CheckpointMismatchError(
                f"--resume requested but no checkpoint exists at {cp_path}; "
                f"omit --resume for a fresh run"
            )
        verify_inputs_unchanged(existing, current_hashes)
        cp = existing
        sys.stdout.write(f"[{chapter_id}] resuming from {cp.current_step or 'start'}\n")
    else:
        cp = Checkpoint(chapter_id=chapter_id)
        cp.inputs = current_hashes
        cp.pending_steps = [
            "parse_inputs",
            "extract_pdf",
            "extract_blocks",
            "repl_parse_blocks",
            "compose_spec",
            "write_spec",
        ]
        write_checkpoint(spec_dir, cp)

    # Step 1: parse inputs
    if "parse_inputs" not in cp.completed_steps:
        cp.current_step = "parse_inputs"
        write_checkpoint(spec_dir, cp)
        plan = parse_chapter_plan(inputs.plan, chapter_id)
        sources = parse_chapter_sources(inputs.sources)
        tutorial = parse_chapter_tutorial(inputs.tutorial)
        cp.tutorial_mode = plan.mode
        _advance(cp, "parse_inputs")
        write_checkpoint(spec_dir, cp)
    else:
        plan = parse_chapter_plan(inputs.plan, chapter_id)
        sources = parse_chapter_sources(inputs.sources)
        tutorial = parse_chapter_tutorial(inputs.tutorial)

    # Step 2: extract PDF pages + book→PDF page map
    if "extract_pdf" not in cp.completed_steps:
        cp.current_step = "extract_pdf"
        write_checkpoint(spec_dir, cp)
        pages = extract_pages(pdf_path)
        cp.book_page_to_pdf_page = build_book_page_map(pages)
        _advance(cp, "extract_pdf")
        write_checkpoint(spec_dir, cp)
    else:
        pages = extract_pages(pdf_path)

    # Step 3: collect code blocks for each declared file/use-case
    blocks_for_target: dict[str, list[CodeBlock]] = {}
    if "extract_blocks" not in cp.completed_steps:
        cp.current_step = "extract_blocks"
        write_checkpoint(spec_dir, cp)
        blocks_for_target = _collect_blocks_for_plan(pages, plan)
        cp.extracted_blocks = [
            ExtractedBlock(
                block_id=b.block_id,
                book_pages=_render_pages(b.book_pages),
                program_id=b.program_id,
                text=b.text,
                pdf_pages=list(b.pdf_pages),
                parse_status="pending",
            )
            for blocks in blocks_for_target.values()
            for b in blocks
        ]
        _advance(cp, "extract_blocks")
        write_checkpoint(spec_dir, cp)
    else:
        blocks_for_target = _collect_blocks_for_plan(pages, plan)

    # Step 4: REPL parse-check each block (FR-003a)
    if "repl_parse_blocks" not in cp.completed_steps:
        cp.current_step = "repl_parse_blocks"
        write_checkpoint(spec_dir, cp)
        for blocks in blocks_for_target.values():
            for b in blocks:
                outcome = repl_parse_block(b.block_id, b.text, repo_root)
                cp.repl_results.append(
                    ReplResult(
                        block_id=b.block_id,
                        passed=outcome.passed,
                        repl_stdout=outcome.stdout,
                        repl_stderr=outcome.stderr,
                    )
                )
                # Find matching ExtractedBlock and update parse_status
                for eb in cp.extracted_blocks:
                    if eb.block_id == b.block_id:
                        eb.parse_status = "passed" if outcome.passed else "failed"
                write_checkpoint(spec_dir, cp)
                if not outcome.passed:
                    raise ReplParseError(
                        block_id=b.block_id,
                        book_pages=_render_pages(b.book_pages),
                        repl_stderr=outcome.stderr,
                    )
        _advance(cp, "repl_parse_blocks")
        write_checkpoint(spec_dir, cp)

    # Step 5: compose the spec body
    if "compose_spec" not in cp.completed_steps:
        cp.current_step = "compose_spec"
        write_checkpoint(spec_dir, cp)

    sync_impact = _build_sync_impact(spec_dir, cp, current_hashes)

    body = render_spec(
        feature_dir_name=spec_dir.name,
        chapter_id=chapter_id,
        plan=plan,
        sources=sources,
        tutorial=tutorial,
        inputs=inputs,
        blocks_for_target=blocks_for_target,
        inputs_hashes=current_hashes,
        sync_impact_report=sync_impact,
    )
    if "compose_spec" not in cp.completed_steps:
        _advance(cp, "compose_spec")
        write_checkpoint(spec_dir, cp)

    # Step 6: write the spec atomically
    cp.current_step = "write_spec"
    write_checkpoint(spec_dir, cp)
    write_atomic(spec_dir / "spec.md", body)
    _advance(cp, "write_spec")
    cp.current_step = None
    cp.terminated_with = "success"
    write_checkpoint(spec_dir, cp)

    sys.stdout.write(f"[{chapter_id}] OK -> {spec_dir / 'spec.md'}\n")
    return 0


def _advance(cp: Checkpoint, step: str) -> None:
    if step not in cp.completed_steps:
        cp.completed_steps.append(step)
    if step in cp.pending_steps:
        cp.pending_steps.remove(step)


def _render_pages(pages: tuple[int, ...] | list[int]) -> str:
    if not pages:
        return "(no book page detected)"
    if len(pages) == 1:
        return f"book p {pages[0]}"
    return f"book pp {pages[0]}–{pages[-1]}"


def _collect_blocks_for_plan(
    pages, plan: ChapterPlan
) -> dict[str, list[CodeBlock]]:
    """Group code blocks per declared file path or use-case name.

    Initial implementation: collect all code blocks for the chapter and
    associate them with each declared target. Later refinements can use
    section-anchor heuristics from the chapter plan to partition more
    finely; the current shape preserves spec correctness (every target
    receives at least one citation pointing at the relevant book pages).
    """
    chapter_blocks = collect_code_blocks(pages, plan.chapter_id)

    out: dict[str, list[CodeBlock]] = {}
    targets: Iterable[str]
    if plan.mode == "multi-actor-distillation":
        targets = (uc.name for uc in plan.use_cases)
    else:
        targets = (f.path for f in plan.files)
    for t in targets:
        out[t] = chapter_blocks
    return out


def _confirm_restart(spec_dir: Path) -> bool:
    if os.environ.get("TUTORIAL_SPECIFY_FORCE") == "1":
        return True
    sys.stderr.write(
        f"--restart will delete the checkpoint at {spec_dir / '.checkpoint.json'} "
        f"and any partially-built spec.md. Type 'y' to proceed: "
    )
    sys.stderr.flush()
    answer = sys.stdin.readline().strip().lower()
    return answer == "y" or answer == "yes"


def _build_sync_impact(
    spec_dir: Path, cp: Checkpoint, current_hashes: dict[str, str]
) -> str | None:
    """Build a Sync Impact Report only if a previous spec exists with different inputs."""
    spec_path = spec_dir / "spec.md"
    if not spec_path.exists():
        return None
    if cp.inputs == current_hashes:
        return None
    return render_sync_impact_report(
        chapter_id=cp.chapter_id,
        old_hashes=cp.inputs,
        new_hashes=current_hashes,
    )


# ---------------- argparse glue ----------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tutorial-specify",
        description=(
            "Generate speckit-compliant specs from olamni/tutorial chapter plans, "
            "sourcing code-bearing content from GLP_ART.pdf."
        ),
    )
    p.add_argument(
        "chapter",
        choices=list(CHAPTER_IDS) + ["all"],
        help="Chapter id (ch01..ch13) or 'all' to process every chapter sequentially.",
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument("--resume", action="store_true", help="Resume from latest checkpoint.")
    g.add_argument("--restart", action="store_true", help="Wipe checkpoint and rerun.")
    p.add_argument("--version", action="version", version=_pkg_version())
    return p


def _pkg_version() -> str:
    from tutorial_specify import __version__
    return f"tutorial-specify {__version__}"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = discover_repo_root()

    if args.chapter == "all":
        skipped: list[str] = []
        ok: list[str] = []
        for ch in CHAPTER_IDS:
            rc = process_chapter(ch, repo_root, resume=args.resume, restart=args.restart)
            if rc == 0:
                ok.append(ch)
            else:
                skipped.append(ch)
        sys.stdout.write(
            f"\nsummary: {len(ok)} OK ({', '.join(ok) or 'none'}); "
            f"{len(skipped)} skipped/failed ({', '.join(skipped) or 'none'})\n"
        )
        return 0 if not skipped else 2

    return process_chapter(
        args.chapter, repo_root, resume=args.resume, restart=args.restart
    )


if __name__ == "__main__":
    raise SystemExit(main())
