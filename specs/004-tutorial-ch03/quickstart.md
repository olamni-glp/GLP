# Implementer Quickstart — Olamni Tutorial Chapter 3

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-30

This is the implementer's quickstart for `/speckit-implement`. The LEARNER-facing quickstarts will live in each `olamni/tutorial/ch03/exercise-NN/ex-NN-tutorial.md` file once written. This file describes how the implementing Claude session executes the chapter-3 work end-to-end.

---

## Pre-flight (do BEFORE creating any files)

1. **Pull `main`**: `git fetch origin && git pull origin main`. Confirm at v2026.04.29-2 or later (v2026.04.29-3 if `claude/fix-misleading-build-line` has merged).
2. **Verify branch**: `git branch --show-current` should print `004-tutorial-ch03`.
3. **Verify Dart SDK**: `"/c/Users/gavri/dart-sdk/bin/dart" --version` — must be 3.9.4+. If absent or older, halt and report (per Edge Cases in spec).
4. **Build the REPL binary**: check `glp_runtime/glp_repl.exe` exists and is fresh. If not, build it. If `claude/fix-misleading-build-line` is merged, use the `--define` form:
   ```bash
   BUILD_COMMIT="$(git log -1 --format='%h %s')"
   "/c/Users/gavri/dart-sdk/bin/dart" compile exe glp_runtime/bin/glp_repl.dart --define=GLP_BUILD_COMMIT="$BUILD_COMMIT" -o glp_runtime/glp_repl.exe
   ```
   If unmerged, build without `--define` and record the omission in research.md.
5. **Record baseline test results**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — must show `Total: 494 | Passed: 494 | Failed: 0` (if v2026.04.29-3 merged) or `Total: 485 | Passed: 485 | Failed: 0` (if only v2026.04.29-2). Record this before ANY file work.
6. **Verify spec inputs are in place**:
   - `specs/004-tutorial-ch03/spec.md` exists with 3 Clarifications resolved (Q1 + Q2 + Q3).
   - `olamni/tutorial/ch03/ch03-specification-input-prompt.md` exists.
   - `olamni/tutorial/ch03/ch03-sources.md` exists.
   - `olamni/tutorial/ch03/spec-rev-eng-input/ch03-DEPRECATED-spec.md` exists.

If any pre-flight step fails: halt, report to project owner, do not proceed.

---

## Implementation order (ex-01 → ex-02 → ex-03)

### Phase 1 — exercise-01 (Program 3.1 + producer/consumer composed pipeline)

1. **Re-read PDF p 27 (book p 15)** byte-exactly for Program 3.1 + surrounding §3.1 prose. Note any drift vs `ch03-sources.md`. If drift found, correct `ch03-sources.md` BEFORE proceeding (per ch01's predict-and-verify lesson).
2. **Re-read PDF p 43 (book p 31)** byte-exactly for `producer/2` + `consumer/3` + Formal 4.2 prose.
3. **Propose 3 inspection goals** to project owner (per `research.md` R-004 — already locked in this plan: `producer(A, 0), producer(B, 0), merge(A?, B?, M), consumer(M?, 0, Sum).`, `producer(A, 0), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).`, `producer(A, 1), producer(B, 1), merge(A?, B?, M), consumer(M?, 0, Sum).`). Wait for explicit approval.
4. **Write `ch-03-ex-01-glp-fair-stream-merger.glp`** per `contracts/glp-file-format.md` File 1 spec (Program 3.1 byte-exact from PDF p 27 + header + 3 `%%` comments).
5. **Write `ch-03-ex-01-producer-consumer.glp`** per `contracts/glp-file-format.md` File 2 spec (producer/2 + consumer/3 byte-exact from PDF p 43 + R-007 provenance header + 4 `%%` comments).
6. **Capture the trace**: load both `.glp` files in the same REPL session and run the composed primary + 3 inspection goals. Use the kernel-snapshot batch pattern from the workflow memory:
   ```bash
   DART="/c/Users/gavri/dart-sdk/bin/dart"
   printf "olamni/tutorial/ch03/exercise-01/ch-03-ex-01-glp-fair-stream-merger.glp\nolamni/tutorial/ch03/exercise-01/ch-03-ex-01-producer-consumer.glp\nproducer(A, 5), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).\nproducer(A, 0), producer(B, 0), merge(A?, B?, M), consumer(M?, 0, Sum).\nproducer(A, 0), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).\nproducer(A, 1), producer(B, 1), merge(A?, B?, M), consumer(M?, 0, Sum).\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex01-trace.txt 2>&1
   ```
7. **Verify the locked binding**: confirm `Sum = 21` appears in `/tmp/ex01-trace.txt` for the primary goal. If not, halt-and-report per FR-013.
8. **Verify both files load**: confirm `✓ Loaded:` for BOTH `glp-fair-stream-merger.glp` AND `producer-consumer.glp` (or whatever load-success message the REPL produces). If procedure-redeclaration conflict between Program 3.1's `merge/3` and either ch4 procedure, halt-and-amend per the spec edge case (no conflict expected since ch4 imports define `producer/2` + `consumer/3`, not `merge/3`).
9. **Verify all three Program 3.1 clauses fired** across the four-goal session (per FR-018). Inspect the trace's stdout for evidence; if any clause was not exercised, halt-and-report.
10. **Write `ex-01-repl-trace.md`** per `contracts/trace-file-format.md` (six phases for ex-01: load Phase A + load Phase B + composed primary Phase C + three inspection Phases D / E / F). Code-block content is byte-verbatim from `/tmp/ex01-trace.txt`. Annotations OUTSIDE the blocks per the contract.
11. **Write `ex-01-tutorial.md`** as the learner-facing step-through (build REPL, load both `.glp` files, run primary + 3 inspection goals, observe SRSW reader/writer pairing across four roles, cross-check trace).
12. **Write `ch03_tutorial.md`** signpost with the cross-chapter import note (per `research.md` R-007), the §3.2 guard curriculum outline (built-in → defined → negation across the three exercises), and the status block reading `exercise-01: pending review`, `exercise-02: pending exercise-01 approval`, `exercise-03: pending exercise-02 approval`.
13. **Update `olamni/tutorial/tutorial.md`** — flip ch03 row from `planned` to `pending review (2026-04-30)`.
14. **Run baseline tests again**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — must still show the same baseline number (494 or 485 depending on which fixes are merged).
15. **Stop and report to project owner**. Provide the trace + tutorial diff for review. Wait for explicit `approved` signal.
16. **On approval**: edit `ch03_tutorial.md` status block to flip `exercise-01: approved 2026-04-30` and `exercise-02: pending review`. Commit. Do NOT begin ex-02 until this step is committed and the project owner has confirmed.

### Phase 2 — exercise-02 (`channel/1` + `process/2` defined-guard demo)

GATE: ex-01 status is `approved`. Halt if not.

17. **Re-read PDF p 34 (book p 22)** byte-exactly for `channel/1` + `process/2` + surrounding §3.2 prose. Note any drift.
18. **Confirm R-008 + R-009 decisions with project owner**: local `handle/1` stub `handle(_).` (per R-008); stand-alone shape, no `merge/3` duplication (per R-009). Wait for explicit approval before writing the file.
19. **Propose 3 inspection goals** to project owner (per `research.md` R-004 — already locked in this plan: `process(foo, Status).`, `process(ch([], []), Status).`, `process([1,2,3], Status).`). Wait for explicit approval.
20. **Write `ch-03-ex-02-defined-guards.glp`** per `contracts/glp-file-format.md` File 3 spec — channel/1 + process/2 byte-exact from PDF p 34 + local `handle/1` stub + header + 4 `%%` comments.
21. **Capture the trace**:
    ```bash
    printf "olamni/tutorial/ch03/exercise-02/ch-03-ex-02-defined-guards.glp\nprocess(ch(a, b), Status).\nprocess(foo, Status).\nprocess(ch([], []), Status).\nprocess([1,2,3], Status).\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex02-trace.txt 2>&1
    ```
22. **Verify locked bindings**: `Status = ok` for primary (`process(ch(a, b), Status).`); `Status = error` for inspection 1; `Status = ok` for inspection 2; `Status = error` for inspection 3. If any mismatch, halt-and-report per FR-013.
23. **Verify both `process/2` clauses fired** (clause 1 for primary + inspection 2; clause 2 for inspections 1 + 3). If either not exercised, halt-and-report.
24. **Write `ex-02-repl-trace.md`** per `contracts/trace-file-format.md` (five phases for ex-02). Strict byte-equality contract per FR-014 — no relaxation.
25. **Write `ex-02-tutorial.md`** as the learner-facing step-through (load file, run primary + 3 inspection goals, observe how `channel/1` defined guard succeeds for ch-shaped inputs and fails for others, the `otherwise` fallback selecting clause 2 when clause 1 fails).
26. **Run baseline tests**: must still show the same baseline number.
27. **Stop and report**. On approval: flip `exercise-02: approved YYYY-MM-DD`, flip `exercise-03: pending review`. Commit.

### Phase 3 — exercise-03 (`lookup/3` complete with both clauses, guard negation demo)

GATE: ex-02 status is `approved`. Halt if not.

28. **Re-read PDF p 34 (book p 22)** byte-exactly for `lookup/3` (both clauses) + surrounding §3.2 prose, plus PDF p 36 (book p 24) for the SRSW Rules for Defined Guards table referenced in trace annotations. Note any drift, especially for the second clause's head-list pattern (the contract's File 4 note flags this for explicit verification).
29. **Confirm R-009 decision with project owner**: stand-alone shape, no `merge/3` or `channel/1` / `process/2` duplication. Wait for explicit approval.
30. **Propose 3 inspection goals** to project owner (per `research.md` R-004: `lookup(a, [(a,1),(b,2),(c,3)], V).`, `lookup(c, [(a,1),(b,2),(c,3)], V).`, `lookup(z, [(a,1),(b,2),(c,3)], V).`). Wait for explicit approval. Note that the third goal may produce `→ fails` OR `→ suspended` depending on runtime behaviour; trace annotation MUST document whichever outcome the runtime produces.
31. **Write `ch-03-ex-03-guard-negation.glp`** per `contracts/glp-file-format.md` File 4 spec — lookup/3 byte-exact from PDF p 34 (both clauses with positive `=?=` and negated `~(=?=)`) + header + 2 `%%` comments.
32. **Capture the trace**:
    ```bash
    printf "olamni/tutorial/ch03/exercise-03/ch-03-ex-03-guard-negation.glp\nlookup(b, [(a,1),(b,2),(c,3)], V).\nlookup(a, [(a,1),(b,2),(c,3)], V).\nlookup(c, [(a,1),(b,2),(c,3)], V).\nlookup(z, [(a,1),(b,2),(c,3)], V).\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex03-trace.txt 2>&1
    ```
33. **Verify locked bindings**: `V = 2` for primary; `V = 1` for inspection 1; `V = 3` for inspection 2; `→ fails` or `→ suspended` for inspection 3 (whichever the runtime produces — both valid). If primary or inspections 1 / 2 mismatch, halt-and-report per FR-013.
34. **Verify both `lookup/3` clauses fired** in the four-goal session (clause 1 in inspection 1; clause 2 followed by clause 1 in primary + inspection 2; clause 2 only in inspection 3). If either was not exercised, halt-and-report.
35. **Write `ex-03-repl-trace.md`** per `contracts/trace-file-format.md` (five phases for ex-03). Strict byte-equality contract per FR-014 — no relaxation. Phase E annotation MUST document whichever no-match outcome the runtime produced and reference the §3.2 SRSW Rules table on book p 24.
36. **Write `ex-03-tutorial.md`** as the learner-facing step-through (load file, run primary + 3 inspection goals, observe positive vs negated branch firing, no-match termination). Tutorial MUST explain that `=?=` is negatable (per the §3.2 SRSW Rules table) but defined guards (e.g., ex-02's `channel/1`) are NOT — the negation form `~(...)` is restricted to negatable built-in guards.
37. **Run baseline tests**: must still show the same baseline number.
38. **Stop and report**. On approval: flip `exercise-03: approved YYYY-MM-DD`, flip `tutorial.md` ch03 row from `pending review (…)` to `implemented YYYY-MM-DD`. Commit.

---

## On failure (any phase)

Per Constitution Principle II (No Workarounds), every failure mode below requires HALT-and-REPORT. Do NOT silently fix, do NOT add try/catch-and-ignore, do NOT mark expected-to-fail.

| Failure | Action |
|---|---|
| Dart absent or below 3.9.4 | Halt at pre-flight step 3. Report to project owner with `dart --version` output. |
| REPL build fails | Halt at pre-flight step 4. Capture full build output. Report. |
| Baseline tests fail | Halt at pre-flight step 5. Report which sections failed. Do NOT proceed with ch03 work. |
| Procedure-redeclaration conflict between Program 3.1's `merge/3` and any ch4 procedure | Halt at Phase 1 step 8. Inspect the conflict; report which procedure conflicts with which. (Note: locked Q1 selection should NOT cause this — producer/2 and consumer/3 don't define merge/3.) |
| GLP file rejected at load | Halt at the relevant phase. The byte-exact PDF transcription is presumed correct; if the runtime rejects it, either the PDF transcription has drift OR the runtime has changed. Re-read PDF, then re-run; if still rejected, report as a runtime bug. |
| Primary-goal locked binding does not match | Halt. Either the prediction is wrong OR the runtime is misbehaving. Report which. Do NOT silently update the spec — propose a new Clarifications amendment per FR-013 if the spec needs changing (ch02 Q3a precedent). |
| `=?=` operator not recognised at parse time | Halt at Phase 3. Report as a parser limitation per the spec edge case. Do NOT work around — `~(=?=)` is the locked Q3 negation form. |
| `~(...)` negation form parser-rejected | Halt at Phase 3. Report as a parser limitation per the spec edge case. Do NOT work around. |
| `lookup/3` second clause's head pattern (cons-with-tail vs. two-element-list) is ambiguous in the PDF | Halt at Phase 3 step 28. Re-read carefully. If still ambiguous, ask project owner to inspect the PDF directly and lock the form via a Clarifications addendum. |
| Local `handle/1` stub interacts unexpectedly with `process/2`'s body | Halt at Phase 2 step 22. The stub is supposed to succeed for any single argument; if the runtime treats it differently, investigate before proceeding. R-008 alternative is body-substitution; switch to that if necessary via Clarifications amendment. |
| Any post-implementation test failure (baseline number drops) | Halt. Identify which test regressed and why. The chapter-3 work touches only `olamni/tutorial/ch03/**` — a regression elsewhere indicates an unrelated bug or accidental scope creep. Investigate before proceeding. |

---

## Definition of Done (chapter-3)

All of the following MUST hold:

- All twelve files written (4 `.glp` + 6 markdown new + 1 signpost + 1 input prompt already exists).
- Top-level `tutorial.md` updated; ch03 row reads `implemented YYYY-MM-DD`.
- Status block in `ch03_tutorial.md` reads `exercise-NN: approved YYYY-MM-DD` for all three N.
- All three traces (ex-01 through ex-03) are byte-equal modulo REPL banner / build wallclock lines to a fresh REPL re-run by an auditor.
- All four `.glp` files load successfully on a clean re-run; primary goals produce the locked bindings (`Sum = 21` for ex-01; `Status = ok` for ex-02; `V = 2` for ex-03).
- All three Program 3.1 clauses are exercised in ex-01's four-goal session; both `process/2` clauses are exercised in ex-02's four-goal session; both `lookup/3` clauses are exercised in ex-03's four-goal session.
- Baseline test suite still passes (494 or 485 depending on which build-provenance fixes are merged).
- The 9 spec edge cases have all been considered; none triggered an undocumented behaviour.
- Branch `004-tutorial-ch03` is committed and pushed.
- Project owner has explicitly approved ALL THREE exercises (3 separate approval events; the gates were respected).

---

## Constitution alignment summary

- **I. Spec-First**: every step traces to spec FR-NNN, SC-NNN, or Clarifications Q-N (Q1+Q2+Q3 plus any post-implement amendments). No code or doc written outside the spec.
- **II. No Workarounds**: every failure is a halt; no try/catch-and-ignore.
- **III. SRSW Discipline**: SRSW respected in all four GLP files. The cross-chapter producer/consumer import preserves byte-exactness including the `:=` body kernel inside the imported clauses (per FR-015 amendment).
- **IV. FCP Reference**: N/A.
- **V. Test-First**: baseline before, baseline after, traces ARE the regression artifacts.
- **VI. Tutorial Charter Compliance**: charter §1, §1.5, design-principles 1–2 cited; cross-chapter import documented as the explicit, narrow exception per `research.md` R-007.
- **Language Design Authority**: no new kernels. The `=?=` operator and the `~(...)` negation form are pre-existing GLP language features per book §3.2; the `:=` body kernel inside the inherited ch4 import is pre-existing (introduced for ch2 territory).
- **Technology Stack**: Dart 3.9.4+, GLP, Markdown — all within stack.
