---

description: "Task list for Olamni Tutorial Chapter 5 — Types and Modes (post-Q7+Q12)"
---

# Tasks: Olamni Tutorial — Chapter 5 (Types and Modes)

**Input**: Design documents from `specs/006-tutorial-ch05/`
**Prerequisites**: plan.md, spec.md (with **12 Clarifications Q1..Q12** + 4 pre-resolved), research.md (R-001..R-012; post-Q7 cleanup applied during /speckit-analyze), data-model.md (post-Q7 cleanup applied during /speckit-analyze), contracts/ (3 files), quickstart.md (post-Q7 cleanup applied during /speckit-analyze)
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V AND the R-006 type-checker operational verification per FR-018 (NEW for ch05). All ~10 ch05 PDF Programs are SRSW-compliant by byte-exact construction (Principle III). Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI.

**Tests**: Captured REPL traces ARE the regression artifacts. No new Dart unit tests. Per FR-016, ch05 files NOT in `test/run_all_tests.sh`. Baseline `bash test/run_all_tests.sh` MUST pass before AND after implementation per Principle V (count unchanged from ch04 ship state). R-006 type-checker verification at T006a is a NEW pre-flight step for ch05; per Q11 empirical capture 2026-05-01 against REPL build `bcd59392`, R-006 already passed and is recorded in research.md Appendix A — re-verified at T001 against current REPL build at /speckit-implement runtime.

**Organization**: Tasks grouped by user story per spec.md AND by sub-section group (inherited from ch04 group-boundary gates per FR-008+FR-009). US1+US2+US3+US4 (P1+P2) cover the four sub-section groups; US5 (P1) covers per-exercise traces+tutorials interleaved with each US1–4 group; US6 (P2) covers chapter signpost; US7 (P3) covers top-level index.

**Post-Q7+Q12 numbering authority**: This tasks.md uses the binding post-Q7 exercise numbering. ex-01 + ex-02 = Foundations (load-only; §5.1 + §5.2). ex-03 = Mode-checking-flow §5.3+§5.4 merged per Q7 (procedure declaration + worked typed merge). ex-04 = Mode-checking-flow §5.5 counter response-slot with Q8 minimal coverage stubs. ex-05 = Flagship §5.6 typed quicksort with Q10 dual amendment. ex-06 = Negatives §5.7.1 type-error. ex-07 = Negatives §5.7.2 mode-error. **Q7 retracts the pre-Q7 Q2/R-012 helper authorization** — no fabricated helpers in any exercise; ex-01 + ex-02 are 1-phase load-only with byte-exact PDF text only.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1..US7); composite labels like [US1+US5] for tasks spanning stories.

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verify Dart SDK: `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. Set `DART="/c/Users/gavri/dart-sdk/bin/dart"`.
- [ ] T002 Verify or rebuild REPL exe at `glp_runtime/glp_repl.exe`. If `claude/fix-misleading-build-line` (tag `v2026.04.29-3` or later) merged, use `--define=GLP_BUILD_COMMIT=...`; else build without (record in research.md Appendix A).
- [ ] T003 Verify `.gitignore` covers `glp_runtime/glp_repl*` and `glp_runtime/.dart_tool/` (inherited from ch01).
- [ ] T004 Record baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — record actual baseline number from ch04 ship state.
- [ ] T005 Verify spec inputs: `specs/006-tutorial-ch05/spec.md`, `olamni/tutorial/ch05/ch05-specification-input-prompt.md`, `olamni/tutorial/ch05/ch05-sources.md`, `olamni/tutorial/ch05/spec-rev-eng-input/ch05-DEPRECATED-spec.md` all exist.
- [ ] **T006a** [NEW for ch05] R-006 type-checker operational verification per FR-018 against CURRENT REPL build (research.md Appendix A captured 2026-04-30 against build `2362202d`; Q11 captured 2026-05-01 against build `bcd59392`; this task re-verifies against the build in use at /speckit-implement runtime): (a) write a scratch positive test file (e.g., `C:\Users\gavri\AppData\Local\Temp\r006-positive.glp` containing `Bit ::= 0 ; 1.`); load via REPL; confirm `✓ Loaded:` + zero errors. (b) write a scratch NEGATIVE test file (e.g., `C:\Users\gavri\AppData\Local\Temp\r006-negative.glp` containing `procedure foo(Number).` + `foo(a).`); load via REPL; confirm load FAILS with a type-error message. **CRITICAL: do NOT use ex-06's PDF form here — ex-06 is implemented in Phase 6, AFTER this verification; T006a only verifies the type-checker's general operational status.** If positive case fails OR negative case succeeds → HALT per FR-013 (ch05 cannot proceed against a broken type-checker). Append both captured outputs to research.md Appendix A.

**Checkpoint**: Phase 1 complete — Dart, REPL, baseline, spec inputs, type-checker verification all confirmed.

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T006 Re-read `GLP_ART.pdf` book pp 47–52 (PDF pp 59–64) byte-exactly for ALL ch05 source code blocks + relevant prose. Note any drift vs `ch05-sources.md`; correct sources file BEFORE proceeding. Per ch01 R-006 lesson, this is non-negotiable. Extra attention to `?` reader marks, `;` alternation separators, `|` list-cons separators, multi-alternative ordering, embedded `?` within structures (e.g., `show(Number?)` inside `CounterMsg`).
- [ ] T007 Confirm subordinate decisions with project owner (auto-mode-approved during /speckit-plan):
  - R-009 filenames (post-Q7+Q12): locked per research.md (7 baseline files for 5 positive exercises + 2 extra `.glp` for negative two-`.glp` pattern in ex-06 + ex-07; total 9 `.glp` files chapter-wide).
  - R-010 within-group sequencing + group-boundary gate enforcement: per FR-009. Within-group order: Foundations ex-01 → ex-02; Mode-checking-flow ex-03 → ex-04; Flagship ex-05 (single); Negatives ex-06 → ex-07.
  - R-012 helper unit-clause / stub body design discipline: **RETRACTED per Q7** for type-only exercises (ex-01, ex-02) — they are 1-phase load-only with byte-exact PDF text only. R-012 retains historical value for audit trail but is NOT applied to any ch05 exercise.
  - Q8 minimal coverage stubs for ex-04 §5.5 counter: required per Q11 T5 empirical (uncovered alternatives `[]`/`clear`/`up`/`down` cause type-checker exhaustiveness failure). Stubs are NOT helpers in the retracted-Q2 sense — they are minimal completions for type-checker exhaustiveness with documented Q-amendment provenance.
  - Q10 dual amendment for ex-05 §5.6 typed quicksort: required per Q11 T4a/T4b/T4c/T4d empirical. Both amendments are LOCKED at the spec layer (qsort declaration corrected per prose+clauses; interleaved layout per parser requirement); both MUST appear in ex-05's `.glp` with documented header provenance.
  - Per-exercise inspection-goal selection: deferred to T-NN-PROPOSE within each runnable-exercise task block (per R-004); load-only exercises ex-01 + ex-02 have NO inspection goals per Q7.

**Checkpoint**: Phase 2 complete — PDF re-read done; subordinate decisions confirmed.

---

## Phase 3: Group Foundations — User Story 1 (§5.1 + §5.2, P1)

**Predecessor gate**: Chapter signpost exists (created during this group's work, see T040) + R-006 type-checker verification PASSED at T006a.

### ex-01 (§5.1 Type Definitions: Bit + Nat + NumList — load-only per Q7)

- [ ] T010 [US1] Create `olamni/tutorial/ch05/exercise-01/`.
- [ ] T011 [US1] Write `ch-05-ex-01-type-definitions.glp` per contracts/glp-file-format.md File 1: §5.1.1 `Bit ::= 0 ; 1.` + §5.1.2 `Nat ::= 0 ; s(Nat).` + §5.1.3 `NumList ::= [] ; [Number | NumList].` byte-exact from book p 47. **NO helper layer** per Q7 retraction. Per-clause `%%` paraphrase per charter §1.5; header block cites Formal 5.1 (book p 48).
- [ ] T012 [US1] Verify load: `printf "<path>\n:quit\n" | $DART run repl.dill` → `✓ Loaded:` + zero errors. Type-check stage validates definitions. If rejected, HALT per FR-013 — book-internal type-system inconsistency or runtime regression; do NOT add fabricated helpers per Q7 retraction.
- [ ] T013 [US5] Write `ex-01-repl-trace.md` per contracts/trace-file-format.md (**1-phase load-only structure** per Q7: Phase A Load only; no goals run; no inspection phases). Strict byte-equality. Phase A annotation explicitly notes "type definitions are non-runnable; the load IS the demonstration".
- [ ] T014 [US5] Write `ex-01-tutorial.md` — learner step-through. Walks through reading the file + loading + observing `✓ Loaded:`. Explicitly notes that ex-01 has no inspection goals per Q7 (book content is non-runnable).

### ex-02 (§5.2 Built-in Types: universal List + Any — load-only per Q7)

- [ ] T020 [US1] Create `olamni/tutorial/ch05/exercise-02/`.
- [ ] T021 [US1] Write `ch-05-ex-02-built-in-types.glp` per contracts/glp-file-format.md File 2: `List ::= [] ; [Any | List].` byte-exact from book p 48 + per-clause `%%` paraphrase + header prose noting `Number`/`Any`/`Atom` built-in types. **NO helper layer** per Q7 retraction.
- [ ] T022 [US1] Verify load → `✓ Loaded:` + zero errors. If rejected, HALT.
- [ ] T023 [US5] Write `ex-02-repl-trace.md` per 1-phase load-only structure.
- [ ] T024 [US5] Write `ex-02-tutorial.md`.

### Chapter signpost + top-level index (interleaved with Foundations group)

- [ ] T040 [US6] Write `olamni/tutorial/ch05/ch05_tutorial.md` per contracts/status-block-format.md initial state (**7 status lines** per Q3+Q7). Document: cross-chapter relationships note (typed `merge/3` ↔ ch04 ex-04 untyped `merge/3`; typed `counter/2` ↔ ch04 ex-06 untyped `counter/1`+`counter_loop/2`); group-structure note (4 groups: Foundations / Mode-checking-flow / Flagship / Negatives); 3 group-boundary gates (Foundations→Mode-checking-flow, Mode-checking-flow→Flagship, Flagship→Negatives); negative-exercise contract note (ex-06 + ex-07 MEANT to fail to load with documented type-error / mode-error messages — Q11 empirical T3 + T6 captures); Sources cross-reference (each exercise → §5.x sub-section). Per FR-005 + Q12 binding form.
- [ ] T041 [US6] Verify status block grep-friendly: `grep -E "^- exercise-NN:" ch05_tutorial.md` returns 7 matches.
- [ ] T042 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch05 row from `planned` to `pending review (YYYY-MM-DD)`. Link target → `ch05/ch05_tutorial.md`.

### Foundations group approval gate (Phase 3 exit)

- [ ] T050 [US1+US5+US6+US7] Run baseline tests: PASS expected (count unchanged from ch04 ship state).
- [ ] T051 [US1+US5+US6+US7] Show Foundations group diff to project owner (2 exercises landed; load-only). Wait for approval.
- [ ] T052 [US1+US5+US6+US7] On approval: edit `ch05_tutorial.md` status block to flip `exercise-01` + `exercise-02` lines to `approved YYYY-MM-DD` (group-atomic; 2 lines per Q7+Q12). Commit `implement(ch05): Foundations group landed (type definitions + built-in types — load-only per Q7)`.

**Checkpoint**: Foundations group approved; Mode-checking-flow group unblocked. Gate-grep contract: `grep -cE "^- exercise-(01|02): approved" ch05_tutorial.md` returns 2 (Q12 binding form).

---

## Phase 4: Group Mode-checking-flow — User Story 2 (§5.3+§5.4 merged + §5.5, P1)

**Predecessor gate**: Foundations group approved (`grep -cE "^- exercise-(01|02): approved" ch05_tutorial.md` returns 2 per Q12). HALT if not.

### ex-03 (§5.3 procedure decl + §5.4 worked typed merge — merged per Q7; full-program; cross-chapter relationship to ch04 ex-04 untyped merge)

- [ ] T060 [US2] Pre-flight gate check: `grep -cE "^- exercise-(01|02): approved" ch05_tutorial.md` MUST return 2 (Q12 post-Q7 grep contract). HALT if any other count.
- [ ] T061 [US2] Create `olamni/tutorial/ch05/exercise-03/`.
- [ ] T062 [US2] Write `ch-05-ex-03-mode-checked-merge.glp` per contracts/glp-file-format.md File 3: per Q4 the type is **`List`** (universal type from §5.2, NOT `NumList`); per Q7 §5.3 + §5.4 are merged into this single exercise (Q11 T2 empirically confirmed §5.3 alone fails to parse with `[syntax] Procedure declaration … must be immediately followed by its clauses`); per Q5 RETRACTED, the §5.4 body text is byte-exact PDF as printed (Q11 T1 empirical confirmation). Inline `List ::= [] ; [Any | List].` (duplicated from ex-02 per FR-010 self-containment) + `procedure merge(List?, List?, List).` byte-exact from book p 49 + 3 clauses byte-exact from book p 49. Header MUST contain canonical R-008 cross-reference block citing ch04 ex-04 (book §4.2.5, p 32) as un-typed predecessor — relationship is RELATIONSHIP not import; 4 untyped clauses in ch04 vs 3 typed clauses in ch05; same procedure name. `%%` annotations on each merge/3 clause walk through head/body mode-check steps from §5.4 prose IN ADDITION to per-clause paraphrase per SC-017+Q12.
- [ ] T063 [US2] Verify load: expect `✓ Loaded:` + zero errors (Q11 T1 empirically confirmed). If rejected, HALT per FR-013.
- [ ] T064 [US2] Propose primary + 3 inspection goals to project owner. Example primary: `merge([1, 3], [2, 4], M).` → `M = [1, 2, 3, 4]` (or one of merge's possible interleavings per the locked goal selection). Inspections exercise empty-input clauses + recursive cases. Wait for approval.
- [ ] T065 [US2] Run 4-goal session + capture verbatim. Verify locked bindings.
- [ ] T066 [US5] Write `ex-03-repl-trace.md` per **5-phase positive structure** (Phase A Load + Phase B Primary + Phases C/D/E Inspections). Phase A annotation MUST acknowledge cross-chapter relationship per contracts/trace-file-format.md annotation rule 5. Phase B annotation references Formal 5.2 Mode Semantics.
- [ ] T067 [US5] Write `ex-03-tutorial.md`.

### ex-04 (§5.5 Counter Response-Slot — full-program; cross-chapter relationship to ch04 ex-06 untyped counter; with Q8 minimal coverage stubs)

- [ ] T070 [US2] Create `olamni/tutorial/ch05/exercise-04/`.
- [ ] T071 [US2] Write `ch-05-ex-04-counter-response-slot.glp` per contracts/glp-file-format.md File 4. Header MUST contain canonical R-008 cross-reference block citing ch04 ex-06 as un-typed predecessor (book §4.2.14; un-typed `counter/1` + `counter_loop/2` — different arity 1→2; relationship is RELATIONSHIP not import). Body content per Q4: `procedure counter(CounterStream?, Number?).` (arg 2 is `Number?` consume-mode, NOT plain `Number` — byte-exact PDF p 50) + `CounterMsg` + `CounterStream` type defs (with embedded `show(Number?)` consume-mode-inside-produce-mode) + the §5.5 response-slot clause per Q6: `counter([show(State?)|S], State) :- number(State?) | counter(S?, State?).` byte-exact from book p 50 (full clause has `number/1` multi-reader-permissive guard + recursive body, NOT just a single response-slot clause head). Per Q8 + Q11 T5: include MINIMAL COVERAGE STUBS for the uncovered `[]` / `clear` / `up` / `down` alternatives (no-op forwarding + termination), explicitly labeled `%% --- Q8 MINIMAL COVERAGE STUBS (type-checker exhaustiveness; book p 50 shows only the show clause) ---` block marker AND on each stub clause's `%%` paraphrase comment. Stubs are NOT fabricated helpers per Q7 — they are minimal completions with documented Q-amendment provenance, distinct in framing from "demonstration helpers".
- [ ] T072 [US2] Verify load: expect `✓ Loaded:` + zero errors (with Q8 stubs in place). If rejected without Q8 stubs, would fail with `counter argument 1: uncovered alternative "[]"` per Q11 T5 empirical. SRSW-validity: `State` appears as 1 writer (head arg 2) + 3 readers (head's `show(State?)`, guard `number(State?)`, body `counter(S?, State?)` arg 2) — multi-reader-permissive `number/1` guard authorises the multi-read.
- [ ] T073 [US2] Propose primary + 3 inspection goals. Example primary: counter response-slot exercise that exchanges a `show(State?)` request and produces a state value — specific shape + locked binding TBD at T073 based on PDF clause structure + Q8 stub forwarding behaviour. Inspections exercise different `CounterMsg` alternatives via the Q8 coverage stubs. Wait for approval.
- [ ] T074 [US2] Run 4-goal session + capture verbatim.
- [ ] T075 [US5] Write `ex-04-repl-trace.md` per 5-phase positive structure. Phase A annotation MUST acknowledge cross-chapter relationship + Q8 stubs framing. Phase B annotation references Formal 5.3 Mode Involution.
- [ ] T076 [US5] Write `ex-04-tutorial.md`.

### Mode-checking-flow group approval gate (Phase 4 exit)

- [ ] T080 [US2+US5] Run baseline tests: PASS expected.
- [ ] T081 [US2+US5] Show Mode-checking-flow group diff (2 exercises). Wait for approval.
- [ ] T082 [US2+US5] On approval: flip ex-03 + ex-04 status block lines atomically. Commit `implement(ch05): Mode-checking-flow group landed (typed merge worked example + counter response-slot with Q8 coverage stubs)`.

**Checkpoint**: Mode-checking-flow group approved; Flagship group unblocked. Gate-grep contract: `grep -cE "^- exercise-(03|04): approved" ch05_tutorial.md` returns 2 (Q12 binding form).

---

## Phase 5: Group Flagship — User Story 3 (§5.6, P1)

**Predecessor gate**: Mode-checking-flow group approved.

### ex-05 (§5.6 Typed Quicksort — full-program; chapter flagship; with Q10 dual amendment)

- [ ] T090 [US3] Pre-flight gate: `grep -cE "^- exercise-(03|04): approved" ch05_tutorial.md` MUST return 2 (Q12 post-Q7 grep contract). HALT if any other count.
- [ ] T091 [US3] Create `olamni/tutorial/ch05/exercise-05/`.
- [ ] T092 [US3] Write `ch-05-ex-05-typed-quicksort.glp` per contracts/glp-file-format.md File 5: 1 type def `NumList ::= [] ; [Number | NumList].` (duplicated inline from ex-01 per FR-010 self-containment) + 3 procedure decls + 6 clauses byte-exact from book p 51. **Per Q10 dual amendments (LOCKED at spec)**: (a) **Issue A — qsort declaration corrected**: declare `procedure qsort(NumList?, NumList, NumList?).` (corrected per book's prose + body call + clause heads — three lines of evidence agree on consume/produce/consume; Q11 T4d empirically confirmed printed declaration `(NumList?, NumList?, NumList)` causes mode-mismatch errors at clause heads + body atoms). The `%%` paraphrase comment on the qsort declaration MUST explicitly document the Q10 amendment with provenance ("printed PDF text shows `(NumList?, NumList?, NumList)` which contradicts the prose + clause shapes; prose-consistent form used per Q10 amendment"). (b) **Issue B — interleaved layout**: declarations interleaved with their respective clauses (PDF stacks all three decls at top of §5.6 then clauses below; REPL parser requires immediate-clause-after-decl per Q11 T4a/T4b empirically confirmed). The `.glp` header block MUST explicitly document the Q10 layout amendment with reason: "PDF stacks the three procedure declarations at the top and clauses below; the REPL parser requires immediate-clause-after-decl, so declarations and clauses are interleaved per Q10 amendment." Clause text remains byte-exact PDF; only LAYOUT is amended. Layout pattern: NumList type def → quicksort decl + 1 clause → qsort decl (Q10-corrected) + 2 clauses → partition decl + 3 clauses.
- [ ] T093 [US3] Verify load: expect `✓ Loaded:` + zero errors with both Q10 amendments applied (Q11 T4c empirically confirmed). If rejected without Q10 amendments → Q11 T4a/T4b/T4d expected failure modes.
- [ ] T094 [US3] Propose primary + 3 inspection goals. Example primary: `quicksort([3,1,4,1,5,9,2,6], S).` → `S = [1,1,2,3,4,5,6,9]`. Inspections exercise `qsort/3` base case + recursive step and `partition/4` element-< / element-≥ branches. Per SC-010, 4-goal session collectively exercises all 6 clauses + 3 procedure declarations. Wait for approval.
- [ ] T095 [US3] Run 4-goal session + capture verbatim.
- [ ] T096 [US5] Write `ex-05-repl-trace.md` per 5-phase positive structure.
- [ ] T097 [US5] Write `ex-05-tutorial.md`.

### Flagship group approval gate (Phase 5 exit)

- [ ] T100 [US3+US5] Run baseline tests: PASS expected.
- [ ] T101 [US3+US5] Show Flagship group diff. Wait for approval.
- [ ] T102 [US3+US5] On approval (single-exercise group): flip ex-05 status block line atomically. Commit `implement(ch05): Flagship group landed (typed quicksort with Q10 dual amendment)`.

**Checkpoint**: Flagship group approved; Negatives group unblocked. Gate-grep contract: `grep -cE "^- exercise-05: approved" ch05_tutorial.md` returns 1 (Q12 binding form).

---

## Phase 6: Group Negatives — User Story 4 (§5.7, P2)

**Predecessor gate**: Flagship group approved + R-006 re-verification (typically no-op since REPL hasn't changed since T001-equivalent).

### ex-06 (§5.7.1 Type Error — negative; two-`.glp`)

- [ ] T110 [US4] Pre-flight gate: `grep -cE "^- exercise-05: approved" ch05_tutorial.md` MUST return 1 (Q12 post-Q7 grep contract). R-006 type-checker re-verification PASSED (re-check against current build via T006a procedure on a scratch file).
- [ ] T111 [US4] Create `olamni/tutorial/ch05/exercise-06/`.
- [ ] T112 [US4] Write `ch-05-ex-06-type-error-failing.glp` per contracts/glp-file-format.md File 6a: `procedure foo(NumList).` + `foo([a, b, c]).` byte-exact from book p 51. Header MARKED `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠`. Per-clause `%%` paraphrase per FR-005+SC-017.
- [ ] T113 [US4] Verify failing-form FAILS to load: per Q11 T3 empirical capture, expect 3-line type-error message `Inconsistent path: Number type requires numeric literal Path: ([|]/2, 0, output) → (a, 1, output)` (and analogous for b, c) at line 5. Capture verbatim. Inspect for per-run-varying segments per R-011 — per Q11 T3, NO such segments observed (no memory address, no tuple-id, no wallclock); full byte-equality holds; R-011 relaxation NOT triggered for current REPL build. If a future REPL build introduces per-run-varying segments → halt-and-amend per R-011 procedure.
- [ ] T114 [US4] Write `ch-05-ex-06-type-error-corrected.glp` per File 6b spec. Project owner-approved corrected form (e.g., re-typed declaration accepting atom values like `procedure foo(List).` if pedagogically appropriate, OR a clause body that constructs valid `NumList` content — specific corrected-form shape decided at T114 with project-owner approval; book does NOT cite a specific corrected form for §5.7.1 unlike §5.7.2). Wait for approval.
- [ ] T115 [US4] Verify corrected-form loads successfully: `✓ Loaded:` + zero errors.
- [ ] T116 [US5] Write `ex-06-repl-trace.md` per contracts/trace-file-format.md **negative 2-phase structure** (Phase A failing-load + Phase B corrected-load). Optional Phase C if a success-confirmation goal is included per T117. Per FR-014 + Q11 T3, full byte-equality holds (no per-run-varying segments); the captured 3-line type-error message is locked into the trace.
- [ ] T117 [US4] *(Optional Phase C — symmetric with T125 for ex-07)* Propose success-confirmation goal for ex-06's corrected form. Wait for approval. Run + capture. Decision per-exercise — may be omitted if the corrected form's "success" is sufficiently demonstrated by the load alone.
- [ ] T118 [US5] Write `ex-06-tutorial.md`. EXPLICITLY state load failure is the demonstrated outcome, NOT a tutorial bug. Cross-reference Q11 T3 empirical capture for the exact error message learners should expect.

### ex-07 (§5.7.2 Mode Error — negative; two-`.glp`; book-cited corrected form)

- [ ] T120 [US4] Create `olamni/tutorial/ch05/exercise-07/`.
- [ ] T121 [US4] Write `ch-05-ex-07-mode-error-failing.glp` per File 7a spec: `procedure bar(Number?, Number).` + `bar(X?, Y).` byte-exact from book pp 51–52. Header MARKED `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠`. Per-clause `%%` paraphrase.
- [ ] T122 [US4] Verify failing-form FAILS to load: per Q11 T6 empirical capture, expect 2-line mode-mismatch error `Variable mode mismatch: writer requires ↑ (produce), got ↓ (consume) Path: (X, 0, input)` + `reader requires ↓ (consume), got ↑ (produce) Path: (Y?, 0, output)` at line 3. Capture verbatim. Inspect per R-011 — per Q11 T6, NO per-run-varying segments observed; full byte-equality holds.
- [ ] T123 [US4] Write `ch-05-ex-07-mode-error-corrected.glp` per File 7b spec: book-cited corrected form `procedure bar(Number?, Number).` + `bar(X, Y?) :- Y := X? + 1.` byte-exact from book p 52. (No proposal step needed — corrected form is BOOK-CITED.) Per FR-015, `:=` is permitted here as a byte-exact PDF clause that uses it.
- [ ] T124 [US4] Verify corrected-form loads successfully: `✓ Loaded:` per Q11 T7 empirical confirmation.
- [ ] T125 [US4] *(Optional Phase C)* Propose success-confirmation goal `bar(5, R).` → `R = 6` to demonstrate the fix actually works. Wait for approval. Run + capture.
- [ ] T126 [US5] Write `ex-07-repl-trace.md` per negative 2-phase or 3-phase structure (3-phase if Phase C included).
- [ ] T127 [US5] Write `ex-07-tutorial.md`. EXPLICITLY state load failure is the demonstrated outcome. Cross-reference Q11 T6+T7 empirical captures.

### Negatives group approval gate + chapter complete (Phase 6 exit)

- [ ] T130 [US4+US5] Run baseline tests: PASS expected.
- [ ] T131 [US4+US5] Show Negatives group diff (2 exercises). Wait for approval.
- [ ] T132 [US4+US5+US7] On approval (chapter complete):
  - Flip ex-06 + ex-07 status block lines to `approved YYYY-MM-DD` atomically.
  - Edit `olamni/tutorial/tutorial.md` ch05 row from `pending review (…)` to `implemented YYYY-MM-DD`.
  - Commit `implement(ch05): chapter complete — Negatives group + top-level index flip`.

**Checkpoint**: All 4 groups approved; chapter 5 complete. All 7 exercises (post-Q7+Q12) in `approved YYYY-MM-DD` state.

---

## Phase 7: Polish & Cross-Cutting

- [ ] T140 [P] No-fabrication audit: verify all files under `specs/006-tutorial-ch05/` are proper `/speckit-*` outputs. Per FR-012 + SC-011.
- [ ] T141 [P] Cross-chapter relationship documentation check: grep ex-03 + ex-04 (post-Q7+Q12) headers for canonical R-008 provenance line; verify `ch05_tutorial.md` signpost prose mentions both relationships. Per FR-002 + SC-007 (Q12 binding form).
- [ ] T142 [P] Cross-chapter scope check: grep all 7 exercise dirs' 9 `.glp` files for procedure names from other chapters. Should match only ch05 native (`merge/3`, `counter/2`, `quicksort/2`, `qsort/3`, `partition/4`, `foo/1`, `bar/2`). The cross-chapter relationships in ex-03/ex-04 are documentation-only — `merge/3` and `counter/2` clauses in ch05 are byte-exact from §5.4/§5.5 PDF, NOT byte-identical to ch04's clauses.
- [ ] T143 [P] Test harness exclusion check: `grep "olamni/tutorial/ch05" test/run_all_tests.sh` MUST return 0 matches. Per FR-016 + SC-014.
- [ ] T144 [P] Body-kernel scope check: `grep -E "now\\(|'_output'" olamni/tutorial/ch05/exercise-*/*.glp` MUST return 0 matches. `:=` permitted only inside ex-07's corrected `bar(X, Y?) :- Y := X? + 1.` per Q11 T7 + book p 52 byte-exact. Per SC-015.
- [ ] T145 [P] No-helper audit (Q7 retraction enforcement): `grep -E "%% --- DEMONSTRATION HELPERS ---" olamni/tutorial/ch05/exercise-*/*.glp` MUST return 0 matches (the pre-Q7 marker MUST NOT appear); helper-named procedures (`bit_test`, `nat_test`, `numlist_test`, `list_test`, `any_test`) MUST NOT appear in any ch05 `.glp`. Q8 minimal coverage stubs in ex-04 are PERMITTED — they are explicitly framed differently with `%% --- Q8 MINIMAL COVERAGE STUBS ---` marker per T071, and are minimal completions for type-checker exhaustiveness.
- [ ] T146 [P] Negative-exercise outcome check: ex-06 + ex-07 failing-form load attempts produce documented type/mode-error messages per Q11 T3+T6 (verifiable via captured traces); corrected forms load successfully per Q11 T7. Per SC-009.
- [ ] T147 Final baseline test pass: PASS expected (count unchanged from ch04 ship state).
- [ ] T148 Trace reproducibility check: re-run all 7 traces; diff against committed `.md` files modulo banner. Per FR-014 + SC-005. Per Q11, no R-011 relaxation needed for current REPL build.
- [ ] T149 [P] Walk-through verification (soft): SC-001 60-min budget logged as known follow-up.
- [ ] T150 Commit + push branch `006-tutorial-ch05`. Per Constitution multi-Claude protocol — `git add` SPECIFIC files only (no `git add -A` or `git add .`).
- [ ] T151 Provide merge instructions to project owner per workflow memory mandatory format (cd to GLP root + checkout main + pull + fetch + merge + push, with actual branch name `006-tutorial-ch05`).

**Checkpoint**: Chapter 5 fully delivered, audited, and ready for merge.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001..T006a sequential. T006a (R-006) is the NEW pre-flight verification BLOCKING all Foundations work.
- **Foundational (Phase 2)**: T006 + T007 — required before any user story.
- **Foundations group (Phase 3)**: T010..T052 sequential within group; signpost (T040–T042) interleaved.
- **Mode-checking-flow group (Phase 4)**: T060..T082; gated on Phase 3 approval (Q12 grep contract: 2 matches).
- **Flagship group (Phase 5)**: T090..T102; gated on Phase 4 approval (Q12 grep contract: 2 matches).
- **Negatives group (Phase 6)**: T110..T132; gated on Phase 5 approval (Q12 grep contract: 1 match) + R-006 re-verification.
- **Polish (Phase 7)**: T140..T151; T140-T146 + T149 [P] independent.

### Approval Gates

| Gate | Blocks | Set by | Q12 grep contract |
|---|---|---|---|
| R-006 type-checker verification (T006a) | T010+ (Phase 3) | T006a itself | (no grep — pre-flight) |
| Foundations group approval (T052) | T060+ (Phase 4) | T052 itself, after T051 | `^- exercise-(01\|02): approved` returns 2 |
| Mode-checking-flow group approval (T082) | T090+ (Phase 5) | T082 itself, after T081 | `^- exercise-(03\|04): approved` returns 2 |
| Flagship group approval (T102) | T110+ (Phase 6) | T102 itself, after T101 | `^- exercise-05: approved` returns 1 |
| Negatives group approval (T132) | (chapter complete) | T132 itself, after T131 | `^- exercise-(06\|07): approved` returns 2 |

### User Story Mapping

- **US1** (P1 Type-system foundations) → Phase 3 ex-01 + ex-02 tasks (T010..T024)
- **US2** (P1 Mode-checking flow) → Phase 4 ex-03 + ex-04 tasks (T060..T076)
- **US3** (P1 Typed quicksort flagship) → Phase 5 ex-05 tasks (T090..T097)
- **US4** (P2 Type errors and mode errors) → Phase 6 ex-06 + ex-07 tasks (T110..T127)
- **US5** (P1 Step-through guides + traces) → Per-exercise trace.md + tutorial.md tasks (T013..T014, T023..T024, T066..T067, T075..T076, T096..T097, T116+T118, T126..T127)
- **US6** (P2 Chapter signpost) → Phase 3 signpost tasks (T040, T041)
- **US7** (P3 Top-level index) → Phase 3 + Phase 6 index tasks (T042, T132 last bullet)

### Parallel Opportunities

- **Phase 7**: T140-T146 + T149 [P] — different files, independent grep audits.
- Most tasks within an exercise are sequential (write file → verify load → propose goals → run goals → write trace → write tutorial).
- Within a sub-section group, exercises are sequential (per R-010): Foundations ex-01 → ex-02; Mode-checking-flow ex-03 → ex-04; Flagship ex-05 (single); Negatives ex-06 → ex-07.
- Across sub-section groups: NO parallelism (gated per FR-008).

---

## Implementation Strategy

### MVP First (Foundations group only)

1. Phase 1 (T001..T006a) — including R-006 type-checker re-verification against current REPL build.
2. Phase 2 (T006..T007).
3. Phase 3 (T010..T052) — Foundations group complete (load-only ex-01 + ex-02) + signpost + top-level index.
4. **STOP and VALIDATE**: Foundations is fully usable for a learner — covers §5.1 type definitions + §5.2 built-in types via load-only exercises. Type-checker is verified operational; no fabricated helpers per Q7.

### Incremental Delivery by Group

5. Phase 4 (Mode-checking-flow group) — 2 exercises with worked-example mode checking + response slots; cross-chapter relationships documented; Q8 coverage stubs in ex-04.
6. Phase 5 (Flagship group) — 1 exercise, the chapter's typed quicksort flagship with Q10 dual amendment.
7. Phase 6 (Negatives group) — 2 exercises with negative-load-test contract; per Q11 R-011 relaxation NOT triggered.
8. Phase 7 (polish + commit + merge instructions).

### Total Wall-Clock Estimate

- Phase 1+2: 30 min (Dart verify, REPL build, baseline test, R-006 type-checker re-verification ~5 min, PDF re-read).
- Phase 3 (Foundations): **15–20 min** (2 load-only exercises; trivial transcription per Q7).
- Phase 4 (Mode-checking-flow): 30–45 min (2 exercises, worked merge ~3 clauses + counter response-slot 1 clause + Q8 coverage stubs + cross-chapter headers).
- Phase 5 (Flagship): 25–35 min (1 exercise, typed quicksort 6 clauses + 3 procedure decls + Q10 dual amendment header + interleaved layout).
- Phase 6 (Negatives): 25–35 min (2 exercises, two-`.glp` pattern each; failing-form verification per Q11 captures + corrected-form proposal/write).
- Phase 7: 20 min (polish + commit + merge instructions).

**Total**: ~2.5–3 hours with auto-mode approvals at group boundaries. Smaller than ch04 (5–7 hr) because volume is smaller (~10 PDF blocks vs ~38), helpers retracted per Q7 (saves ~30 min), and Q11 empirical pre-verification captures the negative-exercise error messages in advance (no surprise inspection for per-run-varying segments).

---

## Notes

- [P] tasks = different files, no shared deps — parallelisable.
- [Story] label maps tasks to spec.md user stories (US1..US7).
- US1+US2+US3+US4 are gated cross-group per FR-008+FR-009 group-boundary model.
- US5 (per-exercise traces+tutorials) interleaves with each group; trace+tutorial happen immediately after the corresponding `.glp` file is written + (for runnable exercises) 4-goal session captured.
- **R-006 type-checker verification (T006a) is a NEW pre-flight step for ch05** — ch05 is the first chapter where the type-checker does meaningful work; if broken, chapter cannot proceed. Already passed against build `2362202d` (research.md Appendix A) + build `bcd59392` (Q11 empirical); re-verified at runtime against current build.
- **Per Q11 empirical (REPL build `bcd59392`, 2026-05-01) R-011 per-run-varying-segment relaxation is NOT triggered for current REPL build** — full byte-equality holds for both negative-exercise error messages. If a future REPL build introduces per-run-varying segments at T113/T122 capture, halt-and-amend per R-011.
- **Per Q7 retraction, NO fabricated helpers in any ch05 exercise.** Type-only exercises ex-01 + ex-02 are 1-phase load-only with byte-exact PDF text only. T145 [P] Polish task explicitly audits this.
- **Q8 minimal coverage stubs in ex-04 are PERMITTED** but explicitly framed as Q-amendment for type-checker exhaustiveness, not as "demonstration helpers". T071 + T145 enforce the framing.
- **Q10 dual amendment in ex-05 is LOCKED at the spec layer** — both amendments (corrected qsort signature + interleaved layout) MUST appear in ex-05's `.glp` per T092 with documented header provenance.
- **Q12 binding numbering applies throughout this tasks.md** — pre-Q7 references (e.g., 8 exercises, ex-03 procedure-decl-only, helpers, Foundations grep returns 3) are STALE and MUST NOT be acted on. Where research.md / data-model.md / quickstart.md still carry pre-Q7 references at /speckit-implement runtime, the implementer falls back to spec.md (Q12 + Q7 + Q11 + Q10 + Q8 + Q6 + Q5 + Q4) as the binding source per FR-013.
- Per FR-013 + Constitution Principle II: any obstacle (Dart absent, REPL build fail, type-checker broken, binding mismatch, byte-exact transcription drift, cross-chapter relationship documentation drift, unexpected error category on negative-exercise load) → HALT and report.
- Per FR-012: Claude does NOT write speckit-format `spec.md`-style files. T140 verifies this.
- Per FR-015 + SC-015: `:=` permitted only inside byte-exact PDF clauses (specifically: ex-07's corrected `bar/2`); `now/1` and `'_output'/1` MUST NOT appear.
- Commit cadence: 4 group-approval commits + 1 polish/final commit = 5 commits total. `git add` SPECIFIC files per multi-Claude protocol.
- Constitution Principle V: baseline tests at T004 + T050 + T080 + T100 + T130 + T147 (6 baseline checks total). All must show PASS unchanged.
