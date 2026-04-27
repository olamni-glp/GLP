# Phase 0 Research: Tutorial-Specify Tool

**Date**: 2026-04-27
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This document records the research done to resolve every NEEDS CLARIFICATION in the Technical Context and to confirm the technology choices satisfy the constitutional Technology Stack and the spec's functional requirements. The five clarifications collected during `/speckit-clarify` (tutorial mode authority, citation format, plan-deficiency policy, `all` semantics, PDF-extraction fidelity) are already integrated into `spec.md` and are not duplicated here.

## Decision 1 — PDF text extraction library

- **Decision**: `pdfplumber` (Python).
- **Rationale**: `pdfplumber` (a layer over `pdfminer.six`) preserves layout columns and indentation when extracting text from TeX-generated PDFs, which `GLP_ART.pdf` is. It exposes per-page text with positional info, lets us identify code regions by font (TeX's `\texttt`/`\verbatim` blocks render in a monospace font that `pdfplumber` reports), and has a permissive licence. It is pure Python, install-only-dep, no native binary required — matches Constitution §Technology Stack "no ad-hoc dependencies" with a single declared addition.
- **Alternatives considered**:
  - `PyPDF2` / `pypdf` — simpler but mangles indentation and struggles with TeX ligatures (e.g., `--` rendered as `–`); would force a regex post-processing layer that adds non-deterministic risk to FR-022.
  - `pymupdf` / `fitz` — fast and accurate, but bundles native code (MuPDF) which complicates Bash + PowerShell parity setup.
  - `tika` (Apache Tika via Python wrapper) — heavyweight Java dependency violates constitution stack.
  - Shelling out to `pdftotext` (poppler-utils) — adds non-Python install burden on Windows.

## Decision 2 — Cross-platform file lock

- **Decision**: `filelock` (Python package).
- **Rationale**: Pure-Python, supports Windows + macOS + Linux without native binaries, well-maintained. Matches FR-021 "file lock on the spec directory while running" with a single declared dep.
- **Alternatives considered**:
  - `portalocker` — comparable, but `filelock` has a more idiomatic API and broader recent adoption.
  - Manual lockfile with `os.O_EXCL` — re-implementing platform quirks (Windows file-handle semantics differ from POSIX `flock`); rejected per Principle II (no workaround re-implementations of solved problems).

## Decision 3 — GLP REPL parse-check invocation (FR-003a)

- **Decision**: Subprocess `dart run bin/glp_repl.dart` from `glp_runtime/` with the extracted code block written to a temporary `.glp` file in a per-block scratch directory. The REPL's exit code + stderr/stdout are parsed for the load-success line (`✓ loaded` or equivalent) versus parse error.
- **Rationale**: Uses the constitutional "REPL is the unified GLP tool" requirement directly (Constitution §Workflow). No second parser is built; no GLP grammar is duplicated in Python. The REPL already exists in this repo and is the single source of truth for what is and isn't a syntactically valid GLP program.
- **Alternatives considered**:
  - Compile a Dart kernel snapshot of the REPL once, then invoke per block — faster but adds setup complexity; current per-invocation startup is ~1 s on a warm Dart cache, well within SC-003.
  - Build a Python GLP lexer — duplicates language definition; violates Principle IV (FCP/REPL is reference architecture for GLP code) by introducing a second authority on what parses.
  - Skip parse-check (best-effort) — directly contradicts the user's "never memory or training" mandate and the FR-003a clarification (Q5: Option A).

## Decision 4 — Checkpoint format and atomicity (FR-016, FR-017)

- **Decision**: JSON file at `specs/<NNN>-tutorial-chNN/.checkpoint.json`, written via the standard atomic pattern: write to `.checkpoint.json.tmp` in the same directory, fsync, then `os.replace()` to the target name. JSON Schema is published as `contracts/checkpoint-schema.json`.
- **Rationale**: JSON is human-readable for debugging, the schema is enforceable via `jsonschema`, and `os.replace()` is atomic on Windows + POSIX (Python 3.3+ guarantee). Matches FR-017 "write-temp-then-rename" requirement.
- **Alternatives considered**:
  - SQLite for state — too heavy for a single-writer per-chapter checkpoint; harder to inspect; pulls in DB-management concerns.
  - Per-step files (e.g., `.checkpoint/step-001.json`) — multiplies file count; harder to atomically advance the head pointer; rejected.

## Decision 5 — Book → PDF page-number mapping (FR-003)

- **Decision**: Two-pass extraction. **Pass 1** scans every PDF page once, reads the page-footer book-page number (visible at bottom of each page in `GLP_ART.pdf`), and builds a `book_page → pdf_page` map persisted in the checkpoint. **Pass 2** consults that map for every citation. The map is recomputed only when the PDF's content-hash changes between runs.
- **Rationale**: The mapping is intrinsic to the PDF (front-matter offset shifts the alignment by ≈ 12 pages in the current `GLP_ART.pdf`) and may shift again if the book is re-typeset. Recomputing once per PDF version is cheap. Storing the map in the checkpoint keeps FR-022 idempotence (same PDF → same map → same citations).
- **Alternatives considered**:
  - Hard-coded constant offset — brittle; a future book revision with new front-matter pages silently corrupts every citation.
  - Use only PDF page numbers in citations — rejected by Q2 clarification (Option A: book pages).

## Decision 6 — Charter / chapter-plan parsing

- **Decision**: Markdown parsed line-by-line for the well-defined structures we care about (the `**Mode**:` header, the `## Files` block listing tutorial files, the `## Use cases` block for chs 7–13, the `[sN]` source citations). No full Markdown AST. The known shapes are stable per the charter; a structural parser keeps the surface small.
- **Rationale**: The charter and per-chapter plans are deliberately ≤ 100 words of action lines (per the charter's own design principles). A full Markdown parser is overkill and introduces new dependency and ambiguity surface. Targeted regex/line-walker is sufficient and easier to test.
- **Alternatives considered**:
  - `markdown-it-py` AST — more general but adds a dep and forces us to traverse a large tree to extract a few headers.
  - YAML front-matter only — would require restructuring every existing chapter plan; violates Principle VI (charter is authoritative; tools accommodate).

## Decision 7 — Skill wrapper interface (FR-012, FR-013)

- **Decision**: `.claude/skills/tutorial-specify/SKILL.md` declares the slash command. Bash and PowerShell scripts under `.claude/skills/tutorial-specify/scripts/{bash,powershell}/` invoke `python -m tutorial_specify.cli` with passthrough arguments. Argument set: positional `{ch01..ch13|all}`, optional `--resume`, optional `--restart`. The Python module discovers the repo root via `git rev-parse --show-toplevel` (or via env override `TUTORIAL_SPECIFY_ROOT` for tests).
- **Rationale**: Matches the existing `.specify/extensions/git/` skill-extension pattern (bash + PowerShell parity). Keeps Python self-contained at `scripts/tutorial_specify/` so the skill is a thin shim. Per-platform script parity is required by Constitution §Technology Stack.
- **Alternatives considered**:
  - Pure Python skill with no bash/ps1 — current Claude Code conventions favour shell entry points for portability and shell-quoting predictability.
  - Single-file skill — fine for tiny skills but this tool has substantial logic; separation of concerns (skill spec vs. tool code) is clearer.

## Decision 8 — Tutorial mode classifier modules (FR-007 / FR-007a)

- **Decision**: One Python module per tutorial mode under `src/tutorial_specify/modes/`:
  - `cohesive_synthesis.py` — composer that weaves multiple short book code blocks into FR text grouped by section, with narrative-paraphrasing comments referenced from `chNN_tutorial.md`.
  - `block_focused.py` — composer that emits one File-section per substantial book Program; FR per file lists exactly the demo goal from the chapter plan.
  - `multi_actor_distillation.py` — composer that generates the `{self, agent, network, actors, boot}.glp` project shape's expectations as FRs and demands a Flutter entry point if the chapter plan declares one.
- **Rationale**: Each mode's spec output structure differs enough that a single composer with branches would obscure the shape; per-mode modules keep the specification of what *that mode* produces close to its code. The composer is selected via the `**Mode**:` header (Q1 clarification).
- **Alternatives considered**:
  - Single composer with mode-conditional branches — harder to test the per-mode FR-output shape; rejected for clarity.
  - Mode-templates as Jinja2 files — adds Jinja dep; current scale doesn't justify; revisit if mode count grows.

## Decision 9 — Idempotence and Sync Impact Report (FR-022, FR-023)

- **Decision**: Idempotence is achieved by (a) sorting all set/dict iterations before serialisation, (b) using a fixed timezone (UTC) for any embedded timestamps, (c) using a deterministic hash of inputs as the sole non-content-derived field. The Sync Impact Report (FR-023) compares the previous spec's content-hash (recorded in the checkpoint) against the current run's; if different, the tool prepends an HTML comment listing changed inputs (charter / plan / sources / tutorial / PDF) with their old vs. new content-hashes.
- **Rationale**: This matches the constitution's own Sync Impact Report format (HTML comment at top of file) and the spec's FR-023 wording. UTC + sorted iteration gives byte-identity (FR-022) without per-system clock skew.
- **Alternatives considered**:
  - Per-run timestamp embedded in spec — defeats FR-022; rejected.
  - Externalised report file — splits the audit trail; HTML comment colocated with content is the spec-kit convention.

## Open NEEDS CLARIFICATION

None. All Technical Context fields are filled with concrete values; the five spec-level ambiguities were resolved in `/speckit-clarify`.
