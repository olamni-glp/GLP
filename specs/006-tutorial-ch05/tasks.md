---

description: "Task list for Olamni Tutorial Chapter 5 — Types and Modes"
---

# Tasks: Olamni Tutorial — Chapter 5 (Types and Modes)

**Input**: Design documents from `specs/006-tutorial-ch05/`
**Prerequisites**: plan.md, spec.md (with 3 Clarifications Q1+Q2+Q3 + 4 pre-resolved), research.md (R-001..R-012), data-model.md, contracts/ (3 files), quickstart.md
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V AND the R-006 type-checker operational verification per FR-018. All ~10 ch05 PDF Programs are SRSW-compliant by byte-exact construction (Principle III); helpers (R-012) MUST also satisfy SRSW + type-check at REPL load. Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI.

**Tests**: Captured REPL traces ARE the regression artifacts. No new Dart unit tests. Per FR-016, ch05 files NOT in `test/run_all_tests.sh`. Baseline `bash test/run_all_tests.sh` MUST pass before AND after implementation per Principle V (count unchanged from ch04 ship state). R-006 type-checker verification at T006a is a NEW pre-flight step for ch05.

**Organization**: Tasks grouped by user story per spec.md AND by sub-section group (inherited from ch04 group-boundary gates per FR-008+FR-009). US1+US2+US3+US4 (P1+P2) cover the four sub-section groups; US5 (P1) covers per-exercise traces+tutorials interleaved with each US1–4 group; US6 (P2) covers chapter signpost; US7 (P3) covers top-level index.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1..US7); composite labels like [US1+US5] for tasks spanning stories.

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verify Dart SDK: `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. Set `DART="/c/Users/gavri/dart-sdk/bin/dart"`.
- [ ] T002 Verify or rebuild REPL exe at `glp_runtime/glp_repl.exe`. If `claude/fix-misleading-build-line` (tag `v2026.04.29-3`) merged, use `--define=GLP_BUILD_COMMIT=...`; else build without (record in research.md Appendix A).
- [ ] T003 Verify `.gitignore` covers `glp_runtime/glp_repl*` and `glp_runtime/.dart_tool/` (inherited from ch01).
- [ ] T004 Record baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — record actual baseline number from ch04 ship state.
- [ ] T005 Verify spec inputs: `specs/006-tutorial-ch05/spec.md`, `olamni/tutorial/ch05/ch05-specification-input-prompt.md`, `olamni/tutorial/ch05/ch05-sources.md`, `olamni/tutorial/ch05/spec-rev-eng-input/ch05-DEPRECATED-spec.md` all exist.
- [ ] **T006a** [NEW for ch05] R-006 type-checker operational verification per FR-018: (a) write a scratch positive test file (e.g., `/tmp/r006-positive.glp` containing `Bit ::= 0 ; 1.`); load via REPL; confirm `✓ Loaded:` + zero errors; (b) write a scratch NEGATIVE test file constructed inline at this task — recommended `procedure foo(Number).` + `foo(a).` clause asserting a non-`Number` atom satisfies `Number` (e.g., `/tmp/r006-negative.glp`); load via REPL; confirm load FAILS with a type-error message. **CRITICAL: do NOT use ex-07's PDF form here — ex-07 is implemented in Phase 6, AFTER this verification; T006a only verifies the type-checker's general operational status.** If positive case fails OR negative case succeeds → HALT per FR-013 (ch05 cannot proceed against a broken type-checker). Record both captured outputs in research.md Appendix A.

**Checkpoint**: Phase 1 complete — Dart, REPL, baseline, spec inputs, type-checker verification all confirmed.

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T006 Re-read `GLP_ART.pdf` book pp 47–52 (PDF pp 59–64) byte-exactly for ALL ch05 source code blocks + relevant prose. Note any drift vs `ch05-sources.md`; correct sources file BEFORE proceeding. Per ch01 R-006 lesson, this is non-negotiable. Extra attention to `?` reader marks, `;` alternation separators, `|` list-cons separators, multi-alternative ordering.
- [ ] T007 Confirm subordinate decisions with project owner (auto-mode-approved during /speckit-plan):
  - R-009 filenames: locked per research.md (8 baseline + 2 extra for negative two-`.glp` pattern).
  - R-010 within-group sequencing + group-boundary gate enforcement: per FR-009.
  - R-012 helper unit-clause / stub body design discipline: per Q2 deferral. Concrete shapes proposed below per-exercise.
  - Per-exercise inspection-goal selection: deferred to T-NN-PROPOSE within each exercise's task block (per R-004).

**Checkpoint**: Phase 2 complete — PDF re-read done; subordinate decisions confirmed.

---

## Phase 3: Group Foundations — User Story 1 (§5.1 + §5.2 + §5.3, P1)

**Predecessor gate**: Chapter signpost exists (created during this group's work) + R-006 type-checker verification PASSED at T006a.

### ex-01 (§5.1 Type Definitions: Bit + Nat + NumList — type-only)

- [ ] T010 [US1] Create `olamni/tutorial/ch05/exercise-01/`.
- [ ] T011a [US1] Propose ex-01 helper shapes to project owner per R-012: e.g., `bit_test/1` × 2 (`bit_test(0).` + `bit_test(1).`) + `nat_test/1` × 3 + `numlist_test/1` × 3. Wait for approval (auto-mode).
- [ ] T011 [US1] Write `ch-05-ex-01-type-definitions.glp` per contracts/glp-file-format.md File 1: §5.1.1 + §5.1.2 + §5.1.3 type defs byte-exact from book p 47 + helper layer below `%% --- DEMONSTRATION HELPERS ---` marker.
- [ ] T012 [US1] Verify load: `printf "<path>\n:quit\n" | $DART run repl.dill` → `✓ Loaded:` + zero errors. Type-check stage validates definitions. If rejected, HALT (potentially helper SRSW/type-check violation per R-012 → propose alternate helper shape).
- [ ] T013 [US1] Propose 3 inspection goals to project owner ("primary" is the load itself for type-only). Examples: `bit_test(0).` (succeeds), `nat_test(s(s(0))).` (succeeds), `numlist_test([1, 2, 3]).` (succeeds). Optional 3rd: `bit_test(2).` to probe type-checker rejection.
- [ ] T014 [US1] Run inspection-goal session + capture verbatim. Verify locked bindings.
- [ ] T015 [US5] Write `ex-01-repl-trace.md` per contracts/trace-file-format.md (5-phase type-only structure: load + first inspection acting as primary + 2 more inspections + closing). Strict byte-equality.
- [ ] T016 [US5] Write `ex-01-tutorial.md` — learner step-through. Explicitly note helpers are demonstration-only, not from book.

### ex-02 (§5.2 Built-in Types: List + Any — type-only)

- [ ] T020 [US1] Create `olamni/tutorial/ch05/exercise-02/`.
- [ ] T021a [US1] Propose ex-02 helper shapes per R-012: `list_test/1` × 3 + `any_test/1` × 3. Wait for approval.
- [ ] T021 [US1] Write `ch-05-ex-02-built-in-types.glp` per contracts/glp-file-format.md File 2: §5.2 universal `List` byte-exact from book p 48 + helper layer.
- [ ] T022 [US1] Verify load. If rejected, HALT.
- [ ] T023 [US1] Propose 3 inspection goals. Examples: `list_test([1, two, 3.0]).` (mixed Any), `any_test(1).`, `any_test([nested, list]).`.
- [ ] T024 [US1] Run inspection-goal session + capture.
- [ ] T025 [US5] Write `ex-02-repl-trace.md`.
- [ ] T026 [US5] Write `ex-02-tutorial.md`.

### ex-03 (§5.3 Procedure Declaration — procedure-decl-only)

- [ ] T030 [US1] Create `olamni/tutorial/ch05/exercise-03/`.
- [ ] T031a [US1] Propose ex-03 stub body shape per R-012. **Preferred Candidate A (SRSW-clean head-pattern)**: `merge([], R?, R).` (1-clause; ties writer position 3 directly to right input via head pattern). Fallback Candidates B + C documented in research.md R-012 if Candidate A is rejected at load. Wait for approval.
- [ ] T031 [US1] Write `ch-05-ex-03-procedure-declaration.glp` per contracts/glp-file-format.md File 3: §5.3 `procedure merge(List?, List?, List).` byte-exact from book p 48 + stub body.
- [ ] T032 [US1] Verify load. If rejected, HALT (potentially stub body SRSW/type-check violation).
- [ ] T033 [US1] Propose 3 inspection goals exercising the stub body. Examples: `merge([], [a, b], M).` → `M = [a, b]`; `merge([1], [2], M).` (exercises 2nd clause if 2-clause stub).
- [ ] T034 [US1] Run inspection-goal session + capture.
- [ ] T035 [US5] Write `ex-03-repl-trace.md`.
- [ ] T036 [US5] Write `ex-03-tutorial.md`.

### Chapter signpost + top-level index (interleaved with Foundations group)

- [ ] T040 [US6] Write `olamni/tutorial/ch05/ch05_tutorial.md` per contracts/status-block-format.md initial state (8 status lines). Document cross-chapter relationships (typed `merge/3` ↔ ch04 untyped, typed `counter/2` ↔ ch04 untyped) + group-structure (4 groups, 3 gates) + negative-exercise contract (ex-07 + ex-08 MEANT to fail).
- [ ] T041 [US6] Verify status block grep-friendly: `grep -E "^- exercise-NN:" ch05_tutorial.md` returns 8 matches.
- [ ] T042 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch05 row from `planned` to `pending review (YYYY-MM-DD)`. Link target → `ch05/ch05_tutorial.md`.

### Foundations group approval gate (Phase 3 exit)

- [ ] T050 [US1+US5+US6+US7] Run baseline tests: PASS expected (count unchanged).
- [ ] T051 [US1+US5+US6+US7] Show Foundations group diff to project owner. Wait for approval.
- [ ] T052 [US1+US5+US6+US7] On approval: edit `ch05_tutorial.md` status block to flip ALL 3 lines (`exercise-01` + `exercise-02` + `exercise-03`) to `approved YYYY-MM-DD` (group-atomic). Commit `implement(ch05): Foundations group landed (type definitions + built-in types + procedure declaration)`.

**Checkpoint**: Foundations group approved; Mode-checking-flow group unblocked.

---

## Phase 4: Group Mode-checking-flow — User Story 2 (§5.4 + §5.5, P1)

**Predecessor gate**: Foundations group approved (`grep -cE "^- exercise-(01|02|03): approved" ch05_tutorial.md` returns 3). HALT if not.

### ex-04 (§5.4 Worked Typed Merge — full-program; cross-chapter relationship to ch04 ex-04)

- [ ] T060 [US2] Pre-flight gate check: `grep -cE "^- exercise-(01|02|03): approved" ch05_tutorial.md` MUST return 3.
- [ ] T061 [US2] Create `olamni/tutorial/ch05/exercise-04/`.
- [ ] T062 [US2] Write `ch-05-ex-04-mode-checked-merge.glp` per contracts/glp-file-format.md File 4. Header MUST contain canonical R-008 cross-reference block citing ch04 ex-04 as un-typed predecessor (book §4.2.5, p 32). `%%` annotations on each merge/3 clause walk through head/body mode-check steps from §5.4 prose IN ADDITION to per-clause paraphrase per SC-017.
- [ ] T063 [US2] Verify load.
- [ ] T064 [US2] Propose primary + 3 inspection goals. Example primary: `merge([1, 3], [2, 4], M).` → `M = [1, 2, 3, 4]` (or fair-merge interleaving). Inspections exercise empty-input clauses + recursive cases.
- [ ] T065 [US2] Run 4-goal session + capture.
- [ ] T066 [US5] Write `ex-04-repl-trace.md`. Phase A annotation MUST acknowledge cross-chapter relationship per contracts/trace-file-format.md annotation rule 5.
- [ ] T067 [US5] Write `ex-04-tutorial.md`.

### ex-05 (§5.5 Counter Response-Slot — full-program; cross-chapter relationship to ch04 ex-06)

- [ ] T070 [US2] Create `olamni/tutorial/ch05/exercise-05/`.
- [ ] T071 [US2] Write `ch-05-ex-05-counter-response-slot.glp` per contracts/glp-file-format.md File 5. Header MUST contain canonical R-008 cross-reference block citing ch04 ex-06 as un-typed predecessor (book §4.2.14).
- [ ] T072 [US2] Verify load.
- [ ] T073 [US2] Propose primary + 3 inspection goals. Example primary: counter response-slot exercise that exchanges a `show(State?)` request and produces a state value (specific shape TBD at T073-equivalent based on PDF clause structure).
- [ ] T074 [US2] Run 4-goal session + capture.
- [ ] T075 [US5] Write `ex-05-repl-trace.md`. Phase A annotation MUST acknowledge cross-chapter relationship.
- [ ] T076 [US5] Write `ex-05-tutorial.md`.

### Mode-checking-flow group approval gate (Phase 4 exit)

- [ ] T080 [US2+US5] Run baseline tests: PASS expected.
- [ ] T081 [US2+US5] Show Mode-checking-flow group diff (2 exercises). Wait for approval.
- [ ] T082 [US2+US5] On approval: flip ex-04 + ex-05 status block lines atomically. Commit `implement(ch05): Mode-checking-flow group landed (typed merge worked example + counter response-slot)`.

**Checkpoint**: Mode-checking-flow group approved; Flagship group unblocked.

---

## Phase 5: Group Flagship — User Story 3 (§5.6, P1)

**Predecessor gate**: Mode-checking-flow group approved.

### ex-06 (§5.6 Typed Quicksort — full-program; chapter flagship)

- [ ] T090 [US3] Pre-flight gate: `grep -cE "^- exercise-(04|05): approved" ch05_tutorial.md` MUST return 2.
- [ ] T091 [US3] Create `olamni/tutorial/ch05/exercise-06/`.
- [ ] T092 [US3] Write `ch-05-ex-06-typed-quicksort.glp` per contracts/glp-file-format.md File 6: 1 type def (`NumList` duplicated inline from ex-04 per FR-010) + 3 procedure decls + 6 clauses byte-exact from book p 51.
- [ ] T093 [US3] Verify load.
- [ ] T094 [US3] Propose primary + 3 inspection goals. Example primary: `quicksort([3,1,4,1,5,9,2,6], S).` → `S = [1,1,2,3,4,5,6,9]`. Inspections exercise `qsort/3` base + recursive + `partition/4` element-< / element-≥ branches. Per SC-010, 4-goal session collectively exercises all 6 clauses + 3 procedure declarations.
- [ ] T095 [US3] Run 4-goal session + capture.
- [ ] T096 [US5] Write `ex-06-repl-trace.md`.
- [ ] T097 [US5] Write `ex-06-tutorial.md`.

### Flagship group approval gate (Phase 5 exit)

- [ ] T100 [US3+US5] Run baseline tests: PASS expected.
- [ ] T101 [US3+US5] Show Flagship group diff. Wait for approval.
- [ ] T102 [US3+US5] On approval (single-exercise group): flip ex-06 status block line atomically. Commit `implement(ch05): Flagship group landed (typed quicksort)`.

**Checkpoint**: Flagship group approved; Negatives group unblocked.

---

## Phase 6: Group Negatives — User Story 4 (§5.7, P2)

**Predecessor gate**: Flagship group approved + R-006 re-verification (typically no-op).

### ex-07 (§5.7.1 Type Error — negative; two-`.glp`)

- [ ] T110 [US4] Pre-flight gate: `grep -cE "^- exercise-06: approved" ch05_tutorial.md` MUST return 1. R-006 type-checker re-verification PASSED.
- [ ] T111 [US4] Create `olamni/tutorial/ch05/exercise-07/`.
- [ ] T112 [US4] Write `ch-05-ex-07-type-error-failing.glp` per contracts/glp-file-format.md File 7a: §5.7.1 `foo/1` failing form byte-exact from book p 51. Header MARKED `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠`.
- [ ] T113 [US4] Verify failing-form FAILS to load: expect type-error message documenting `'a' is not a Number` (or current REPL build's equivalent text). Capture verbatim. Inspect for per-run-varying segments per R-011 — if any (memory address, tuple-id, etc.), HALT and propose Clarifications amendment per FR-013.
- [ ] T114 [US4] Propose corrected form to project owner (e.g., re-typed `procedure foo(Atom).` to accept the offending value, OR fixed clause body). Wait for approval.
- [ ] T115 [US4] Write `ch-05-ex-07-type-error-corrected.glp` per File 7b spec.
- [ ] T116 [US4] Verify corrected-form loads successfully: `✓ Loaded:` + zero errors.
- [ ] T117 [US5] Write `ex-07-repl-trace.md` per contracts/trace-file-format.md negative 2-phase structure (Phase A failing-load + Phase B corrected-load). Optional Phase C if a success-confirmation goal is included per T119. Per FR-014, full byte-equality holds modulo per-run-varying segments authorised at T113.
- [ ] T118 [US5] Write `ex-07-tutorial.md`. EXPLICITLY state load failure is the demonstrated outcome, NOT a tutorial bug.
- [ ] T119 [US4] *(Optional Phase C — symmetric with T125 for ex-08)* Propose success-confirmation goal for ex-07's corrected form (e.g., if corrected form re-types `procedure foo(Atom).` then `foo(a).` succeeds). Wait for approval. Run + capture. Decision per-exercise — may be omitted if the corrected form's "success" is sufficiently demonstrated by the load alone.

### ex-08 (§5.7.2 Mode Error — negative; two-`.glp`; book-cited corrected form)

- [ ] T120 [US4] Create `olamni/tutorial/ch05/exercise-08/`.
- [ ] T121 [US4] Write `ch-05-ex-08-mode-error-failing.glp` per File 8a spec: §5.7.2 `bar/2` failing form byte-exact from book pp 51–52. Header MARKED `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠`.
- [ ] T122 [US4] Verify failing-form FAILS to load: expect mode-error message. Capture verbatim. Inspect per R-011.
- [ ] T123 [US4] Write `ch-05-ex-08-mode-error-corrected.glp` per File 8b spec: book-cited corrected form `bar(X, Y?) :- Y := X? + 1.` byte-exact from book p 52. (No proposal step needed — corrected form is BOOK-CITED.)
- [ ] T124 [US4] Verify corrected-form loads successfully.
- [ ] T125 [US4] *(Optional Phase C)* Propose success-confirmation goal `bar(5, R).` → `R = 6` to demonstrate the fix actually works. Wait for approval. Run + capture.
- [ ] T126 [US5] Write `ex-08-repl-trace.md` per negative 2-phase or 3-phase structure.
- [ ] T127 [US5] Write `ex-08-tutorial.md`. EXPLICITLY state load failure is the demonstrated outcome.

### Negatives group approval gate + chapter complete (Phase 6 exit)

- [ ] T130 [US4+US5] Run baseline tests: PASS expected.
- [ ] T131 [US4+US5] Show Negatives group diff (2 exercises). Wait for approval.
- [ ] T132 [US4+US5+US7] On approval (chapter complete):
  - Flip ex-07 + ex-08 status block lines to `approved YYYY-MM-DD` atomically.
  - Edit `olamni/tutorial/tutorial.md` ch05 row from `pending review (…)` to `implemented YYYY-MM-DD`.
  - Commit `implement(ch05): chapter complete — Negatives group + top-level index flip`.

**Checkpoint**: All 4 groups approved; chapter 5 complete.

---

## Phase 7: Polish & Cross-Cutting

- [ ] T140 [P] No-fabrication audit: verify all files under `specs/006-tutorial-ch05/` are proper `/speckit-*` outputs. Per FR-012 + SC-011.
- [ ] T141 [P] Cross-chapter relationship documentation check: grep ex-04 + ex-05 headers for canonical R-008 provenance line; verify `ch05_tutorial.md` signpost prose mentions both relationships. Per FR-002 + SC-007.
- [ ] T142 [P] Cross-chapter scope check: grep all 8–10 ch05 `.glp` files for procedure names from other chapters. Should match only ch05 native (`merge/3`, `counter/2`, `quicksort/2`, `qsort/3`, `partition/4`, `foo/1`, `bar/2`, helper names from R-012). The cross-chapter relationships in ex-04/ex-05 are documentation-only — `merge/3` and `counter/2` clauses in ch05 are byte-exact from §5.4/§5.5 PDF, NOT byte-identical to ch04's clauses.
- [ ] T143 [P] Test harness exclusion check: `grep "olamni/tutorial/ch05" test/run_all_tests.sh` MUST return 0 matches. Per FR-016 + SC-014.
- [ ] T144 [P] Body-kernel scope check: `grep -E "now\\(|'_output'" olamni/tutorial/ch05/exercise-*/*.glp` MUST return 0 matches. `:=` permitted only inside ex-08's corrected `bar(X, Y?) :- Y := X? + 1.`. Per SC-015.
- [ ] T145 [P] Helper-layer discipline check: ex-01/ex-02/ex-03 helpers below `%% --- DEMONSTRATION HELPERS ---` marker; helper names don't collide with PDF procedure names; each helper carries `%%` per clause. Per R-012.
- [ ] T146 [P] Negative-exercise outcome check: ex-07 + ex-08 failing-form load attempts produce documented type/mode-error messages (verifiable via captured traces); corrected forms load successfully. Per SC-009.
- [ ] T147 Final baseline test pass: PASS expected (count unchanged from ch04 ship state).
- [ ] T148 Trace reproducibility check: re-run all 8 traces; diff against committed `.md` files modulo banner (and modulo R-011 per-run-varying segments for negatives if relaxation applied). Per FR-014 + SC-005.
- [ ] T149 [P] Walk-through verification (soft): SC-001 60-min budget logged as known follow-up.
- [ ] T150 Commit + push branch `006-tutorial-ch05`. Per Constitution multi-Claude protocol — `git add` SPECIFIC files only.
- [ ] T151 Provide merge instructions to project owner per workflow memory mandatory format.

**Checkpoint**: Chapter 5 fully delivered, audited, and ready for merge.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001..T006a sequential. T006a (R-006) is the NEW pre-flight verification BLOCKING all Foundations work.
- **Foundational (Phase 2)**: T006 + T007 — required before any user story.
- **Foundations group (Phase 3)**: T010..T052 sequential within group; signpost + top-level interleaved.
- **Mode-checking-flow group (Phase 4)**: T060..T082; gated on Phase 3 approval.
- **Flagship group (Phase 5)**: T090..T102; gated on Phase 4 approval.
- **Negatives group (Phase 6)**: T110..T132; gated on Phase 5 approval + R-006 re-verification.
- **Polish (Phase 7)**: T140..T151; T140-T146 + T149 [P] independent.

### Approval Gates

| Gate | Blocks | Set by |
|---|---|---|
| R-006 type-checker verification (T006a) | T010+ (Phase 3) | T006a itself |
| Foundations group approval (T052) | T060+ (Phase 4) | T052 itself, after T051 |
| Mode-checking-flow group approval (T082) | T090+ (Phase 5) | T082 itself, after T081 |
| Flagship group approval (T102) | T110+ (Phase 6) | T102 itself, after T101 |
| Negatives group approval (T132) | (chapter complete) | T132 itself, after T131 |

### Parallel Opportunities

- **Phase 7**: T140-T146 + T149 [P] — different files, independent grep audits.
- Most tasks within an exercise are sequential (propose helpers/goals → write file → verify load → run goals → write trace → write tutorial).
- Within a sub-section group, exercises are sequential (per R-010).
- Across sub-section groups: NO parallelism (gated).

---

## Implementation Strategy

### MVP First (Foundations group only)

1. Phase 1 (T001..T006a) — including R-006 type-checker verification.
2. Phase 2 (T006..T007).
3. Phase 3 (T010..T052) — Foundations group complete + signpost + top-level index.
4. **STOP and VALIDATE**: Foundations is fully usable for a learner — covers §5.1 type definitions + §5.2 built-in types + §5.3 procedure declaration syntax. Type-checker is verified operational; helpers exercise the type/mode shapes.

### Incremental Delivery by Group

5. Phase 4 (Mode-checking-flow group) — 2 exercises with worked-example mode checking + response slots; cross-chapter relationships documented.
6. Phase 5 (Flagship group) — 1 exercise, the chapter's typed quicksort flagship.
7. Phase 6 (Negatives group) — 2 exercises with negative-load-test contract; R-011 per-run-varying handling on captured error messages.
8. Phase 7 (polish + commit).

### Total Wall-Clock Estimate

- Phase 1+2: 30 min (Dart verify, REPL build, baseline test, R-006 type-checker verification ~5 min, PDF re-read).
- Phase 3 (Foundations): 30–45 min (3 exercises, mostly type-defs + helpers + procedure-decl + stub).
- Phase 4 (Mode-checking-flow): 30–45 min (2 exercises, worked merge ~5 clauses + counter response-slot 1 clause + cross-chapter headers).
- Phase 5 (Flagship): 20–30 min (1 exercise, typed quicksort 6 clauses + 3 procedure decls).
- Phase 6 (Negatives): 30–45 min (2 exercises, two-`.glp` pattern each; failing-form verification + corrected-form proposal/write).
- Phase 7: 20 min (polish + commit + merge instructions).

**Total**: ~3–4 hours with auto-mode approvals at group boundaries. Smaller than ch04 (5–7 hr) because volume is smaller (~10 PDF blocks vs ~38) but with the new R-006 + R-011 + R-012 disciplines.

---

## Notes

- [P] tasks = different files, no shared deps — parallelisable.
- [Story] label maps tasks to spec.md user stories (US1..US7).
- US1+US2+US3+US4 are gated cross-group per FR-008+FR-009 group-boundary model.
- US5 (per-exercise traces+tutorials) interleaves with each group; trace+tutorial happen immediately after the corresponding `.glp` file is written + 4-goal session captured.
- **R-006 type-checker verification (T006a) is a NEW pre-flight step for ch05** — ch05 is the first chapter where the type-checker does meaningful work; if broken, chapter cannot proceed.
- **R-011 per-run-varying-segment handling** applies only to negative-exercise error messages (T113, T122). If observed, halt-and-amend per FR-013; otherwise full byte-equality holds.
- **R-012 helper-layer discipline** applies only to ex-01/ex-02/ex-03 (type-only/proc-decl-only). Helpers must satisfy SRSW + type-check at REPL load; helper-shape proposal at T011a/T021a/T031a; helpers below the `%% --- DEMONSTRATION HELPERS ---` marker; no PDF-procedure-name collision.
- Per FR-013 + Constitution Principle II: any obstacle (Dart absent, REPL build fail, type-checker broken, binding mismatch, byte-exact transcription drift, cross-chapter relationship documentation drift, helper SRSW violation, unexpected error category on negative-exercise load) → HALT and report.
- Per FR-012: Claude does NOT write speckit-format `spec.md`-style files. T140 verifies this.
- Per FR-015 + SC-015: `:=` permitted only inside byte-exact PDF clauses (specifically: ex-08's corrected `bar/2`); `now/1` and `'_output'/1` MUST NOT appear.
- Commit cadence: 4 group-approval commits + 1 polish/final commit = 5 commits total. `git add` SPECIFIC files per multi-Claude protocol.
- Constitution Principle V: baseline tests at T004 + T050 + T080 + T100 + T130 + T147 (6 baseline checks total). All must show PASS unchanged.
