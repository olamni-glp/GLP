# Implementation Plan: Olamni Tutorial — Chapter 1 (Fair Stream Merger)

**Branch**: `002-tutorial-ch01` | **Date**: 2026-04-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-tutorial-ch01/spec.md` (with 3 resolved Clarifications, 2026-04-28).

## Summary

Build the chapter-1 tutorial under `olamni/tutorial/ch01/`: one runnable exercise that loads Program 1.1 (Fair Stream Merger) verbatim from `GLP_ART.pdf` p 5 in the GLP REPL, plus a learner-targeted step-through guide and a verbatim captured REPL trace. Add a chapter signpost (`ch01_tutorial.md`) with a date-stamped status block enforcing the approval gate, plus a top-level signpost (`tutorial.md`) listing chapter 1 only (incremental). Two further variants of the same Program (different variable names) are scoped but gated behind explicit approval of exercise-01.

Technical approach: pure documentation + GLP-source feature. No runtime / type-system / language changes. Implementation step uses the existing `glp_runtime/bin/glp_repl.dart` compiled to a host executable to capture the verbatim REPL trace; the predicted binding `Xs = [1, a, 2, b, 3]` is empirically verified during the trace step (Clarification Q1 — mismatch is halt-and-report).

## Technical Context

**Language/Version**: Dart `^3.9.4` (REPL build only — `dart compile exe glp_runtime/bin/glp_repl.dart`); GLP (`.glp` source — Program 1.1 verbatim from PDF p 5); Markdown (all written documentation); Bash + PowerShell parity for any wrapper scripts.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency (provides the REPL). NO new third-party Dart packages, NO Python tooling, NO Flutter dependency.
**Storage**: On-disk Markdown files + one `.glp` source file. No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` MUST be recorded before implementation begins. Feature-specific verification = the empirical REPL run that produces `ex-01-repl-trace.md`. No new Dart unit tests. No Flutter build (chapter 1 is REPL-only per `olamni/tutorial/charter.md` §1).
**Target Platform**: Windows host for development (this repo); learner-facing artifacts MUST be platform-agnostic (Markdown + `.glp` work on macOS / Linux / Windows with any Dart 3.9.4+ host).
**Project Type**: **Tutorial chapter (under charter)** — Constitution Option C.
**Performance Goals**: Learner completes exercise-01 in <5 min given a working REPL (per spec SC-001). REPL build (`dart compile exe`) <30 s on typical hardware. Primary demo goal completes in <1 s.
**Constraints**:
- Predicted binding `Xs = [1, a, 2, b, 3]` MUST be empirically verified during implementation; mismatch is a halt-and-report bug, not a silent fix (per spec Clarification Q1).
- `ex-01-repl-trace.md` MUST be byte-verbatim inside its fenced code blocks; brief preface + per-phase annotations + brief postscript MUST be CLEARLY OUTSIDE the code blocks (per spec Clarification Q3 / FR-003).
- Approval-gate enforcement is a status block in `ch01_tutorial.md` greppable by downstream sessions (per spec Clarification Q2 / FR-007).
- Plan-then-act discipline: every implementation step (build REPL, write `.glp`, run trace, write tutorial, write signpost) MUST be presented as a numbered step and approved before action (per spec FR-011).
- No fabrication: Claude MUST NOT impersonate `/speckit-specify` output (per spec FR-010).
**Scale/Scope**: Single chapter (ch01) this round. One exercise (`exercise-01/`); `exercise-02/` and `exercise-03/` are scoped in spec but gated. ~6 files written (.glp + 4 markdown new + 1 markdown extended).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec at `specs/002-tutorial-ch01/spec.md` produced via proper-channel `/speckit-specify`; Clarifications integrated via proper-channel `/speckit-clarify`; this plan cites both.
- **II. No Workarounds**: **PASS**. No try/catch-and-ignore in scope. The "halt-and-report" rule for any binding mismatch (Clarification Q1) is the canonical anti-workaround posture. Any REPL-build failure halts implementation (per Edge Cases in spec).
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. Program 1.1 is the canonical SRSW example in the book; no `skipSRSW`; no ad-hoc relaxations introduced.
- **IV. FCP Reference Architecture**: **N/A**. No runtime / heap / dispatch / suspension changes; documentation + GLP-source feature only.
- **V. Test-First Discipline**: **PASS** with caveats. Baseline = `bash test/run_all_tests.sh` recorded before implementation begins. Feature-specific test = the captured REPL trace (which IS the regression artifact). No new Dart unit tests required (the .glp loads under the existing GLP REPL pipeline, which itself runs SRSW + types + compile). No Flutter UI affected (chapter 1 = REPL-only per charter).
- **VI. Tutorial Charter Compliance**: **PASS**. Plan cites `olamni/tutorial/charter.md`. Note: per the v0.1.0 release-notes anchor and the spec Assumptions, no `ch01_plan.md` exists under the new workflow (the previous fabricated `ch01_plan.md` was deleted in commit `592d89e3` and quarantined work cleaned in `146f430c`); the charter principles still apply (section-driven for chs 1–6; `%%` paraphrase comments per §1.5; REPL-only per §1).
- **Language Design Authority**: **N/A**. No new guard / system predicate / body kernel / directive / type-system feature.
- **Technology Stack**: **PASS**. All deps within Constitution-authorised stack (GLP source; Dart ^3.9.4 for REPL build; Markdown; Bash + PowerShell parity for any helper scripts).

**Result**: All applicable principles PASS or N/A. No Complexity Tracking entries required. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 research and Phase 1 design (research.md + data-model.md + contracts/ + quickstart.md), the Constitution Check is **re-validated**:

- **I. Spec-First**: still PASS. No design decision contradicts the spec; all 4 deferred items resolved in research.md with rationale tracing back to FRs.
- **II. No Workarounds**: still PASS. quickstart.md "On failure" section reinforces the halt-and-report posture for every plausible failure mode (Dart absent, REPL build fails, binding mismatch, SRSW/type errors).
- **III. SRSW Discipline**: still PASS. `glp-file-format.md` contract explicitly forbids `skipSRSW` and any anti-spec language flag.
- **IV. FCP Reference Architecture**: still N/A. No runtime touch.
- **V. Test-First**: still PASS with caveats. Captured trace IS the regression artifact for this feature.
- **VI. Tutorial Charter Compliance**: still PASS. R-001 references charter §1.5; R-006 references charter scope (formal-track out of scope per charter).
- **Language Design Authority**: still N/A.
- **Technology Stack**: still PASS. R-002 confirms no new third-party deps.

**Post-design verdict**: no new violations introduced by Phase 1 design. Plan complete.

## Project Structure

### Documentation (this feature)

```text
specs/002-tutorial-ch01/
├── spec.md                            # /speckit-specify + /speckit-clarify output (existing)
├── plan.md                            # this file (/speckit-plan output)
├── research.md                        # Phase 0 output (this command)
├── data-model.md                      # Phase 1 output (this command)
├── quickstart.md                      # Phase 1 output (this command)
├── contracts/                         # Phase 1 output (this command)
│   ├── trace-file-format.md           # ex-NN-repl-trace.md structural contract
│   ├── status-block-format.md         # ch01_tutorial.md approval-gate format
│   └── glp-file-format.md             # ch-XX-ex-NN-*.glp content contract
├── checklists/
│   └── requirements.md                # /speckit-clarify output (existing)
├── QUARANTINE-DO-NOT-USE/             # existing — quarantined fabricated content
│   └── quarantine_002_ch01_spec.md
└── tasks.md                           # Phase 2 (/speckit-tasks — NOT created by this command)
```

### Source Code (repository root)

**Constitution Option C: Tutorial chapter under charter.**

```text
olamni/tutorial/charter.md             # cited per Principle VI (existing, untouched)
olamni/tutorial/tutorial.md            # incremental top-level signpost (NEW or EXTEND; per spec FR-005)
olamni/tutorial/ch01/
├── ch01-sources.md                    # PDF code-block index (existing, committed in 592d89e3)
├── ch01-specification-input-prompt.md # rev-eng output, no speckit ceremony (NEW; per spec FR-006)
├── ch01_tutorial.md                   # chapter signpost with status block (NEW; per spec FR-004)
├── spec-rev-eng-input/
│   └── ch01-DEPRECATED-spec.md        # rev-eng input copy (existing, committed in 146f430c)
└── exercise-01/
    ├── ch-01-ex-01-fair-stream-merger.glp   # Program 1.1 verbatim + %% comments (NEW; per spec FR-001)
    ├── ex-01-tutorial.md                    # learner-targeted step-through guide (NEW; per spec FR-002)
    └── ex-01-repl-trace.md                  # verbatim captured REPL session (NEW; per spec FR-003)

# REPL build artifact (transient, not committed)
glp_repl.exe                            # built from glp_runtime/bin/glp_repl.dart via `dart compile exe`
                                       # location and gitignore strategy: see research.md R-002
```

**Structure Decision**: Constitution Option C — Tutorial chapter under charter. Cites Constitution Principle VI (Tutorial Charter Compliance), `olamni/tutorial/charter.md` §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments), and §design-principles 1–2 (section-driven; reader on §X.Y loads matching file). No multi-actor / Flutter scope (chapter 1 is REPL-only per charter §1).

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
