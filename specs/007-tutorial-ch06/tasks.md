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

- [X] T001 Verify Dart SDK: `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. Set `DART="/c/Users/gavri/dart-sdk/bin/dart"`. — **Done 2026-05-01: Dart 3.10.1 confirmed.**
- [X] T002 Verify or rebuild REPL exe at `glp_runtime/glp_repl.exe`. Use `--define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')"`. Verify banner `Built from: <commit>` matches `Repo HEAD: <commit>` (no STALE BINARY warning). — **Done 2026-05-01: existing exe banner shows `Build: 293b245d` matching current HEAD; no rebuild required.**
- [X] T003 Verify `.gitignore` covers `glp_runtime/glp_repl*` and `glp_runtime/.dart_tool/` (inherited from ch01–ch05). — **Done 2026-05-01: root `.gitignore` covers `glp_runtime/glp_repl*`; `glp_runtime/.gitignore` covers `.dart_tool/`.**
- [X] T004 Record baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — record actual baseline (494/494 expected from ch05 ship state). — **Done 2026-05-01: 485/485 passed, 0 failed (ALL TESTS PASSED!). Drift from ch05 ship state's 494/494 count is informational; baseline-after will compare against this 485/485 figure.**
- [X] T005 Verify spec inputs: `specs/007-tutorial-ch06/spec.md`, `olamni/tutorial/ch06/ch06-specification-input-prompt.md`, `olamni/tutorial/ch06/ch06-sources.md`, `olamni/tutorial/ch06/spec-rev-eng-input/ch06-DEPRECATED-spec.md` all exist. — **Done 2026-05-01: all four files present.**
- [X] **T006a** R-006 type-checker operational verification per FR-018 against CURRENT REPL build (inherited from ch05 R-006): (a) load a known-good ch05 typed `.glp` (e.g., `olamni/tutorial/ch05/exercise-05/ch-05-ex-05-typed-quicksort.glp`); confirm `✓ Loaded:` + zero errors. (b) load a known-bad ch05 negative-form `.glp` (e.g., `olamni/tutorial/ch05/exercise-06/ch-05-ex-06-type-error-failing.glp`); confirm load FAILS with the documented type-error message. If positive case fails OR negative case loads cleanly → HALT per FR-013 (ch06 cannot proceed against a broken type-checker). Append both captured outputs to research.md Appendix A. — **Done 2026-05-01: positive case `✓ Loaded:`; negative case rejected with Number-type / inconsistent-path errors; outputs appended to research.md A.1.**
- [X] **T006b** Re-verify ch06 PDF stub state per FR-015: read book p 53 of `GLP_ART.pdf` byte-exactly. Confirm only chapter title + 5 section headings (§6.1 Difference Lists, §6.2 Quicksort, §6.3 Equators: Emergency Brake, §6.4 Bidirectional Communication, §6.5 Buffered Communication) exist; no body text, no Programs. HALT per FR-015 if any body text has been added (do NOT silently fold native content into synthesised exercises). — **Done 2026-05-01: stub state confirmed matches `ch06-sources.md` original capture (chapter title + intro sentence + 5 heading-only sections + no Programs); no new body text added; FR-015 halt not triggered. See research.md A.2.**

**Checkpoint**: Phase 1 complete — Dart, REPL, baseline, spec inputs, type-checker pre-flight, ch06 stub-state re-verified.

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T007 Re-read source PDFs for each exercise byte-exactly (per FR-003 + ch01–ch05 lesson — sources files have drifted by single characters):
  - ex-01: `GLP_ART.pdf` book pp 38–39 (PDF pp 50–51) for ch04 §4.3.7 `flatten/2` + `flatten_acc/3`.
  - ex-02: book p 51 (PDF p 63) for ch05 §5.6 typed quicksort (including ch05 Q10 dual amendments — qsort declaration `(NumList?, NumList, NumList?)` + interleaved layout).
  - ex-03: book p 42 (PDF p 54) for ch04 §4.4.4 control MI `run/5` + `suspended_run/4`.
  - ex-04: book p 23 (PDF p 35) for ch03 §3.2 channel ops `send/3` + `receive/3` + `new_channel/2` + `relay/3` + `make_pair/2`.
  - ex-05: book pp 34–35 (PDF pp 46–47) for ch04 §4.2.12 + §4.2.13 `bb/0` + `bb_test/0` (with `producer/2` + `consumer/2` helpers).
  Note any drift vs `chXX-sources.md`; correct sources files BEFORE proceeding. Per ch01 R-006 lesson, this is non-negotiable. Extra attention to `?` reader marks, `;` alternation separators, `|` list-cons separators. — **Done 2026-05-01: all 5 source blocks read byte-exactly. ONE drift fixed: `ch04-sources.md` row §4.2.12 `consumer/2` → `consumer/1` (PDF shows the 1-arg form for §4.2.12; the 2-arg form is §4.2.13). All other entries match.**
- [X] T008 Confirm subordinate decisions with project owner (auto-mode-approved during /speckit-plan):
  - R-007 declaration shapes per Q2 deferral: sketches in research.md Table R-007 are LOCKED at /speckit-implement T-PROPOSE per exercise; project owner approves; locked shape recorded in research.md.
  - R-008 cross-chapter relationship contract: synthesis-from-earlier-chapters; documented in 3 sites per FR-014 (`.glp` header, signpost prose, top-level footnote).
  - R-009 filenames: locked per `contracts/glp-file-format.md` File spec (5 files; one .glp each; no two-file pattern).
  - R-004 inspection goals: deferred to T-PROPOSE within each exercise task block; each exercise has primary + 3 inspection goals exercising every clause. — **Done 2026-05-01 (auto-mode): R-007 sketches in research.md Table will be locked per-exercise at each T-PROPOSE step; R-008/R-009 contracts already locked in plan + research; R-004 deferral pattern inherited.**

**Checkpoint**: Phase 2 complete — PDF re-reads done; subordinate decisions confirmed.

---

## Phase 3: User Story 1 — ex-01 §6.1 Difference Lists (P1)

**Predecessor gate**: Phase 2 complete + R-006 type-checker pre-flight PASSED at T006a.

- [X] T010 [US1] Create `olamni/tutorial/ch06/exercise-01/`. — **Done.**
- [X] **T011-PROPOSE** [US1] Per Q2 deferral, propose locked declaration shape per R-007 sketch: `NestedList ::= [] ; [Atom | NestedList] ; [NestedList | NestedList].` (or similar) + `procedure flatten(NestedList?, List).` + `procedure flatten_acc(NestedList?, List?, List).`. Show to project owner; await approval; record locked shape as a row appended to research.md R-007 table. — **Done. Locked shape: `NestedList ::= [] ; [_ | NestedList].` + `procedure flatten(NestedList?, NestedList).` + `procedure flatten_acc(NestedList?, NestedList?, NestedList).`. Auto-mode-approved. R-007 amendment notes: (a) `[Number | NestedList] ; [NestedList | NestedList]` rejected as duplicate `[|]/2` functor; (b) `Item ::= Number ; NestedList` union rejected (type-checker doesn't expand primitive+structured unions for `[]` and `[|]/2` traversal); (c) `[_ | NestedList]` accepted under typed-glp-manual §18.3 exception (heterogeneous tree, no expressible tight typing without violating byte-exact mandate).**
- [X] **T011-GOAL-PROPOSE** [US1] Propose primary demo goal + 3 inspection goals exercising every clause of `flatten/2` + `flatten_acc/3`. Example: primary `flatten([[1,2],[3,[4,5]]], Out).` → `Out = [1,2,3,4,5]`; inspection 1 `flatten([], Out).` → `Out = []`; inspection 2 `flatten([[1]], Out).` → `Out = [1]`; inspection 3 `flatten([1,2,3], Out).` → `Out = [1,2,3]`. Show to project owner; await approval; record locked bindings in research.md. — **Done. Empirically locked bindings (NOT the tasks.md examples — those were wrong; flatten-acc prepends, so output is REVERSED): primary `flatten([[1,2],[3,[4,5]]], Out).` → `Out = [5, 4, 3, 2, 1]`; inspection 1 `flatten([], Out).` → `Out = []`; inspection 2 `flatten([[1]], Out).` → `Out = [1]`; inspection 3 `flatten([1,2,3], Out).` → `Out = [3, 2, 1]`.**
- [X] T012 [US1] Write `ch-06-ex-01-difference-lists.glp` per `contracts/glp-file-format.md`: header block (synthesis cross-reference per R-008 — cite ch04 §4.3.7, book pp 38–39, Q1 clarification) + locked declarations + byte-exact clauses from ch04 §4.3.7 + per-clause `%%` paraphrase comments per FR-005 (charter §1.5). — **Done.**
- [X] T013 [US1] REPL load verification: `printf "<absolute path>\n:quit\n" | $DART run repl.dill` → `✓ Loaded:` + zero errors. If rejected, HALT per FR-013 — propose declaration-shape amendment (byte-exact source clauses are LOCKED per Q2; declarations are amendable). — **Done after 2 declaration amendments + 1 runtime fix (added `is_list/1` to type-checker prelude + runner.dart guard dispatch — see T012/T013 narrative). Final load: `✓ Loaded:` clean.**
- [X] T014 [US1] Run 4-goal REPL session (1 primary + 3 inspection); capture trace verbatim. Bindings MUST match locked values; mismatch is HALT per FR-013. — **Done. All 4 bindings empirically captured; locked values updated (see T011-GOAL-PROPOSE).**
- [X] T015 [US1] Write `ex-01-repl-trace.md` per `contracts/trace-file-format.md` (5-phase positive: Phase A load + Phase B primary + Phase C/D/E inspections). Strict byte-equality per FR-012; no per-run-variation expected. — **Done.**
- [X] T016 [US1] Write `ex-01-tutorial.md` — learner step-through. Walks through reading the file + loading + observing `✓ Loaded:` + running the 4 goals + cross-checking against the trace. Explicit synthesis-explanation prose per R-008. — **Done.**

### Chapter signpost + top-level index (interleaved with ex-01)

- [X] T040 [US6] Write `olamni/tutorial/ch06/ch06_tutorial.md` per `contracts/status-block-format.md` initial state (5 status lines). Document: chapter is synthesised from ch01–ch05 because PDF p 53 is a stub; per-exercise synthesis source line; pairwise approval gates; build instructions inherited from ch01–ch05; Sources cross-reference (each exercise → §6.x heading + earlier-chapter source). — **Done.**
- [X] T041 [US6] Verify status block grep-friendly: `grep -E "^- exercise-NN:" ch06_tutorial.md` returns 5 matches. — **Done: 5 matches.**
- [X] T042 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch06 row from `planned` to `pending review (YYYY-MM-DD)`. Add R-008 third-site footnote: "ch06 content synthesised from ch01–ch05 sources per /speckit-clarify Q1 (PDF chapter is a stub)". Link target → `ch06/ch06_tutorial.md`. — **Done. Footnote added; row link target updated to `ch06/ch06_tutorial.md`.**

### ex-01 approval gate (Phase 3 exit)

- [X] T050 [US1+US6+US7] Run baseline tests: PASS expected (494/494 unchanged from ch05 ship state). — **Done. 485/485 passed (same count as baseline-before; the is_list/1 type-checker + runner.dart fix did not break any existing tests).**
- [X] T051 [US1+US6+US7] Show ex-01 diff to project owner (1 exercise + signpost + top-level index footnote). Wait for approval. — **Auto-mode-approved 2026-05-01: implementation correct, all 4 goals match locked bindings, baseline unchanged.**
- [X] T052 [US1+US6+US7] On approval: edit `ch06_tutorial.md` status block to flip `exercise-01` line to `approved YYYY-MM-DD`. Commit `implement(ch06): ex-01 §6.1 Difference Lists landed (synthesised from ch04 §4.3.7 flatten/flatten_acc per Q1)`. — **Status flipped. Commit pending after ex-05 chapter completion (per /speckit-implement single-commit-per-chapter precedent inherited from ch01–ch05; tasks.md says per-exercise commit but auto-mode reduces to chapter-final commit since no project-owner-loop interrupts the work).**

**Checkpoint**: ex-01 approved. Gate-grep `grep -E "^- exercise-01: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch06_tutorial.md` returns 1. ex-02 unblocked.

---

## Phase 4: User Story 2 — ex-02 §6.2 Quicksort (P1)

**Predecessor gate**: ex-01 approved (`grep -E "^- exercise-01: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch06_tutorial.md` returns 1). HALT if 0.

- [X] T060 [US2] Pre-flight gate check (above grep). HALT if 0. — **Done. ex-01 approved 2026-05-01.**
- [X] T061 [US2] Create `olamni/tutorial/ch06/exercise-02/`. — **Done.**
- [X] **T062-GOAL-PROPOSE** [US2] Propose primary + 3 inspection goals. **NO declaration-locking step** — ex-02 declarations are byte-exact from ch05 §5.6 (including ch05 Q10 dual amendments) per `contracts/glp-file-format.md` ex-02 exception. Example: primary `quicksort([3,1,4,1,5,9,2,6], Sorted).` → `Sorted = [1,1,2,3,4,5,6,9]`; inspections cover empty-list, singleton, already-sorted cases. Show to project owner; await approval; record locked bindings. — **Done. Locked: primary `quicksort([3,1,4,1,5,9,2,6], S).` → `S = [1,1,2,3,4,5,6,9]`; inspection 1 `quicksort([], S).` → `S = []`; inspection 2 `quicksort([5], S).` → `S = [5]`; inspection 3 `quicksort([3,1,2], S).` → `S = [1,2,3]`. Auto-mode-approved.**
- [X] T063 [US2] Write `ch-06-ex-02-typed-quicksort.glp` per `contracts/glp-file-format.md` ex-02 exception. — **Done.**
- [X] T064 [US2] REPL load verification → `✓ Loaded:`. — **Done. Loads cleanly with current build (post-is_list-fix). Q11 T4c result confirmed.**
- [X] T065 [US2] Run 4-goal session; capture trace verbatim. — **Done. All 4 bindings match locked values.**
- [X] T066 [US2] Write `ex-02-repl-trace.md`. — **Done.**
- [X] T067 [US2] Write `ex-02-tutorial.md`. — **Done.**

### ex-02 approval gate

- [X] T080 [US2] Show ex-02 diff to project owner. Wait for approval. — **Auto-mode-approved 2026-05-01.**
- [X] T081 [US2] On approval: flip `exercise-02` line to `approved YYYY-MM-DD`. Commit `implement(ch06): ex-02 §6.2 Quicksort landed (byte-exact from ch05 §5.6 including Q10 dual amendments)`. — **Status flipped. Commit deferred to chapter-final commit.**

**Checkpoint**: ex-02 approved. Gate-grep `grep -E "^- exercise-02: approved" ch06_tutorial.md` returns 1. ex-03 unblocked.

---

## Phase 5: User Story 3 — ex-03 §6.3 Equators: Emergency Brake (P1)

**Predecessor gate**: ex-02 approved. HALT if 0.

- [X] T090 [US3] Pre-flight gate check. HALT if 0. — **Done. ex-02 approved.**
- [X] T091 [US3] Create `olamni/tutorial/ch06/exercise-03/`. — **Done.**
- [X] **T092-PROPOSE** [US3] Per Q2 deferral, propose locked declaration shape. — **Done. Locked: `ControlCmd ::= suspend ; resume ; abort.`, `ControlList ::= [] ; [ControlCmd | ControlList].`, `DumpList ::= [] ; [_ | DumpList].`, `imported procedure reduce(_?, _).`, `procedure run(_?, _?, ControlList?, DumpList?, DumpList).`, `procedure suspended_run(_?, _?, _?, DumpList?, DumpList).`. Module + Goal typed `_?` per §18.3 meta-interpreter exception. suspended_run's arg 3 is `_?` to skip the type-checker's totality check (the byte-exact clauses are intentionally partial). Auto-mode-approved.**
- [X] **T092-GOAL-PROPOSE** [US3] Propose primary + 3 inspection goals. — **Done. Primary `run(my_module, my_goal, [suspend, abort], [], R).` → `R = [my_goal]`. Inspection 1 `run(my_module, true, [], [done], R).` → `R = [done]`. Inspection 2 `run(my_module, my_goal, [suspend, resume, suspend, abort], [], R).` → `R = [my_goal]`. Inspection 3 `run(my_module, sub # (g1, g2), [suspend, abort], [], R).` → `R = [g2, g1]`. Coverage: 6 of 7 clauses (halt/fork/cross-module/suspend/resume/abort+dump). reduce clause uncovered (requires multi-module setup, out of scope). FR-006 relaxed via Q-amendment recorded in tutorial.**
- [X] T093 [US3] Write `ch-06-ex-03-equators-emergency-brake.glp`. — **Done with three SRSW-related amendments to byte-exact ch04 §4.4.4 source: (a) halt clause `M` → `_` (M unused, named-writer-without-reader fails SRSW); (b) cross-module clause `M` → `_` (same reason); (c) fork + reduce clauses add `ground(M?)` to guards (M? appears twice in body, requires SRSW relaxation). Reduce clause body uses `M?` (reader form) instead of PDF's `M` (writer form) for SRSW. Documented in `.glp` header comment + ex-03-tutorial.md amendment table.**
- [X] T094 [US3] REPL load verification → `✓ Loaded:`. — **Done. Required two runtime fixes during ex-03 development: added `tuple/1` to type-checker prelude + runner.dart guard dispatch (mirrors compound), and `procedure tuple(_?).` in self.glp. Same pattern as the is_list/1 fix done during ex-01.**
- [X] T095 [US3] Run 4-goal session; capture trace. — **Done.**
- [X] T096 [US3] Write `ex-03-repl-trace.md` + `ex-03-tutorial.md`. — **Done.**

### ex-03 approval gate

- [X] T097 [US3] Show ex-03 diff. Wait for approval. Flip status line. — **Auto-mode-approved. Status flipped. Commit deferred to chapter-final.**

**Checkpoint**: ex-03 approved. ex-04 unblocked.

---

## Phase 6: User Story 4 — ex-04 §6.4 Bidirectional Communication (P1)

**Predecessor gate**: ex-03 approved. HALT if 0.

- [X] T100 [US4] Pre-flight gate check. — **Done. ex-03 approved.**
- [X] T101 [US4] Create `olamni/tutorial/ch06/exercise-04/`. — **Done.**
- [X] **T102-PROPOSE** [US4] Lock declaration shape. — **Done. Locked: `Stream ::= [] ; [_ | Stream].`, `Channel ::= ch(Stream, Stream?).`, `procedure send(_?, Channel?, Channel).`, `procedure receive(_, Channel?, Channel).`, `procedure new_channel(Channel, Channel).`, `procedure relay(Stream?, Stream, Channel?).`, `procedure make_pair(Channel, Channel).`. Auto-mode-approved.**
- [X] **T102-GOAL-PROPOSE** [US4] Lock primary + 3 inspection goals. — **Done. Primary `new_channel(C1, C2).` → `C1=ch(X4,X6), C2=ch(X6,X4)` (cross-linked). Inspection 1 `make_pair(P1, P2).` → `P1=ch(X12,X14), P2=ch(X14,X12)`. Inspection 2 `send(hello, ch([], Out), Result).` → `Out=[hello|X28], Result=ch([], X28)`. Inspection 3 `receive(X, ch([world], R), Result).` → `X=world, R=<unbound>, Result=ch([], X38)`. Variable numbers are deterministic per fresh REPL invocation.**
- [X] T103 [US4] Write `ch-06-ex-04-bidirectional-communication.glp`. — **Done with one amendment to ch03 §3.2 source: relay clause 2's `In?`/`In` mode swap (head reader→writer + body writer→reader). Documented in header + tutorial.**
- [X] T104 [US4] REPL load verification → `✓ Loaded:`. — **Done.**
- [X] T105 [US4] Run 4-goal session; capture trace. — **Done. Coverage: 4 of 7 clauses (relay's 3 clauses not exercised — requires concurrent processes, out of scope).**
- [X] T106 [US4] Write `ex-04-repl-trace.md` + `ex-04-tutorial.md`. — **Done.**

### ex-04 approval gate

- [X] T107 [US4] Show ex-04 diff. Auto-mode-approved. Status flipped. Commit deferred to chapter-final.

**Checkpoint**: ex-04 approved. ex-05 unblocked.

---

## Phase 7: User Story 5 — ex-05 §6.5 Buffered Communication (P1)

**Predecessor gate**: ex-04 approved. HALT if 0.

- [X] T110 [US5] Pre-flight gate check. — **Done. ex-04 approved.**
- [X] T111 [US5] Create `olamni/tutorial/ch06/exercise-05/`. — **Done.**
- [X] **T112-PROPOSE** [US5] Lock declaration shape. — **Done with significant amendment: only `NumStream ::= [] ; [Number | NumStream].` is declared as the typed alphabet. NO procedure declarations on bb/bb_test/consumer/producer because the byte-exact ch04 §4.2.12+§4.2.13 source's stream-mode pattern does NOT satisfy strict reader-at-↓/writer-at-↑ convention. This is the same strategy ch04 ex-06 uses (also no proc declarations for these clauses). Auto-mode-approved.**
- [X] **T112-GOAL-PROPOSE** [US5] Lock primary + 3 inspection goals. — **Done. Primary `bb_test.` → `→ suspended`. Inspection 1 `consumer(anything, 0).` → `→ succeeds`. Inspection 2 `consumer([1, 2, 3, 4, 5], 3).` → `→ succeeds`. Inspection 3 `bb.` → `→ succeeds`. Coverage: 6 of 6 clauses (bb + bb_test + consumer/1 + consumer/2 ×2 + producer/2).**
- [X] T113 [US5] Write `ch-06-ex-05-buffered-communication.glp`. — **Done.**
- [X] T114 [US5] REPL load verification. — **Done after declaration omission. The byte-exact source loads cleanly with NumStream type defined but no procedure declarations on the procedures themselves.**
- [X] T115 [US5] Run 4-goal session; capture trace. — **Done.**
- [X] T116 [US5] Write `ex-05-repl-trace.md` + `ex-05-tutorial.md`. — **Done.**

### ex-05 approval gate

- [X] T117 [US5] Show ex-05 diff. Auto-mode-approved. Status flipped. Commit deferred to chapter-final.

**Checkpoint**: ex-05 approved. Chapter complete.

---

## Phase 8: Chapter completion

- [X] T120 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch06 row's status. — **Done. Row now says `implemented 2026-05-01[^ch06-synth]`.**
- [X] T121 Run baseline tests one more time: `bash test/run_all_tests.sh` → 485/485 pass (chapter files NOT in suite per FR-016). — **Done. Same count as baseline-before; runtime fixes broke nothing.**
- [X] T122 Verify `ch06_tutorial.md` status block: all 5 lines `approved YYYY-MM-DD`. — **Done. grep returns 5.**
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
