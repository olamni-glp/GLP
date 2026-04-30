# Implementer Quickstart — Olamni Tutorial Chapter 4

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-30

This is the implementer's quickstart for `/speckit-implement`. Chapter 4 is large (10 exercises, ~38 Programs, ~133 `%%` comments); the implementer plans time accordingly.

---

## Pre-flight (do BEFORE creating any files)

1. **Pull `main`**: confirm at v2026.04.30 or later (post-ch03 ship).
2. **Verify branch**: `git branch --show-current` should print `005-tutorial-ch04`.
3. **Verify Dart SDK**: `"/c/Users/gavri/dart-sdk/bin/dart" --version` — must be 3.9.4+.
4. **Build the REPL binary**: rebuild if stale. If `claude/fix-misleading-build-line` is merged, use `--define=GLP_BUILD_COMMIT=...`; otherwise build without (banner shows `Built from: unknown` — clear signal but not blocking).
5. **Record baseline test results**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — must show `Total: 485 | Passed: 485 | Failed: 0` per ch03 ship state. Record actual baseline in research.md for use by post-implementation tasks.
6. **Verify spec inputs are in place**:
   - `specs/005-tutorial-ch04/spec.md` exists with 3 Clarifications (Q1+Q2+Q3).
   - `olamni/tutorial/ch04/ch04-specification-input-prompt.md` exists.
   - `olamni/tutorial/ch04/ch04-sources.md` exists.
   - `olamni/tutorial/ch04/spec-rev-eng-input/ch04-DEPRECATED-spec.md` exists.

If any pre-flight step fails: halt, report to project owner, do not proceed.

---

## Implementation order (4 sub-section groups, sequential by group)

### Group 1: §4.1 (ex-01 + ex-02)

**Predecessor gate**: chapter signpost exists (created during this group's work).

1. **Re-read PDF book pp 25–30** (PDF pp 37–42) byte-exactly for §4.1 Programs + surrounding prose. Note any drift vs `ch04-sources.md`; correct sources file BEFORE proceeding.
2. **Create `olamni/tutorial/ch04/exercise-01/`** + write `ch-04-ex-01-constants-and-gates.glp` per `contracts/glp-file-format.md` File 1 spec. 17 unit clauses byte-exact from book pp 25–28.
3. **Verify ex-01 file loads** via REPL:
   ```bash
   printf "olamni/tutorial/ch04/exercise-01/ch-04-ex-01-constants-and-gates.glp\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
   ```
   Expect `✓ Loaded:`. If rejected, HALT.
4. **Propose 1 primary + 3 inspection goals to project owner** for ex-01. Wait for explicit approval (or auto-mode) before running.
5. **Run ex-01 4-goal session** + capture verbatim output. Verify locked bindings.
6. **Write `ex-01-repl-trace.md`** per `contracts/trace-file-format.md` (5 phases).
7. **Write `ex-01-tutorial.md`** — learner step-through.
8. **Write `ch04_tutorial.md`** signpost initially with status block per `contracts/status-block-format.md` initial state (ex-01 + ex-02 = `pending review`; ex-03..ex-10 = `pending exercise-N approval`).
9. **Update `olamni/tutorial/tutorial.md`** — flip ch04 row from `planned` to `pending review (YYYY-MM-DD)`.
10. **Repeat steps 2–7 for ex-02** (`ch-04-ex-02-compound-circuits.glp`; 17 clauses incl. duplicated gates from ex-01 per FR-010 self-containment).
11. **Run baseline tests post-§4.1 group**: `bash test/run_all_tests.sh` — expect 485/485 PASS.
12. **Stop and report to project owner**. Show §4.1 group diff. Wait for explicit `approved` signal (or auto-mode).
13. **On §4.1 group approval**: edit `ch04_tutorial.md` status block to flip BOTH `exercise-01: approved YYYY-MM-DD` + `exercise-02: approved YYYY-MM-DD` (group-atomic flip). Commit with message `implement(ch04): §4.1 group landed (constants + compound circuits)`.

### Group 2: §4.2 (ex-03 + ex-04 + ex-05 + ex-06)

**Predecessor gate**: §4.1 group fully approved (check via `grep -cE "^- exercise-(01|02): approved" ch04_tutorial.md` returns 2). Halt if not.

14. **Re-read PDF book pp 31–37** (PDF pp 43–49) byte-exactly for §4.2 Programs + surrounding prose + Formal 4.2 (p 31) + Formal 4.3 (pp 35–36).
15. **For ex-03** (cross-chapter inversion): write `ch-04-ex-03-producer-consumer-reverse.glp` per `contracts/glp-file-format.md` File 3 spec. CRITICAL: producer/2 + consumer/3 clauses MUST be byte-identical to ch03's `ch-03-ex-01-producer-consumer.glp`. Verify via `diff` modulo headers + `%%` (per FR-002 + SC-007).
16. **Verify ex-03 loads + run 4-goal session + write trace + tutorial.**
17. **Repeat for ex-04 (`merge-variants`), ex-05 (`stream-operators`), ex-06 (`buffered-and-monitors`).** Each may need elevated `:limit` for primary/inspection goals (see contracts/trace-file-format.md). ex-05's distribute_indexed works fine with structs-in-lists per Q2 retraction; no special handling.
18. **Run baseline tests post-§4.2 group**: 485/485 PASS expected.
19. **Stop and report.** Show §4.2 group diff (4 exercises landed). Wait for approval.
20. **On §4.2 group approval**: flip ex-03..ex-06 status block lines all to `approved YYYY-MM-DD` atomically. Commit.

### Group 3: §4.3 (ex-07 + ex-08)

**Predecessor gate**: §4.2 group fully approved.

21. **Re-read PDF book pp 37–41** (PDF pp 49–53) byte-exactly for §4.3 Programs + surrounding prose.
22. **Write ex-07** (`recursive-numerics.glp`) — 6 Programs (Peano + integer arith + factorial + fact_acc + fib + fib_linear). ~27 clauses.
23. **Verify ex-07 loads + 4-goal session + trace + tutorial.**
24. **Write ex-08** (`recursive-list-tree.glp`) — 6 Programs (flatten + tree_sum + insertion_sort + mergesort + distribute_ng + substitute). ~32 clauses. Note: distribute_ng's `=..` in body works fine per Q2 retraction.
25. **Verify ex-08 loads + 4-goal session + trace + tutorial.**
26. **Run baseline tests post-§4.3 group**: 485/485 PASS expected.
27. **Stop and report.** Wait for approval.
28. **On §4.3 group approval**: flip ex-07 + ex-08 status block lines atomically. Commit.

### Group 4: §4.4 (ex-09 + ex-10)

**Predecessor gate**: §4.3 group fully approved.

29. **Re-read PDF book pp 41–43** (PDF pp 53–55) byte-exactly for §4.4 Programs + surrounding prose.
30. **Write ex-09** (`metaprogramming-foundations.glp`) — 4.4.1 reduce/2 (3 unit clauses encoding the merge program) + 4.4.2 trust-mode run/2 (4 clauses).
31. **Verify ex-09 loads + 4-goal session + trace + tutorial.** Trust-mode MI primary goal: `run(merge, merge([1,2],[3,4],Z)).` may need elevated `:limit`.
32. **Write ex-10** (`advanced-meta-interpreters.glp`) — 4.4.3 fail-safe + 4.4.4 control + 4.4.5 tracing + replay. May need ex-09's reduce/2 duplicated inline per FR-010.
33. **Verify ex-10 loads + 4-goal session + trace + tutorial.** May need elevated `:limit` for control/tracing goals.
34. **Run baseline tests post-§4.4 group**: 485/485 PASS expected.
35. **Stop and report.** Wait for approval.
36. **On §4.4 group approval (chapter complete)**:
   - Flip ex-09 + ex-10 status block lines to `approved YYYY-MM-DD` atomically.
   - Edit `olamni/tutorial/tutorial.md` ch04 row from `pending review (…)` to `implemented YYYY-MM-DD`.
   - Commit with message `implement(ch04): chapter complete — §4.4 group + top-level index flip`.

---

## Polish & Cross-Cutting

37. **No-fabrication audit**: verify all files under `specs/005-tutorial-ch04/` are proper `/speckit-*` outputs. Per FR-012 + SC-011.
38. **Cross-chapter inversion identity check**: `diff` ex-03's producer/consumer clauses against ch03's import. Per FR-002 + SC-007.
39. **Cross-chapter scope check**: grep all 10 ch04 `.glp` files for procedure names from other chapters; should match only ch04 native + the cross-chapter inversion duplicates.
40. **Test harness exclusion check**: `grep "olamni/tutorial/ch04" test/run_all_tests.sh` MUST return zero matches. Per FR-016.
41. **Body-kernel scope check**: `:=` permitted only inside byte-exact PDF clauses that use it; `now/1` and `'_output'/1` MUST NOT appear anywhere in ch04. Per spec FR-015.
42. **Final baseline**: 485/485 PASS expected.
43. **Trace reproducibility check**: re-run all 10 traces; diff against committed `.md` files modulo banner.
44. **Walk-through verification (soft)**: log SC-001 90-min budget as known follow-up.
45. **Commit + push** branch `005-tutorial-ch04`. Per Constitution multi-Claude protocol — `git add` SPECIFIC files only.
46. **Provide merge instructions** to project owner per the workflow memory's mandatory format.

---

## On failure (any phase)

Per Constitution Principle II (No Workarounds), every failure mode below requires HALT-and-REPORT. Do NOT silently fix, do NOT add try/catch-and-ignore, do NOT mark expected-to-fail.

| Failure | Action |
|---|---|
| Dart absent or below 3.9.4 | Halt at pre-flight 3. Report. |
| REPL build fails | Halt at pre-flight 4. Capture full build output. Report. |
| Baseline tests fail | Halt at pre-flight 5. Report which sections failed. Do NOT proceed. |
| GLP file rejected at load | Halt at the relevant phase. Re-read PDF byte-exact; if still rejected, report as runtime bug. |
| Primary-goal locked binding does not match | Halt. Either prediction is wrong OR runtime is misbehaving. Report which. Do NOT silently update spec — propose Clarifications amendment per FR-013 if needed (ch02 Q3a / ch03 Q4 precedent). |
| `=..` in body OR structs-in-lists rejected (contradicting Q2 retraction) | Halt. Per Q2 these are stale-CLAUDE.md artefacts that work in the current build. If they suddenly fail, that's a runtime regression — report and investigate. |
| Procedure-redeclaration conflict during ex-NN load (e.g., ex-02 duplicating gates from ex-01) | Per FR-010 self-containment, each `.glp` is loaded standalone in a fresh REPL session. If you see redeclaration conflicts, you may have loaded multiple ch04 files in one session — load them separately. |
| Cross-chapter inversion identity check fails (`diff` between ch03 and ch04 producer/consumer shows clause-text differences) | Halt at step 15 verification. Either ch03's import drifted OR ch04's reclaim is wrong. Re-read PDF byte-exact + fix the divergent file. Per SC-007. |
| Goal exceeds REPL execution limit (`:limit`) | Bump limit via REPL `:limit` directive before the goal. Document in trace if the limit was bumped. |
| Any post-implementation test failure (485 → less than 485) | Halt. ch04 work is entirely under `olamni/tutorial/ch04/**` per FR-016; harness regression indicates unrelated bug or scope creep. Investigate before proceeding. |

---

## Definition of Done (chapter-4)

All of the following MUST hold:

- All ~50 files written (10 `.glp` + 20 markdown new + 1 signpost + 1 input prompt already existed).
- Top-level `tutorial.md` updated; ch04 row reads `implemented YYYY-MM-DD`.
- Status block in `ch04_tutorial.md` reads `exercise-NN: approved YYYY-MM-DD` for all 10 NN.
- All 10 traces are byte-equal modulo REPL banner / build wallclock lines to a fresh REPL re-run by an auditor.
- All 10 `.glp` files load successfully on a clean re-run; primary goals produce the locked bindings.
- Cross-chapter inversion identity verified: ex-03's producer/consumer clauses byte-identical to ch03's import.
- Baseline test suite still passes (485/485 if `claude/fix-misleading-build-line` unmerged; 494/494 if merged).
- Branch `005-tutorial-ch04` is committed and pushed.
- Project owner has explicitly approved ALL FOUR groups (4 separate group-approval events; group-boundary gates respected).

---

## Constitution alignment summary

- **I. Spec-First**: every step traces to spec FR-NNN, SC-NNN, or Clarifications Q-N (Q1+Q2+Q3). No code or doc written outside the spec.
- **II. No Workarounds**: every failure is a halt; no try/catch-and-ignore. Q2 retraction is the canonical anti-workaround posture.
- **III. SRSW Discipline**: all ~38 Programs are SRSW-compliant by byte-exact construction.
- **IV. FCP Reference**: N/A.
- **V. Test-First**: baseline before, baseline at each group boundary, baseline after; traces ARE regression artifacts.
- **VI. Tutorial Charter Compliance**: charter §1, §1.5, design-principles 1–2 cited; cross-chapter inversion documented; no other cross-chapter imports.
- **Language Design Authority**: no new kernels / guards / system predicates / directives.
- **Technology Stack**: Dart 3.9.4+, GLP, Markdown — all within stack.
