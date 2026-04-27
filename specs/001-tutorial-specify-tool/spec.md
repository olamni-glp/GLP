# Feature Specification: Tutorial-Specify Tool — Speckit Spec Generator for Olamni Tutorial Chapters

**Feature Branch**: `001-tutorial-specify-tool`
**Created**: 2026-04-27
**Status**: Draft
**Input**: User description: build a Python-encoded tool and skill wrapper `/tutorial-specify` that researches and rewrites each `chNN_plan.md` in `olamni/tutorial/` into a well-crafted speckit-compliant specification executable through the speckit toolchain (`/speckit-clarify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`); the spec MUST not prematurely design or implement, MUST keep the charter's tutorial file names and structure, MUST require source extraction from `GLP_ART.pdf` (never memory or training), MUST classify the chapter's tutorial mode (cohesive-synthesis / block-focused / multi-actor-distillation), MUST require GLP REPL testing per the charter, and the spec-building process MUST be resilient to host-session context compaction via continuous disk-checkpointing and resumability.
**Constitution**: `.specify/memory/constitution.md` v1.1.0 — Principle I (Spec-First) governs this spec. Generated downstream specs MUST inherit Principles V (Test-First, REPL + `dart test` + `flutter build` gates) and VI (Tutorial Charter Compliance). The tool itself is Python tooling per §Technology Stack.

## Clarifications

### Session 2026-04-27

- Q: Who assigns the tutorial mode (cohesive-synthesis / block-focused / multi-actor-distillation) for each chapter? → A: Pre-declared in `chNN_plan.md` as a header line (e.g., `**Mode**: multi-actor-distillation`); the tool reads it and never guesses.
- Q: What is the canonical citation format for `GLP_ART.pdf` references in generated specs? → A: Book pages with `§X.Y` section identifiers and `Program N.N` references where applicable (e.g., `book pp 37–40 §4.3`, `Program 1.1`); the tool maps book→PDF page numbers internally for extraction.
- Q: How should the tool handle deficiencies in `chNN_plan.md` (missing scope, missing files, inconsistencies)? → A: Abort the deficient chapter with a precise error; under `all`, continue with other chapters and emit a summary of skipped chapters at the end. The tool MUST NOT auto-amend, prompt interactively, or proceed with placeholders.
- Q: When invoked as `/tutorial-specify all`, does the tool process chapters sequentially or in parallel? → A: Sequential, deterministic order ch01 → ch13, one chapter at a time, single file lock at a time. No `--parallel` flag.
- Q: What fidelity guarantee must the tool give for code blocks extracted from `GLP_ART.pdf`? → A: Strong — every extracted code block MUST round-trip through the GLP REPL parser without error before the generated spec writes a citation to it; parse failure aborts the chapter with a precise error pointing to the offending block.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate a Single Chapter Spec (Priority: P1)

A tutorial author runs `/tutorial-specify ch04` and receives a generated `specs/<NNN>-tutorial-ch04/spec.md` that fully captures chapter 4's tutorial files (per `olamni/tutorial/ch01-04_plan.md`), their scope, the chapter's tutorial mode, explicit citations to relevant pages and Programs in `GLP_ART.pdf`, and a mandatory REPL-testing acceptance criterion.

**Why this priority**: This is the MVP — without working single-chapter generation, the tool delivers no value. All other capabilities depend on it.

**Independent Test**: Run `/tutorial-specify ch04`; open the generated spec; verify (a) it lists every file from `ch01-04_plan.md` for ch04, (b) every code-bearing requirement cites a specific `GLP_ART.pdf` page or Program, (c) it classifies the chapter's tutorial mode, (d) it has an explicit REPL acceptance test, (e) the spec passes spec-quality validation with ≤3 `[NEEDS CLARIFICATION]` markers.

**Acceptance Scenarios**:

1. **Given** `charter.md` and `ch01-04_plan.md` describing chapter 4's files, **When** `/tutorial-specify ch04` is invoked, **Then** `specs/<NNN>-tutorial-ch04/spec.md` is created listing each ch04 tutorial file with scope drawn from book §4.1–§4.4 with cited page numbers.
2. **Given** chapter 12 has §12.7 + §12.8 GLP implementation code, **When** `/tutorial-specify ch12` runs, **Then** the spec classifies ch12 as multi-actor-distillation mode and lists the three-participant Alice/Bob/Carol play as a required deliverable.
3. **Given** chapter 6 is only a TOC page in the book, **When** `/tutorial-specify ch06` runs, **Then** the spec follows the charter's directive to source material from elsewhere (`typed_book/`, §4.2 Buffered, §5.6 Quicksort, `naming-conventions.md` for equators) without fabricating book content.

### User Story 2 - End-to-End Spec → Implement Pipeline (Priority: P2)

The generated spec runs cleanly through the full speckit toolchain (`/speckit-clarify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`) without manual rework.

**Why this priority**: Validates that generated specs are not just well-formatted but executable. The tool's value is automation, not document generation.

**Independent Test**: Take the spec from US1, run `/speckit-clarify` (expect no spec rewrites). Run `/speckit-plan` (expect Constitution Check rows populated). Run `/speckit-tasks` (expect Phase 1 baseline-test task per Principle V). Run `/speckit-implement` (in dry-run if available; expect no missing-field errors).

**Acceptance Scenarios**:

1. **Given** a spec generated by `/tutorial-specify`, **When** `/speckit-plan` runs against it, **Then** the plan's Project Structure selects "Option C: Tutorial chapter (under charter)" and references the correct `olamni/tutorial/chNN/` paths.
2. **Given** a spec generated by `/tutorial-specify`, **When** `/speckit-tasks` runs, **Then** the task list includes a mandatory Phase 1 task to record the REPL + `dart test` baseline per Constitution Principle V.

### User Story 3 - Resilient Re-run After Context Compaction (Priority: P1)

While `/tutorial-specify ch12` is processing chapter 12 (which spans book pp 115–127 of `GLP_ART.pdf` and produces the multi-actor consensus play), the host Claude session undergoes context compaction. The user re-invokes `/tutorial-specify ch12 --resume`. The tool resumes from the latest disk-recorded checkpoint, completes the spec without re-doing work, and produces a spec byte-identical to what would have been produced had compaction never occurred.

**Why this priority**: Co-equal with US1 — context compaction is a real failure mode in long-running Claude tasks. Without resumability, output quality is non-deterministic and depends on how far into the work compaction strikes. Per the user's directive, this MUST be absolutely prevented.

**Independent Test**: Start `/tutorial-specify ch12`; mid-process, kill the host session (simulating compaction); restart with `--resume`; diff the resulting spec against a spec generated in a single uninterrupted run; verify byte-equality.

**Acceptance Scenarios**:

1. **Given** a partial run that wrote `specs/<NNN>-tutorial-ch12/.checkpoint.json` after extracting §12.3, **When** the tool is re-invoked with `--resume`, **Then** the tool reads the checkpoint, skips §12.3 extraction, and resumes from §12.4.
2. **Given** the tool is killed mid-write of `spec.md`, **When** the tool is re-invoked with `--resume`, **Then** `spec.md` is reconstructed atomically (no partial-write corruption) and matches the expected output.
3. **Given** an input `chNN_plan.md` has changed since the last checkpoint, **When** the tool is re-invoked with `--resume`, **Then** the tool detects the change via content-hash mismatch and either restarts from scratch (with `--restart`) or aborts with a clear error — partial state from a different input is never silently mixed with current work.

### Edge Cases

- **Chapter with no book content** (ch6, ch13): Tool MUST follow the charter's directive to source from alternative locations (`typed_book/`, `naming-conventions.md`, ch13 design notes). Tool MUST NOT fabricate book content.
- **Mid-extraction PDF read failure**: Tool MUST log the failure to the checkpoint and abort with a clear error; on `--resume`, retry from the failed step.
- **Charter or chNN_plan.md changes between runs**: Tool MUST detect input drift via content-hashing in the checkpoint and require explicit `--restart` rather than silently re-using stale checkpoints.
- **Concurrent invocations on the same chapter**: Tool MUST use a file lock on the spec directory to prevent corruption of shared state.
- **Disk full mid-checkpoint**: Tool MUST write checkpoints atomically (write-temp-then-rename); a failed write MUST leave the previous valid checkpoint intact.
- **`GLP_ART.pdf` missing or unreadable**: Tool MUST abort immediately with a clear error pointing to the configured PDF path. The tool MUST NOT fall back to memory or training as a substitute.

## Requirements *(mandatory)*

### Functional Requirements

#### Inputs and Source-of-Truth

- **FR-001**: The tool MUST read `olamni/tutorial/charter.md` and the per-chapter `chNN_plan.md`, `chNN-sources.md`, and `chNN_tutorial.md` files (or `ch01-04_plan.md` and `ch01-04-sources.md` for chs 1–4) and treat them as the authoritative scope inputs.
- **FR-002**: The tool MUST extract content for each chapter's referenced sections directly from `GLP_ART.pdf` at the project root. The tool MUST NOT use any model memory, training data, summary, or prior conversation as a substitute for fresh PDF extraction.
- **FR-003**: Each generated spec MUST cite, for every code-bearing requirement, the corresponding location in `GLP_ART.pdf` using the canonical format: book page numbers (printed at the bottom of each book page) plus section identifier `§X.Y` and Program identifier `Program N.N` where the book provides them. Example: `book pp 37–40 §4.3, Program 1.1`. The tool MUST map book→PDF page numbers internally for extraction; PDF page numbers MUST NOT appear in the generated spec.
- **FR-003a**: Before the generated spec writes any citation referencing an extracted code block, the tool MUST verify extraction fidelity by round-tripping that block through the GLP REPL parser (`dart run bin/glp_repl.dart` or equivalent) and confirming a clean parse. If the REPL reports a parse error, the tool MUST abort the chapter with a precise error identifying the offending book page, section, and block; the tool MUST NOT fall back to memory, training data, or best-effort heuristics to "fix" the extracted code.

#### Output Specification Quality

- **FR-004**: Each generated spec MUST be a speckit-compliant `spec.md` that the speckit toolchain (`/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`) processes without manual rework.
- **FR-005**: Each generated spec MUST preserve exactly the tutorial file names and directory structure designated by the charter and per-chapter plan; the spec MUST NOT propose alternative names, paths, or organisational structures.
- **FR-006**: Each generated spec MUST cover every tutorial file listed in the chapter plan, with a clear scope statement per file.
- **FR-007**: Each generated spec MUST classify the chapter's tutorial mode as one of:
  - **(a) cohesive-synthesis** — multiple short book code blocks woven into one tutorial file with narrative comments paraphrasing book prose. Typical of chapters with many small examples (ch 1, ch 3, early sections of ch 5).
  - **(b) block-focused** — each substantial Program in the book gets its own tutorial file. Typical of mid-book chapters where Programs are self-contained.
  - **(c) multi-actor-distillation** — the chapter's multi-process / multi-actor code is distilled into a project-shaped multi-actor play (`{self, agent, network, actors, boot}.glp` plus optional Flutter entry point). Typical of chs 8–12.

  The mode for each chapter MUST be pre-declared in the corresponding `chNN_plan.md` (or `ch01-04_plan.md` for chs 1–4) as a header line of the form `**Mode**: <cohesive-synthesis | block-focused | multi-actor-distillation>`. The tool MUST read this declaration and copy it into the generated spec; the tool MUST NOT infer, guess, or auto-classify the mode.
- **FR-007a**: If the relevant chapter plan lacks a `**Mode**:` declaration, the tool MUST abort with a clear error directing the author to add the declaration before re-running. The tool MUST NOT proceed with a default or inferred mode.
- **FR-007b**: Plan-deficiency handling — when `chNN_plan.md` has any deficiency (missing `**Mode**` per FR-007a; a file listed without a scope statement; a Mode-vs-files inconsistency such as `multi-actor-distillation` declared without a `boot.glp`; a charter-vs-plan disagreement), the tool MUST abort processing of that chapter with a precise error message identifying the deficiency. When invoked with `all`, the tool MUST continue processing other chapters and emit a final summary listing every chapter skipped and why. The tool MUST NOT auto-amend the plan, prompt the user interactively, or substitute placeholders / best-effort defaults.
- **FR-008**: Each generated spec MUST NOT prematurely design or implement: Functional Requirements MUST describe WHAT, not HOW; specific Dart/Python/Flutter library or function choices MUST be deferred to `/speckit-plan`.
- **FR-009**: Each generated spec MUST include an explicit Functional Requirement that downstream design and implementation MUST be based on `GLP_ART.pdf` in source — never memory, training data, or summary.
- **FR-010**: Each generated spec MUST include an explicit acceptance criterion that the resulting tutorial code is verified by loading and running it in the GLP REPL (`cd glp_runtime/bin; dart run glp_repl.dart`; load file or project; run goal; → succeeds or → suspended), per `olamni/tutorial/charter.md`.
- **FR-011**: Each generated spec MUST cite `olamni/tutorial/charter.md` and the relevant `chNN_plan.md`, `chNN-sources.md`, `chNN_tutorial.md` paths in its Assumptions section, satisfying Constitution Principle VI.

#### Skill Wrapper

- **FR-012**: The tool MUST be invocable as a Claude Code skill `/tutorial-specify` taking one positional argument — a chapter identifier (`ch01`, `ch02`, …, `ch13`) or `all` — and two optional flags: `--resume` and `--restart`. When the argument is `all`, the tool MUST process chapters sequentially in deterministic order (ch01 → ch13), one chapter at a time, holding a single file lock at a time. No parallel-execution flag is provided.
- **FR-013**: The skill wrapper MUST be located at `.claude/skills/tutorial-specify/` following Claude Code skill conventions.
- **FR-014**: The implementation language MUST be Python `^3.13` per Constitution §Technology Stack.

#### Resilience to Context Compaction

- **FR-015**: The spec-building process MUST run uninterrupted and unaffected by host-session context compaction. No in-memory state is required to make progress; all state required for resumption MUST be persisted to disk.
- **FR-016**: After every meaningful step (PDF extraction of a section, classification of tutorial mode, draft of a spec section, validation pass), the tool MUST write a checkpoint to `specs/<NNN>-tutorial-chNN/.checkpoint.json` capturing: the current step, completed steps, pending steps, content-hashes of all input files, and intermediate artefacts.
- **FR-017**: Checkpoints MUST be written atomically — write to a temporary file then rename — so that a crash mid-write leaves the previous valid checkpoint intact.
- **FR-018**: When re-invoked with `--resume`, the tool MUST read the latest valid checkpoint and resume processing at the next pending step. Completed steps MUST NOT be re-executed.
- **FR-019**: When re-invoked with `--resume`, the tool MUST verify that input file content-hashes match the hashes recorded in the checkpoint. If any input has changed, the tool MUST abort with a clear error advising the user to use `--restart` instead, never silently proceeding with mixed state.
- **FR-020**: Specification quality MUST be byte-identical between (a) a single uninterrupted run and (b) a run that experienced one or more compaction-induced restarts via `--resume`. The tool MUST NOT produce non-deterministic output for identical inputs.
- **FR-021**: The tool MUST hold a file lock on the spec directory while running, preventing concurrent runs from corrupting shared state.

#### Idempotence and Sync Impact

- **FR-022**: Re-running `/tutorial-specify chNN` on an unchanged chapter (no charter, plan, sources, tutorial, or PDF changes) MUST produce a spec byte-identical to the previous run.
- **FR-023**: Re-running on a chapter whose inputs have changed MUST produce a Sync Impact Report (HTML comment at top of `spec.md`) detailing what changed, comparable in format to the constitution's Sync Impact Report.

### Key Entities

- **Chapter Plan**: A per-chapter `chNN_plan.md` (or `ch01-04_plan.md`) describing the tutorial files to be built, their scope, demo goals, and acceptance criteria.
- **Chapter Sources**: A per-chapter `chNN-sources.md` listing the book pages, repository references, and supporting documents that supply material.
- **Chapter Tutorial**: A per-chapter `chNN_tutorial.md` containing the human-facing tutorial narrative.
- **Tutorial Charter**: `olamni/tutorial/charter.md` — the master document the generated spec MUST cite per Constitution Principle VI.
- **GLP_ART.pdf**: The book's PDF source at the project root; the mandatory authoritative reference for code-bearing content.
- **Generated Spec**: A speckit-compliant `spec.md` per chapter, under `specs/<NNN>-tutorial-chNN/spec.md`.
- **Checkpoint**: A JSON file at `specs/<NNN>-tutorial-chNN/.checkpoint.json` recording the current processing state, completed steps, pending steps, and input content-hashes for resumability.
- **Tutorial Mode Classification**: A label on each generated spec — one of `cohesive-synthesis`, `block-focused`, `multi-actor-distillation` — derived from the chapter's content shape per FR-007.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `/tutorial-specify ch04` produces a `spec.md` that passes the spec-quality checklist with at most 3 `[NEEDS CLARIFICATION]` markers.
- **SC-002**: A learner reading the corresponding chapter of `GLP_ART.pdf` alongside the generated tutorial finds 100% of tutorial code traceable to a specific book page or Program identifier.
- **SC-003**: All 13 chapter plans can be processed by the tool in under 15 minutes total wall-clock time on a typical developer laptop.
- **SC-004**: Re-running the tool on an unchanged chapter produces a `spec.md` byte-identical to the previous run.
- **SC-005**: A run interrupted at any point and resumed via `--resume` produces a `spec.md` byte-identical to an uninterrupted run.
- **SC-006**: Every generated spec, when piped into `/speckit-plan` and `/speckit-tasks`, produces a plan and task list that pass their own validation without manual editing.
- **SC-007**: 100% of code-bearing requirements in any generated spec cite `GLP_ART.pdf` using the canonical format `book pp X–Y §A.B[, Program N.N]` (book pages, never PDF pages).

## Assumptions

- `GLP_ART.pdf` is at the project root (`D:\bstdev\research\glp\glp\GLP_ART.pdf`) and contains the full Art of Grassroots Logic Programming book in textually-extractable form (suitable for standard Python PDF libraries).
- `olamni/tutorial/charter.md` is current and authoritative; per Constitution Principle VI, divergence is amended in the charter first.
- The 13 chapter plans live at `olamni/tutorial/ch01-04_plan.md` (chs 1–4 combined) and `olamni/tutorial/chNN/chNN_plan.md` (chs 5–13).
- Per Principle I (Spec-First), this specification is the source of truth for the tool's scope; later refinements proceed via `/speckit-clarify`.
- The Claude Code session running `/tutorial-specify` may experience context compaction at any point; the tool's state model assumes this and persists to disk continuously rather than relying on conversation memory.
