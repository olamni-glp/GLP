"""Parse charter.md and per-chapter plan/sources/tutorial files.

Implements FR-001, FR-007a, FR-007b. Per /research.md Decision 6, this is a
targeted line-walker rather than a full Markdown parser, since the
chapter-plan shapes are deliberately simple and stable per the charter's
own design principles.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from tutorial_specify.errors import MissingModeError, PlanDeficiencyError
from tutorial_specify.modes import VALID_MODES


# Regexes
_MODE_LINE = re.compile(r"^\s*\*\*Mode\*\*\s*:\s*([a-z\-]+)\s*$")
_FILE_ROW = re.compile(r"^- ([^:]+\.glp)\s*:\s*(.+?)\.\s*$")
_USE_CASE_ROW = re.compile(r"^- ([a-z0-9\-]+/)\s*:\s*(.+?)\.\s*$")
_SOURCE_ROW = re.compile(r"^\s*(\d+)\.\s+(.*\S)\s*$")


@dataclass
class FileRow:
    """A single 'Files (code → test goal)' row from a chapter plan (chs 1–6)."""

    path: str  # relative to chNN/, e.g. ch04/ch-04-ex-01-...glp
    scope: str  # the right-hand side describing what the file does + demo goal


@dataclass
class UseCase:
    """A 'Use cases' entry from a chapter plan (chs 7–13)."""

    name: str  # e.g. "blocklace-consensus/"
    scope: str  # full description (often references multi-line content)
    file_paths: list[str] = field(default_factory=list)  # detected glp paths within


@dataclass
class ChapterPlan:
    """Parsed contents of `chNN_plan.md` (or `ch01-04_plan.md` for chs 1–4)."""

    path: Path
    chapter_id: str  # e.g. "ch04"
    mode: str  # one of VALID_MODES
    shared_block: list[str] = field(default_factory=list)
    files: list[FileRow] = field(default_factory=list)
    use_cases: list[UseCase] = field(default_factory=list)
    acceptance: list[str] = field(default_factory=list)
    raw: str = ""

    def chapter_files(self) -> list[str]:
        """All `.glp` paths declared in the plan, regardless of which list."""
        out = [f.path for f in self.files]
        for uc in self.use_cases:
            out.extend(uc.file_paths)
        return out


@dataclass
class ChapterSources:
    path: Path
    sources: list[tuple[int, str]]  # (id, citation) per `[sN]`


@dataclass
class ChapterTutorial:
    path: Path
    title: str
    raw: str  # whole markdown body for narrative paraphrasing later


@dataclass
class TutorialInputs:
    """Bundle of input files for a single chapter run."""

    charter: Path
    plan: Path
    sources: Path
    tutorial: Path

    def all(self) -> list[Path]:
        return [self.charter, self.plan, self.sources, self.tutorial]


def parse_chapter_plan(path: Path, chapter_id: str) -> ChapterPlan:
    """Parse the per-chapter plan file. Raises MissingModeError / PlanDeficiencyError."""
    if not path.exists():
        raise PlanDeficiencyError(f"chapter plan not found at {path}")

    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    mode: str | None = None
    section: str | None = None
    files: list[FileRow] = []
    use_cases: list[UseCase] = []
    shared_block: list[str] = []
    acceptance: list[str] = []

    for line in lines:
        m = _MODE_LINE.match(line)
        if m:
            mode = m.group(1).strip()
            continue

        if line.startswith("## "):
            heading = line[3:].strip().lower()
            if heading == "shared":
                section = "shared"
            elif heading.startswith("files"):
                section = "files"
            elif heading.startswith("use cases"):
                section = "use_cases"
            elif heading.startswith("acceptance") or heading.startswith("test"):
                section = "acceptance"
            else:
                section = None
            continue

        if section == "shared" and line.startswith("- "):
            shared_block.append(line[2:].strip())
        elif section == "files":
            mf = _FILE_ROW.match(line)
            if mf:
                files.append(FileRow(path=mf.group(1).strip(), scope=mf.group(2).strip()))
        elif section == "use_cases" and line.startswith("- "):
            mu = _USE_CASE_ROW.match(line)
            if mu:
                # name like "blocklace-consensus/", scope is everything after ':'
                use_cases.append(
                    UseCase(name=mu.group(1).strip(), scope=mu.group(2).strip())
                )
            elif use_cases:
                # continuation lines or detected file paths
                stripped = line.strip()
                if stripped:
                    use_cases[-1].scope += " " + stripped
        elif section == "acceptance" and line.startswith("- "):
            acceptance.append(line[2:].strip())

    if mode is None:
        raise MissingModeError(
            f"chapter plan {path} lacks the mandatory `**Mode**:` header. "
            f"Add a header line of the form: **Mode**: <cohesive-synthesis | "
            f"block-focused | multi-actor-distillation>"
        )
    if mode not in VALID_MODES:
        raise MissingModeError(
            f"chapter plan {path} has invalid mode {mode!r}; valid modes: "
            f"{sorted(VALID_MODES)}"
        )

    # Detect file paths embedded in use-case scopes (e.g., "{self,agent,network,actors,boot}.glp")
    for uc in use_cases:
        for path_match in re.findall(r"[a-z_][a-z0-9_/-]*\.glp", uc.scope):
            uc.file_paths.append(path_match)

    plan = ChapterPlan(
        path=path,
        chapter_id=chapter_id,
        mode=mode,
        shared_block=shared_block,
        files=files,
        use_cases=use_cases,
        acceptance=acceptance,
        raw=raw,
    )

    _validate_plan_consistency(plan)
    return plan


def _validate_plan_consistency(plan: ChapterPlan) -> None:
    """FR-007b: enforce mode-vs-files consistency and required scope statements."""
    if plan.mode == "multi-actor-distillation":
        if not plan.use_cases:
            raise PlanDeficiencyError(
                f"chapter plan {plan.path} declares Mode: multi-actor-distillation "
                f"but has no `## Use cases` section"
            )
        for uc in plan.use_cases:
            joined = " ".join(uc.file_paths)
            if "boot.glp" not in joined:
                raise PlanDeficiencyError(
                    f"chapter plan {plan.path}: use case {uc.name!r} declared under "
                    f"multi-actor-distillation mode but its file list does not include "
                    f"`boot.glp` — add boot.glp or change the declared Mode"
                )
    elif plan.mode in ("cohesive-synthesis", "block-focused"):
        if not plan.files:
            raise PlanDeficiencyError(
                f"chapter plan {plan.path} declares Mode: {plan.mode} but has no "
                f"`## Files` section with at least one `.glp` row"
            )
        for f in plan.files:
            if not f.scope.strip():
                raise PlanDeficiencyError(
                    f"chapter plan {plan.path}: file row {f.path!r} has an empty "
                    f"scope statement"
                )


def parse_chapter_sources(path: Path) -> ChapterSources:
    if not path.exists():
        raise PlanDeficiencyError(f"chapter sources not found at {path}")
    raw = path.read_text(encoding="utf-8")
    sources: list[tuple[int, str]] = []
    for line in raw.splitlines():
        m = _SOURCE_ROW.match(line)
        if m:
            sources.append((int(m.group(1)), m.group(2).strip()))
    return ChapterSources(path=path, sources=sources)


def parse_chapter_tutorial(path: Path) -> ChapterTutorial:
    if not path.exists():
        raise PlanDeficiencyError(f"chapter tutorial not found at {path}")
    raw = path.read_text(encoding="utf-8")
    title = next(
        (line[2:].strip() for line in raw.splitlines() if line.startswith("# ")),
        "(untitled)",
    )
    return ChapterTutorial(path=path, title=title, raw=raw)


def resolve_inputs(repo_root: Path, chapter_id: str) -> TutorialInputs:
    """Resolve the four input file paths for a chapter.

    chs 1–4 share `ch01-04_plan.md` and `ch01-04-sources.md` at the tutorial root.
    chs 5–13 use `chNN/chNN_plan.md`, `chNN/chNN-sources.md`, `chNN/chNN_tutorial.md`.
    """
    tutorial_dir = repo_root / "olamni" / "tutorial"
    charter = tutorial_dir / "charter.md"

    if chapter_id in {"ch01", "ch02", "ch03", "ch04"}:
        plan = tutorial_dir / "ch01-04_plan.md"
        sources = tutorial_dir / "ch01-04-sources.md"
        tutorial = tutorial_dir / chapter_id / f"{chapter_id}_tutorial.md"
    else:
        plan = tutorial_dir / chapter_id / f"{chapter_id}_plan.md"
        sources = tutorial_dir / chapter_id / f"{chapter_id}-sources.md"
        tutorial = tutorial_dir / chapter_id / f"{chapter_id}_tutorial.md"

    return TutorialInputs(charter=charter, plan=plan, sources=sources, tutorial=tutorial)
