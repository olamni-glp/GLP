# Implementer Quickstart — Olamni Tutorial Chapter 2

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-28

This is the implementer's quickstart for `/speckit-implement`. The LEARNER-facing quickstarts will live in each `olamni/tutorial/ch02/exercise-NN/ex-NN-tutorial.md` file once written. This file describes how the implementing Claude session executes the chapter-2 work end-to-end.

---

## Pre-flight (do BEFORE creating any files)

1. **Pull `main`**: `git fetch origin && git pull origin main`. Confirm at v2026.04.28-2 or later.
2. **Verify branch**: `git branch --show-current` should print `003-tutorial-ch02`.
3. **Verify Dart SDK**: `"/c/Users/gavri/dart-sdk/bin/dart" --version` — must be 3.9.4+. If absent or older, halt and report (per Edge Cases in spec).
4. **Verify REPL binary**: check `glp_runtime/glp_repl.exe` exists. If not, build it: `"/c/Users/gavri/dart-sdk/bin/dart" compile exe glp_runtime/bin/glp_repl.dart -o glp_runtime/glp_repl.exe`.
5. **Record baseline test results**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — must show `Total: 476 | Passed: 476 | Failed: 0`. Record this before ANY file work.
6. **Verify spec inputs are in place**:
   - `specs/003-tutorial-ch02/spec.md` exists with 5 Clarifications resolved.
   - `olamni/tutorial/ch02/ch02-specification-input-prompt.md` exists.
   - `olamni/tutorial/ch02/ch02-sources.md` exists.
   - `olamni/tutorial/ch02/spec-rev-eng-input/ch02-DEPRECATED-spec.md` exists.

If any pre-flight step fails: halt, report to project owner, do not proceed.

---

## Implementation order (ex-01 → ex-02 → ex-03)

### Phase 1 — exercise-01 (LP/GLP append contrast)

1. **Re-read PDF p 10** byte-exactly for Example 2.1 + surrounding §2.1 / §2.2 prose. Note any drift vs `ch02-sources.md`. If drift found, correct `ch02-sources.md` BEFORE proceeding (per ch01's predict-and-verify lesson).
2. **Re-read PDF pp 31–32** byte-exactly for the GLP `append/3` + surrounding §4.2 prose.
3. **Propose 3 inspection goals** to project owner (per `research.md` R-004 — already locked in this plan: `append([], [a,b,c], Zs)`, `append([1,2,3], [], Zs)`, `append([], [], Zs)`). Wait for explicit approval.
4. **Write `ch-02-ex-01-classical-append-LP-only.glp`** per `contracts/glp-file-format.md` File 1 spec.
5. **Write `ch-02-ex-01-glp-append.glp`** per `contracts/glp-file-format.md` File 2 spec.
6. **Capture the trace**: run the LP-only file's load attempt + the GLP file's load + the four goals through the REPL. Use the kernel-snapshot batch pattern from the workflow memory:
   ```bash
   DART="/c/Users/gavri/dart-sdk/bin/dart"
   printf "olamni/tutorial/ch02/exercise-01/ch-02-ex-01-classical-append-LP-only.glp\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex01-rejection.txt 2>&1
   printf "olamni/tutorial/ch02/exercise-01/ch-02-ex-01-glp-append.glp\nappend([1,2,3], [a,b,c], Zs).\nappend([], [a,b,c], Zs).\nappend([1,2,3], [], Zs).\nappend([], [], Zs).\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex01-success.txt 2>&1
   ```
7. **Verify the locked binding**: confirm `Zs = [1, 2, 3, a, b, c]` appears in `/tmp/ex01-success.txt`. If not, halt-and-report.
8. **Verify the SRSW rejection**: confirm an error (not `✓ Loaded`) appears in `/tmp/ex01-rejection.txt`. If the LP-only file silently loaded, halt-and-report.
9. **Write `ex-01-repl-trace.md`** per `contracts/trace-file-format.md` (six phases for ex-01). Code-block content is byte-verbatim from `/tmp/ex01-rejection.txt` and `/tmp/ex01-success.txt`. Annotations OUTSIDE the blocks per the contract.
10. **Write `ex-01-tutorial.md`** as the learner-facing step-through (build REPL, attempt LP-only load, observe rejection, load GLP file, run primary + 3 inspection goals, cross-check trace).
11. **Write `ch02_tutorial.md`** signpost with the cross-chapter import note (per `research.md` R-007) and the status block reading `exercise-01: pending review`, `exercise-02: pending exercise-01 approval`, `exercise-03: pending exercise-02 approval`.
12. **Update `olamni/tutorial/tutorial.md`** — flip ch02 row from `planned` to `pending review (2026-04-28)`.
13. **Run baseline tests again**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — must still show `476/476 Passed`.
14. **Stop and report to project owner**. Provide the trace + tutorial diff for review. Wait for explicit `approved` signal.
15. **On approval**: edit `ch02_tutorial.md` status block to flip `exercise-01: approved 2026-04-28` and `exercise-02: pending review`. Commit. Do NOT begin ex-02 until this step is committed and the project owner has confirmed.

### Phase 2 — exercise-02 (`append_and_sum/4`)

GATE: ex-01 status is `approved`. Halt if not.

16. **Write `ch-02-ex-02-append-and-sum.glp`** per `contracts/glp-file-format.md` File 3 spec — duplicate the GLP `append/3` byte-exact from ex-01, define `sum/2` per `research.md` R-008, define `append_and_sum/4` per R-008.
17. **Capture the trace**: run the load + primary + 3 inspection goals (per `research.md` R-004 ex-02 set):
    ```bash
    printf "olamni/tutorial/ch02/exercise-02/ch-02-ex-02-append-and-sum.glp\nappend_and_sum([1,2,3], [4,5,6], Zs, Sum).\nappend_and_sum([], [4,5,6], Zs, Sum).\nappend_and_sum([1,2,3], [], Zs, Sum).\nappend_and_sum([], [], Zs, Sum).\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex02-trace.txt 2>&1
    ```
18. **Verify locked bindings**: `Zs = [1, 2, 3, 4, 5, 6]`, `Sum = 21` for the primary; `Zs = [4, 5, 6]`, `Sum = 15` for inspection 1; etc. If any mismatch, halt-and-report.
19. **Write `ex-02-repl-trace.md`** per `contracts/trace-file-format.md` (five phases for ex-02). Strict byte-equality contract per FR-014 — no relaxation.
20. **Write `ex-02-tutorial.md`** as the learner-facing step-through (load file, run primary + 3 inspection goals, observe how `Sum` is bound by `sum/2` while `Zs` is being built by `append/3` — the SRSW concurrency idea made concrete).
21. **Run baseline tests**: must still show `476/476`.
22. **Stop and report**. On approval: flip `exercise-02: approved YYYY-MM-DD`, flip `exercise-03: pending review`. Commit.

### Phase 3 — exercise-03 (`timed_append/3`)

GATE: ex-02 status is `approved`. Halt if not.

23. **Write `ch-02-ex-03-timed-append.glp`** per `contracts/glp-file-format.md` File 4 spec — duplicate GLP `append/3` byte-exact, define `timed_append/3` per `research.md` R-009.
24. **Capture the trace**: run the load + primary + 3 inspection goals (per `research.md` R-004 ex-03 set):
    ```bash
    printf "olamni/tutorial/ch02/exercise-03/ch-02-ex-03-timed-append.glp\ntimed_append([1,2,3], [a,b,c], Zs).\ntimed_append([], [], Zs).\ntimed_append([1,2,3,4,5,6,7,8,9,10], [a,b,c,d,e,f,g,h,i,j], Zs).\ntimed_append([1], [a], Zs).\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex03-trace.txt 2>&1
    ```
25. **Verify locked bindings + output shape**: `Zs = [1, 2, 3, a, b, c]` for the primary; `elapsed_ms(N)` line emitted. The `N` value varies per run (per FR-014); only the SHAPE is locked. If `Zs` differs from locked or the `elapsed_ms` line is missing, halt-and-report.
26. **Write `ex-03-repl-trace.md`** per `contracts/trace-file-format.md` (five phases for ex-03). Apply the FR-014 relaxation only to the integer N inside `elapsed_ms(N)`. Annotation MUST contain "varies per run; the SHAPE matters, not the specific number".
27. **Write `ex-03-tutorial.md`** as the learner-facing step-through (load file, run primary + 3 inspection goals, observe the `elapsed_ms(N)` line printed BEFORE the `Zs = …` binding because `_output` fires inside the body, plus the per-run variation in N).
28. **Run baseline tests**: must still show `476/476`.
29. **Stop and report**. On approval: flip `exercise-03: approved YYYY-MM-DD`, flip `tutorial.md` ch02 row from `pending review (…)` to `implemented YYYY-MM-DD`. Commit.

---

## On failure (any phase)

Per Constitution Principle II (No Workarounds), every failure mode below requires HALT-and-REPORT. Do NOT silently fix, do NOT add try/catch-and-ignore, do NOT mark expected-to-fail.

| Failure | Action |
|---|---|
| Dart absent or below 3.9.4 | Halt at pre-flight step 3. Report to project owner with `dart --version` output. |
| REPL build fails | Halt at pre-flight step 4. Capture full build output. Report. |
| Baseline tests fail | Halt at pre-flight step 5. Report which sections failed. Do NOT proceed with ch02 work. |
| LP-only file silently LOADS in the REPL (no SRSW rejection) | Halt at Phase 1 step 8. This is a runtime regression — the analyser is supposed to reject this exact pattern. Report as a runtime bug. |
| GLP file rejected at load | Halt at Phase 1 step 9 (or analogous step in Phase 2 / 3). The byte-exact PDF transcription is presumed correct; if the runtime rejects it, either the PDF transcription has drift OR the runtime has changed. Re-read PDF, then re-run; if still rejected, report as a runtime bug. |
| Primary-goal locked binding does not match | Halt. Either the prediction is wrong OR the runtime is misbehaving. Report which. Do NOT silently update the spec. |
| `now/1` returns a non-integer | Halt at Phase 3. The body kernel `_now` returns `DateTime.now().millisecondsSinceEpoch` which is always integer; non-integer means the kernel has changed. Report as a runtime regression. |
| `'_output'/1` callback raises | Halt at Phase 3. Report. |
| Any post-implementation test failure (476 → less than 476) | Halt. Identify which test regressed and why. The chapter-2 work touches only `olamni/tutorial/ch02/**` — a regression elsewhere indicates an unrelated bug or accidental scope creep. Investigate before proceeding. |

---

## Definition of Done (chapter-2)

All of the following MUST hold:

- All twelve files written (4 `.glp` + 6 markdown + 1 signpost + 1 input prompt already exists).
- Top-level `tutorial.md` updated; ch02 row reads `implemented YYYY-MM-DD`.
- Status block in `ch02_tutorial.md` reads `exercise-NN: approved YYYY-MM-DD` for all three N.
- All three traces (ex-01 through ex-03) are byte-equal modulo per-exercise relaxations to a fresh REPL re-run by an auditor.
- The classical LP append file is REJECTED by the REPL on a clean re-run.
- Baseline test suite still passes (476/476).
- The 8 spec edge cases have all been considered; none triggered an undocumented behaviour.
- Branch `003-tutorial-ch02` is committed and pushed.
- Project owner has explicitly approved ALL THREE exercises (3 separate approval events; the gates were respected).

---

## Constitution alignment summary

- **I. Spec-First**: every step traces to spec FR-NNN, SC-NNN, or Clarifications Q-N. No code or doc written outside the spec.
- **II. No Workarounds**: every failure is a halt; no try/catch-and-ignore.
- **III. SRSW Discipline**: SRSW respected in 3 GLP files; INTENTIONALLY violated in 1 LP-only file (the violation IS the demonstration).
- **IV. FCP Reference**: N/A.
- **V. Test-First**: baseline before, baseline after, traces ARE the regression artifacts.
- **VI. Tutorial Charter Compliance**: charter §1, §1.5, design-principles 1–2 cited; cross-chapter import documented as the explicit, narrow exception per `research.md` R-007.
- **Language Design Authority**: no new kernels.
- **Technology Stack**: Dart 3.9.4+, GLP, Markdown — all within stack.
