---

description: "Task list for Olamni Tutorial Chapter 3 — GLP Core + §3.2 Guard Curriculum"
---

# Tasks: Olamni Tutorial — Chapter 3 (GLP Core + §3.2 Guard Curriculum)

**Input**: Design documents from `specs/004-tutorial-ch03/`
**Prerequisites**: plan.md, spec.md (with 3 Clarifications Q1+Q2+Q3 — all variation shapes spec-locked), research.md (9 R-NNN), data-model.md, contracts/ (3 files), quickstart.md (all present)
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V (Test-First). All four ch03 `.glp` files are SRSW-compliant by construction (Principle III). Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI; no `chNN_plan.md` exists under the new workflow (per spec Assumptions).

**Tests**: This feature delivers documentation + GLP source; the captured REPL traces ARE the regression artifacts (per Plan §V "Test-First with caveats"). No new Dart unit tests required. Per spec FR-016, ch03 exercise files are NOT added to `test/run_all_tests.sh`. Baseline `bash test/run_all_tests.sh` MUST pass before AND after implementation per Principle V (494/494 expected if `claude/fix-misleading-build-line` merged; 485/485 otherwise).

**Organization**: Tasks grouped by user story per spec.md. US1 (P1) + US2 (P1) form the MVP for exercise-01 — together they deliver the composed producer-merger-consumer pipeline + its captured trace. US3 (P2) = chapter signpost. US4 (P2 gated) = ex-02 defined guards. US5 (P3 gated) = ex-03 guard negation. US6 (P3) = top-level index update. The three exercises are sequenced behind their two predecessor-approval gates; the signpost + top-level index are interleaved with ex-01 because they reference it. All three variation-shape gates are CLOSED in the spec via Clarifications Q1+Q2+Q3.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1, US2, US3, US4, US5, US6). Setup / Foundational / Polish phases have NO story label.

## Path Conventions

Project type per plan.md is **Tutorial chapter under charter (Constitution Option C)**:
- Tutorial source under `olamni/tutorial/ch03/`
- Top-level index `olamni/tutorial/tutorial.md` (existing from ch01 + ch02; extend)
- REPL build artifact at `glp_runtime/glp_repl.exe` (per research R-002, inherited from ch01 + ch02)
- All paths repo-relative.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify host capabilities, ensure REPL is built, record the baseline.

- [X] T001 Verify Dart SDK on this Windows host: run `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. If absent or below 3.9.4, halt and report to project owner per spec Edge Cases. Set session variable `DART="/c/Users/gavri/dart-sdk/bin/dart"`.
- [X] T002 Verify or rebuild REPL executable at `glp_runtime/glp_repl.exe`: if it already exists from ch01 / ch02 sessions AND `glp_runtime/bin/glp_repl.dart` is unchanged, reuse; otherwise build. If `claude/fix-misleading-build-line` is merged into main, use the build-provenance form: `BUILD_COMMIT="$(git log -1 --format='%h %s')" && "$DART" compile exe glp_runtime/bin/glp_repl.dart --define=GLP_BUILD_COMMIT="$BUILD_COMMIT" -o glp_runtime/glp_repl.exe`. If unmerged, build without `--define` and record the omission in research.md per R-002.
- [X] T003 Verify `.gitignore` already covers `glp_runtime/glp_repl*` (added during ch01's R-002). If missing for any reason, add it.
- [X] T003a Verify input-prompt prerequisite per spec FR-007: confirm `olamni/tutorial/ch03/ch03-specification-input-prompt.md` exists and is non-empty (e.g., `wc -l olamni/tutorial/ch03/ch03-specification-input-prompt.md` returns >50 lines). This file is created BEFORE `/speckit-specify` runs (it is the rev-eng input); T003a is verification only, not creation. If absent or empty, halt and report — the spec is missing its plain-prose source.
- [X] T004 Record baseline test pass: run `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` and capture exit status + summary. Per Constitution Principle V, this MUST pass BEFORE implementation begins. Expected: `Total: 494 | Passed: 494 | Failed: 0` (post v2026.04.29-3) or `Total: 485 | Passed: 485 | Failed: 0` (post v2026.04.29-2 only). Record the actual baseline number in `research.md` for use by post-implementation tasks T021, T031, T041, T047.

**Checkpoint**: Dart verified, REPL ready, baseline recorded. Phase 1 complete.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: PDF source re-reads (book p 15 + p 31 + p 22 + p 24) plus subordinate-decomposition + inspection-goal confirmations — all gate every user story.

**⚠️ CRITICAL**: No user story work can begin until T005 + T006 + T007 + T008 + T009 complete.

- [X] T005 Re-read `GLP_ART.pdf` book p 15 (PDF p 27) byte-exactly for Program 3.1 (GLP Fair Stream Merger). Re-read surrounding §3.1 prose (book pp 15–17) for Reader/Writer pairs + SO Invariant + GLP operational semantics + GLP Safety + Monotonicity paragraphs that the file's header comment will paraphrase. Note any drift vs `ch03-sources.md`; correct the sources file BEFORE proceeding (per ch01's predict-and-verify lesson). Note byte-exact form: `merge([X|Xs],Ys,[X?|Zs?]) :- merge(Ys?,Xs?,Zs).\nmerge(Xs,[Y|Ys],[Y?|Zs?]) :- merge(Xs?,Ys?,Zs).\nmerge([],[],[]).`
- [X] T006 Re-read `GLP_ART.pdf` book p 31 (PDF p 43) byte-exactly for `producer/2` + `consumer/3` definitions (chapter 4 §4.2.1 + §4.2.2 "Producers and Consumers"). Re-read the immediately surrounding prose ("A producer that counts down from N" + "A consumer that sums stream elements" + Formal 4.2 SRSW in Continuation Calls) for the cross-chapter import provenance comment. Note byte-exact form per `contracts/glp-file-format.md` File 2 spec.
- [X] T007 Re-read `GLP_ART.pdf` book p 22 (PDF p 34) byte-exactly for THREE separate idioms: (a) `channel/1` defined-guard type test + `process/2` two-clause dispatch (locked per Q2 for ex-02); (b) `lookup/3` complete with both clauses including the `~(=?=)` negation (locked per Q3 for ex-03). Re-read the §3.2 introduction prose distinguishing built-in / defined / negation guard species. **Critical verification**: confirm the second `lookup/3` clause's head pattern — cons-with-tail (`[(K,_)|Rest]`) vs. two-element-list (`[(K,_), Rest]`). The implementation depends on this literal byte-exact form. If ambiguous, ask project owner to inspect PDF directly. ALSO re-read book p 24 (PDF p 36) for the SRSW Rules for Defined Guards table (referenced in ex-03 trace annotations; not re-encoded as code).
- [X] T008 Confirm subordinate-decomposition decisions with project owner (per `research.md` R-008 + R-009; auto-mode-approved during /speckit-plan unless overridden):
  - **R-008 `handle/1` resolution for ex-02**: define `handle/1` locally as a tautological unit clause `handle(_).` (preserves byte-exactness of `process/2`).
  - **R-009 ex-02 composition**: stand-alone — no `merge/3` duplication.
  - **R-009 ex-03 composition**: stand-alone — no `merge/3` or `channel/1` / `process/2` duplication.

  Wait for explicit approval (or auto-mode "continue to completion now") before any `.glp` writing. Per spec FR-013, this is the plan-then-act gate.
- [X] T009 Confirm the locked inspection goals to project owner per `research.md` R-004 (auto-mode-approved during /speckit-plan unless project owner overrides):
  - **ex-01** (3 goals): `producer(A, 0), producer(B, 0), merge(A?, B?, M), consumer(M?, 0, Sum).` → `Sum = 0`; `producer(A, 0), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` → `Sum = 6`; `producer(A, 1), producer(B, 1), merge(A?, B?, M), consumer(M?, 0, Sum).` → `Sum = 2`.
  - **ex-02** (3 goals): `process(foo, Status).` → `Status = error`; `process(ch([], []), Status).` → `Status = ok`; `process([1,2,3], Status).` → `Status = error`.
  - **ex-03** (3 goals): `lookup(a, [(a,1),(b,2),(c,3)], V).` → `V = 1`; `lookup(c, [(a,1),(b,2),(c,3)], V).` → `V = 3`; `lookup(z, [(a,1),(b,2),(c,3)], V).` → `→ fails` OR `→ suspended` (whichever the runtime produces; trace annotation must document).

  Wait for explicit approval before any REPL run.

**Checkpoint**: Byte-exact code for all four PDF locations in working memory; subordinate decompositions confirmed; inspection goal sets confirmed. User stories may now begin.

---

## Phase 3: User Story 1 — Run Program 3.1 + ch4 exemplar in a composed pipeline (Priority: P1) 🎯 MVP-1/2

**Goal**: Learner loads BOTH `.glp` files (Program 3.1 + producer/consumer pair) and runs the composed primary demo goal `producer(A, 5), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` observing `Sum = 21`. Empirically verifies the locked binding from spec Clarifications Q1.

**Independent Test**: REPL accepts both `.glp` files (no procedure-redeclaration conflict); composed primary goal succeeds with locked binding `Sum = 21`; three inspection goals produce documented bindings (per SC-002, SC-003, SC-004).

### Implementation for User Story 1

- [X] T010 [US1] Create directory `olamni/tutorial/ch03/exercise-01/`.
- [X] T011 [US1] Write `olamni/tutorial/ch03/exercise-01/ch-03-ex-01-glp-fair-stream-merger.glp` per `contracts/glp-file-format.md` File 1 spec — Program 3.1 byte-exact from PDF p 15 (per T005), header block paraphrasing §3.1 prose on Reader/Writer pairs + SO Invariant + GLP operational semantics, three `%%` paraphrase comments (one per merge clause). **Verification step (per spec SC-006)**: after writing the file, strip the header comment block and the per-clause `%%` annotations; the remaining three-line clause corpus MUST equal the byte-exact form recalled in T005. If any byte differs, HALT and re-read PDF p 15 byte-exactly before re-writing.
- [X] T012 [US1] Write `olamni/tutorial/ch03/exercise-01/ch-03-ex-01-producer-consumer.glp` per `contracts/glp-file-format.md` File 2 spec — `producer/2` + `consumer/3` byte-exact from PDF p 31 (per T006), header block with the canonical R-007 cross-chapter provenance lines (six lines including the inherited-`:=` line), four `%%` paraphrase comments (one per producer/consumer clause). **Verification step (per spec SC-007)**: after writing the file, strip the header comment block and the per-clause `%%` annotations; the remaining four-clause corpus MUST equal the byte-exact form recalled in T006. If any byte differs, HALT.
- [X] T013 [US1] Verify both `.glp` files load without error or procedure-redeclaration conflict: run `"$DART" run glp_runtime/.dart_tool/repl.dill` with input loading first the merger, then the producer-consumer pair, then `:quit`. Expect `✓ Loaded:` for BOTH files. If either is rejected, HALT and report. If procedure-redeclaration conflict surfaces (none expected since the imported procedures are `producer/2` + `consumer/3`, not `merge/3`), HALT and amend per FR-013.
- [X] T014 [US1] Run the composed primary goal `producer(A, 5), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` under the REPL with both files loaded. Expect locked binding `Sum = 21` and `→ succeeds`. If mismatch, HALT and report (do NOT silently overwrite spec — propose Clarifications amendment per ch02 Q3a precedent).
- [X] T015 [US1] Run the three approved inspection goals from T009 (ex-01 set) in order. Expect: `Sum = 0`, `Sum = 6`, `Sum = 2`. Capture stdin + stdout verbatim for each. Verify all THREE Program 3.1 clauses fired across the four-goal session (per FR-018) — clause 1 + clause 2 alternating in primary + inspection 3; clause 3 in primary (end), inspection 1 (immediate), inspection 2 (after stream B exhausts), inspection 3 (end). If any clause not exercised, HALT and report.

**Checkpoint**: Both `.glp` files written, composed pipeline verified, all three Program 3.1 clauses exercised, all four ex-01 goal captures in hand. US1 deliverable in hand.

---

## Phase 4: User Story 2 — Step-through guide + trace for ex-01 (Priority: P1) 🎯 MVP-2/2

**Goal**: Learner has a step-through guide (`ex-01-tutorial.md`) and a verbatim captured trace (`ex-01-repl-trace.md`) covering the load of BOTH `.glp` files plus the composed primary plus the three inspection goals.

**Independent Test**: Reader follows `ex-01-tutorial.md` start-to-finish on a fresh machine; their REPL output matches `ex-01-repl-trace.md` byte-for-byte modulo timestamps (per SC-005).

### Implementation for User Story 2

- [X] T016 [US2] Write `olamni/tutorial/ch03/exercise-01/ex-01-repl-trace.md` per `contracts/trace-file-format.md` (six phases for ex-01: Phase A = Program 3.1 load, Phase B = producer-consumer load, Phase C = composed primary goal, Phases D-E-F = three inspection goals). Code-block content byte-verbatim from T013 + T014 + T015 captures. Annotation between Phase B and Phase C explicitly explains the cross-chapter composition per the contract: "the composed primary goal references procedures from BOTH loaded `.glp` files; SRSW pairing connects four roles (producer A, producer B, merger, consumer)". Strict byte-equality contract per FR-014.
- [X] T017 [US2] Write `olamni/tutorial/ch03/exercise-01/ex-01-tutorial.md` — learner-targeted step-through guide. Sections: "Before you start" (read §3.1 + skim §3.2 to know the guard species ahead); "Building the REPL" (one-time, point to ch01 / ch02 quickstart for full instructions); "The exercise" (six steps mirroring the trace phases — load Program 3.1, load producer-consumer, run composed primary observing the producer-merger-consumer SRSW pipeline, run three inspection goals exercising different clauses); "Cross-check against the captured trace"; "What you've learned" (SRSW reader/writer pairs across multiple roles + cross-chapter import as a documented exception + built-in guards as the foundation; ex-02 + ex-03 will introduce defined guards + negation).

**Checkpoint**: Learner-facing tutorial + verbatim trace exist; trace satisfies SC-005 byte-equality contract. MVP (US1+US2 = ex-01 complete) in hand.

---

## Phase 5: User Story 3 — Chapter signpost (Priority: P2)

**Goal**: `ch03_tutorial.md` exists; lists exercise-01 with one-line summary; documents the cross-chapter import; outlines the §3.2 guard curriculum (built-in → defined → negation across the three exercises); status block grep-friendly per `contracts/status-block-format.md`.

**Independent Test**: `ch03_tutorial.md` exists; `grep -E "^- exercise-NN:" olamni/tutorial/ch03/ch03_tutorial.md` returns exactly three matches in order.

### Implementation for User Story 3

- [X] T018 [US3] Write `olamni/tutorial/ch03/ch03_tutorial.md` (chapter signpost, **underscore** filename per workflow memory). Sections: "Chapter 3 — GLP Core" intro (formal presentation of GLP semantics + §3.2 guard species; the substrate that chapters 4+ build on); "How to work with this chapter's tutorial code" (read §3.1+§3.2, build REPL, pick exercise from status block); "Cross-chapter import" (plain-prose explanation of the §4.2.1 + §4.2.2 producer/consumer pair and why ch03 imports it); "§3.2 Guard Curriculum" (plain-prose outline of the three-step progression: ex-01 built-in → ex-02 defined → ex-03 negation); "Exercises" (links to all three with one-line summaries; ex-02 / ex-03 visibly marked as planned/pending until they exist); status block per `contracts/status-block-format.md` initial state (`exercise-01: pending review`, `exercise-02: pending exercise-01 approval`, `exercise-03: pending exercise-02 approval`); "Sources" (links to ch03-sources.md + ch04-sources.md + the deprecated spec rev-eng-input).
- [X] T019 [US3] Verify the status block is grep-friendly: `grep -E "^- exercise-NN:" olamni/tutorial/ch03/ch03_tutorial.md` returns exactly three matches in order (`exercise-01`, `exercise-02`, `exercise-03`).

**Checkpoint**: Chapter signpost discoverable; status block enforceable. US3 complete.

---

## Phase 6: User Story 6 — Top-level index update (Priority: P3, partial)

**Goal**: `olamni/tutorial/tutorial.md` (already exists from ch01 + ch02) is extended; chapter-3 row flips from `planned` to `pending review (YYYY-MM-DD)` initially, then to `implemented YYYY-MM-DD` after all exercises approved (final flip in T043).

**Independent Test**: `olamni/tutorial/tutorial.md` chapter-3 row links to `ch03/ch03_tutorial.md` (no broken link); status text reflects current state.

### Implementation for User Story 6

- [X] T020 [US6] Edit `olamni/tutorial/tutorial.md` — flip ch03 row from `planned` to `pending review (YYYY-MM-DD)` where `YYYY-MM-DD` is the ISO date the implementer runs this step (e.g., `pending review (2026-05-02)` if implementation runs on 2 May 2026). Link target changes from `ch03/ch03-sources.md` to `ch03/ch03_tutorial.md`. (Final flip to `implemented YYYY-MM-DD` happens in Phase 11 T045 after all three exercises are approved.) Chapters 4–13 rows unchanged.

**Checkpoint**: Top-level index reflects ch03 in flight. US6 partial complete (final state set in T043).

---

## Phase 7: ex-01 approval gate

- [X] T021 [US1+US2+US3] Run baseline tests post-ex-01-implementation: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh`. Expect identical baseline number to T004 (494/494 or 485/485).
- [X] T022 [US1+US2+US3] Show ex-01 implementation diff to project owner. Wait for explicit `approved` signal (or auto-mode "continue to completion now").
- [X] T023 [US1+US2+US3] On approval: edit `ch03_tutorial.md` status block to flip `exercise-01: approved YYYY-MM-DD` and `exercise-02: pending review`. Commit (`git add` SPECIFIC files only — see commit-scope discipline).

**Checkpoint**: ex-01 approval gate passed. Phase 8 (ex-02) becomes unblocked.

---

## Phase 8: User Story 4 — ex-02 §3.2 defined guards (Priority: P2, GATED)

**⚠️ GATE**: T023 must have flipped `exercise-01: approved` AND ex-01 trace must have covered all "thoroughly REPL-tested" criteria (per FR-008): every Program 3.1 clause exercised, both `.glp` files exercised, primary + 3 inspection goals captured.

**Goal**: Learner studies `channel/1` + `process/2` (locked shape per Clarifications Q2) which demonstrates §3.2's defined-guard machinery — a unit-clause defined guard `channel/1` unfolded at `process/2` clause 1's guard site.

**Independent Test**: Run `process(ch(a, b), Status).` against the loaded ex-02 file; observe `Status = ok` AND `→ succeeds` (per spec FR-009 locked binding + Clarifications Q2).

### Implementation for User Story 4

- [X] T024 [US4] Pre-flight gate: `grep -E "^- exercise-01: approved" olamni/tutorial/ch03/ch03_tutorial.md` MUST return one match. If not, HALT.
- [X] T025 [US4] Create directory `olamni/tutorial/ch03/exercise-02/`.
- [X] T026 [US4] Write `olamni/tutorial/ch03/exercise-02/ch-03-ex-02-defined-guards.glp` per `contracts/glp-file-format.md` File 3 spec and `research.md` R-008 + R-009. Define `channel/1` unit clause byte-exact from PDF p 22 (per T007). Define `process/2` two clauses byte-exact from PDF p 22. Define `handle/1` locally as `handle(_).` (per R-008 stand-alone stub decision approved at T008). Stand-alone — no `merge/3` duplication (per R-009). Header block + four `%%` paraphrase comments per R-001.
- [X] T027 [US4] Verify the file is ACCEPTED at load. If rejected, HALT.
- [X] T028 [US4] Run primary goal `process(ch(a, b), Status).` Expect locked binding `Status = ok`. If mismatch, HALT.
- [X] T029 [US4] Run three approved inspection goals (ex-02 set from T009): `process(foo, Status).`, `process(ch([], []), Status).`, `process([1,2,3], Status).`. Expect: `Status = error`, `Status = ok`, `Status = error`. Capture verbatim. Verify BOTH `process/2` clauses fired (clause 1 in primary + inspection 2; clause 2 in inspections 1 + 3) AND `channel/1` unit clause exercised — if either not exercised, HALT.
- [X] T030 [US4] Write `ex-02-repl-trace.md` per `contracts/trace-file-format.md` (five phases). Strict byte-equality contract per FR-014 — no relaxation. Phase B annotation MUST identify that the `channel/1` defined guard succeeded at `process/2` clause 1's guard site. Phase C annotation MUST identify the `otherwise` fallback selection.
- [X] T031 [US4] Write `ex-02-tutorial.md` — learner step-through emphasising the defined-guard machinery: the unit clause `channel(ch(_, _)).` becomes a guard predicate that the compiler unfolds at `channel(X?)` guard sites; the §3.2 distinction between built-in (used in ex-01) and defined (used here) guard species; setup for ex-03's negation form.

**Checkpoint**: ex-02 fully landed; awaiting approval.

---

## Phase 9: ex-02 approval gate

- [X] T032 [US4] Run baseline tests post-ex-02-implementation: expect identical baseline number to T004.
- [X] T033 [US4] Show ex-02 diff to project owner. Wait for `approved` signal.
- [X] T034 [US4] On approval: edit `ch03_tutorial.md` status block to flip `exercise-02: approved YYYY-MM-DD` and `exercise-03: pending review`. Commit.

**Checkpoint**: ex-02 approval gate passed. Phase 10 (ex-03) becomes unblocked.

---

## Phase 10: User Story 5 — ex-03 §3.2 guard negation (Priority: P3, GATED)

**⚠️ GATE**: T034 must have flipped `exercise-02: approved` AND ex-02 trace must have covered all "thoroughly REPL-tested" criteria.

**Goal**: Learner studies `lookup/3` complete with both clauses (locked shape per Clarifications Q3) — clause 1 with positive `=?=`, clause 2 with negated `~(=?=)` on the same operator. Demonstrates that the `~(...)` form is restricted to negatable built-in guards per the §3.2 SRSW Rules table on book p 24.

**Independent Test**: Run `lookup(b, [(a,1),(b,2),(c,3)], V).` against the loaded ex-03 file; observe BOTH clauses firing in sequence (clause 2 descends past `(a,1)`; clause 1 matches `(b,2)`); `V = 2` AND `→ succeeds` (per spec FR-010 locked binding + Clarifications Q3).

### Implementation for User Story 5

- [X] T035 [US5] Pre-flight gate: `grep -E "^- exercise-02: approved" olamni/tutorial/ch03/ch03_tutorial.md` MUST return one match. If not, HALT.
- [X] T036 [US5] Create directory `olamni/tutorial/ch03/exercise-03/`.
- [X] T037 [US5] Write `olamni/tutorial/ch03/exercise-03/ch-03-ex-03-guard-negation.glp` per `contracts/glp-file-format.md` File 4 spec and `research.md` R-009. Define `lookup/3` byte-exact from PDF p 22 (per T007) — BOTH clauses, including the second clause's `~(Key? =?= K?)` negation on a built-in negatable guard. Stand-alone — no `merge/3` or `channel/1` / `process/2` duplication (per R-009). Header block + two `%%` paraphrase comments. **Verification step**: confirm the second clause's head pattern matches T007's byte-exact PDF re-read (cons-with-tail vs. two-element list).
- [X] T038 [US5] Verify the file is ACCEPTED at load. If rejected, HALT (especially if `~(...)` form is parser-rejected — per spec edge case, halt-and-report; do NOT work around).
- [X] T039 [US5] Run primary goal `lookup(b, [(a,1),(b,2),(c,3)], V).` Expect locked binding `V = 2`. If mismatch, HALT.
- [X] T040 [US5] Run three approved inspection goals (ex-03 set from T009): `lookup(a, [(a,1),(b,2),(c,3)], V).`, `lookup(c, [(a,1),(b,2),(c,3)], V).`, `lookup(z, [(a,1),(b,2),(c,3)], V).`. Expect: `V = 1`, `V = 3`, `→ fails`. Capture verbatim. Verify BOTH `lookup/3` clauses fired (clause 1 alone in inspection 1; clause 2 followed by clause 1 in primary + inspection 2; clause 2 only in inspection 3) — if either not exercised, HALT. **If inspection 3 produces `→ suspended` instead of `→ fails`, HALT and report as a runtime anomaly per Principle II — the input list is fully ground; suspension on the empty residue indicates a runtime issue worth investigating BEFORE proceeding with ex-03.**
- [X] T041 [US5] Write `ex-03-repl-trace.md` per `contracts/trace-file-format.md` (five phases). Strict byte-equality contract per FR-014 — NO relaxation since ch3 has no wallclock-derived output. Phase B annotation MUST identify the two-clause sequence (clause 2 first, then clause 1). Phase E annotation MUST document whichever no-match outcome the runtime produced AND reference the §3.2 SRSW Rules for Defined Guards table on book p 24 to remind the learner that `=?=` is negatable but defined guards (e.g., ex-02's `channel/1`) are not.
- [X] T042 [US5] Write `ex-03-tutorial.md` — learner step-through emphasising the guard-negation form: `~(=?=)` succeeds when the equality test fails; the recursion descends only when the negative branch fires; the §3.2 SRSW Rules distinction between negatable built-in guards (`=?=` and friends) and non-negatable defined guards (e.g., ex-02's `channel/1`).

**Checkpoint**: ex-03 fully landed; awaiting approval.

---

## Phase 11: ex-03 approval gate + chapter complete

- [X] T043 [US5+US6] Run baseline tests post-ex-03-implementation: expect identical baseline number to T004.
- [X] T044 [US5] Show ex-03 diff to project owner. Wait for `approved` signal.
- [X] T045 [US5+US6] On approval:
  - Edit `ch03_tutorial.md` status block to flip `exercise-03: approved YYYY-MM-DD`.
  - Edit `olamni/tutorial/tutorial.md` ch03 row from `pending review (…)` to `implemented YYYY-MM-DD`.
  - Commit.

**Checkpoint**: All three exercises approved; chapter 3 complete in the top-level index.

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Final audits, no-fabrication check, full-suite verification, branch push, merge instructions.

- [X] T046 [P] No-fabrication audit: verify all files under `specs/004-tutorial-ch03/` (excluding `QUARANTINE-DO-NOT-USE/`) are proper `/speckit-*` outputs. List the files and confirm each was generated by /speckit-specify, /speckit-clarify, /speckit-plan, or /speckit-tasks. Per spec FR-012 + SC-011.
- [X] T047 [P] Verify FR-015 (no extraneous cross-chapter imports beyond the locked Q1 producer/consumer): grep all four ch03 `.glp` files for any procedure name from chapters other than ch3 + ch4 §4.2.1+§4.2.2. Should match only Program 3.1's `merge/3`, the imported `producer/2` + `consumer/3`, ex-02's locked `channel/1` + `process/2` + local `handle/1` stub, ex-03's `lookup/3`. Any other chapter reference is a violation; HALT and report.
- [X] T048 [P] Verify FR-016 (test harness exclusion): `grep "olamni/tutorial/ch03" test/run_all_tests.sh` MUST return zero matches. Per SC-014.
- [X] T049 [P] Verify SC-015 (body-kernel scope): grep all four ch03 `.glp` files. Lines containing `:=` MUST appear ONLY in `ch-03-ex-01-producer-consumer.glp` (inside the `producer/2` and `consumer/3` recursive clauses byte-exact from PDF p 31, per FR-015 amendment). Lines containing `now/1` or `'_output'/1` MUST NOT appear in ANY ch03 `.glp` file (per SC-015). Any violation is a HALT.
- [X] T050 [P] Verify SC-016 (§3.2 guard curriculum observable across exercises): inspect the four `.glp` files. ex-01's two files MUST use ONLY built-in guards (`>`, `ground` — no `~(...)` form, no `channel/1` defined guard). ex-02's file MUST use `channel/1` defined guard at a guard position (no `~(...)` form yet). ex-03's file MUST use the `~(=?=)` negation form on `=?=` (a built-in negatable guard) — MUST NOT contain `~(channel(...))` or any defined-guard negation.
- [X] T051 Final baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh`. Expect identical baseline to T004 (494/494 or 485/485). If diverges, HALT — investigate which test regressed and why; ch03 work touches only `olamni/tutorial/ch03/**`, so any harness regression indicates an unrelated bug or accidental scope creep.
- [X] T052 Trace reproducibility check (SC-005): re-run all three traces against the existing `.glp` files and `diff` against the committed `.md` files modulo REPL banner / build wallclock lines. ALL THREE traces MUST be byte-identical (no per-run-variation relaxation in chapter 3 — no wallclock content exists to vary).
- [X] T053 [P] Walk-through verification (SC-001 — soft): note that this requires an external fresh-eyes reader and cannot be self-tested; log as a known follow-up rather than blocking.
- [X] T054 Commit + push branch `004-tutorial-ch03`. Per Constitution multi-Claude protocol — `git add` SPECIFIC files only, never `git add -A` or `git add .`. Specifically, stage only the files this session created or modified under `specs/004-tutorial-ch03/` and `olamni/tutorial/ch03/` and `olamni/tutorial/tutorial.md` and `CLAUDE.md`.
- [X] T055 Provide merge instructions to project owner per the workflow memory's mandatory format:
  ```bash
  cd D:/bstdev/research/glp/glp
  git checkout main
  git pull origin main
  git fetch origin 004-tutorial-ch03
  git merge -m "Merge 004-tutorial-ch03 into main" origin/004-tutorial-ch03
  git push origin main
  ```

**Checkpoint**: Chapter 3 fully delivered, audited, and ready for merge. Constitution Principle V (Test-First) satisfied (baseline preserved); Principle VI (Charter Compliance) satisfied (charter cited; no fabricated specs).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001 → T002 → T003 → T004 sequential.
- **Foundational (Phase 2)**: T005 + T006 + T007 (PDF re-reads, all needed) + T008 (subordinate decisions) + T009 (inspection goals) — all required before any user story. T008 + T009 require explicit project-owner approval (gates; auto-mode-satisfiable).
- **User Stories (Phase 3+)**: All depend on Phase 2 complete.
  - **MVP (US1+US2 = ex-01)** sequential: T010 → T011 → T012 → T013 → T014 → T015 (US1 done) → T016 → T017 (US2 done).
  - US3 (T018–T019, signpost) depends on ex-01 files existing (so it can link them) → run after T017.
  - US6 partial (T020, top-level index) depends on US3 (signpost link target) → run after T019.
  - **Approval gate (Phase 7)**: T021 → T022 → T023 — gate is project-owner-approval signal.
  - US4 (T024–T031, ex-02) GATED behind T023 (`exercise-01: approved`).
  - US5 (T035–T042, ex-03) GATED behind T034 (`exercise-02: approved`).
- **Polish (Phase 12)**: T046, T047, T048, T049, T050, T053 [P] independent. T051 depends on all exercises landed. T052 depends on traces existing. T054 + T055 final.

### Within Each User Story

- US1 (T010-T015): mkdir → write Program 3.1 `.glp` → write producer/consumer `.glp` → verify both load → run composed primary → run inspections.
- US2 (T016-T017): write trace from US1 captures → write tutorial referencing trace.
- US3 (T018-T019): write signpost → verify status block grep-friendly.
- US4 (T024-T031): gate-check → mkdir → write `.glp` → verify load → run primary + inspections → write trace → write tutorial.
- US5 (T035-T042): same shape as US4 with negation-form-specific verification.

### Approval Gates

| Gate | Blocks | Set by |
|---|---|---|
| T008 (subordinate decompositions confirmed) | All Phase 3+ | Auto-mode-approved during /speckit-plan; project owner may override at T008 |
| T009 (inspection goals confirmed) | All Phase 3+ | Auto-mode-approved during /speckit-plan; project owner may override at T009 |
| T022 (ex-01 diff approved) | T023 | Project owner explicit reply |
| T023 (`exercise-01: approved`) | T024+ (Phase 8) | T023 itself, after T022 |
| T033 (ex-02 diff approved) | T034 | Project owner explicit reply |
| T034 (`exercise-02: approved`) | T035+ (Phase 10) | T034 itself, after T033 |
| T044 (ex-03 diff approved) | T045 | Project owner explicit reply |

### Parallel Opportunities

- **Phase 1**: All sequential (each step builds on the prior).
- **Phase 2**: T005 + T006 + T007 PDF re-reads can be sequenced or parallel-conceptual; in practice the implementer reads one PDF location at a time.
- **Phase 12**: T046, T047, T048, T049, T050, T053 [P] — different audits, different files, no shared state.
- US4 vs US5: NO parallelism (US5 gated on US4 approval).
- US2 vs US3 vs US6: weakly parallelisable (different files), but in practice US2 → US3 → US6 sequential because each references the prior.
- Most tasks are sequential within an exercise; parallelism is limited because the feature is documentation + REPL captures.

---

## Parallel Example: Phase 12 polish

```bash
# T046, T047, T048, T049, T050, T053 can run in parallel:
Task: "No-fabrication audit of specs/004-tutorial-ch03/"
Task: "Cross-chapter-import scope check via grep across the 4 .glp files"
Task: "Test harness exclusion check via grep test/run_all_tests.sh"
Task: "Body-kernel scope check via grep for := / now / '_output'"
Task: "§3.2 guard curriculum observability check across the 4 .glp files"
Task: "Walk-through verification log entry for SC-001"
```

---

## Implementation Strategy

### MVP First (US1 + US2 = ex-01)

1. Complete Phase 1: Setup (T001–T004).
2. Complete Phase 2: Foundational (T005–T009 — inc. inspection-goal + subordinate-decomposition confirmations).
3. Complete Phase 3: US1 (T010–T015) — both `.glp` files + composed primary + inspections.
4. Complete Phase 4: US2 (T016–T017) — trace + tutorial.
5. **STOP and VALIDATE**: ex-01 is fully usable for a learner who knows where to find the file.

### Add discoverability (US3 + US6 partial)

6. Complete Phase 5: US3 (T018–T019) — chapter signpost.
7. Complete Phase 6: US6 partial (T020) — top-level index flip to `pending review`.
8. **STOP and VALIDATE**: A learner arriving at `olamni/tutorial/tutorial.md` can navigate to ch03 and the exercise.

### Approval + ex-02 (US4)

9. Complete Phase 7: ex-01 approval gate (T021–T023).
10. Complete Phase 8: US4 (T024–T031) — ex-02 with `channel/1` + `process/2` defined guard.
11. Complete Phase 9: ex-02 approval gate (T032–T034).

### ex-03 (US5)

12. Complete Phase 10: US5 (T035–T042) — ex-03 with `lookup/3` guard negation.
13. Complete Phase 11: ex-03 approval gate + final flip (T043–T045).

### Polish + commit

14. Complete Phase 12: Polish (T046–T055).

---

## Notes

- [P] tasks = different files, no shared deps — parallelisable.
- [Story] label maps tasks to spec.md user stories (US1–US6).
- **Composite [USN+USM+...] labels** are intentional for cross-story tasks: approval-gate tasks (T021 / T022 / T023, T032 / T033 / T034, T043 / T044 / T045) span all user stories whose exercise is being approved; T045 covers both US5 (ex-03 approval flip) and US6 (top-level index final flip). These are NOT a format violation — they accurately reflect that the task closes multiple stories in one logical step.
- US4 and US5 are **gated** — cannot start until predecessor's `approved` flag is set in `ch03_tutorial.md`.
- Per spec FR-013 and Constitution Principle I (Spec-First) + Discussion Mode default, every task that writes a file MUST be presented to project owner before action; this tasks.md is the plan, but the implementation cycle still respects plan-then-act per task.
- Per spec FR-012 and the no-fabrication discipline: **Claude does NOT write speckit-format `spec.md`-style files for this or any other chapter**. T046 verifies this.
- Per spec FR-015 (cross-chapter import scope, including the body-kernel-inheritance amendment) + FR-016 (test harness exclusion), these are testable via grep — T047 + T048 + T049 + T050.
- Constitution Principle II: any obstacle (Dart absent, REPL build fail, binding mismatch, SRSW error on a GLP file, parser rejection of `~(...)` form, ambiguous PDF transcription) → HALT and report. NEVER `skipSRSW`, NEVER catch-and-ignore, NEVER silently substitute a locked shape (Q1 / Q2 / Q3) with a different one — propose a Clarifications amendment per FR-013.
- Commit cadence: one commit per logical group (Setup, Foundational, US1+US2, US3+US6 partial, ex-01 approval, US4, ex-02 approval, US5, ex-03 approval+flip, Polish). Per Constitution multi-Claude protocol — `git add` SPECIFIC files, never `git add -A`.
- Constitution Principle V: baseline tests run before AND after — T004 + T021 + T032 + T043 + T051. ALL must show identical baseline number.
