# Phase 1 Data Model: Tutorial-Specify Tool

**Date**: 2026-04-27
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

This file enumerates every entity the tool reads, writes, or carries in its checkpointed state, with field names, types, validation rules, lifecycle, and source-of-truth attribution.

## Entity Map

```text
                   reads (read-only)
   ┌─────────────────────────────────────────────────┐
   │                                                 │
   ▼                                                 │
Charter ──> ChapterPlan ──> ChapterSources           │
                │      └──> ChapterTutorial         │
                │                                    │
                ▼                                    │
        TutorialModeDecl ────────────┐               │
                                     ▼               │
                              ModeComposer ──> GeneratedSpec ──┐
                                     ▲                          │
                                     │                          ▼
                              CodeBlockExtraction ──> ReplParseResult
                                     ▲                          │
                                     │                          │
                                  GLPArtPdf                     │
                                                                │
                              Checkpoint ◄──── writes ──────────┘
                                     │
                                     ▼
                              FileLock (per spec dir)
```

## Inputs (read-only — tool MUST NOT modify)

### Charter

- **Path**: `olamni/tutorial/charter.md`
- **Authority**: Constitution Principle VI; the single source of truth for tutorial scope.
- **Fields the tool reads**:
  - `output_targets` (free text) — output dir + filename conventions for chs 1–6 vs. chs 7–13
  - `scope` (free text) — in/out of scope declarations
  - `design_principles` (numbered list) — unit of grouping rules per chapter group
  - `implementation_principles` (numbered list) — multi-agent template, REPL conventions, commit policy
  - `build_order` (free text) — chapter ordering
  - `notes_carried_forward` (bulleted list) — prior-clarify residue, e.g., ch6/ch13 design notes
- **Validation**:
  - File MUST exist; tool aborts otherwise.
  - Content-hash recorded in checkpoint; mismatch on `--resume` triggers FR-019 abort.

### ChapterPlan

- **Path**: `olamni/tutorial/ch01-04_plan.md` (chs 1–4) or `olamni/tutorial/chNN/chNN_plan.md` (chs 5–13).
- **Authority**: Per-chapter scope contract.
- **Fields the tool reads** (parsed line-by-line per Decision 6 in `research.md`):
  - `mode` (enum: `cohesive-synthesis` | `block-focused` | `multi-actor-distillation`) — read from `**Mode**:` header line. **MANDATORY**; absence → FR-007a abort.
  - `shared_block` (free text bullets) — common preamble (REPL invocation, conventions).
  - `files_or_use_cases` (list of records) — per-tutorial-file or per-use-case rows.
    - For chs 1–6: `{ path, scope, demo_goal }`.
    - For chs 7–13: `{ name, paths_under_chNN, scope, demo_play }`.
  - `acceptance` (list of strings) — chapter-level acceptance criteria.
- **Validation**:
  - `mode` MUST be one of the three enum values; other values → FR-007a abort.
  - `files_or_use_cases` MUST be non-empty.
  - For `multi-actor-distillation` mode, every use case MUST list paths including a `boot.glp`; missing → FR-007b abort.
  - For `block-focused` mode, every file MUST have a non-empty `scope` and `demo_goal`; missing → FR-007b abort.

### ChapterSources

- **Path**: `olamni/tutorial/ch01-04-sources.md` (chs 1–4) or `olamni/tutorial/chNN/chNN-sources.md` (chs 5–13).
- **Fields the tool reads**:
  - `numbered_sources` (list of records `{ id: int, citation: str }`) — `[s1]`, `[s2]`, …
- **Validation**:
  - File MUST exist; tool aborts otherwise.
  - `[sN]` references in the plan MUST resolve to entries here; unresolved → FR-007b abort.
  - At least one source MUST cite `GLP_ART.pdf` (book pages) for chapters whose mode requires book extraction. Exception: ch 13 (no book content per the charter's notes-carried-forward).

### ChapterTutorial

- **Path**: `olamni/tutorial/ch01/ch01_tutorial.md`, `olamni/tutorial/chNN/chNN_tutorial.md`, etc.
- **Fields the tool reads**:
  - `title` (string)
  - `prose_per_file` (dict `path -> paragraph`) — narrative the tool may paraphrase as inline `%%` comments in the implementation phase.
- **Validation**:
  - File MUST exist; tool aborts otherwise.

### GLPArtPdf

- **Path**: `GLP_ART.pdf` at the project root.
- **Authority**: Mandatory authoritative source for code-bearing content per FR-002 and FR-009.
- **Fields the tool reads**:
  - Per page: `{ pdf_page_number: int, book_page_number: int | None, text_layout: list, code_blocks: list }`
  - `book_page_to_pdf_page: dict[int, int]` — built once per PDF content-hash via Decision 5.
- **Validation**:
  - File MUST exist; absence → FR (edge case: GLP_ART.pdf missing) abort with clear error.
  - File MUST be PDF and parseable by `pdfplumber`; otherwise abort.

## Internal entities (computed)

### TutorialModeDecl

- **Type**: enum `cohesive-synthesis | block-focused | multi-actor-distillation`.
- **Source**: `ChapterPlan.mode`.
- **Lifecycle**: read at chapter start, never re-evaluated.
- **Validation**: see `ChapterPlan.mode` validation.

### CodeBlockExtraction

- **Fields**:
  - `block_id` (string) — stable per-PDF id (e.g., `ch04-pp37-block-01`).
  - `book_pages` (string) — citation form, e.g., `book pp 37–40 §4.3`.
  - `program_id` (string | None) — e.g., `Program 1.1` if the book labels it.
  - `text` (string) — the extracted code, indentation preserved.
  - `pdf_pages` (list of int) — internal use only; never appears in spec output (per FR-003).
  - `parse_status` (enum: `pending | passed | failed`) — set after `ReplParseResult`.
- **Validation**:
  - `text` MUST be non-empty.
  - `parse_status` MUST be `passed` before this block is allowed to appear in `GeneratedSpec`; otherwise FR-003a abort.

### ReplParseResult

- **Fields**:
  - `block_id` (string) — links back to `CodeBlockExtraction`.
  - `passed` (bool).
  - `repl_stdout` (string) — captured for the abort error message.
  - `repl_stderr` (string).
- **Lifecycle**: produced by Decision 3 subprocess; persisted in checkpoint per block.

### Checkpoint

- **Path**: `specs/<NNN>-tutorial-chNN/.checkpoint.json`.
- **Format**: JSON, schema published as `contracts/checkpoint-schema.json`.
- **Top-level fields**:
  - `schema_version` (string, semver of the checkpoint schema).
  - `chapter_id` (string, e.g., `ch04`).
  - `started_at` (ISO 8601 UTC string).
  - `last_updated_at` (ISO 8601 UTC string).
  - `inputs` (dict): each input file's path → SHA-256 content-hash (charter, plan, sources, tutorial, PDF).
  - `book_page_to_pdf_page` (dict, int → int) — Decision 5 map.
  - `tutorial_mode` (string enum).
  - `extracted_blocks` (list of `CodeBlockExtraction` records).
  - `repl_results` (list of `ReplParseResult` records).
  - `completed_steps` (ordered list of step names).
  - `pending_steps` (ordered list of step names).
  - `current_step` (string | None).
  - `terminated_with` (enum `null | success | aborted`) and `abort_reason` (string | None).
- **Validation**:
  - JSON Schema validation on read; malformed → abort with hint to use `--restart`.
  - Atomic write via temp + rename per Decision 4.

### GeneratedSpec

- **Path**: `specs/<NNN>-tutorial-chNN/spec.md`.
- **Format**: speckit-compliant markdown matching `.specify/templates/spec-template.md` v1.1.0.
- **Top-level fields**:
  - HTML-comment Sync Impact Report (FR-023) when re-running with changed inputs.
  - `## Clarifications` section (initially empty; downstream `/speckit-clarify` populates).
  - `## User Scenarios & Testing` (mandatory).
  - `## Requirements > Functional Requirements` — every code-bearing requirement carries a citation `book pp X–Y §A.B[, Program N.N]`.
  - `## Success Criteria > Measurable Outcomes` — at least one criterion is the REPL load-and-run goal from the chapter plan (FR-010).
  - `## Assumptions` — cites `olamni/tutorial/charter.md` and the relevant `chNN_plan.md`, `chNN-sources.md`, `chNN_tutorial.md` paths (FR-011).
- **Validation**:
  - Every code-bearing FR MUST cite `GLP_ART.pdf` per FR-003 format; tool refuses to write the file if any FR lacks a citation.
  - File written atomically (temp + rename).

### FileLock

- **Path**: `specs/<NNN>-tutorial-chNN/.lock`.
- **Lifecycle**: acquired at run start, held until the chapter completes (success or abort), released on process exit.
- **Validation**: if lock is already held, abort with a clear "another invocation is processing this chapter" error.

## Lifecycle / state transitions

```
   start
     │
     ▼
   acquire FileLock ──── if held by other run: ABORT (concurrency) ──┐
     │                                                                │
     ▼                                                                │
   load Charter, ChapterPlan, ChapterSources, ChapterTutorial         │
     │                                                                │
     ▼                                                                │
   parse TutorialModeDecl ──── missing/invalid: ABORT (FR-007a) ──────┤
     │                                                                │
     ▼                                                                │
   validate ChapterPlan ──── deficient: ABORT (FR-007b) ──────────────┤
     │                                                                │
     ▼                                                                │
   read or build book_page_to_pdf_page ──── PDF unreadable: ABORT ────┤
     │                                                                │
     ▼                                                                │
   for each book section in ChapterPlan:                              │
     ├─ extract CodeBlockExtraction(s)                                │
     ├─ for each block: ReplParseResult                               │
     │     └── failed: ABORT (FR-003a) ────────────────────────────────┤
     ├─ checkpoint after each block                                   │
     ▼                                                                │
   compose GeneratedSpec via mode composer                            │
     │                                                                │
     ▼                                                                │
   atomic write spec.md, mark checkpoint terminated_with=success      │
     │                                                                │
     ▼                                                                │
   release FileLock                                                   │
     │                                                                │
     ▼                                                                ▼
   exit 0                                                          exit 2 (abort)
```

`--resume` enters the diagram at the step recorded in `Checkpoint.current_step` after re-validating that all `inputs` content-hashes match.

`--restart` deletes `Checkpoint` (after confirming with the user via stderr) and starts from the top.
