---

description: "Task list for Olamni Tutorial Chapter 2 — LP/GLP Append Contrast + Body Kernels"
---

# Tasks: Olamni Tutorial — Chapter 2 (LP/GLP Append Contrast + Body Kernels)

**Input**: Design documents from `specs/003-tutorial-ch02/`
**Prerequisites**: plan.md, spec.md (with 5 Clarifications), research.md (9 R-NNN), data-model.md, contracts/ (3 files), quickstart.md (all present)
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V (Test-First). The three GLP `.glp` files are SRSW-compliant; the one classical-LP `.glp` file IS the canonical SRSW-violating example for didactic purposes (Principle III — the analyser doing its job is the demonstration). Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI; no `chNN_plan.md` exists under the new workflow (per spec Assumptions).

**Tests**: This feature delivers documentation + GLP source; the captured REPL traces ARE the regression artifacts (per Plan §V "Test-First with caveats"). No new Dart unit tests required. Per spec FR-016, ch02 exercise files are NOT added to `test/run_all_tests.sh`. Baseline `bash test/run_all_tests.sh` MUST pass before AND after implementation per Principle V (476/476 expected per workflow memory).

**Organization**: Tasks grouped by user story per spec.md. US1+US2+US3 (all P1) form the MVP for exercise-01 — together they deliver the LP→GLP contrast pair. US4 (P2 gated) = ex-02 arithmetic. US5 (P3 gated) = ex-03 time + I/O. US6+US7 (P2/P3) = chapter signpost + top-level index update. The three exercises are sequenced behind their approval gates; the signpost + top-level index are interleaved with ex-01 because they reference it.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1, US2, US3, US4, US5, US6, US7). Setup / Foundational / Polish phases have NO story label.

## Path Conventions

Project type per plan.md is **Tutorial chapter under charter (Constitution Option C)**:
- Tutorial source under `olamni/tutorial/ch02/`
- Top-level index `olamni/tutorial/tutorial.md` (existing from ch01; extend)
- REPL build artifact at `glp_runtime/glp_repl.exe` (per research R-002, inherited from ch01)
- All paths repo-relative.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify host capabilities, ensure REPL is built, record the baseline.

- [ ] T001 Verify Dart SDK on this Windows host: run `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. If absent or below 3.9.4, halt and report to project owner per spec Edge Cases. Set session variable `DART="/c/Users/gavri/dart-sdk/bin/dart"`.
- [ ] T002 Verify or rebuild REPL executable at `glp_runtime/glp_repl.exe`: if it already exists from ch01's session AND `glp_runtime/bin/glp_repl.dart` is unchanged, reuse; otherwise build with `"$DART" compile exe glp_runtime/bin/glp_repl.dart -o glp_runtime/glp_repl.exe`. Verify the binary exists and runs.
- [ ] T003 Verify `.gitignore` already covers `glp_runtime/glp_repl*` (added during ch01's R-002). If missing for any reason, add it.
- [ ] T004 Record baseline test pass: run `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` and capture exit status + summary. Per Constitution Principle V, this MUST pass BEFORE implementation begins. Expected per workflow memory: `Total: 476 | Passed: 476 | Failed: 0`.

**Checkpoint**: Dart verified, REPL ready, baseline recorded. Phase 1 complete.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: PDF source re-reads (both ch 2 and ch 4 §4.2) and inspection-goal confirmation — both gate every user story.

**⚠️ CRITICAL**: No user story work can begin until T005 + T006 + T007 complete.

- [ ] T005 Re-read `GLP_ART.pdf` book p 10 (PDF p 22) byte-exactly for Example 2.1 (classical LP append). Re-read surrounding §2.1 prose (book pp 9–11) for the LP-syntax definitions and the operational-semantics paragraphs that the LP-only file's header comment will paraphrase. Note any drift vs `ch02-sources.md`; correct the sources file BEFORE proceeding (per ch01's predict-and-verify lesson).
- [ ] T006 Re-read `GLP_ART.pdf` book pp 31–32 (PDF pp 43–44) byte-exactly for the GLP `append/3` definition (chapter 4 §4.2 "List Reversal — Naive Reverse"). Re-read the immediately surrounding prose ("This is O(n²)" plus the two paragraphs introducing reverse + naive reverse) for the cross-chapter import provenance comment. Note byte-exact form: `append([], Ys, Ys?).\nappend([X|Xs], Ys, [X?|Zs?]) :- append(Xs?, Ys?, Zs).`
- [ ] T007 Confirm the locked inspection goals to project owner per `research.md` R-004 (auto-mode-approved during /speckit-plan unless project owner overrides):
  - **ex-01**: `append([], [a,b,c], Zs).`, `append([1,2,3], [], Zs).`, `append([], [], Zs).`
  - **ex-02**: `append_and_sum([], [4,5,6], Zs, Sum).`, `append_and_sum([1,2,3], [], Zs, Sum).`, `append_and_sum([], [], Zs, Sum).`
  - **ex-03**: `timed_append([], [], Zs).`, `timed_append([1..10], [a..j], Zs).`, `timed_append([1], [a], Zs).`
  Wait for explicit approval (or auto-mode "continue to completion now") before any REPL run. Per spec FR-013, this is the plan-then-act gate.

**Checkpoint**: Byte-exact code for both source pages in working memory; inspection goal sets confirmed. User stories may now begin.

---

## Phase 3: User Story 1 — Observe SRSW rejection of classical LP append (Priority: P1) 🎯 MVP-1/3

**Goal**: Learner attempts to load `ch-02-ex-01-classical-append-LP-only.glp` in the REPL and observes the SRSW analyser rejecting the file. The rejection IS the demonstration (per FR-001, SC-002).

**Independent Test**: Run the REPL with the LP-only file path; observe `Error loading: …` SRSW-violation message; no `✓ Loaded` line.

### Implementation for User Story 1

- [ ] T008 [US1] Create directory `olamni/tutorial/ch02/exercise-01/`.
- [ ] T009 [US1] Write `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-classical-append-LP-only.glp` per `contracts/glp-file-format.md` File 1 spec — Example 2.1 byte-exact from PDF p 10 (per T005), header block flagging `% INTENTIONALLY ILL-FORMED FOR GLP — illustrates classical LP contraction`, one `%%` paraphrase comment per clause drawn from §2.1 prose captured in T005. **Verification step (per spec SC-006)**: after writing the file, strip the header comment block and the per-clause `%%` annotations; the remaining two-line clause corpus MUST equal the byte-exact form recalled in T005 — i.e., `append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).\nappend([], Ys, Ys).\n`. If any byte differs, HALT and re-read PDF p 10 byte-exactly before re-writing.
- [ ] T010 [US1] Verify the LP-only file is REJECTED at load: run `"$DART" run glp_runtime/.dart_tool/repl.dill` with input `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-classical-append-LP-only.glp\n:quit\n`. Expect an `Error loading: …` SRSW-violation message. If the file silently loads (no error), HALT and report — this is a runtime regression per spec SC-002. Capture the verbatim rejection output for use in T020.

**Checkpoint**: Classical LP file written + analyser rejection captured. US1 deliverable in hand.

---

## Phase 4: User Story 2 — Load GLP append and run primary + inspection goals (Priority: P1) 🎯 MVP-2/3

**Goal**: Learner loads `ch-02-ex-01-glp-append.glp` in the REPL, runs the primary goal `append([1,2,3], [a,b,c], Zs).` plus three inspection goals, observes the locked binding `Zs = [1, 2, 3, a, b, c]`. Empirically verifies the locked binding from spec FR-002.

**Independent Test**: REPL accepts the GLP file (no errors); primary goal succeeds with locked binding; three inspection goals produce documented bindings (per SC-003, SC-004).

### Implementation for User Story 2

- [ ] T011 [US2] Write `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-glp-append.glp` per `contracts/glp-file-format.md` File 2 spec — GLP `append/3` byte-exact from PDF pp 31–32 (per T006), header block with cross-chapter import provenance per `research.md` R-007, one `%%` paraphrase comment per clause.
- [ ] T012 [US2] Verify the GLP file is ACCEPTED at load: run the REPL with input `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-glp-append.glp\n:quit\n`. Expect `✓ Loaded: …`. If rejected, HALT and report.
- [ ] T013 [US2] Run the primary goal `append([1,2,3], [a,b,c], Zs).` under the REPL. Expect locked binding `Zs = [1, 2, 3, a, b, c]` and `→ succeeds`. If mismatch, HALT and report (do NOT silently overwrite spec).
- [ ] T014 [US2] Run the three approved inspection goals from T007 (ex-01 set) in order. Expect: `Zs = [a, b, c]`, `Zs = [1, 2, 3]`, `Zs = []`. Capture stdin + stdout verbatim for each.

**Checkpoint**: GLP file loads, locked binding verified, all three inspection goals captured. US2 deliverable in hand.

---

## Phase 5: User Story 3 — Step-through guide + trace for ex-01 (Priority: P1) 🎯 MVP-3/3

**Goal**: Learner has a step-through guide (`ex-01-tutorial.md`) and a verbatim captured trace (`ex-01-repl-trace.md`) covering BOTH the LP-only rejection and the GLP file's success path.

**Independent Test**: Reader follows `ex-01-tutorial.md` start-to-finish on a fresh machine; their REPL output matches `ex-01-repl-trace.md` byte-for-byte modulo timestamps (per SC-005).

### Implementation for User Story 3

- [ ] T015 [US3] Write `olamni/tutorial/ch02/exercise-01/ex-01-repl-trace.md` per `contracts/trace-file-format.md` (six phases for ex-01: Phase A=LP-only load attempt, Phase B=GLP file load, Phase C=primary goal, Phases D-E-F=three inspection goals). Code-block content byte-verbatim from T010 + T012-T014 captures. Annotation between Phase A and Phase B explicitly explains the LP→GLP contrast per the contract.
- [ ] T016 [US3] Write `olamni/tutorial/ch02/exercise-01/ex-01-tutorial.md` — learner-targeted step-through guide. Sections: "Before you start" (read §2.1 + §2.2 + Formal 2.1), "Building the REPL" (one-time), "The exercise" (six steps mirroring the trace phases), "Cross-check against the captured trace", "What you've learned" (SRSW + LP→GLP transition + Formal 2.1 made concrete).

**Checkpoint**: Learner-facing tutorial + verbatim trace exist; trace satisfies SC-005 byte-equality contract. MVP (US1+US2+US3 = ex-01 complete) in hand.

---

## Phase 6: User Story 6 — Chapter signpost (Priority: P2)

**Goal**: `ch02_tutorial.md` exists; lists exercise-01 with one-line summary; documents cross-chapter import; status block grep-friendly per `contracts/status-block-format.md`.

**Independent Test**: `ch02_tutorial.md` exists; `grep -E "^- exercise-01:" olamni/tutorial/ch02/ch02_tutorial.md` returns the expected line.

### Implementation for User Story 6

- [ ] T017 [US6] Write `olamni/tutorial/ch02/ch02_tutorial.md` (chapter signpost, **underscore** filename per workflow memory). Sections: "Chapter 2 — Logic Programs and Linear Logic" intro (theoretical chapter, bridged to runnable code via ch 4 §4.2 GLP append import); "How to work with this chapter's tutorial code" (read §2.1+§2.2, build REPL, pick exercise from status block); "Exercises" (links to all three with one-line summaries; ex-02 / ex-03 visibly marked as planned/pending until they exist); status block per `contracts/status-block-format.md` initial state (`exercise-01: pending review`, `exercise-02: pending exercise-01 approval`, `exercise-03: pending exercise-02 approval`); "Sources" (links to ch02-sources.md and the deprecated spec rev-eng-input).
- [ ] T018 [US6] Verify the status block is grep-friendly: `grep -E "^- exercise-NN:" olamni/tutorial/ch02/ch02_tutorial.md` returns exactly three matches in order.

**Checkpoint**: Chapter signpost discoverable; status block enforceable. US6 complete.

---

## Phase 7: User Story 7 — Top-level index update (Priority: P3)

**Goal**: `olamni/tutorial/tutorial.md` (already exists from ch01) is extended; chapter-2 row flips from `planned` to `pending review (2026-04-28)` initially, then to `implemented YYYY-MM-DD` after all exercises approved.

**Independent Test**: `olamni/tutorial/tutorial.md` chapter-2 row links to `ch02/ch02_tutorial.md` (no broken link); status text reflects current state.

### Implementation for User Story 7

- [ ] T019 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch02 row from `planned` to `pending review (2026-04-28)`; link target changes from `ch02/ch02-sources.md` to `ch02/ch02_tutorial.md`. (Final flip to `implemented YYYY-MM-DD` happens in Phase 11 after all three exercises are approved.) Chapters 3–13 rows unchanged.

**Checkpoint**: Top-level index reflects ch02 in flight. US7 partial complete (final state set in T036).

---

## Phase 8: ex-01 approval gate

- [ ] T020 [US1+US2+US3] Run baseline tests post-ex-01-implementation: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh`. Expect 476/476 PASS (unchanged from T004).
- [ ] T021 [US1+US2+US3] Show ex-01 implementation diff to project owner. Wait for explicit `approved` signal (or auto-mode "continue to completion now").
- [ ] T022 [US1+US2+US3] On approval: edit `ch02_tutorial.md` status block to flip `exercise-01: approved YYYY-MM-DD` and `exercise-02: pending review`. Commit.

**Checkpoint**: ex-01 approval gate passed. Phase 9 (ex-02) becomes unblocked.

---

## Phase 9: User Story 4 — ex-02 GLP arithmetic (Priority: P2, GATED)

**⚠️ GATE**: T022 must have flipped `exercise-01: approved` AND ex-01 trace must have covered all "thoroughly REPL-tested" criteria (per FR-008): every clause exercised, both files exercised, primary + 3 inspection goals captured.

**Goal**: Learner studies `append_and_sum/4` (locked shape per Clarification Q3) which appends two number lists AND concurrently sums the result. Demonstrates SRSW's producer/consumer pairing with arithmetic via `:=`.

**Independent Test**: Run `append_and_sum([1,2,3], [4,5,6], Zs, Sum).` against the loaded ex-02 file; observe `Zs = [1, 2, 3, 4, 5, 6]` AND `Sum = 21` AND `→ succeeds` (per SC-013).

### Implementation for User Story 4

- [ ] T023 [US4] Pre-flight gate: `grep -E "^- exercise-01: approved" olamni/tutorial/ch02/ch02_tutorial.md` MUST return one match. If not, HALT.
- [ ] T024 [US4] Create directory `olamni/tutorial/ch02/exercise-02/`.
- [ ] T025 [US4] Write `olamni/tutorial/ch02/exercise-02/ch-02-ex-02-append-and-sum.glp` per `contracts/glp-file-format.md` File 3 spec and `research.md` R-008 (amended 2026-04-29). Duplicate GLP `append/3` byte-exact from ex-01 (no cross-file dependency). Define `sum/2` (2 clauses, head `sum([X|Xs], Total?)` — writers in head, readers in body). Define `append_and_sum/3` (1 clause, with internal `Zs` paired writer/reader between `append` sub-call and `sum` sub-call). Header block + per-clause `%%` comments per R-001.
- [ ] T026 [US4] Verify the file is ACCEPTED at load. If rejected, HALT.
- [ ] T027 [US4] Run primary goal `append_and_sum([1,2,3], [4,5,6], Sum).` Expect `Sum = 21`. If mismatch, HALT.
- [ ] T028 [US4] Run three approved inspection goals (ex-02 set from T007, amended): `append_and_sum([], [4,5,6], Sum).`, `append_and_sum([1,2,3], [], Sum).`, `append_and_sum([], [], Sum).`. Expect: `Sum=15`, `Sum=6`, `Sum=0`. Capture verbatim.
- [ ] T029 [US4] Write `ex-02-repl-trace.md` per `contracts/trace-file-format.md` (five phases). Strict byte-equality contract (per FR-014 — no relaxation for ex-02).
- [ ] T030 [US4] Write `ex-02-tutorial.md` — learner step-through emphasising the producer/consumer pairing made concrete with arithmetic (`Sum` is being computed by `sum/2` while `Zs` is still being constructed by `append/3` — same SRSW idiom, different domain).

**Checkpoint**: ex-02 fully landed; awaiting approval.

---

## Phase 10: ex-02 approval gate

- [ ] T031 [US4] Run baseline tests post-ex-02-implementation: expect 476/476 PASS.
- [ ] T032 [US4] Show ex-02 diff to project owner. Wait for `approved` signal.
- [ ] T033 [US4] On approval: edit `ch02_tutorial.md` status block to flip `exercise-02: approved YYYY-MM-DD` and `exercise-03: pending review`. Commit.

**Checkpoint**: ex-02 approval gate passed. Phase 11 (ex-03) becomes unblocked.

---

## Phase 11: User Story 5 — ex-03 system time + I/O (Priority: P3, GATED)

**⚠️ GATE**: T033 must have flipped `exercise-02: approved` AND ex-02 trace must have covered all "thoroughly REPL-tested" criteria.

**Goal**: Learner studies `timed_append/3` (locked shape per Clarification Q3) which captures `now(Start)`, runs `append/3`, captures `now(End)`, computes elapsed via `:=`, emits `'_output'(elapsed_ms(N))`. Demonstrates that SRSW also governs side-effecting kernels.

**Independent Test**: Run `timed_append([1,2,3], [a,b,c], Zs).`; observe `elapsed_ms(N)` line emitted (N varies per run; SHAPE locked per FR-014) AND `Zs = [1, 2, 3, a, b, c]` AND `→ succeeds` (per SC-014).

### Implementation for User Story 5

- [ ] T034 [US5] Pre-flight gate: `grep -E "^- exercise-02: approved" olamni/tutorial/ch02/ch02_tutorial.md` MUST return one match. If not, HALT.
- [ ] T035 [US5] Create directory `olamni/tutorial/ch02/exercise-03/`.
- [ ] T036 [US5] Write `olamni/tutorial/ch02/exercise-03/ch-02-ex-03-timed-append.glp` per `contracts/glp-file-format.md` File 4 spec and `research.md` R-009. Duplicate GLP `append/3` byte-exact (no cross-file dependency). Define `timed_append/3` with `now/1` × 2, `ground/1` guard, `:=` subtraction, `'_output'/1` call. Header block + per-clause `%%` comments.
- [ ] T037 [US5] Verify the file is ACCEPTED at load. If rejected, HALT.
- [ ] T038 [US5] Run primary goal `timed_append([1,2,3], [a,b,c], Zs).` Expect `Zs = [1, 2, 3, a, b, c]` AND a `'_output'(elapsed_ms(N))` printed line where N is a non-negative integer. If `Zs` mismatches OR `elapsed_ms` line missing, HALT.
- [ ] T039 [US5] Run three approved inspection goals (ex-03 set from T007). Capture verbatim. Note that N values will vary across goals (typically 0–5 ms).
- [ ] T040 [US5] Write `ex-03-repl-trace.md` per `contracts/trace-file-format.md` (five phases) WITH the FR-014 elapsed-ms relaxation: annotation MUST contain the literal phrase "varies per run; the SHAPE matters, not the specific number".
- [ ] T041 [US5] Write `ex-03-tutorial.md` — learner step-through emphasising side-effects + the `ground/1` guard's role in sequencing now-end after append-completion + the per-run variation in `elapsed_ms`.

**Checkpoint**: ex-03 fully landed; awaiting approval.

---

## Phase 12: ex-03 approval gate + chapter complete

- [ ] T042 [US5] Run baseline tests post-ex-03-implementation: expect 476/476 PASS.
- [ ] T043 [US5] Show ex-03 diff to project owner. Wait for `approved` signal.
- [ ] T044 [US5+US7] On approval:
  - Edit `ch02_tutorial.md` status block to flip `exercise-03: approved YYYY-MM-DD`.
  - Edit `olamni/tutorial/tutorial.md` ch02 row from `pending review (…)` to `implemented YYYY-MM-DD`.
  - Commit.

**Checkpoint**: All three exercises approved; chapter 2 complete in the top-level index.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Final audits, no-fabrication check, full-suite verification.

- [ ] T045 [P] No-fabrication audit: verify all files under `specs/003-tutorial-ch02/` (excluding `QUARANTINE-DO-NOT-USE/`) are proper `/speckit-*` outputs. List the 12 files and confirm each was generated by /speckit-specify, /speckit-clarify, /speckit-plan, or /speckit-tasks. Per spec FR-012 + SC-011.
- [ ] T046 [P] Verify FR-015 (no extraneous cross-chapter imports): grep all four ch02 `.glp` files for any reference to chapters other than ch 2 + ch 4 §4.2 append. Should match only the documented provenance comments.
- [ ] T047 [P] Verify FR-016 (test harness exclusion): `grep "olamni/tutorial/ch02" test/run_all_tests.sh` MUST return zero matches. Per SC-016.
- [ ] T048 Final baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh`. Expect 476/476 PASS, identical to baseline (T004).
- [ ] T049 Trace reproducibility check (SC-005): re-run all three traces against the existing `.glp` files and `diff` against the committed `.md` files modulo per-exercise relaxations. ex-01 + ex-02 traces MUST be byte-identical (modulo banner / build wallclock); ex-03 trace MUST be byte-identical except for the integer N inside `elapsed_ms(N)`.
- [ ] T050 [P] Walk-through verification (SC-001 — soft): note that this requires an external fresh-eyes reader and cannot be self-tested; log as a known follow-up rather than blocking.
- [ ] T051 Commit + push branch `003-tutorial-ch02`. Per Constitution multi-Claude protocol — `git add` SPECIFIC files only.
- [ ] T052 Provide merge instructions to project owner per the workflow memory's mandatory format:
  ```bash
  cd D:/bstdev/research/glp/glp
  git checkout main
  git pull origin main
  git fetch origin 003-tutorial-ch02
  git merge -m "Merge 003-tutorial-ch02 into main" origin/003-tutorial-ch02
  git push origin main
  ```

**Checkpoint**: Chapter 2 fully delivered, audited, and ready for merge. Constitution Principle V (Test-First) satisfied (476 baseline preserved); Principle VI (Charter Compliance) satisfied (charter cited; no fabricated specs).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001 → T002 → T003 → T004 sequential.
- **Foundational (Phase 2)**: T005 + T006 + T007 — all required before any user story. T007 requires explicit project-owner approval (gate; satisfied by /speckit-clarify Q3 lock).
- **User Stories (Phase 3+)**: All depend on Phase 2 complete.
  - **MVP (US1+US2+US3 = ex-01)** sequential: T008 → T009 → T010 (US1 done) → T011 → T012 → T013 → T014 (US2 done) → T015 → T016 (US3 done).
  - US6 (T017–T018, signpost) depends on ex-01 files existing (so it can link them) → run after US3.
  - US7 (T019, top-level index) depends on US6 (signpost link target) → run after T017.
  - **Approval gate (Phase 8)**: T020 → T021 → T022 — gate is project-owner-approval signal.
  - US4 (T023–T030, ex-02) GATED behind T022 (`exercise-01: approved`).
  - US5 (T034–T041, ex-03) GATED behind T033 (`exercise-02: approved`).
- **Polish (Phase 13)**: T045–T047 [P] independent. T048 depends on all exercises landed. T049 depends on traces existing. T051 + T052 final.

### Within Each User Story

- US1 (T008-T010): mkdir → write LP-only `.glp` → verify rejection.
- US2 (T011-T014): write GLP `.glp` → verify load → run primary → run inspections.
- US3 (T015-T016): write trace from US1+US2 captures → write tutorial referencing trace.
- US4 (T023-T030): gate-check → mkdir → write `.glp` → verify load → run primary + inspections → write trace → write tutorial.
- US5 (T034-T041): same shape as US4 with elapsed-ms relaxation in T040.

### Approval Gates

| Gate | Blocks | Set by |
|---|---|---|
| T007 (inspection goals confirmed) | All Phase 3+ | Auto-mode-approved during /speckit-clarify Q3 lock; project owner may override at T007 |
| T021 (ex-01 diff approved) | T022 | Project owner explicit reply |
| T022 (`exercise-01: approved`) | T023+ (Phase 9) | T022 itself, after T021 |
| T032 (ex-02 diff approved) | T033 | Project owner explicit reply |
| T033 (`exercise-02: approved`) | T034+ (Phase 11) | T033 itself, after T032 |
| T043 (ex-03 diff approved) | T044 | Project owner explicit reply |

### Parallel Opportunities

- **Phase 1**: All sequential (each step builds on the prior).
- **Phase 13**: T045, T046, T047, T050 [P] — different audits, different files, no shared state.
- US4 vs US5: NO parallelism (US5 gated on US4 approval).
- US3 vs US6 vs US7: weakly parallelisable (different files), but in practice US3 → US6 → US7 sequential because each references the prior.
- Most tasks are sequential within an exercise; parallelism is limited because the feature is documentation + REPL captures.

---

## Parallel Example: Phase 13 polish

```bash
# T045, T046, T047, T050 can run in parallel:
Task: "No-fabrication audit of specs/003-tutorial-ch02/"
Task: "Cross-chapter-import scope check via grep across the 4 .glp files"
Task: "Test harness exclusion check via grep test/run_all_tests.sh"
Task: "Walk-through verification log entry for SC-001"
```

---

## Implementation Strategy

### MVP First (US1 + US2 + US3 = ex-01)

1. Complete Phase 1: Setup (T001–T004).
2. Complete Phase 2: Foundational (T005–T007 — inc. inspection-goal confirmation).
3. Complete Phase 3: US1 (T008–T010) — LP-only file + observe rejection.
4. Complete Phase 4: US2 (T011–T014) — GLP file + run primary + inspections.
5. Complete Phase 5: US3 (T015–T016) — trace + tutorial.
6. **STOP and VALIDATE**: ex-01 is fully usable for a learner who knows where to find the file.

### Add discoverability (US6 + US7)

7. Complete Phase 6: US6 (T017–T018) — chapter signpost.
8. Complete Phase 7: US7 partial (T019) — top-level index flip to `pending review`.
9. **STOP and VALIDATE**: A learner arriving at `olamni/tutorial/tutorial.md` can navigate to ch02 and the exercise.

### Approval + ex-02 (US4)

10. Complete Phase 8: ex-01 approval gate (T020–T022).
11. Complete Phase 9: US4 (T023–T030) — ex-02 with arithmetic.
12. Complete Phase 10: ex-02 approval gate (T031–T033).

### ex-03 (US5)

13. Complete Phase 11: US5 (T034–T041) — ex-03 with time + I/O.
14. Complete Phase 12: ex-03 approval gate + final flip (T042–T044).

### Polish + commit

15. Complete Phase 13: Polish (T045–T052).

---

## Notes

- [P] tasks = different files, no shared deps — parallelisable.
- [Story] label maps tasks to spec.md user stories (US1–US7).
- US4 and US5 are **gated** — cannot start until predecessor's `approved` flag is set in `ch02_tutorial.md`.
- Per spec FR-013 and Constitution Principle I (Spec-First) + Discussion Mode default, every task that writes a file MUST be presented to project owner before action; this tasks.md is the plan, but the implementation cycle still respects plan-then-act per task.
- Per spec FR-012 and the no-fabrication discipline: **Claude does NOT write speckit-format `spec.md`-style files for this or any other chapter**. T045 verifies this.
- Per spec FR-015 (cross-chapter import scope) and FR-016 (test harness exclusion), these are testable via grep — T046 + T047.
- Constitution Principle II: any obstacle (Dart absent, REPL build fail, binding mismatch, SRSW error on a GLP file, missing kernel) → HALT and report. NEVER `skipSRSW`, NEVER catch-and-ignore.
- Commit cadence: one commit per logical group (Setup, Foundational, US1+US2+US3, US6+US7, ex-01 approval, US4, ex-02 approval, US5, ex-03 approval+flip, Polish). Per Constitution multi-Claude protocol — `git add` SPECIFIC files, never `git add -A`.
- Constitution Principle V: baseline tests run before AND after — T004 + T031 + T042 + T048. ALL must show 476/476 PASS.
