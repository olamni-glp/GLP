---

description: "Task list for Olamni Tutorial Chapter 1 — Fair Stream Merger"
---

# Tasks: Olamni Tutorial — Chapter 1 (Fair Stream Merger)

**Input**: Design documents from `specs/002-tutorial-ch01/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md (all present)
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V (Test-First). The `.glp` exercise is itself canonical SRSW (Principle III). Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI; no `chNN_plan.md` exists under the new workflow (per spec Assumptions).

**Tests**: This feature delivers documentation + GLP source; the captured REPL trace IS the regression artifact (per Plan §V "Test-First with caveats"). No new Dart unit tests required. Baseline `bash test/run_all_tests.sh` MUST pass before AND after implementation per Principle V.

**Organization**: Tasks grouped by user story per spec.md (US1, US2, US3 = P1/P1/P2; US4 = P3; US5 = P3 gated). US1+US2 together form the MVP for exercise-01. US5 is the planned ex-02 / ex-03 work and is **explicitly NOT implemented this round**; its tasks are listed for traceability and gated behind approval per FR-007.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1, US2, US3, US4, US5). Setup / Foundational / Polish phases have NO story label.

## Path Conventions

Project type per plan.md is **Tutorial chapter under charter (Constitution Option C)**:
- Tutorial source under `olamni/tutorial/ch01/`
- Top-level index `olamni/tutorial/tutorial.md`
- REPL build artifact at `glp_runtime/glp_repl.exe` (per research R-002)
- All paths repo-relative.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify host capabilities, build the REPL once, record the baseline.

- [ ] T001 Verify Dart SDK on this Windows host: run `dart --version`, confirm `^3.9.4`. If absent or below 3.9.4, halt and report to project owner per spec Edge Cases.
- [ ] T002 Build REPL executable: `dart compile exe glp_runtime/bin/glp_repl.dart -o glp_runtime/glp_repl.exe`. Verify the binary exists and runs (`./glp_runtime/glp_repl.exe --version` or equivalent smoke test).
- [ ] T003 Update `.gitignore` at repo root to ignore `glp_runtime/glp_repl*` (matches both `.exe` Windows form and Unix unsuffixed form). Verify no existing pattern conflicts (per research.md R-002 implementation note).
- [ ] T004 Record baseline test pass: run `bash test/run_all_tests.sh` and capture exit status + summary. Per Constitution Principle V, this MUST pass BEFORE implementation begins.

**Checkpoint**: Dart verified, REPL built, gitignore updated, baseline recorded. Phase 1 complete.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: PDF source re-read and inspection-goal approval — both gate every user story.

**⚠️ CRITICAL**: No user story work can begin until both T005 and T006 complete (T006 requires explicit approval).

- [ ] T005 Re-read `GLP_ART.pdf` book pp 5–6 (PDF pp 17–18) for byte-exact Program 1.1 plus the §1.6 prose surrounding the program block (per research.md R-006). Record the verbatim 3-clause merge program in working memory; record the surrounding prose sentences that paraphrase comments will draw from.
- [ ] T006 Propose 3 inspection goals to project owner for explicit approval (per research.md R-004): (1) `merge([1,2,3,4], [a], Xs).` asymmetric, (2) `merge([], [a, b, c], Xs).` empty stream, (3) `merge([], [], Xs).` base case. Wait for approval before any REPL run. Per spec FR-002 / FR-011, this is the plan-then-act gate.

**Checkpoint**: Byte-exact Program 1.1 in working memory; inspection goals approved by project owner. User stories may now begin.

---

## Phase 3: User Story 1 — Load and run Program 1.1 in the GLP REPL (Priority: P1) 🎯 MVP

**Goal**: Learner loads `ch-01-ex-01-fair-stream-merger.glp` in the REPL, runs the primary goal, sees the predicted fair interleaving `Xs = [1, a, 2, b, 3]`. Empirically verifies the locked binding from spec Clarification Q1.

**Independent Test**: Open the generated `.glp` file in the GLP REPL; load completes with zero errors (no SRSW violation, no type error, no compile error per SC-002); run `merge([1,2,3],[a,b],Xs).`; observe the locked binding and `→ succeeds` (per SC-003).

### Implementation for User Story 1

- [ ] T007 [US1] Create directory `olamni/tutorial/ch01/exercise-01/`.
- [ ] T008 [US1] Write `olamni/tutorial/ch01/exercise-01/ch-01-ex-01-fair-stream-merger.glp` per `contracts/glp-file-format.md` — Program 1.1 verbatim from PDF p 5 (3 clauses, original variable names `X, Xs, Y, Ys, Zs`), header block + one-line `%%` paraphrase comment per clause drawn from the §1.6 prose captured in T005.
- [ ] T009 [US1] Verify the .glp loads cleanly under the REPL: `glp_runtime/glp_repl.exe` → `load olamni/tutorial/ch01/exercise-01/ch-01-ex-01-fair-stream-merger.glp` → expect zero errors. Per spec SC-002 and Constitution Principle II, any error halts implementation.
- [ ] T010 [US1] Run the primary goal `merge([1,2,3],[a,b],Xs).` under the REPL; capture stdin + stdout verbatim. Per spec Clarification Q1: if `Xs` ≠ `[1, a, 2, b, 3]`, halt and report (do NOT silently overwrite the spec).
- [ ] T011 [US1] Run the 3 approved inspection goals in order: asymmetric, empty-stream, base-case (per T006); capture stdin + stdout verbatim for each.

**Checkpoint**: The `.glp` loads, the primary goal returns the locked binding, all 3 inspection goals produce documented outcomes. User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 — Step through a guided session for exercise-01 (Priority: P1)

**Goal**: Learner has a step-through guide (`ex-01-tutorial.md`) and a verbatim captured trace (`ex-01-repl-trace.md`) to follow and self-verify.

**Independent Test**: Reader follows `ex-01-tutorial.md` start-to-finish on a fresh machine with a working GLP REPL; their REPL output matches `ex-01-repl-trace.md` byte-for-byte modulo timestamps (per SC-004).

### Implementation for User Story 2

- [ ] T012 [US2] Write `olamni/tutorial/ch01/exercise-01/ex-01-repl-trace.md` per `contracts/trace-file-format.md` from the captured REPL output of T010 + T011. Structure: 1–3 sentence learner-targeted preface stating what the trace demonstrates; 5 fenced ```glp code blocks (build/load + 4 goal phases); 1–2 brief annotation lines outside each code block explaining what the learner should expect, what it means, why it matters; 1–3 sentence learner-targeted postscript summarising what the trace proved. Code-block contents byte-verbatim from T010/T011 captures.
- [ ] T013 [US2] Write `olamni/tutorial/ch01/exercise-01/ex-01-tutorial.md` — the learner-targeted step-through guide. Walks the learner through the same 5 phases as the trace but with more pedagogical scaffolding (link to PDF §1.4–§1.6, build instructions, "now try this" prompts mapping to each inspection goal, "what to look for" guidance, link to `ex-01-repl-trace.md` for verbatim cross-reference).

**Checkpoint**: Learner-facing tutorial + verbatim trace both exist; trace satisfies SC-004 byte-equality contract; tutorial signposts the trace. User Stories 1 AND 2 work independently as the MVP.

---

## Phase 5: User Story 3 — Find chapter 1 from the chapter signpost (Priority: P2)

**Goal**: Learner opens `olamni/tutorial/ch01/ch01_tutorial.md` and discovers exercise-01 with brief intro + status block.

**Independent Test**: `ch01_tutorial.md` exists; lists `exercise-01/` with one-line summary; status block is grep-friendly per `contracts/status-block-format.md`; pre-flight grep for `^- exercise-01:` returns the expected line.

### Implementation for User Story 3

- [ ] T014 [US3] Write `olamni/tutorial/ch01/ch01_tutorial.md` (chapter signpost). Sections: (a) brief intro to chapter 1 (Fair Stream Merger; one paragraph); (b) prerequisites (working REPL; link to repo's REPL-build instructions); (c) `## Exercise status` block per `contracts/status-block-format.md` initial state — `exercise-01: pending exercise-01 approval` / `exercise-02: pending exercise-01 approval` / `exercise-03: not yet implemented`; (d) one-line summary + link to `exercise-01/ex-01-tutorial.md`; (e) marked future entries for `exercise-02/` and `exercise-03/` (planned, pending approval).
- [ ] T015 [US3] Verify the status block is grep-friendly: `grep -E "^- exercise-01:" olamni/tutorial/ch01/ch01_tutorial.md` returns exactly one match with the expected `pending exercise-01 approval` text. Per spec Clarification Q2 / `contracts/status-block-format.md`.

**Checkpoint**: Chapter signpost discoverable; status block enforceable. User Story 3 complete.

---

## Phase 6: User Story 4 — Find chapter 1 from the top-level index (Priority: P3)

**Goal**: Top-level `olamni/tutorial/tutorial.md` exists / is updated to list Chapter 1.

**Independent Test**: `olamni/tutorial/tutorial.md` exists; chapter-status table contains a row for ch01 linking to `ch01/ch01_tutorial.md`; chapters 2–13 rows link to existing `chXX-sources.md` files (no broken links).

### Implementation for User Story 4

- [ ] T016 [US4] Write (or extend, if it exists) `olamni/tutorial/tutorial.md` per research.md R-003 schema: brief intro paragraph; chapter-status table with one row per chapter (1: implemented after approval; 2–13: planned, linking to existing `chXX-sources.md`); prerequisites section (Dart `^3.9.4`, REPL build); one-paragraph "how to use this tutorial" referencing `olamni/tutorial/charter.md` design principles. For this round the ch01 row is initially `pending review` (date `2026-04-28`); flips to `implemented` only after Udi approves exercise-01 (Phase 9).
- [ ] T017 [US4] Verify all 12 planned-chapter links resolve: each `chXX-sources.md` file referenced in the table MUST exist on disk. Halt on any broken link.

**Checkpoint**: Top-level index discoverable; all 13 chapter links resolve. User Story 4 complete.

---

## Phase 7: User Story 5 — Practice variable renaming via ex-02 and ex-03 (Priority: P3, GATED)

**⚠️ NOT IMPLEMENTED THIS ROUND.** These tasks are listed for traceability per spec FR-008 and the data-model.md lifecycle. Implementation of ex-02 is gated behind explicit approval of exercise-01 (Phase 9). Implementation of ex-03 is gated behind explicit approval of ex-02. Per `contracts/status-block-format.md` pre-flight check.

**Goal (eventual)**: Learner studies semantic-name variant (ex-02) and single-letter variant (ex-03), confirms identical merge outcome — internalising that GLP semantics depend on reader/writer pairing, not variable names.

**Independent Test (eventual)**: Each variant `.glp` loads cleanly and produces the same `Xs = [1, a, 2, b, 3]` for the primary goal, despite different variable names.

### Implementation for User Story 5 (FUTURE — DO NOT EXECUTE THIS ROUND)

- [ ] T018 [US5] Pre-flight gate: `grep -E "^- exercise-01: approved" olamni/tutorial/ch01/ch01_tutorial.md`. If no match, refuse to proceed; ask Udi for explicit approval per spec FR-007.
- [ ] T019 [US5] Create directory `olamni/tutorial/ch01/exercise-02/`.
- [ ] T020 [US5] Write `olamni/tutorial/ch01/exercise-02/ch-01-ex-02-fair-stream-merger.glp` — same structure as ex-01 but variables renamed per spec FR-008: `X→First, Xs→RestFirst, Y→Second, Ys→RestSecond, Zs→Out`.
- [ ] T021 [US5] Verify ex-02 .glp loads cleanly and produces the locked binding `Out = [1, a, 2, b, 3]` for the primary goal.
- [ ] T022 [US5] Write `olamni/tutorial/ch01/exercise-02/ex-02-tutorial.md` and `ex-02-repl-trace.md` following the same contracts as ex-01.
- [ ] T023 [US5] Update `ch01_tutorial.md` status block: `exercise-02: pending exercise-02 approval`. Repeat the approval gate before ex-03.
- [ ] T024 [US5] Pre-flight gate for ex-03: `grep -E "^- exercise-02: approved"`. If no match, refuse to proceed.
- [ ] T025 [US5] Create directory `olamni/tutorial/ch01/exercise-03/` and write `ch-01-ex-03-fair-stream-merger.glp` with `X→A, Xs→As, Y→B, Ys→Bs, Zs→Cs`.
- [ ] T026 [US5] Verify ex-03 .glp loads cleanly and produces `Cs = [1, a, 2, b, 3]`.
- [ ] T027 [US5] Write `ex-03-tutorial.md` and `ex-03-repl-trace.md`.
- [ ] T028 [US5] Update `ch01_tutorial.md` status block: `exercise-03: pending exercise-03 approval`. Add ex-02 / ex-03 rows to `olamni/tutorial/tutorial.md` chapter-1 row's exercises sub-list.

**Checkpoint (eventual)**: All three exercises implemented; status block reflects current approval state; learner can compare three variants of the same Program.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Round out the chapter with the rev-eng-input prompt (per FR-006), validate no fabrication (FR-010), and document.

- [ ] T029 [P] Write `olamni/tutorial/ch01/ch01-specification-input-prompt.md` per spec FR-006 — plain prose describing what the chapter's tutorial requires, drawing from `olamni/tutorial/ch01/spec-rev-eng-input/ch01-DEPRECATED-spec.md` but **stripping all speckit ceremony**: NO Feature Branch / Status / Constitution / FR-NNN / User Story / Given-When-Then forms. Output is the rev-eng input prompt that drove this very spec; lives separately from `specs/002-tutorial-ch01/spec.md`.
- [ ] T030 [P] No-fabrication audit: verify Claude has not introduced any speckit-format `spec.md`-style file under `specs/002-tutorial-ch01/` (other than the proper-channel `spec.md` produced by `/speckit-specify` itself + this `tasks.md`). Per spec FR-010 / SC-006.
- [ ] T031 Run `bash test/run_all_tests.sh` post-implementation; verify pass status matches the baseline recorded in T004. Per Constitution Principle V (Test-First).
- [ ] T032 Show the implementation diff to project owner. Wait for explicit approval. Per spec FR-011 / Plan-then-act.
- [ ] T033 On approval: flip `ch01_tutorial.md` status block `exercise-01: pending exercise-01 approval` → `exercise-01: approved <YYYY-MM-DD>`. Flip top-level `tutorial.md` ch01 row `pending review` → `implemented <YYYY-MM-DD>`. Per `contracts/status-block-format.md` update protocol.
- [ ] T034 Commit + push + merge to main; bump CalVer release tag. Per project release pattern (`v2026.04.28` was the spec/clarify cut; the implementation cut is the next CalVer increment).

**Checkpoint**: ch01 exercise-01 fully delivered, approved, and released. Phase 7 (ex-02 / ex-03) becomes unblocked once T033 sets `exercise-01: approved`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001 → T002 → T003 → T004 sequential (each step builds on the prior).
- **Foundational (Phase 2)**: T005 + T006 — both required before US1. T006 requires explicit project-owner approval (gate).
- **User Stories (Phase 3+)**: All depend on Phase 2 complete.
  - US1 (T007–T011) MUST complete before US2 (T012–T013) — the trace in US2 derives from REPL captures in US1.
  - US3 (T014–T015) and US4 (T016–T017) are independent of US1/US2 in pure file-creation sense BUT the signposts SHOULD reference the actually-existing exercise files (so practical ordering: US1+US2 first).
  - US5 (T018–T028) is fully GATED — never starts until T033 sets `exercise-01: approved`.
- **Polish (Phase 8)**: T029–T030 [P] independent. T031 depends on US1+US2 completion. T032 depends on T029–T031. T033 depends on T032 approval. T034 depends on T033.

### Within Each User Story

- US1 sequence: T007 (mkdir) → T008 (write .glp) → T009 (load test) → T010 (primary goal) → T011 (inspection goals).
- US2 sequence: T012 (write trace from US1 captures) → T013 (write tutorial referencing trace).
- US3: T014 (write signpost) → T015 (verify grep).
- US4: T016 (write index) → T017 (verify links).
- US5: gated; sequence per task IDs.

### Approval Gates

| Gate | Blocks | Set by |
|---|---|---|
| T006 (inspection goals approved) | All Phase 3+ | Udi explicit reply |
| T032 (implementation diff approved) | T033, T034 | Udi explicit reply |
| T033 (`exercise-01: approved`) | T018 (Phase 7) | T033 itself, after T032 |
| T024 grep (`exercise-02: approved`) | T025+ | T032+ for ex-02 cycle |

### Parallel Opportunities

- **Phase 1**: T002 and T003 could be parallel BUT T003 needs T002 to know the binary name to ignore — keep sequential.
- **Phase 8**: T029 and T030 are [P] — different files, no shared deps.
- **Phase 7 (when unblocked)**: T020 (ex-02 .glp) and T025 (ex-03 .glp) cannot be parallel because ex-03 is gated on ex-02 approval.
- Most tasks in this feature are sequential within a story; parallelism is limited because the feature is documentation + a single REPL run.

---

## Parallel Example: Phase 8 polish

```bash
# T029 and T030 can run in parallel:
Task: "Write rev-eng input prompt at olamni/tutorial/ch01/ch01-specification-input-prompt.md"
Task: "Audit specs/002-tutorial-ch01/ for absence of Claude-fabricated speckit-format files"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Complete Phase 1: Setup (T001–T004).
2. Complete Phase 2: Foundational (T005, T006 — inc. approval gate).
3. Complete Phase 3: User Story 1 (T007–T011).
4. Complete Phase 4: User Story 2 (T012–T013).
5. **STOP and VALIDATE**: Test exercise-01 independently; the .glp loads, primary goal returns locked binding, trace is verbatim, tutorial walks through it.
6. This is the MVP — exercise-01 is fully usable for a learner who knows where to find the file.

### Add discoverability (US3 + US4)

7. Complete Phase 5: User Story 3 (T014–T015) — chapter signpost.
8. Complete Phase 6: User Story 4 (T016–T017) — top-level index.
9. **STOP and VALIDATE**: A learner arriving at `olamni/tutorial/tutorial.md` can navigate to ch01 and the exercise.

### Polish + release

10. Complete Phase 8 partially (T029, T030, T031, T032).
11. **STOP and seek approval** (T032).
12. Complete T033 (status flips), T034 (commit + push + merge + CalVer bump).

### Gated future work (US5)

13. Once `exercise-01: approved` in `ch01_tutorial.md`, propose exercise-02 implementation as a fresh `/speckit-tasks` cycle (or extend this tasks.md). Repeat the same approval-gate cycle for ex-03.

---

## Notes

- [P] tasks = different files, no shared deps — parallelisable.
- [Story] label maps tasks to spec.md user stories (US1–US5).
- US5 is **explicitly gated** — its tasks (T018–T028) MUST NOT execute this round.
- Per spec FR-011 and Constitution Principle I (Spec-First) + Discussion Mode default, every task that writes a file MUST be presented to project owner before action; this tasks.md is the plan, but the implementation cycle still respects plan-then-act per task.
- Per spec FR-010 and the no-fabrication discipline: **Claude does NOT write speckit-format `spec.md`-style files for this or any other chapter**. T030 verifies this.
- Constitution Principle II: any obstacle (Dart absent, REPL build fail, binding mismatch, SRSW error) → HALT and report. NEVER `skipSRSW`, NEVER catch-and-ignore.
- Commit cadence: one commit per logical group (Setup, Foundational, US1, US2, US3, US4, Polish). Per Constitution multi-Claude protocol — `git add` SPECIFIC files, never `git add -A`.
