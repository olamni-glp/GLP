<!--
SYNC IMPACT REPORT — post /speckit-analyze (2026-04-27)
- Q1 (branch model) → Constitution amended to v1.2.0; speckit feature branches
  `<NNN>-<short-name>` formally accepted alongside `claude/<name>-<session-id>`.
- Q2 (skill wrapper location) → Confirmed: `.claude/skills/tutorial-specify/`; no plan change.
- Q3 (chapter spec-dir numbering) → Confirmed sequential `<NNN>-tutorial-chNN/`; no plan change.
- Q4 (REPL parse-check granularity) → Confirmed extracted-blocks-only; no plan change.
- Q5 (Principle VI applicability) → Confirmed PASS verdict for this feature; no plan change.
- Q6 (test-fixture PDF) → tasks.md T003 amended: synthetic `glp_art_mock.tex` → `glp_art_mock.pdf`
  in place of a redacted `GLP_ART.pdf` excerpt; eliminates copyright exposure.
- Templates ⚠ pending alignment review: none triggered.
- Deferred TODOs: none.
-->

# Implementation Plan: Tutorial-Specify Tool — Speckit Spec Generator for Olamni Tutorial Chapters

**Branch**: `001-tutorial-specify-tool` | **Date**: 2026-04-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-tutorial-specify-tool/spec.md`

## Summary

Build a Python `^3.13` command-line tool plus its `/tutorial-specify` Claude Code skill wrapper that converts each `olamni/tutorial/chNN_plan.md` (or the combined `ch01-04_plan.md` for chs 1–4) into a speckit-compliant `spec.md` under `specs/<NNN>-tutorial-chNN/`. The tool extracts code-bearing content directly from `GLP_ART.pdf`, validates each extracted code block by round-tripping it through the GLP REPL parser, and writes specs that downstream `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement` commands consume without manual rework. The tool persists state to disk after every meaningful step so that host-session context compaction cannot corrupt or lose work — `--resume` reconstructs progress from the latest valid checkpoint and produces a spec byte-identical to an uninterrupted run. Tutorial-mode classification (`cohesive-synthesis` / `block-focused` / `multi-actor-distillation`) is read from a `**Mode**:` header in the chapter plan, never inferred. Page citations use book pages plus `§X.Y` and `Program N.N` identifiers. Plan-deficient chapters are aborted with a precise error and other chapters continue when `all` is invoked.

## Technical Context

**Language/Version**: Python `^3.13` (the tool itself, per Constitution §Technology Stack); invokes Dart `^3.9.4` via subprocess for GLP REPL parse-checks; reads `GLP_ART.pdf` as a binary input.
**Primary Dependencies**: `pdfplumber` (PDF text extraction with layout preservation), `filelock` (cross-platform file lock per FR-021), `pyyaml` (charter / chapter-plan front-matter parsing), Python stdlib `subprocess` (REPL invocation), `hashlib` (input content-hashing for FR-019), `json` (checkpoint atomic write per FR-017). Each dep MUST be added via `pyproject.toml` per Constitution §Technology Stack.
**Storage**: On-disk only. Output: `specs/<NNN>-tutorial-chNN/spec.md` (markdown). State: `specs/<NNN>-tutorial-chNN/.checkpoint.json` (JSON; atomic write-then-rename). Lock: `specs/<NNN>-tutorial-chNN/.lock`. No database, no in-memory state required for resumption.
**Testing**: `pytest` for the Python tool's unit + integration suite; integration tests run against fixture `chNN_plan.md` files plus a small fixture PDF (a redacted few pages of `GLP_ART.pdf`); plus an end-to-end smoke test that runs `tutorial-specify ch04` against the live chapter plan and a real `GLP_ART.pdf`. Per Constitution Principle V the unified REPL test suite (`bash test/run_all_tests.sh`) MUST also pass since the tool invokes the REPL. `flutter build` is N/A (no UI).
**Target Platform**: Windows, macOS, Linux desktop. Both Bash and PowerShell invocation per Constitution §Technology Stack parity rule. Python 3.13+ on each.
**Project Type**: Build/CI tooling (Python ^3.13) with a Claude Code skill wrapper. Constitution-stack Option D primarily; touches Option C (`olamni/tutorial/**`) only by reading, never writing.
**Performance Goals**: All 13 chapters processed under 15 min wall-clock (SC-003); per-chapter median under 2 min including REPL parse-check of every extracted block.
**Constraints**: FR-022 byte-identical idempotence (no nondeterministic output); FR-020 byte-identity across `--resume` paths; FR-021 file lock; FR-002 no memory/training fallback for code content; FR-009 every code-bearing requirement cites `GLP_ART.pdf`. The tool MUST NOT modify any input file (charter, chapter plans, PDF) — read-only on inputs; write-only on `specs/<NNN>-tutorial-chNN/**`.
**Scale/Scope**: 13 chapters; per-chapter plan ≤ 100 words narrative + ≤ 8 file/use-case rows; PDF ~140 pages, ≤ 1 MB; expected ~50 distinct code blocks per chapter on average; checkpoint JSON ≤ 200 KB.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.1.0.*

| Principle / Section | Verdict | Justification |
|---------------------|---------|---------------|
| **I. Spec-First Development (NON-NEGOTIABLE)** | PASS | Spec at `specs/001-tutorial-specify-tool/spec.md` exists, is current, and was clarified through 5 `/speckit-clarify` Q&As before this plan was written. |
| **II. No Workarounds** | PASS | Plan-deficiency policy aborts on first defect (spec FR-007a, FR-007b) — no try/catch-and-ignore, no expected-to-fail markings, no placeholder substitution. PDF extraction failures abort the chapter (spec FR-003a) — no memory fallback. |
| **III. SRSW Discipline (NON-NEGOTIABLE)** | N/A | Python tooling; no `.glp` code is authored by this feature. The tool merely invokes the REPL to parse-check extracted book code, which already conformed to SRSW when typeset by the author. |
| **IV. FCP Reference Architecture** | N/A | No heap, runtime, or bytecode VM work. The tool is pure I/O + PDF extraction + subprocess orchestration. |
| **V. Test-First Discipline** | PASS | Pytest unit tests + integration tests against fixture chapter plans MUST pass before declaring done. Baseline tests recorded BEFORE work begins (Phase-1 task in `tasks.md`). Bug fixes add regression tests; new FRs each get acceptance-test coverage. |
| **VI. Tutorial Charter Compliance** | PASS | The tool's *purpose* is to honour the charter. FR-001 reads the charter and plans as authoritative inputs; FR-005 forbids alternative file names or structures; FR-011 cites the charter and per-chapter sub-plans in the Assumptions of every generated spec. |
| **Language Design Authority** | N/A | No new guards, system predicates, body kernels, directives, or type-system features. |
| **Technology Stack** | PASS | Python `^3.13` and the listed deps (`pdfplumber`, `filelock`, `pyyaml`) are within the constitution-authorised stack; deps are declared in `pyproject.toml` per the rule "no ad-hoc dependencies". |

**Result**: All applicable principles PASS. No `Complexity Tracking` rows required.

## Project Structure

### Documentation (this feature)

```text
specs/001-tutorial-specify-tool/
├── spec.md                                # /speckit-specify output (clarified)
├── plan.md                                # this file (/speckit-plan output)
├── research.md                            # Phase 0 output
├── data-model.md                          # Phase 1 output
├── quickstart.md                          # Phase 1 output
├── contracts/
│   ├── cli-interface.md                   # CLI command contract
│   ├── spec-output-format.md              # generated spec.md structural contract
│   └── checkpoint-schema.json             # checkpoint JSON Schema (Draft 2020-12)
├── checklists/
│   └── requirements.md                    # /speckit-specify quality checklist
└── tasks.md                               # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
# Option D: Tooling (Python ^3.13) — selected
scripts/tutorial_specify/                  # Python tool implementation
├── pyproject.toml                         # Python ^3.13; pdfplumber, filelock, pyyaml deps
├── src/
│   └── tutorial_specify/
│       ├── __init__.py
│       ├── cli.py                         # entry point: argparse + chapter dispatch
│       ├── charter.py                     # parse charter.md and chNN_plan.md / sources / tutorial
│       ├── pdf_extract.py                 # pdfplumber wrappers; book↔PDF page mapping
│       ├── repl_parse.py                  # subprocess wrapper for GLP REPL parse-check (FR-003a)
│       ├── checkpoint.py                  # atomic write-then-rename; content-hash verify
│       ├── lock.py                        # filelock wrapper
│       ├── render_spec.py                 # build the speckit-compliant spec.md from extracted material
│       └── modes/                         # one module per tutorial mode classifier
│           ├── cohesive_synthesis.py
│           ├── block_focused.py
│           └── multi_actor_distillation.py
└── tests/
    ├── unit/                              # pytest unit tests
    │   ├── test_charter.py
    │   ├── test_pdf_extract.py
    │   ├── test_repl_parse.py
    │   ├── test_checkpoint.py
    │   ├── test_lock.py
    │   ├── test_render_spec.py
    │   └── test_modes.py
    ├── integration/                       # pytest integration tests
    │   ├── test_resume_byte_identical.py  # SC-005 / FR-020
    │   ├── test_idempotence.py            # SC-004 / FR-022
    │   ├── test_plan_deficiency_abort.py  # FR-007a, FR-007b
    │   └── test_pdf_fidelity_repl.py      # FR-003a
    └── fixtures/
        ├── ch_minimal_plan.md             # smallest valid plan
        ├── ch_missing_mode.md             # FR-007a abort fixture
        ├── ch_inconsistent.md             # FR-007b abort fixture
        └── glp_art_excerpt.pdf            # 4–6 pages of redacted GLP_ART.pdf for tests

# Skill wrapper (Claude Code skill convention) — selected
.claude/skills/tutorial-specify/
├── SKILL.md                               # skill spec consumed by Claude Code
└── scripts/
    ├── bash/
    │   └── run.sh                         # invokes scripts/tutorial_specify cli.py via python -m
    └── powershell/
        └── run.ps1                        # PowerShell parity per Constitution §Technology Stack

# Inputs (read-only)
olamni/tutorial/
├── charter.md
├── ch01-04_plan.md
├── ch01-04-sources.md
├── chNN/                                  # for chs 5–13
│   ├── chNN_plan.md
│   ├── chNN-sources.md
│   └── chNN_tutorial.md
GLP_ART.pdf                                # at repo root
```

**Structure Decision**: Option D (Python tooling at `scripts/tutorial_specify/`) is the primary location. The skill wrapper at `.claude/skills/tutorial-specify/` provides the `/tutorial-specify` slash command and shells out to the Python tool via bash/PowerShell parity scripts. Inputs at `olamni/tutorial/**` and `GLP_ART.pdf` are read-only; the tool's only writes are under `specs/<NNN>-tutorial-chNN/**`. This layout satisfies Constitution Principles I (Spec-First — spec drove every directory choice), V (Test-First — tests/ subtree planned alongside src/), VI (Tutorial Charter Compliance — charter + per-chapter plans are inputs, not edited), and §Technology Stack (Python ^3.13; bash + PowerShell parity).

## Complexity Tracking

> No Constitution violations. This section is intentionally empty.
