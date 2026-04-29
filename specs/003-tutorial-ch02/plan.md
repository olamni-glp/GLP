# Implementation Plan: Olamni Tutorial — Chapter 2 (LP/GLP Append Contrast + Body Kernels)

**Branch**: `003-tutorial-ch02` | **Date**: 2026-04-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/003-tutorial-ch02/spec.md` (with 5 resolved Clarifications, 2026-04-28).

## Summary

Build the chapter-2 tutorial under `olamni/tutorial/ch02/`: three runnable exercises that progressively introduce the runtime's body kernels.

- **ex-01** demonstrates the LP→GLP transition by pairing classical LP `append/3` (PDF p 10, Example 2.1 — INTENTIONALLY rejected by the SRSW analyser) with GLP `append/3` (cross-chapter import from PDF pp 31–32, ch 4 §4.2 — accepted and runnable). Two `.glp` files per dir; primary demo goal `append([1,2,3], [a,b,c], Zs).` with locked binding `Zs = [1, 2, 3, a, b, c]`.
- **ex-02** introduces GLP arithmetic via `:=` by adding `append_and_sum/4` (locked shape per Clarifications) which appends two number lists AND concurrently sums the result. Helper `sum/2`. Primary goal `append_and_sum([1,2,3], [4,5,6], Zs, Sum).` → `Zs = [1,2,3,4,5,6]`, `Sum = 21`.
- **ex-03** introduces system time via `now/1` and ground-term I/O via `'_output'/1` by adding `timed_append/3` (locked shape per Clarifications) which captures start, runs append, captures end, computes elapsed via `:=` subtraction, and emits `'_output'(elapsed_ms(N))`. Primary goal `timed_append([1,2,3], [a,b,c], Zs).` → `Zs = [1,2,3,a,b,c]` plus shape-locked output line.

Each later exercise duplicates `append/3` inline (per Clarifications Q2 — no cross-file dependencies; each exercise dir is self-contained). Approval gates between exercises (status block in `ch02_tutorial.md`); ex-02 cannot begin until ex-01 is approved AND thoroughly REPL-tested; ex-03 cannot begin until ex-02 likewise.

Technical approach: pure documentation + GLP-source feature. No runtime / type-system / language changes. Implementation uses the existing `glp_runtime/bin/glp_repl.dart` compiled to a host executable to capture verbatim REPL traces (the same artifact ch01 produced). Predicted bindings are empirically verified during the trace step; mismatch is halt-and-report (Constitution Principle II).

## Technical Context

**Language/Version**: Dart `^3.9.4` (REPL build only — `dart compile exe glp_runtime/bin/glp_repl.dart`); GLP (`.glp` source — Example 2.1 verbatim from PDF p 10 + GLP `append/3` verbatim from PDF pp 31–32 + locally-defined `sum/2` helper for ex-02 + locally-defined `timed_append/3` for ex-03); Markdown (all written documentation); Bash + PowerShell parity for any wrapper scripts.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency (provides the REPL). `programs/self.glp` (root prelude — provides `:=`, `now/1`, `'_output'/1`, comparison guards). NO new third-party Dart packages, NO Python tooling, NO Flutter dependency.
**Storage**: On-disk Markdown files + four `.glp` source files (one classical-LP, three GLP). No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` MUST be recorded before implementation begins. Feature-specific verification = the empirical REPL run that produces `ex-NN-repl-trace.md` for each of the three exercises. No new Dart unit tests. No Flutter build (chapter 2 is REPL-only per `olamni/tutorial/charter.md` §1). Per spec FR-016, ch02 exercise files are NOT added to `test/run_all_tests.sh`.
**Target Platform**: Windows host for development (this repo); learner-facing artifacts MUST be platform-agnostic (Markdown + `.glp` work on macOS / Linux / Windows with any Dart 3.9.4+ host).
**Project Type**: **Tutorial chapter (under charter)** — Constitution Option C.
**Performance Goals**: Learner completes exercise-01 in <10 min given a working REPL (per spec SC-001 — extended from ch01's <5 min because ex-01 has TWO files instead of one). REPL build (`dart compile exe`) <30 s on typical hardware. Each primary demo goal completes in <1 s.
**Constraints**:
- Predicted bindings (ex-01 `Zs = [1,2,3,a,b,c]`, ex-02 `Zs = [1,2,3,4,5,6]` + `Sum = 21`, ex-03 `Zs = [1,2,3,a,b,c]` + `elapsed_ms(N)` shape) MUST be empirically verified during implementation; mismatch is a halt-and-report bug, not a silent fix (per spec Clarification Q3 / FR-009 / FR-010).
- ex-01 trace MUST capture BOTH the SRSW rejection of the LP-only file AND the success path of the GLP file — the rejection is the demonstration, not a bug (per spec FR-004 / SC-002).
- ex-02 trace inherits the strict byte-equality contract of ex-01 (per Clarification Q1 / FR-014). Only ex-03 gets the elapsed-ms relaxation.
- Each later `.glp` MUST duplicate `append/3` inline (per Clarification Q2 / FR-009 / FR-010). NO cross-file dependencies between exercises.
- ex-02 and ex-03 MUST NOT import code from any chapter beyond ch 4 §4.2's `append/3` (per Clarification Q4 / FR-015).
- Approval-gate enforcement is a status block in `ch02_tutorial.md` greppable by downstream sessions (per spec FR-008).
- Plan-then-act discipline: every implementation step (build REPL, write each `.glp`, run trace, write tutorial, write signpost) MUST be presented as a numbered step and approved before action (per spec FR-013).
- No fabrication: Claude MUST NOT impersonate `/speckit-specify` output (per spec FR-012).
**Scale/Scope**: Single chapter (ch02) this round. Three exercises (`exercise-01/`, `exercise-02/`, `exercise-03/`). ~12 files written: 4 `.glp` (ex-01 has 2 files, ex-02 has 1, ex-03 has 1) + 6 Markdown new (3 tutorials + 3 traces) + 1 signpost + 1 input prompt (ALREADY WRITTEN at this turn) + 1 markdown extended (top-level `tutorial.md`).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec at `specs/003-tutorial-ch02/spec.md` produced via proper-channel `/speckit-specify`; 5 Clarifications integrated via proper-channel `/speckit-clarify`; this plan cites both. The plain-prose input prompt is `olamni/tutorial/ch02/ch02-specification-input-prompt.md`.
- **II. No Workarounds**: **PASS**. No try/catch-and-ignore in scope. The "halt-and-report" rule for any binding mismatch (Clarifications Q3 + FR-009 + FR-010) is the canonical anti-workaround posture. Any REPL-build failure halts implementation (per Edge Cases in spec). The intentional SRSW rejection of `ch-02-ex-01-classical-append-LP-only.glp` is NOT a workaround — it is the chapter's pedagogical demonstration (US1 + SC-002).
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. The classical LP append IS the contraction-violating example the SRSW analyser is supposed to reject; the chapter relies on the analyser doing its job. The GLP append (and `append_and_sum`, `timed_append`) are SRSW-compliant. No `skipSRSW`; no ad-hoc relaxations introduced.
- **IV. FCP Reference Architecture**: **N/A**. No runtime / heap / dispatch / suspension changes; documentation + GLP-source feature only.
- **V. Test-First Discipline**: **PASS** with caveats. Baseline = `bash test/run_all_tests.sh` recorded before implementation begins (expected: 476/476 passing per workflow memory). Feature-specific tests = the captured REPL traces (which ARE the regression artifacts for this feature). No new Dart unit tests required (the `.glp` files load under the existing GLP REPL pipeline). No Flutter UI affected (chapter 2 = REPL-only per charter).
- **VI. Tutorial Charter Compliance**: **PASS**. Plan cites `olamni/tutorial/charter.md` §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments — applies to BOTH the LP-only and the GLP files), and §design-principles 1–2 (section-driven for chs 1–6). The cross-chapter import from ch 4 §4.2 is documented in the input prompt, in the spec FR-002 + FR-009 + FR-010, and in the importing `.glp` files' header comments. Per the workflow memory, no `ch02_plan.md` is required (the previous fabricated `chXX_plan.md` files were deleted in commit `592d89e3`).
- **Language Design Authority**: **N/A**. No new guard / system predicate / body kernel / directive / type-system feature. The body kernels used (`:=`, `now/1`, `'_output'/1`) are pre-existing in `programs/self.glp` and `glp_runtime/lib/runtime/body_kernels.dart`.
- **Technology Stack**: **PASS**. All deps within Constitution-authorised stack (GLP source; Dart ^3.9.4 for REPL build; Markdown; Bash + PowerShell parity for any helper scripts).

**Result**: All applicable principles PASS or N/A. No Complexity Tracking entries required. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 research and Phase 1 design (research.md + data-model.md + contracts/ + quickstart.md), the Constitution Check is **re-validated**:

- **I. Spec-First**: still PASS. No design decision contradicts the spec; all 9 deferred items resolved in research.md with rationale tracing back to FRs.
- **II. No Workarounds**: still PASS. quickstart.md "On failure" section reinforces the halt-and-report posture for every plausible failure mode (Dart absent, REPL build fails, binding mismatch, SRSW/type errors, missing kernel).
- **III. SRSW Discipline**: still PASS. The contracts explicitly require SRSW compliance for the GLP files and explicitly require SRSW rejection for the LP-only file; no `skipSRSW` or anti-spec language flag is introduced.
- **IV. FCP Reference Architecture**: still N/A. No runtime touch.
- **V. Test-First**: still PASS with caveats. Captured traces ARE the regression artifacts for this feature.
- **VI. Tutorial Charter Compliance**: still PASS. R-001 references charter §1.5; R-006 references charter scope (formal-track and Example 2.2 narrative-only out of scope per charter). Cross-chapter import documented in R-007.
- **Language Design Authority**: still N/A.
- **Technology Stack**: still PASS. R-002 confirms no new third-party deps.

**Post-design verdict**: no new violations introduced by Phase 1 design. Plan complete.

## Project Structure

### Documentation (this feature)

```text
specs/003-tutorial-ch02/
├── spec.md                            # /speckit-specify + /speckit-clarify output (existing)
├── plan.md                            # this file (/speckit-plan output)
├── research.md                        # Phase 0 output (this command)
├── data-model.md                      # Phase 1 output (this command)
├── quickstart.md                      # Phase 1 output (this command)
├── contracts/                         # Phase 1 output (this command)
│   ├── trace-file-format.md           # ex-NN-repl-trace.md structural contract
│   ├── status-block-format.md         # ch02_tutorial.md approval-gate format
│   └── glp-file-format.md             # ch-02-ex-NN-*.glp content contract
├── checklists/
│   └── requirements.md                # /speckit-clarify output (existing)
├── QUARANTINE-DO-NOT-USE/             # existing — quarantined fabricated content
│   └── quarantine_003_ch02_spec.md
└── tasks.md                           # Phase 2 (/speckit-tasks — created by chained execution)
```

### Source Code (repository root)

**Constitution Option C: Tutorial chapter under charter.**

```text
olamni/tutorial/charter.md             # cited per Principle VI (existing, untouched)
olamni/tutorial/tutorial.md            # incremental top-level signpost (EXTEND ch02 row; per spec FR-006)
olamni/tutorial/ch02/
├── ch02-sources.md                    # PDF code-block index (existing, committed in 592d89e3)
├── ch02-specification-input-prompt.md # rev-eng output, no speckit ceremony (EXISTING; per spec FR-007)
├── ch02_tutorial.md                   # chapter signpost with status block (NEW; per spec FR-005)
├── spec-rev-eng-input/
│   └── ch02-DEPRECATED-spec.md        # rev-eng input copy (existing, committed in 146f430c)
├── exercise-01/
│   ├── ch-02-ex-01-classical-append-LP-only.glp  # Example 2.1 verbatim + header (NEW; per spec FR-001)
│   ├── ch-02-ex-01-glp-append.glp                # GLP append byte-exact pp 31–32 + %% (NEW; per spec FR-002)
│   ├── ex-01-tutorial.md                         # learner step-through (NEW; per spec FR-003)
│   └── ex-01-repl-trace.md                       # verbatim captured REPL session (NEW; per spec FR-004)
├── exercise-02/                       # GATED — only after ex-01 approved + REPL-tested
│   ├── ch-02-ex-02-append-and-sum.glp            # duplicated append/3 + sum/2 + append_and_sum/4 (NEW; per FR-009)
│   ├── ex-02-tutorial.md                         # learner step-through (NEW)
│   └── ex-02-repl-trace.md                       # verbatim captured REPL session (NEW; strict per FR-014)
└── exercise-03/                       # GATED — only after ex-02 approved + REPL-tested
    ├── ch-02-ex-03-timed-append.glp              # duplicated append/3 + timed_append/3 (NEW; per FR-010)
    ├── ex-03-tutorial.md                         # learner step-through (NEW)
    └── ex-03-repl-trace.md                       # verbatim captured REPL session w/ elapsed-ms relaxation (NEW; per FR-014)

# REPL build artifact (transient, not committed; reused from ch01 if still present)
glp_runtime/glp_repl.exe               # built from glp_runtime/bin/glp_repl.dart via `dart compile exe`
                                       # location and gitignore strategy: see research.md R-002 (inherited from ch01)
```

**Structure Decision**: Constitution Option C — Tutorial chapter under charter. Cites Constitution Principle VI (Tutorial Charter Compliance), `olamni/tutorial/charter.md` §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments — applies to all four `.glp` files in this chapter), and §design-principles 1–2 (section-driven; reader on §2.1/§2.2 loads matching files; ch 4 §4.2 import is the documented exception to "matching file" rule). No multi-actor / Flutter scope (chapter 2 is REPL-only per charter §1).

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
