# Implementer Quickstart — Olamni Tutorial Chapter 5

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-30 (initial); **2026-05-01 staleness header added during /speckit-analyze remediation**

> **⚠ STALENESS NOTICE (2026-05-01, post-Q7+Q12 binding)**
>
> This quickstart.md was authored against pre-Q7 spec state (8 exercises, helper-bearing Foundations group of 3 exercises, helper proposal step at /speckit-implement, "5-phase trace adjusted for type-only kind"). Post-Q7+Q12 binding: 7 exercises, **no fabricated helpers** (Q7 retracts Q2/R-012), Foundations = ex-01+ex-02 (2 exercises, both 1-phase load-only).
>
> **Binding authority: spec.md (Q12-unified) + tasks.md (post-Q7+Q12) + plan.md (post-Q12) + contracts/* (post-Q7+Q12).**
>
> **Stale narrative blocks**:
> - **Pre-flight step 6 (R-006)** is CURRENT — type-checker verification still required at /speckit-implement T006a; current REPL build re-verification (Q11 captured against `bcd59392`).
> - **"Implementation order (4 sub-section groups)"** — group composition under Q7+Q12: Foundations (ex-01 + ex-02 — load-only — NO helpers), Mode-checking-flow (ex-03 + ex-04), Flagship (ex-05), Negatives (ex-06 + ex-07). Within-group sequencing intact.
> - **"Group 1: Foundations"** — step 2 "Propose ex-01 + ex-02 + ex-03 helper shapes" is RETRACTED per Q7. Steps 3–8 apply only to ex-01 + ex-02 (NO helper layer, 1-phase load-only trace, no inspection goals). The pre-Q7 ex-03 procedure-decl-only step is dissolved into the Mode-checking-flow group's ex-03 (§5.3+§5.4 merged per Q7).
> - **"Group 2: Mode-checking-flow"** — exercise renumbering: pre-Q7 ex-04 (§5.4 worked merge) → post-Q7 ex-03; pre-Q7 ex-05 (§5.5 counter) → post-Q7 ex-04. Q8 minimal coverage stubs are required for ex-04 (post-Q7) — see contracts/glp-file-format.md File 4.
> - **"Group 3: Flagship"** — exercise renumbering: pre-Q7 ex-06 (§5.6 typed quicksort) → post-Q7 ex-05. Q10 dual amendment (corrected qsort signature + interleaved layout) MUST be applied per Q11 T4 empirical confirmation. Locked primary goal candidate `quicksort([3,1,4,1,5,9,2,6], S).` ⇒ `S = [1,1,2,3,4,5,6,9]` still applies.
> - **"Group 4: Negatives"** — exercise renumbering: pre-Q7 ex-07 (§5.7.1 type-error) → post-Q7 ex-06; pre-Q7 ex-08 (§5.7.2 mode-error) → post-Q7 ex-07. Per Q11 empirical T3+T6, both negative-exercise error messages have full byte-equality (no per-run-varying segments observed; R-011 relaxation NOT triggered for current REPL build).
> - **"Definition of Done"** — "all 8 NN" → all 7 NN post-Q7. "All 6 positive traces" → all 5 positive+load-only traces (ex-01..ex-05). "All 2 negative traces" → ex-06 + ex-07 post-Q7. "Helper layers" requirement RETRACTED.
> - **"On failure" table** — "Helper unit-clause violates SRSW or type-check (ex-01/ex-02/ex-03)" row RETRACTED per Q7.
>
> **Implementer guidance**: When this quickstart.md conflicts with spec.md, spec.md wins per FR-013. The narrative below remains useful for understanding the implementation flow, but the exercise numbering, helper authorization, and group composition MUST be cross-checked against spec.md Q12 + tasks.md before acting.

This is the implementer's quickstart for `/speckit-implement`. Chapter 5 is smaller in volume than ch04 (7 exercises post-Q7 vs 10; ~10 byte-exact Programs vs ~38; ~20–30 `%%` comments post-Q7 vs ~133) but introduces three exercise kinds (load-only / full-program / negative) plus the type-checker's first meaningful pipeline activation. (Subject to staleness annotations in the notice block above.)

---

## Pre-flight (do BEFORE creating any files)

1. **Pull `main`**: confirm at v2026.04.30 or later (post-ch04 ship).
2. **Verify branch**: `git branch --show-current` should print `006-tutorial-ch05`.
3. **Verify Dart SDK**: `"/c/Users/gavri/dart-sdk/bin/dart" --version` — must be 3.9.4+.
4. **Build the REPL binary**: rebuild if stale. If `claude/fix-misleading-build-line` (tag `v2026.04.29-3`) is merged, use `--define=GLP_BUILD_COMMIT=...`; otherwise build without (banner shows `Built from: unknown` — clear signal but not blocking).
5. **Record baseline test results**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — record actual baseline test count from ch04 ship state in research.md Appendix.
6. **R-006 type-checker operational verification** (NEW for ch05): per FR-018 + research R-006:
   - Construct a minimal positive test (e.g., load a 2-line file containing `Bit ::= 0 ; 1.`). Expect `✓ Loaded:` with zero errors.
   - Construct a minimal negative test (e.g., a clause asserting a non-`Number` value satisfies `Number`, OR use `procedure foo(Number).` + `foo(a).` as a deliberate type-error trigger). Expect a type-error message; load fails.
   - If positive case fails OR negative case succeeds → HALT per FR-013. ch05 work cannot proceed against a broken type-checker.
   - Record both captured outputs in `research.md` Appendix A (created at this step).
7. **Verify spec inputs are in place**:
   - `specs/006-tutorial-ch05/spec.md` exists with 3 Clarifications (Q1+Q2+Q3) + 4 pre-resolved.
   - `olamni/tutorial/ch05/ch05-specification-input-prompt.md` exists.
   - `olamni/tutorial/ch05/ch05-sources.md` exists.
   - `olamni/tutorial/ch05/spec-rev-eng-input/ch05-DEPRECATED-spec.md` exists.

If any pre-flight step fails: halt, report to project owner, do not proceed.

---

## Implementation order (4 sub-section groups, sequential by group)

### Group 1: Foundations (ex-01 + ex-02 + ex-03)

**Predecessor gate**: chapter signpost exists (created during this group's work) + R-006 type-checker verification PASSED.

1. **Re-read PDF book p 47** (PDF p 59) byte-exactly for §5.1 type definitions + surrounding prose + Formal 5.1 (p 48). Extra attention to `?` reader marks, `;` alternation separators, `|` list-cons separators.
2. **Propose ex-01 + ex-02 + ex-03 helper shapes** (R-012 + Q2 deferral) to project owner. Wait for approval (or auto-mode). Helpers proposed per R-012 concrete shapes: ex-01 `bit_test/1` × 2 + `nat_test/1` × 3 + `numlist_test/1` × 3; ex-02 `list_test/1` × 3 + `any_test/1` × 3; ex-03 stub `merge(L?, R?, M) :- L? = [], M = R?.` (1-clause; expand to 2 if type-checker rejects trivial form).
3. **Create `olamni/tutorial/ch05/exercise-01/`** + write `ch-05-ex-01-type-definitions.glp` per `contracts/glp-file-format.md` File 1 spec. 3 type defs byte-exact from book p 47 + helper layer below `%% --- DEMONSTRATION HELPERS ---` marker.
4. **Verify ex-01 file loads** via REPL:
   ```bash
   printf "olamni/tutorial/ch05/exercise-01/ch-05-ex-01-type-definitions.glp\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
   ```
   Expect `✓ Loaded:` + zero errors. The type-check stage validates `Bit`/`Nat`/`NumList` definitions. If rejected, HALT (could indicate helper SRSW/type-check violation per R-012).
5. **Propose 3 inspection goals to project owner** for ex-01 (per R-004; "primary" is the load itself for type-only). Wait for approval.
6. **Run ex-01 inspection-goal session** + capture verbatim output. Verify locked bindings.
7. **Write `ex-01-repl-trace.md`** per `contracts/trace-file-format.md` (5 phases adjusted for type-only kind: load + first inspection + 2 more inspections + closing).
8. **Write `ex-01-tutorial.md`** — learner step-through. Explicitly note that helpers are demonstration-only, not from the book.
9. **Write `ch05_tutorial.md`** signpost initially with status block per `contracts/status-block-format.md` initial state (ex-01 = `pending review`; ex-02..ex-08 = `pending exercise-N approval`). Include cross-chapter relationships note + group-structure note + negative-exercise contract note + Sources cross-reference per FR-005.
10. **Update `olamni/tutorial/tutorial.md`** — flip ch05 row from `planned` to `pending review (YYYY-MM-DD)`.
11. **Repeat steps 3–8 for ex-02** (`ch-05-ex-02-built-in-types.glp`; 1 type def + 6 helper unit clauses).
12. **Repeat steps 3–8 for ex-03** (`ch-05-ex-03-procedure-declaration.glp`; 1 procedure decl + 1–2 stub clauses).
13. **Run baseline tests post-Foundations group**: `bash test/run_all_tests.sh` — expect baseline PASS unchanged.
14. **Stop and report to project owner**. Show Foundations group diff (3 exercises landed). Wait for explicit `approved` signal (or auto-mode).
15. **On Foundations group approval**: edit `ch05_tutorial.md` status block to flip `exercise-01` + `exercise-02` + `exercise-03` to `approved YYYY-MM-DD` (group-atomic flip). Commit with message `implement(ch05): Foundations group landed (type definitions + built-in types + procedure declaration)`.

### Group 2: Mode-checking-flow (ex-04 + ex-05)

**Predecessor gate**: Foundations group fully approved (check via `grep -cE "^- exercise-(01|02|03): approved" ch05_tutorial.md` returns 3). Halt if not.

16. **Re-read PDF book pp 49–50** (PDF pp 61–62) byte-exactly for §5.4 worked merge + §5.5 counter response-slot + Formal 5.2 + Formal 5.3.
17. **Write ex-04** (`mode-checked-merge.glp`) per `contracts/glp-file-format.md` File 4 spec. CRITICAL: header MUST contain canonical R-008 cross-reference block citing ch04 ex-04 untyped predecessor. `%%` annotations on each merge/3 clause walk through the head/body mode-check steps from §5.4 prose IN ADDITION to per-clause paraphrase per SC-017.
18. **Verify ex-04 loads + propose 1 primary + 3 inspection goals + run 4-goal session + write trace + tutorial.** ex-04's trace's Phase A annotation MUST include the cross-chapter relationship disclosure per `contracts/trace-file-format.md` annotation rule 5.
19. **Write ex-05** (`counter-response-slot.glp`) per File 5 spec. Header MUST contain canonical R-008 cross-reference block citing ch04 ex-06 untyped predecessor. ex-05's trace Phase A annotation analogously discloses the cross-chapter relationship.
20. **Verify ex-05 loads + 4-goal session + trace + tutorial.**
21. **Run baseline tests post-Mode-checking-flow group**: baseline PASS expected.
22. **Stop and report.** Wait for approval.
23. **On Mode-checking-flow group approval**: flip ex-04 + ex-05 status block lines atomically. Commit.

### Group 3: Flagship (ex-06)

**Predecessor gate**: Mode-checking-flow group fully approved.

24. **Re-read PDF book p 51** (PDF p 63) byte-exactly for §5.6 typed quicksort.
25. **Write ex-06** (`typed-quicksort.glp`) per File 6 spec. 1 type def (NumList; duplicated inline from ex-04 per FR-010) + 3 procedure decls + 6 clauses byte-exact.
26. **Verify ex-06 loads + propose 1 primary + 3 inspection goals + run 4-goal session + write trace + tutorial.** Primary goal target: `quicksort([3,1,4,1,5,9,2,6], S).` ⇒ `S = [1,1,2,3,4,5,6,9]` (or whichever input list /speckit-implement T006-equivalent locks).
27. **Verify SC-010**: 4-goal session collectively exercises all 6 clauses + 3 procedure declarations.
28. **Run baseline tests post-Flagship group**: baseline PASS expected.
29. **Stop and report.** Wait for approval.
30. **On Flagship group approval (single-exercise)**: flip ex-06 status block line atomically. Commit.

### Group 4: Negatives (ex-07 + ex-08)

**Predecessor gate**: Flagship approved + R-006 type-checker re-verification (typically no-op since REPL hasn't changed since T001-equivalent).

31. **Re-read PDF book pp 51–52** (PDF pp 63–64) byte-exactly for §5.7.1 type-error + §5.7.2 mode-error illustrations + corrected form `bar(X, Y?) :- Y := X? + 1.`.
32. **Write ex-07 failing form** (`ch-05-ex-07-type-error-failing.glp`) per File 7a spec. Header explicitly marked `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠`.
33. **Verify ex-07 failing form FAILS to load**:
    ```bash
    printf "olamni/tutorial/ch05/exercise-07/ch-05-ex-07-type-error-failing.glp\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
    ```
    Expect a type-error message documenting the type mismatch. Capture verbatim. Inspect for per-run-varying segments per R-011 — if any (memory address, tuple-id), HALT and propose Clarifications amendment per FR-013.
34. **Propose corrected form** for ex-07 to project owner (e.g., re-typed `procedure foo(Atom).`). Wait for approval.
35. **Write ex-07 corrected form** (`ch-05-ex-07-type-error-corrected.glp`) per File 7b spec.
36. **Verify ex-07 corrected form loads successfully**: expect `✓ Loaded:` + zero errors.
37. **Write ex-07 trace + tutorial.** Trace structure: 2 phases (Phase A failing-load + Phase B corrected-load) OR 3 phases if a success-confirmation goal is included.
38. **Repeat steps 32–37 for ex-08** (`mode-error-failing.glp` + `mode-error-corrected.glp`). The corrected form is BOOK-CITED `bar(X, Y?) :- Y := X? + 1.` from book p 52. Optional Phase C exercises `bar(5, R).` ⇒ `R = 6`.
39. **Run baseline tests post-Negatives group**: baseline PASS expected.
40. **Stop and report.** Show Negatives group diff (2 exercises landed). Wait for approval.
41. **On Negatives group approval (chapter complete)**:
    - Flip ex-07 + ex-08 status block lines to `approved YYYY-MM-DD` atomically.
    - Edit `olamni/tutorial/tutorial.md` ch05 row from `pending review (…)` to `implemented YYYY-MM-DD`.
    - Commit with message `implement(ch05): chapter complete — Negatives group + top-level index flip`.

---

## Polish & Cross-Cutting

42. **No-fabrication audit**: verify all files under `specs/006-tutorial-ch05/` are proper `/speckit-*` outputs. Per FR-012 + SC-011.
43. **Cross-chapter relationship documentation check**: grep ex-04 + ex-05 headers for the canonical R-008 provenance line. Verify `ch05_tutorial.md` signpost prose mentions both relationships. Per FR-002 + SC-007.
44. **Cross-chapter scope check**: grep all 8–10 ch05 `.glp` files for procedure names from other chapters; should match only ch05 native (the cross-chapter relationships in ex-04/ex-05 are documentation, not code imports — `merge/3` and `counter/2` clauses in ch05 are byte-exact from §5.4/§5.5 PDF, NOT byte-identical to ch04's clauses).
45. **Test harness exclusion check**: `grep "olamni/tutorial/ch05" test/run_all_tests.sh` MUST return zero matches. Per FR-016 + SC-014.
46. **Body-kernel scope check**: `:=` permitted only inside byte-exact PDF clauses that use it (specifically: ex-08's corrected `bar(X, Y?) :- Y := X? + 1.`); `now/1` and `'_output'/1` MUST NOT appear anywhere in ch05. Per spec FR-015 + SC-015.
47. **Helper-layer discipline check**: ex-01/ex-02/ex-03 helpers are below `%% --- DEMONSTRATION HELPERS ---` marker; helper procedure names do not collide with PDF-Program names (R-012 rule 6); each helper carries `%%` per clause.
48. **Negative-exercise outcome check**: ex-07 failing-form + ex-08 failing-form load attempts produce documented type/mode-error messages (verifiable via the captured traces). Per SC-009.
49. **Final baseline**: baseline PASS expected.
50. **Trace reproducibility check**: re-run all 8 traces; diff against committed `.md` files modulo banner (and modulo R-011 per-run-varying segments for negative exercises if relaxation was applied).
51. **Walk-through verification (soft)**: log SC-001 60-min budget as known follow-up.
52. **Commit + push** branch `006-tutorial-ch05`. Per Constitution multi-Claude protocol — `git add` SPECIFIC files only.
53. **Provide merge instructions** to project owner per the workflow memory's mandatory format.

---

## On failure (any phase)

Per Constitution Principle II (No Workarounds), every failure mode below requires HALT-and-REPORT. Do NOT silently fix, do NOT add try/catch-and-ignore, do NOT mark expected-to-fail.

| Failure | Action |
|---|---|
| Dart absent or below 3.9.4 | Halt at pre-flight 3. Report. |
| REPL build fails | Halt at pre-flight 4. Capture full build output. Report. |
| Baseline tests fail | Halt at pre-flight 5. Report which sections failed. Do NOT proceed. |
| **R-006 type-checker false-negative or false-positive** | Halt at pre-flight 6. ch05 work CANNOT proceed against a broken type-checker. Report which case (false-negative / false-positive) + captured output. |
| GLP file rejected at load (positive exercise) | Halt at the relevant phase. Re-read PDF byte-exact; if still rejected, this is either (a) a book-internal SRSW/type-check inconsistency requiring Clarifications amendment per ch04 Q4–Q10 precedent, or (b) a runtime regression. Report. |
| Helper unit-clause violates SRSW or type-check (ex-01/ex-02/ex-03) | Halt. Helper shape is amendable per R-012 rule 1; propose alternate helper shape and re-verify. The byte-exact PDF type definition is locked; only the helper changes. |
| Primary-goal locked binding does not match | Halt. Either prediction is wrong OR runtime is misbehaving. Report which. Do NOT silently update spec — propose Clarifications amendment per FR-013 if needed. |
| Cross-chapter relationship documentation drift (header citation form mismatches R-008 canonical) | Halt at the relevant exercise. Align with R-008 canonical block; do not freelance. |
| **Negative exercise's failing-form load SUCCEEDS** (false-positive type-checker) | Halt. The expected-to-fail load did not fail. Either (a) the type-checker has a false-positive on §5.7.1 or §5.7.2 PDF code (regression), or (b) the implementer transcribed the failing form wrong. Investigate. Per spec edge case "Type-checker is in a broken state". |
| **Negative exercise's failing-form load fails with UNEXPECTED error** (e.g., parse error rather than type-error) | Halt. Report the captured error. Either the implementer's transcription is wrong OR the REPL build's error categorisation has changed. Re-read PDF byte-exact + verify; if still unexpected, propose Clarifications amendment. |
| Negative exercise's error message contains per-run-varying segment | Halt at /speckit-implement T026/T037-equivalent per R-011. Propose Clarifications amendment for R-011 relaxation. |
| Procedure-redeclaration conflict during ex-NN load | Per FR-010 self-containment, each `.glp` is loaded standalone in a fresh REPL session. If you see redeclaration conflicts, you may have loaded multiple ch05 files in one session — load them separately. |
| Goal exceeds REPL execution limit (`:limit`) | Bump limit via REPL `:limit` directive before the goal. Document in trace if the limit was bumped. (Less likely in ch05 than ch04 — quicksort is the only candidate.) |
| Any post-implementation test failure (baseline → less than baseline) | Halt. ch05 work is entirely under `olamni/tutorial/ch05/**` per FR-016; harness regression indicates unrelated bug or scope creep. Investigate before proceeding. |

---

## Definition of Done (chapter-5)

All of the following MUST hold:

- All ~30 files written (8 baseline `.glp` + 2 extra for negative two-file pattern + 16 markdown new + 1 signpost; 1 input prompt + 1 sources index + 1 deprecated spec copy already existed).
- Top-level `tutorial.md` updated; ch05 row reads `implemented YYYY-MM-DD`.
- Status block in `ch05_tutorial.md` reads `exercise-NN: approved YYYY-MM-DD` for all 8 NN.
- All 6 positive traces (ex-01 through ex-06) are byte-equal modulo REPL banner / build wallclock lines to a fresh REPL re-run by an auditor.
- All 2 negative traces (ex-07 + ex-08) are byte-equal modulo REPL banner / build wallclock lines AND modulo R-011 per-run-varying segments (if relaxation applied) to a fresh REPL re-run.
- All POSITIVE `.glp` files (ex-01 through ex-06) load successfully on a clean re-run; primary goals produce the locked bindings.
- All NEGATIVE failing-form `.glp` files (ex-07-failing, ex-08-failing) FAIL to load on a clean re-run with the documented error messages.
- All NEGATIVE corrected-form `.glp` files (ex-07-corrected, ex-08-corrected) load successfully on a clean re-run.
- Cross-chapter relationship documentation: ex-04 + ex-05 headers contain canonical R-008 cross-reference; signpost prose mentions both relationships.
- Helper layers: ex-01/ex-02/ex-03 follow R-012 discipline (under marker; SRSW/type-check valid; no PDF-Program shadowing; `%%` per clause).
- R-006 type-checker verification PASSED at pre-flight 6 (recorded in research.md Appendix A).
- Baseline test suite still passes (count unchanged from ch04 ship state).
- Branch `006-tutorial-ch05` is committed and pushed.
- Project owner has explicitly approved ALL FOUR groups (Foundations / Mode-checking-flow / Flagship / Negatives — 4 separate group-approval events; group-boundary gates respected).

---

## Constitution alignment summary

- **I. Spec-First**: every step traces to spec FR-NNN, SC-NNN, or Clarifications Q-N (Q1+Q2+Q3 + 4 pre-resolved). No code or doc written outside the spec.
- **II. No Workarounds**: every failure is a halt; no try/catch-and-ignore. R-011 per-run-variation relaxation is itself a halt-and-amend, not a workaround.
- **III. SRSW Discipline**: all ~10 PDF Programs are SRSW-compliant by byte-exact construction. Helpers (R-012) MUST also satisfy SRSW.
- **IV. FCP Reference**: N/A. The REPL's type-checker is exercised as a black-box validator.
- **V. Test-First**: baseline before, baseline at each group boundary, baseline after; traces ARE regression artifacts. R-006 type-checker verification is itself a baseline-establishing test.
- **VI. Tutorial Charter Compliance**: charter §1, §1.5, design-principles 1–2 cited; cross-chapter relationships documented; no code imports.
- **Language Design Authority**: no new kernels / guards / system predicates / directives / type-system features. The type-system + mode declarations + `procedure` keyword + built-ins all PRE-EXIST.
- **Technology Stack**: Dart 3.9.4+, GLP, Markdown — all within stack.
