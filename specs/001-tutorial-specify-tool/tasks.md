---
description: "Task list for Tutorial-Specify Tool implementation"
---

# Tasks: Tutorial-Specify Tool — Speckit Spec Generator for Olamni Tutorial Chapters

**Input**: Design documents from `specs/001-tutorial-specify-tool/`
**Prerequisites**: [plan.md](plan.md) (required), [spec.md](spec.md) (required for user stories), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/)
**Constitution**: [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md) v1.1.0. Phase 1 (Setup) MUST include a baseline test run per Principle V (Test-First). The tool invokes the GLP REPL for code-block parse-checks (FR-003a), so the unified REPL test suite MUST be in the baseline. Tasks under `olamni/tutorial/**` are read-only per FR (CLI contract); per Principle VI the charter is cited but not edited.

**Tests**: MANDATORY per Constitution Principle V — every bug fix MUST add a regression test, every functional requirement MUST have at least one acceptance-test mapping. Tests MUST NOT be deleted or marked expected-to-fail to silence a defect.

**Organization**: Tasks are grouped by user story (US1, US2, US3) so each story can be implemented, tested, and demonstrated independently. P1 stories first.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Maps task to user story (US1 / US2 / US3)
- File paths are relative to repo root unless absolute

## Path Conventions

- Tool code: `scripts/tutorial_specify/src/tutorial_specify/`
- Tool tests: `scripts/tutorial_specify/tests/`
- Skill wrapper: `.claude/skills/tutorial-specify/`
- Inputs (read-only): `olamni/tutorial/**`, `GLP_ART.pdf`
- Outputs: `specs/<NNN>-tutorial-chNN/**`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project scaffolding and baseline test recording.

- [ ] T001 Initialize Python package at `scripts/tutorial_specify/pyproject.toml` (name=`tutorial-specify`, requires-python=`>=3.13`, deps: `pdfplumber`, `filelock`, `pyyaml`, `jsonschema`); create `src/tutorial_specify/__init__.py` and `tests/` directory structure
- [ ] T002 [P] Create skill wrapper scaffolding: `.claude/skills/tutorial-specify/SKILL.md` (declares slash command per `contracts/cli-interface.md`); placeholder run scripts at `scripts/bash/run.sh` and `scripts/powershell/run.ps1` (just print "TODO" for now)
- [ ] T003 [P] Create test fixtures under `scripts/tutorial_specify/tests/fixtures/`:
  - `ch_minimal_plan.md` (smallest valid chapter plan with `**Mode**: block-focused`, one file row, one source ref)
  - `ch_missing_mode.md` (FR-007a abort fixture)
  - `ch_inconsistent.md` (FR-007b abort fixture: declares `multi-actor-distillation` mode but no `boot.glp` in file list)
  - `glp_art_mock.tex` plus a tiny build script (`build_mock_pdf.sh` / `.ps1`) that compiles it to `glp_art_mock.pdf` — a synthetic 4–6-page PDF containing TeX-typeset GLP-shaped code blocks in the same monospace-font conventions as the real book, with no actual book content. Per /speckit-analyze Q6/A: avoids any copyright exposure and gives reproducible test data the tool can extract from end-to-end.
- [ ] T004 Record Constitution Principle V baseline tests:
  - `bash test/run_all_tests.sh > /tmp/repl-baseline.txt 2>&1`
  - `cd glp_runtime && dart test > /tmp/dart-baseline.txt 2>&1 && cd ..`
  - `cd scripts/tutorial_specify && python -m pip install -e . && python -m pytest --collect-only > /tmp/pytest-baseline.txt 2>&1 && cd ../..`
  - Capture pass counts; subsequent task completions MUST not regress these numbers

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core modules every user story depends on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T005 [P] Implement `src/tutorial_specify/lock.py` — `filelock` wrapper class with context-manager API; per-spec-dir lock file `specs/<NNN>-tutorial-chNN/.lock`; raises a typed `ConcurrentInvocationError` on contention (FR-021)
- [ ] T006 [P] Implement `src/tutorial_specify/checkpoint.py` — atomic write-then-rename via `os.replace()`; SHA-256 input content-hashing; load + validate against `contracts/checkpoint-schema.json` via `jsonschema`; resume-mismatch detection (FR-016, FR-017, FR-019)
- [ ] T007 [P] Implement `src/tutorial_specify/charter.py` — line-walker parsers for `charter.md`, `chNN_plan.md` / `ch01-04_plan.md`, `chNN-sources.md`, `chNN_tutorial.md`; extracts `**Mode**:` header, file/use-case rows, `[sN]` source references; raises `MissingModeError` (FR-007a) and `PlanDeficiencyError` (FR-007b) with precise messages
- [ ] T008 [P] Implement `src/tutorial_specify/pdf_extract.py` — `pdfplumber` wrapper that opens `GLP_ART.pdf`, builds book→PDF page map (Decision 5), extracts code blocks identified by monospace font, preserves indentation; refuses to operate without a configured PDF path (FR-002, FR-003)
- [ ] T009 Implement `src/tutorial_specify/repl_parse.py` — subprocess wrapper that writes a code block to a temp `.glp`, runs `dart run bin/glp_repl.dart` with a `load <temp>` script, captures stdout/stderr + exit code, returns `ReplParseResult` per `data-model.md`; honours `TUTORIAL_SPECIFY_REPL_TIMEOUT_S` (FR-003a). Depends on T005–T008 only for shared types

**Checkpoint**: Foundation ready — all three user stories can now build on `lock`, `checkpoint`, `charter`, `pdf_extract`, `repl_parse`.

---

## Phase 3: User Story 1 - Generate a Single Chapter Spec (Priority: P1) 🎯 MVP

**Goal**: `/tutorial-specify ch04` produces a spec passing the spec-quality checklist with ≤3 `[NEEDS CLARIFICATION]` markers, citing `GLP_ART.pdf` book pages, classifying tutorial mode from the plan header, and aborting on plan deficiencies.

**Independent Test**: Run `/tutorial-specify ch04`; open the generated spec; verify file list matches `ch01-04_plan.md` for ch04, every code-bearing requirement cites a book page or Program, mode classification matches the plan's `**Mode**:` header, and a REPL acceptance test is present.

### Tests for User Story 1

> Write these tests FIRST; ensure they FAIL before implementation lands.

- [ ] T010 [P] [US1] Unit test `scripts/tutorial_specify/tests/unit/test_charter.py` — parses `ch_minimal_plan.md` correctly; raises `MissingModeError` on `ch_missing_mode.md`; raises `PlanDeficiencyError` on `ch_inconsistent.md`
- [ ] T011 [P] [US1] Unit test `scripts/tutorial_specify/tests/unit/test_pdf_extract.py` — opens `glp_art_excerpt.pdf`; book→PDF map correct on the excerpt; extracts at least one code block with indentation preserved
- [ ] T012 [P] [US1] Unit test `scripts/tutorial_specify/tests/unit/test_repl_parse.py` — known-good `.glp` snippet returns `passed=True`; deliberately mangled snippet returns `passed=False` with non-empty `repl_stderr`
- [ ] T013 [P] [US1] Unit test `scripts/tutorial_specify/tests/unit/test_render_spec.py` — every code-bearing FR ends with `(book pp X–Y §A.B[, Program N.N])`; PDF page numbers do NOT appear; section order matches `contracts/spec-output-format.md`
- [ ] T014 [P] [US1] Unit test `scripts/tutorial_specify/tests/unit/test_modes.py` — each composer (`cohesive_synthesis`, `block_focused`, `multi_actor_distillation`) emits its mode-specific shape per `contracts/spec-output-format.md` § "Per-mode shape"
- [ ] T015 [US1] Integration test `scripts/tutorial_specify/tests/integration/test_plan_deficiency_abort.py` — runs the tool against `ch_missing_mode` and `ch_inconsistent` fixtures via subprocess; asserts exit 2 and that stderr contains the precise file path and deficiency description (FR-007a, FR-007b)
- [ ] T016 [US1] Integration test `scripts/tutorial_specify/tests/integration/test_pdf_fidelity_repl.py` — runs the tool against a fixture chapter referencing a deliberately-mangled code-block region; asserts exit 2 and REPL parse failure surfaced in stderr (FR-003a)

### Implementation for User Story 1

- [ ] T017 [P] [US1] Implement `src/tutorial_specify/render_spec.py` — assembles markdown per `contracts/spec-output-format.md`: header, Clarifications stub, User Scenarios from chapter plan, Functional Requirements with citations, Success Criteria including REPL load+goal (FR-010), Assumptions citing charter + per-chapter plan files (FR-011); refuses to write any FR lacking a citation (FR-003)
- [ ] T018 [P] [US1] Implement `src/tutorial_specify/modes/cohesive_synthesis.py` — emits one P1 user story per chapter; FRs grouped by book §; one tutorial file enumerated
- [ ] T019 [P] [US1] Implement `src/tutorial_specify/modes/block_focused.py` — emits one user story per book Program; one FR per file; demo goal per file
- [ ] T020 [P] [US1] Implement `src/tutorial_specify/modes/multi_actor_distillation.py` — emits one user story per use case; Key Entities section enumerates typed unions; project-shape FRs require `{self,agent,network,actors,boot}.glp`; if plan declares Flutter entry, an FR requires `glp_multiagent/lib/main_olamni_chNN_<use-case>.dart`
- [ ] T021 [US1] Implement `src/tutorial_specify/cli.py` happy-path (no `--resume` yet) — argparse for positional chapter + `--resume`/`--restart`; resolves `<NNN>-tutorial-chNN` directory (sequential prefix from existing `specs/`); acquires `FileLock`; loads inputs via `charter`; selects mode composer per `**Mode**:`; iterates book-section-by-book-section through `pdf_extract` → `repl_parse`; calls composer; writes `spec.md` atomically; depends on T005–T009 and T017–T020
- [ ] T022 [US1] Implement skill wrapper bash script `.claude/skills/tutorial-specify/scripts/bash/run.sh` — invokes `python -m tutorial_specify "$@"`; sets `TUTORIAL_SPECIFY_ROOT` to `git rev-parse --show-toplevel`; passes through exit code (FR-012, FR-013)
- [ ] T023 [US1] Implement skill wrapper PowerShell script `.claude/skills/tutorial-specify/scripts/powershell/run.ps1` — PowerShell parity per Constitution §Technology Stack
- [ ] T024 [US1] Author `SKILL.md` — declares `/tutorial-specify` slash command, argument schema, exit code semantics; references `contracts/cli-interface.md` as the authoritative contract

**Checkpoint**: User Story 1 fully functional — generates a spec for any single chapter with valid plan; aborts cleanly on deficiencies; cites book pages; passes REPL parse-check on every extracted block.

---

## Phase 4: User Story 3 - Resilient Re-run After Context Compaction (Priority: P1)

**Goal**: `/tutorial-specify ch12 --resume` after host compaction completes the run from the last checkpoint; output is byte-identical to a single uninterrupted run.

**Independent Test**: Start `/tutorial-specify ch12`; kill mid-process; rerun with `--resume`; diff resulting spec.md against a fresh full run; assert byte-identical (FR-020 / SC-005).

### Tests for User Story 3

- [ ] T025 [P] [US3] Unit test `scripts/tutorial_specify/tests/unit/test_checkpoint.py` — atomic write survives simulated crash mid-write (truncate `.tmp` after first half); resume reads latest valid checkpoint; rejects checkpoint with mismatched input content-hashes (FR-019)
- [ ] T026 [P] [US3] Unit test `scripts/tutorial_specify/tests/unit/test_lock.py` — first acquisition succeeds; second acquisition while first held raises `ConcurrentInvocationError` (FR-021); release on context exit; stale-lock detection only when lock-PID is dead
- [ ] T027 [US3] Integration test `scripts/tutorial_specify/tests/integration/test_resume_byte_identical.py` — runs the tool on a fixture chapter; SIGKILLs after second checkpoint; restarts with `--resume`; produces final `spec.md`; runs the same chapter cleanly to a fresh dir; asserts both `spec.md` files are byte-identical (FR-020 / SC-005)
- [ ] T028 [US3] Integration test `scripts/tutorial_specify/tests/integration/test_idempotence.py` — runs the tool twice on an unchanged fixture chapter; asserts both `spec.md` files are byte-identical (FR-022 / SC-004)

### Implementation for User Story 3

- [ ] T029 [US3] Wire `Checkpoint` writes into `cli.py` after every meaningful step: input loaded → checkpoint; book→PDF map built → checkpoint; each block extracted → checkpoint; each `repl_parse` result → checkpoint; spec composed → checkpoint; spec written → terminate (FR-016)
- [ ] T030 [US3] Implement `--resume` flag in `cli.py` — load `.checkpoint.json`; validate schema; verify input hashes match (FR-019); replay from `current_step`; abort with `--restart` hint on mismatch
- [ ] T031 [US3] Implement `--restart` flag in `cli.py` — interactive `y/N` prompt on stderr unless `TUTORIAL_SPECIFY_FORCE=1`; on confirm, delete `.checkpoint.json` and proceed from scratch; mutually exclusive with `--resume` (CLI contract)
- [ ] T032 [US3] Implement Sync Impact Report header generation in `render_spec.py` — when an existing `spec.md` is being overwritten and prior input hashes (recorded in last checkpoint) differ from current, prepend an HTML comment listing changed inputs old→new content-hashes (FR-023)

**Checkpoint**: User Story 3 fully functional — context compaction cannot corrupt or lose work; idempotent runs produce byte-identical output.

---

## Phase 5: User Story 2 - End-to-End Toolchain Pipeline (Priority: P2)

**Goal**: A spec generated by `/tutorial-specify` runs cleanly through `/speckit-clarify` → `/speckit-plan` → `/speckit-tasks` without manual rework.

**Independent Test**: Generate `specs/<NNN>-tutorial-ch04/spec.md`; pipe it through each downstream speckit command; assert no spec rewrites required.

### Tests for User Story 2

- [ ] T033 [P] [US2] Integration test `scripts/tutorial_specify/tests/integration/test_pipeline_clarify.py` — runs `/speckit-clarify` against a generated ch04 spec; asserts no `[NEEDS CLARIFICATION]` count > 0 and no spec-quality checklist failures
- [ ] T034 [P] [US2] Integration test `scripts/tutorial_specify/tests/integration/test_pipeline_plan.py` — runs `/speckit-plan`; asserts the resulting `plan.md` selects "Option C: Tutorial chapter (under charter)" and references the correct `olamni/tutorial/chNN/` paths
- [ ] T035 [P] [US2] Integration test `scripts/tutorial_specify/tests/integration/test_pipeline_tasks.py` — runs `/speckit-tasks`; asserts the task list includes a Phase 1 baseline-test task (`bash test/run_all_tests.sh` and `dart test`) per Constitution Principle V

### Implementation for User Story 2

- [ ] T036 [US2] No new code expected — the spec output contract from US1 is designed for downstream consumption. Tests T033–T035 validate that promise. If any test fails, fix `render_spec.py` and the relevant mode composer (NOT the speckit tools).

**Checkpoint**: User Story 2 fully functional — generated specs are first-class inputs to the rest of the speckit toolchain.

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T037 [P] Documentation: `scripts/tutorial_specify/README.md` summarising the tool's purpose, install steps, and pointer to the spec/plan/contracts under `specs/001-tutorial-specify-tool/`
- [ ] T038 [P] Per-mode composer docstrings: each `modes/*.py` MUST have a module-level docstring describing the mode's output shape, citing `contracts/spec-output-format.md`
- [ ] T039 [P] Add `--version` flag to `cli.py` printing the package version from `pyproject.toml`
- [ ] T040 Final test sweep per Constitution Principle V:
  - `cd scripts/tutorial_specify && pytest && cd ../..`
  - `bash test/run_all_tests.sh` (must match T004 baseline pass count)
  - `cd glp_runtime && dart test && cd ..` (must match T004 baseline pass count)
- [ ] T041 Final acceptance: run `/tutorial-specify all` against the live repo and the real `GLP_ART.pdf`; observe 13 specs generated under 15 min wall-clock (SC-003); spot-check that one cohesive-synthesis, one block-focused, and one multi-actor-distillation spec each pass `/speckit-clarify` validation (SC-001, SC-006)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2; MVP target
- **User Story 3 (Phase 4)**: Depends on Phase 3 happy-path CLI (T021); the resume layer wraps US1
- **User Story 2 (Phase 5)**: Depends on US1 + US3 spec output stabilising; can run in parallel with US3 once US1 ships
- **Polish (Phase N)**: All user stories complete

### User Story Dependencies

- **US1 (P1, MVP)**: No dependencies on other user stories.
- **US3 (P1)**: Builds on US1 — `cli.py` acquires checkpointing layer; tests reuse US1 fixtures.
- **US2 (P2)**: Validates the contract US1 produces; no code dependency on US3.

### Within Each User Story

- Tests written and failing BEFORE implementation lands (Constitution Principle V).
- Module implementations in dependency order: `lock`/`checkpoint`/`charter`/`pdf_extract` → `repl_parse` → `render_spec` → mode composers → `cli.py` → skill wrapper.
- Each acceptance scenario in `spec.md` MUST map to at least one task here.

### Parallel Opportunities

- **Setup**: T002, T003 can run in parallel with T001 once `pyproject.toml` exists.
- **Foundational**: T005, T006, T007, T008 are file-disjoint and can run in parallel.
- **US1 tests**: T010–T014 are file-disjoint and run in parallel; T015–T016 must wait for US1 implementation.
- **US1 implementation**: T017–T020 are file-disjoint and can run in parallel; T021 is the integration point.
- **US3 tests**: T025, T026 in parallel; T027, T028 require US3 implementation.
- **US2 tests**: T033–T035 in parallel; require US1 + US3 implementations stable.

---

## Notes

- `[P]` tasks = different files, no dependencies; safe to parallelise.
- Every task referencing a Functional Requirement cites it inline (e.g., FR-007a) — traceability per Constitution Principle I.
- Verify tests fail before implementing them per Principle V (Test-First).
- Commit after each task or logical group; never `git add -A` per Constitution §Workflow.
- Stop at any checkpoint to validate the user story independently.
- Avoid: vague tasks; same-file conflicts among `[P]`-marked tasks; cross-story dependencies that break independence.
