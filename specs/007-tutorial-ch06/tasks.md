---

description: "Task list for Olamni Tutorial Chapter 6 — Typed Programming"
---

# Tasks: Olamni Tutorial — Chapter 6 (Typed Programming)

**Input**: Design documents from `specs/007-tutorial-ch06/`
**Prerequisites**: plan.md, spec.md (with **2 Clarifications Q1+Q2**), research.md (R-001..R-009), data-model.md, contracts/ (3 files), quickstart.md
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V AND the R-006 type-checker operational verification per FR-018 (inherited from ch05). All 5 ch06 source Programs are SRSW-compliant by byte-exact construction (Principle III). Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI.

**Tests**: Captured REPL traces ARE the regression artifacts. No new Dart unit tests. Per FR-016, ch06 files NOT in `test/run_all_tests.sh`. Baseline `bash test/run_all_tests.sh` MUST pass before AND after implementation per Principle V (count unchanged from ch05 ship state — 494/494 expected per workflow memory). R-006 type-checker verification at T006a re-verifies against the build in use at /speckit-implement runtime.

**Organization**: Tasks grouped by user story per spec.md (one user story per exercise: US1 = ex-01 §6.1, US2 = ex-02 §6.2, US3 = ex-03 §6.3, US4 = ex-04 §6.4, US5 = ex-05 §6.5). Pairwise gates between exercises per FR-008 + `contracts/status-block-format.md`. Plus US6 (chapter signpost) and US7 (top-level index) interleaved.

**Pairwise-gate authority**: `grep -E "^- exercise-0NN: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch06/ch06_tutorial.md` MUST return ≥1 match before ex-(NN+1) work begins. Four gates total (between ex-01→ex-02, ex-02→ex-03, ex-03→ex-04, ex-04→ex-05).

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1..US7).

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verify Dart SDK: `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. Set `DART="/c/Users/gavri/dart-sdk/bin/dart"`.
- [ ] T002 Verify or rebuild REPL exe at `glp_runtime/glp_repl.exe`. Use `--define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')"`. Verify banner `Built from: <commit>` matches `Repo HEAD: <commit>` (no STALE BINARY warning).
- [ ] T003 Verify `.gitignore` covers `glp_runtime/glp_repl*` and `glp_runtime/.dart_tool/` (inherited from ch01–ch05).
- [ ] T004 Record baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — record actual baseline (494/494 expected from ch05 ship state).
- [ ] T005 Verify spec inputs: `specs/007-tutorial-ch06/spec.md`, `olamni/tutorial/ch06/ch06-specification-input-prompt.md`, `olamni/tutorial/ch06/ch06-sources.md`, `olamni/tutorial/ch06/spec-rev-eng-input/ch06-DEPRECATED-spec.md` all exist.
- [ ] **T006a** R-006 type-checker operational verification per FR-018 against CURRENT REPL build (inherited from ch05 R-006): (a) load a known-good ch05 typed `.glp` (e.g., `olamni/tutorial/ch05/exercise-05/ch-05-ex-05-typed-quicksort.glp`); confirm `✓ Loaded:` + zero errors. (b) load a known-bad ch05 negative-form `.glp` (e.g., `olamni/tutorial/ch05/exercise-06/ch-05-ex-06-type-error-failing.glp`); confirm load FAILS with the documented type-error message. If positive case fails OR negative case loads cleanly → HALT per FR-013 (ch06 cannot proceed against a broken type-checker). Append both captured outputs to research.md Appendix A.
- [ ] **T006b** Re-verify ch06 PDF stub state per FR-015: read book p 53 of `GLP_ART.pdf` byte-exactly. Confirm only chapter title + 5 section headings (§6.1 Difference Lists, §6.2 Quicksort, §6.3 Equators: Emergency Brake, §6.4 Bidirectional Communication, §6.5 Buffered Communication) exist; no body text, no Programs. HALT per FR-015 if any body text has been added (do NOT silently fold native content into synthesised exercises).

**Checkpoint**: Phase 1 complete — Dart, REPL, baseline, spec inputs, type-checker pre-flight, ch06 stub-state re-verified.

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T007 Re-read source PDFs for each exercise byte-exactly (per FR-003 + ch01–ch05 lesson — sources files have drifted by single characters):
  - ex-01: `GLP_ART.pdf` book pp 38–39 (PDF pp 50–51) for ch04 §4.3.7 `flatten/2` + `flatten_acc/3`.
  - ex-02: book p 51 (PDF p 63) for ch05 §5.6 typed quicksort (including ch05 Q10 dual amendments — qsort declaration `(NumList?, NumList, NumList?)` + interleaved layout).
  - ex-03: book p 42 (PDF p 54) for ch04 §4.4.4 control MI `run/5` + `suspended_run/4`.
  - ex-04: book p 23 (PDF p 35) for ch03 §3.2 channel ops `send/3` + `receive/3` + `new_channel/2` + `relay/3` + `make_pair/2`.
  - ex-05: book pp 34–35 (PDF pp 46–47) for ch04 §4.2.12 + §4.2.13 `bb/0` + `bb_test/0` (with `producer/2` + `consumer/2` helpers).
  Note any drift vs `chXX-sources.md`; correct sources files BEFORE proceeding. Per ch01 R-006 lesson, this is non-negotiable. Extra attention to `?` reader marks, `;` alternation separators, `|` list-cons separators.
- [ ] T008 Confirm subordinate decisions with project owner (auto-mode-approved during /speckit-plan):
  - R-007 declaration shapes per Q2 deferral: sketches in research.md Table R-007 are LOCKED at /speckit-implement T-PROPOSE per exercise; project owner approves; locked shape recorded in research.md.
  - R-008 cross-chapter relationship contract: synthesis-from-earlier-chapters; documented in 3 sites per FR-014 (`.glp` header, signpost prose, top-level footnote).
  - R-009 filenames: locked per `contracts/glp-file-format.md` File spec (5 files; one .glp each; no two-file pattern).
  - R-004 inspection goals: deferred to T-PROPOSE within each exercise task block; each exercise has primary + 3 inspection goals exercising every clause.

**Checkpoint**: Phase 2 complete — PDF re-reads done; subordinate decisions confirmed.

---

## Phase 3: User Story 1 — ex-01 §6.1 Difference Lists (P1)

**Predecessor gate**: Phase 2 complete + R-006 type-checker pre-flight PASSED at T006a.

- [ ] T010 [US1] Create `olamni/tutorial/ch06/exercise-01/`.
- [ ] **T011-PROPOSE** [US1] Per Q2 deferral, propose locked declaration shape per R-007 sketch: `NestedList ::= [] ; [Atom | NestedList] ; [NestedList | NestedList].` (or similar) + `procedure flatten(NestedList?, List).` + `procedure flatten_acc(NestedList?, List?, List).`. Show to project owner; await approval; record locked shape as a row appended to research.md R-007 table.
- [ ] **T011-GOAL-PROPOSE** [US1] Propose primary demo goal + 3 inspection goals exercising every clause of `flatten/2` + `flatten_acc/3`. Example: primary `flatten([[1,2],[3,[4,5]]], Out).` → `Out = [1,2,3,4,5]`; inspection 1 `flatten([], Out).` → `Out = []`; inspection 2 `flatten([[1]], Out).` → `Out = [1]`; inspection 3 `flatten([1,2,3], Out).` → `Out = [1,2,3]`. Show to project owner; await approval; record locked bindings in research.md.
- [ ] T012 [US1] Write `ch-06-ex-01-difference-lists.glp` per `contracts/glp-file-format.md`: header block (synthesis cross-reference per R-008 — cite ch04 §4.3.7, book pp 38–39, Q1 clarification) + locked declarations + byte-exact clauses from ch04 §4.3.7 + per-clause `%%` paraphrase comments per FR-005 (charter §1.5).
- [ ] T013 [US1] REPL load verification: `printf "<absolute path>\n:quit\n" | $DART run repl.dill` → `✓ Loaded:` + zero errors. If rejected, HALT per FR-013 — propose declaration-shape amendment (byte-exact source clauses are LOCKED per Q2; declarations are amendable).
- [ ] T014 [US1] Run 4-goal REPL session (1 primary + 3 inspection); capture trace verbatim. Bindings MUST match locked values; mismatch is HALT per FR-013.
- [ ] T015 [US1] Write `ex-01-repl-trace.md` per `contracts/trace-file-format.md` (5-phase positive: Phase A load + Phase B primary + Phase C/D/E inspections). Strict byte-equality per FR-012; no per-run-variation expected.
- [ ] T016 [US1] Write `ex-01-tutorial.md` — learner step-through. Walks through reading the file + loading + observing `✓ Loaded:` + running the 4 goals + cross-checking against the trace. Explicit synthesis-explanation prose per R-008.

### Chapter signpost + top-level index (interleaved with ex-01)

- [ ] T040 [US6] Write `olamni/tutorial/ch06/ch06_tutorial.md` per `contracts/status-block-format.md` initial state (5 status lines). Document: chapter is synthesised from ch01–ch05 because PDF p 53 is a stub; per-exercise synthesis source line; pairwise approval gates; build instructions inherited from ch01–ch05; Sources cross-reference (each exercise → §6.x heading + earlier-chapter source).
- [ ] T041 [US6] Verify status block grep-friendly: `grep -E "^- exercise-NN:" ch06_tutorial.md` returns 5 matches.
- [ ] T042 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch06 row from `planned` to `pending review (YYYY-MM-DD)`. Add R-008 third-site footnote: "ch06 content synthesised from ch01–ch05 sources per /speckit-clarify Q1 (PDF chapter is a stub)". Link target → `ch06/ch06_tutorial.md`.

### ex-01 approval gate (Phase 3 exit)

- [ ] T050 [US1+US6+US7] Run baseline tests: PASS expected (494/494 unchanged from ch05 ship state).
- [ ] T051 [US1+US6+US7] Show ex-01 diff to project owner (1 exercise + signpost + top-level index footnote). Wait for approval.
- [ ] T052 [US1+US6+US7] On approval: edit `ch06_tutorial.md` status block to flip `exercise-01` line to `approved YYYY-MM-DD`. Commit `implement(ch06): ex-01 §6.1 Difference Lists landed (synthesised from ch04 §4.3.7 flatten/flatten_acc per Q1)`.

**Checkpoint**: ex-01 approved. Gate-grep `grep -E "^- exercise-01: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch06_tutorial.md` returns 1. ex-02 unblocked.

---

## Phase 4: User Story 2 — ex-02 §6.2 Quicksort (P1)

**Predecessor gate**: ex-01 approved (`grep -E "^- exercise-01: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch06_tutorial.md` returns 1). HALT if 0.

- [ ] T060 [US2] Pre-flight gate check (above grep). HALT if 0.
- [ ] T061 [US2] Create `olamni/tutorial/ch06/exercise-02/`.
- [ ] **T062-GOAL-PROPOSE** [US2] Propose primary + 3 inspection goals. **NO declaration-locking step** — ex-02 declarations are byte-exact from ch05 §5.6 (including ch05 Q10 dual amendments) per `contracts/glp-file-format.md` ex-02 exception. Example: primary `quicksort([3,1,4,1,5,9,2,6], Sorted).` → `Sorted = [1,1,2,3,4,5,6,9]`; inspections cover empty-list, singleton, already-sorted cases. Show to project owner; await approval; record locked bindings.
- [ ] T063 [US2] Write `ch-06-ex-02-typed-quicksort.glp` per `contracts/glp-file-format.md` ex-02 exception: type defs + procedure declarations + clauses ALL byte-exact from ch05 §5.6 (including ch05 Q10 dual amendments — corrected qsort declaration `(NumList?, NumList, NumList?)` + interleaved layout). Header block notes ALL three are byte-exact (NOT just clauses) + cites ch05 §5.6 + ch05 Q10 + ch06 §6.2 heading per R-008. Per-clause `%%` paraphrase per FR-005.
- [ ] T064 [US2] REPL load verification → `✓ Loaded:` (Q11 T4c empirically confirmed loads cleanly with both Q10 amendments). If rejected, HALT per FR-013 — likely a regression in the type-checker between ch05 ship and now; report.
- [ ] T065 [US2] Run 4-goal session; capture trace verbatim. Bindings MUST match locked values.
- [ ] T066 [US2] Write `ex-02-repl-trace.md` per 5-phase positive structure.
- [ ] T067 [US2] Write `ex-02-tutorial.md` — synthesis-explanation prose noting this is a re-presentation of ch05 §5.6 under §6.2.

### ex-02 approval gate

- [ ] T080 [US2] Show ex-02 diff to project owner. Wait for approval.
- [ ] T081 [US2] On approval: flip `exercise-02` line to `approved YYYY-MM-DD`. Commit `implement(ch06): ex-02 §6.2 Quicksort landed (byte-exact from ch05 §5.6 including Q10 dual amendments)`.

**Checkpoint**: ex-02 approved. Gate-grep `grep -E "^- exercise-02: approved" ch06_tutorial.md` returns 1. ex-03 unblocked.

---

## Phase 5: User Story 3 — ex-03 §6.3 Equators: Emergency Brake (P1)

**Predecessor gate**: ex-02 approved. HALT if 0.

- [ ] T090 [US3] Pre-flight gate check. HALT if 0.
- [ ] T091 [US3] Create `olamni/tutorial/ch06/exercise-03/`.
- [ ] **T092-PROPOSE** [US3] Per Q2 deferral, propose locked declaration shape per R-007 sketch: `Goal ::= ...`, `Control ::= suspend ; resume ; abort.`, `ControlStream ::= [] ; [Control | ControlStream].`, plus `procedure run(Goal?, ControlStream?, …).` + `procedure suspended_run(Goal?, ControlStream?, …).`. Goal type is non-trivial; the implementer may reuse ch05's encoding patterns or propose a minimal Goal type sufficient for the abort demo. Show to project owner; await approval; record locked shape.
- [ ] **T092-GOAL-PROPOSE** [US3] Propose primary + 3 inspection goals. Primary MUST demonstrate emergency-brake semantics (a goal running under the control MI receives `abort` on the control stream and halts). Show to project owner; await approval; record locked bindings.
- [ ] T093 [US3] Write `ch-06-ex-03-equators-emergency-brake.glp` per `contracts/glp-file-format.md`: header block per R-008 (synthesis from ch04 §4.4.4, book p 42; "Equators: Emergency Brake" approximated by control-MI's abort message per /speckit-clarify Q1 — input prompt analogue retained) + locked declarations + byte-exact clauses + `%%` paraphrase per FR-005.
- [ ] T094 [US3] REPL load verification → `✓ Loaded:`. HALT per FR-013 if rejected — propose declaration amendment (clauses are LOCKED).
- [ ] T095 [US3] Run 4-goal session; capture trace.
- [ ] T096 [US3] Write `ex-03-repl-trace.md` + `ex-03-tutorial.md`.

### ex-03 approval gate

- [ ] T097 [US3] Show ex-03 diff. Wait for approval. Flip status line. Commit `implement(ch06): ex-03 §6.3 Equators: Emergency Brake landed (synthesised from ch04 §4.4.4 control MI per Q1)`.

**Checkpoint**: ex-03 approved. ex-04 unblocked.

---

## Phase 6: User Story 4 — ex-04 §6.4 Bidirectional Communication (P1)

**Predecessor gate**: ex-03 approved. HALT if 0.

- [ ] T100 [US4] Pre-flight gate check. HALT if 0.
- [ ] T101 [US4] Create `olamni/tutorial/ch06/exercise-04/`.
- [ ] **T102-PROPOSE** [US4] Per Q2 deferral, propose locked declaration shape per R-007 sketch: `Channel ::= ch(Stream, Stream?).` (canonical ch05 §5.5 form per typed-glp-manual.md §5) + `procedure send(Any?, Channel?, Channel).` + `procedure receive(Any, Channel?, Channel).` + `procedure new_channel(Channel, Channel).` + `procedure relay(Stream?, Stream, Channel?).` + `procedure make_pair(Channel, Channel).`. Show to project owner; await approval; record locked shape.
- [ ] **T102-GOAL-PROPOSE** [US4] Propose primary + 3 inspection goals demonstrating bidirectional message flow (`new_channel` allocates a pair; `send` on one end + `receive` on the other delivers the value). Show to project owner; await approval; record locked bindings.
- [ ] T103 [US4] Write `ch-06-ex-04-bidirectional-communication.glp` per `contracts/glp-file-format.md`: header per R-008 (cite ch03 §3.2, book p 23) + locked declarations + byte-exact clauses + `%%` paraphrase.
- [ ] T104 [US4] REPL load verification → `✓ Loaded:`. HALT per FR-013 if rejected.
- [ ] T105 [US4] Run 4-goal session; capture trace.
- [ ] T106 [US4] Write `ex-04-repl-trace.md` + `ex-04-tutorial.md`.

### ex-04 approval gate

- [ ] T107 [US4] Show ex-04 diff. Wait for approval. Flip status line. Commit `implement(ch06): ex-04 §6.4 Bidirectional Communication landed (synthesised from ch03 §3.2 channel ops)`.

**Checkpoint**: ex-04 approved. ex-05 unblocked.

---

## Phase 7: User Story 5 — ex-05 §6.5 Buffered Communication (P1)

**Predecessor gate**: ex-04 approved. HALT if 0.

- [ ] T110 [US5] Pre-flight gate check. HALT if 0.
- [ ] T111 [US5] Create `olamni/tutorial/ch06/exercise-05/`.
- [ ] **T112-PROPOSE** [US5] Per Q2 deferral, propose locked declaration shape per R-007 sketch: `Stream ::= [] ; [Number | Stream].` + `procedure bb().` + `procedure producer(Number?, Stream).` + `procedure consumer(Stream?, Number).` + `procedure bb_test().`. Show to project owner; await approval; record locked shape.
- [ ] **T112-GOAL-PROPOSE** [US5] Propose primary `bb_test.` + 3 inspection goals. Show to project owner; await approval; record locked bindings.
- [ ] T113 [US5] Write `ch-06-ex-05-buffered-communication.glp` per `contracts/glp-file-format.md`: header per R-008 (cite ch04 §4.2.12 + §4.2.13, book pp 34–35) + locked declarations + byte-exact clauses (bb + producer + consumer + bb_test) + `%%` paraphrase.
- [ ] T114 [US5] REPL load verification → `✓ Loaded:`. HALT per FR-013 if rejected.
- [ ] T115 [US5] Run 4-goal session; capture trace.
- [ ] T116 [US5] Write `ex-05-repl-trace.md` + `ex-05-tutorial.md`.

### ex-05 approval gate

- [ ] T117 [US5] Show ex-05 diff. Wait for approval. Flip status line. Commit `implement(ch06): ex-05 §6.5 Buffered Communication landed (synthesised from ch04 §4.2.12+§4.2.13 bb)`.

**Checkpoint**: ex-05 approved. Chapter complete.

---

## Phase 8: Chapter completion

- [ ] T120 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch06 row's status from `pending review (YYYY-MM-DD)` to `implemented YYYY-MM-DD`. **Replace** the date in the row (do NOT keep both dates; the row carries one date — the latest event). R-008 footnote remains unchanged.
- [ ] T121 Run baseline tests one more time: `bash test/run_all_tests.sh` → 494/494 pass (chapter files NOT in suite per FR-016).
- [ ] T122 Verify `ch06_tutorial.md` status block: all 5 lines `approved YYYY-MM-DD`. `grep -cE "^- exercise-(01|02|03|04|05): approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch06_tutorial.md` returns 5.
- [ ] T123 Final commit: `implement(ch06): chapter complete — 5 exercises (Typed Programming) synthesised from ch01–ch05 sources per /speckit-clarify Q1+Q2`.
- [ ] T124 Provide merge instructions to user per CLAUDE.md §14 (mandatory format with absolute paths).

**Final checkpoint**: ch06 chapter complete; all 5 exercises approved; top-level index updated; ready for merge to main.

---

## Parallel execution opportunities

- **T040 + T042** can run in parallel with T010–T016 (signpost + top-level index updates touch different files than exercise-01).
- **T013 + T014 + T015 + T016** are sequential (each depends on the prior).
- **T011-PROPOSE + T011-GOAL-PROPOSE** are sequential (declaration locking precedes goal locking).
- Phases 3–7 are strictly sequential per pairwise gates.

## Dependencies

- Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8.
- Each Phase k+1 is gated by the prior phase's approval (per `contracts/status-block-format.md` grep contract).
- Phase 8's T122 + T123 are gated by T117 (ex-05 approval).
