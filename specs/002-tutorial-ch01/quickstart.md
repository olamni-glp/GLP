# Quickstart — Olamni Tutorial Chapter 1 (Fair Stream Merger)

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-28

This is the implementer's quickstart for delivering exercise-01 of chapter 1. It compresses the full plan into an actionable checklist for the Claude session running `/speckit-implement` (or any human implementer).

The learner-facing quickstart lives later, in `olamni/tutorial/ch01/exercise-01/ex-01-tutorial.md` (which this spec drives the production of).

## Prerequisites

- [ ] Branch is `002-tutorial-ch01`.
- [ ] HEAD is at the merge commit on main OR a descendant on this feature branch.
- [ ] Working tree is clean for the files this implementation will touch (do NOT commit other in-progress work alongside).
- [ ] `dart --version` runs and reports `^3.9.4`.
- [ ] `glp_runtime/bin/glp_repl.dart` exists in the working tree.
- [ ] PDF `GLP_ART.pdf` is at the repo root and readable.

## Step-by-step (high level — see `tasks.md` for the full enumeration produced by `/speckit-tasks`)

1. **Verify Dart SDK**: `dart --version`. If missing or below `^3.9.4`, halt and report to project owner.
2. **Build REPL**: `dart compile exe glp_runtime/bin/glp_repl.dart -o glp_runtime/glp_repl.exe`. (Add `glp_runtime/glp_repl*` to `.gitignore` if not already there — see research.md R-002.)
3. **Re-read PDF p 5–6** for byte-exact Program 1.1 + paraphrase prose source (per research.md R-006).
4. **Propose 3 inspection goals** to the project owner for approval (per research.md R-004 — asymmetric, empty, base-case). Wait for explicit approval before running them.
5. **Write `olamni/tutorial/ch01/exercise-01/ch-01-ex-01-fair-stream-merger.glp`** following the contract at `contracts/glp-file-format.md`. Use original variable names (`X, Xs, Y, Ys, Zs`).
6. **Run the REPL session** — load the .glp, run primary goal, run the 3 approved inspection goals. Capture verbatim into a temp buffer.
7. **Verify the predicted binding** `Xs = [1, a, 2, b, 3]` matches the actual REPL output for the primary goal (per spec Clarification Q1). On mismatch: halt, report, do NOT silently overwrite the spec.
8. **Write `ex-01-repl-trace.md`** following the contract at `contracts/trace-file-format.md`: 1–3 sentence preface, 5 fenced code blocks (build/load + 4 goal phases), brief per-phase annotations, 1–3 sentence postscript.
9. **Write `ex-01-tutorial.md`** — the learner-targeted step-through guide that walks through the same 5 phases but with more pedagogical scaffolding. References `ex-01-repl-trace.md` for the verbatim trace.
10. **Write `olamni/tutorial/ch01/ch01_tutorial.md`** — chapter signpost with the **Exercise status** block per `contracts/status-block-format.md`. Initial state:
    ```
    - exercise-01: pending exercise-01 approval
    - exercise-02: pending exercise-01 approval
    - exercise-03: not yet implemented
    ```
11. **Write `olamni/tutorial/ch01/ch01-specification-input-prompt.md`** — rev-eng output, plain prose, NO speckit ceremony (per spec FR-006). Source: strip ceremony from `spec-rev-eng-input/ch01-DEPRECATED-spec.md`.
12. **Write/extend `olamni/tutorial/tutorial.md`** — top-level signpost per research.md R-003. Chapter 1 row marked `pending review`; chapters 2–13 rows marked `planned`.
13. **Show diffs to project owner**. Do NOT commit. Wait for approval.
14. **On approval**: flip status block to `exercise-01: approved YYYY-MM-DD`, commit, push, merge to main, bump CalVer release.

## What this quickstart is NOT

- **Not a learner quickstart.** That's `ex-01-tutorial.md`, written later.
- **Not a substitute for `/speckit-tasks`.** The full task enumeration (with dependencies, checkboxes, atomic commits) comes from running `/speckit-tasks` next.
- **Not authorisation to act.** Each step requires the plan-then-act discipline (FR-011): present the step, get approval, then act.

## On failure

Per Constitution Principle II (No Workarounds):
- Dart absent / wrong version → halt, report, ask Udi how to proceed.
- REPL build fails → halt, report build error verbatim, ask Udi.
- Predicted binding mismatch (step 7) → halt, report both predicted and actual, ask Udi which to trust.
- SRSW / type / compile error on `.glp` load → halt, report exact REPL error, do NOT add `skipSRSW` or any other bypass.
