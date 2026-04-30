# Implementation Plan: Olamni Tutorial — Chapter 3 (GLP Core + §3.2 Guard Curriculum)

**Branch**: `004-tutorial-ch03` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/004-tutorial-ch03/spec.md` (with 3 resolved Clarifications, 2026-04-29 / 2026-04-30).

## Summary

Build the chapter-3 tutorial under `olamni/tutorial/ch03/`: three runnable exercises that progressively introduce the §3.2 guard species (built-in → defined → negation) on top of Program 3.1's GLP Fair Stream Merger.

- **ex-01** — Program 3.1 (`merge/3` byte-exact from PDF p 15) paired with `producer/2` + `consumer/3` (byte-exact from PDF p 43, locked per Clarifications Q1) into a composed producer-merger-consumer pipeline. Two `.glp` files per dir; primary demo goal `producer(A, 5), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` with locked binding `Sum = 21`. Built-in guards only (`>` from `producer/2`, `ground` from `consumer/3`); the body kernel `:=` appears only inside the verbatim ch4-imported procedures (per FR-015 amendment).
- **ex-02** — defined-guards variation locked per Clarifications Q2 to `channel/1` + `process/2` (byte-exact from PDF p 34 / book p 22). Single `.glp` file. Primary goal `process(ch(a, b), Status).` with locked binding `Status = ok`. The book's `process/2` body calls `handle/1` which is undefined in the book; /speckit-plan picks between local-stub-definition `handle(_).` and body-substitution (replace `handle(X?)` with `true`); decision recorded in `research.md` (see R-008).
- **ex-03** — guard-negation amplification locked per Clarifications Q3 to `lookup/3` complete with both clauses (byte-exact from PDF p 34 / book p 22). Single `.glp` file. Primary goal `lookup(b, [(a,1),(b,2),(c,3)], V).` with locked binding `V = 2`. The two clauses demonstrate positive `=?=` (clause 1) and negated `~(=?=)` (clause 2) on the same operator — the canonical §3.2 negation pedagogy.

Each later exercise's `.glp` MAY duplicate Program 3.1's `merge/3` and/or the producer/consumer pair inline only if the chosen composition exercises them (per FR-009 / FR-010 conditional-duplication rule). If ex-02 / ex-03 stand alone (no `merge/3` composition), no duplication is required. Two predecessor-approval gates govern progression (status block in `ch03_tutorial.md`); ex-02 cannot begin until ex-01 is approved AND thoroughly REPL-tested; ex-03 cannot begin until ex-02 likewise. All three variation-shape gates are CLOSED in the spec via Clarifications Q1+Q2+Q3.

Technical approach: pure documentation + GLP-source feature. No runtime / type-system / language changes. Implementation uses the existing `glp_runtime/bin/glp_repl.dart` compiled to a host executable to capture verbatim REPL traces (the same artifact ch01 + ch02 produced). Predicted bindings are empirically verified during the trace step; mismatch is halt-and-report (Constitution Principle II).

## Technical Context

**Language/Version**: Dart `^3.9.4` (REPL build only — `dart compile exe glp_runtime/bin/glp_repl.dart [--define=GLP_BUILD_COMMIT=...]`); GLP (`.glp` source — Program 3.1 verbatim from PDF p 15 + `producer/2` + `consumer/3` verbatim from PDF p 43 + `channel/1` + `process/2` verbatim from PDF p 34 + `lookup/3` verbatim from PDF p 34 + locally-defined `handle/1` stub for ex-02 if R-008 picks the stub option); Markdown (all written documentation); Bash + PowerShell parity for any wrapper scripts.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency (provides the REPL). `programs/self.glp` (root prelude — provides `:=`, comparison guards `>`, `=?=`, `ground`, `otherwise`). NO new third-party Dart packages, NO Python tooling, NO Flutter dependency. NO new body kernels (`:=` is pre-existing; ch3 inherits its use only via byte-exact ch4 import per FR-015 amendment).
**Storage**: On-disk Markdown files + four `.glp` source files (ex-01 has 2 files for the contrast pair; ex-02 has 1; ex-03 has 1). No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` MUST be recorded before implementation begins. Feature-specific verification = the empirical REPL run that produces `ex-NN-repl-trace.md` for each of the three exercises. No new Dart unit tests. No Flutter build (chapter 3 is REPL-only per `olamni/tutorial/charter.md` §1). Per spec FR-016, ch03 exercise files are NOT added to `test/run_all_tests.sh`.
**Target Platform**: Windows host for development (this repo); learner-facing artifacts MUST be platform-agnostic (Markdown + `.glp` work on macOS / Linux / Windows with any Dart 3.9.4+ host).
**Project Type**: **Tutorial chapter (under charter)** — Constitution Option C.
**Performance Goals**: Learner completes exercise-01 in <15 min given a working REPL (per spec SC-001 — extended from ch02's <10 min because ex-01's composed pipeline references procedures across two files). REPL build (`dart compile exe`) <30 s on typical hardware. Each primary demo goal completes in <1 s.
**Constraints**:
- Three locked bindings (ex-01 `Sum = 21`, ex-02 `Status = ok`, ex-03 `V = 2`) MUST be empirically verified during implementation; mismatch is halt-and-report per FR-013, with amendment via a new Clarifications entry preserving audit trail (ch02 Q3a precedent).
- ex-01 trace MUST capture the load of BOTH `.glp` files plus the composed primary goal plus three inspection goals across all THREE clauses of Program 3.1 (per FR-018).
- ALL THREE traces (ex-01, ex-02, ex-03) inherit strict byte-equality modulo REPL banner / build wallclock lines (per FR-014); chapter 3 introduces no wallclock-derived output, so ch02's elapsed-ms relaxation does NOT apply.
- ex-02 and ex-03 `.glp` files MAY duplicate Program 3.1's `merge/3` (and ch4 producer/consumer) inline ONLY IF the chosen composition exercises them (per FR-009 / FR-010 conditional-duplication rule).
- Body kernels appear in ch3 ONLY inside byte-exact ch4-imported procedures (`producer/2`'s `:=` decrement, `consumer/3`'s `:=` accumulation per FR-015 amendment). NO new body kernel introductions; `now/1` and `'_output'/1` are entirely out of scope (those are ch2 territory per FR-015 + SC-015).
- The book's `process/2` body calls `handle/1` which is undefined in the book; /speckit-plan picks resolution per R-008 (local stub `handle(_).` preserves byte-exactness; body substitution `true` deviates with header annotation).
- Approval-gate enforcement is a status block in `ch03_tutorial.md` greppable by downstream sessions (per spec FR-008).
- Plan-then-act discipline: every implementation step (build REPL, write each `.glp`, run trace, write tutorial, write signpost) MUST be presented as a numbered step and approved before action (per spec FR-013).
- No fabrication: Claude MUST NOT impersonate `/speckit-specify` output (per spec FR-012).
**Scale/Scope**: Single chapter (ch03) this round. Three exercises (`exercise-01/`, `exercise-02/`, `exercise-03/`). ~12 files written: 4 `.glp` (ex-01 has 2, ex-02 has 1, ex-03 has 1) + 6 Markdown new (3 tutorials + 3 traces) + 1 signpost (ch03_tutorial.md) + 1 input prompt (ALREADY WRITTEN as of branch creation) + 1 markdown extended (top-level `tutorial.md`).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec at `specs/004-tutorial-ch03/spec.md` produced via proper-channel `/speckit-specify`; 3 Clarifications integrated via proper-channel `/speckit-clarify`; this plan cites both. The plain-prose input prompt is `olamni/tutorial/ch03/ch03-specification-input-prompt.md`.
- **II. No Workarounds**: **PASS**. No try/catch-and-ignore in scope. The "halt-and-report" rule for any binding mismatch (FR-013) is the canonical anti-workaround posture. Any REPL-build failure halts implementation (per Edge Cases in spec). The intentional `:=` body-kernel inheritance from the byte-exact ch4 import (per FR-015 amendment) is NOT a workaround — it is the documented consequence of the byte-exact provenance rule (FR-002 + SC-007), explicitly amended in spec.md Clarifications Q1.
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. Program 3.1 (the chapter's anchor) is the SRSW-compliant fair merger that motivates the entire chapter; `producer/2`, `consumer/3`, `channel/1`, `process/2`, and `lookup/3` are ALL SRSW-compliant per their byte-exact book sources. No `skipSRSW`; no ad-hoc relaxations introduced. The `=?=` operator and the `~(...)` negation form are pre-existing GLP language features per the book §3.2 and pre-existing in `programs/self.glp` and the runtime — NOT new language additions.
- **IV. FCP Reference Architecture**: **N/A**. No runtime / heap / dispatch / suspension changes; documentation + GLP-source feature only.
- **V. Test-First Discipline**: **PASS** with caveats. Baseline = `bash test/run_all_tests.sh` recorded before implementation begins (expected: 494/494 if `claude/fix-misleading-build-line` merged, 485/485 otherwise per workflow memory's REPL Infrastructure section). Feature-specific tests = the captured REPL traces (which ARE the regression artifacts for this feature). No new Dart unit tests required (the `.glp` files load under the existing GLP REPL pipeline). No Flutter UI affected (chapter 3 = REPL-only per charter).
- **VI. Tutorial Charter Compliance**: **PASS**. Plan cites `olamni/tutorial/charter.md` §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments — applies to BOTH `.glp` files in ex-01 + the ex-02 + ex-03 files), and §design-principles 1–2 (section-driven for chs 1–6). The cross-chapter import from ch4 §4.2.1 + §4.2.2 is documented in the input prompt, in the spec FR-002 + Clarifications Q1, and in the importing `.glp` files' header comments. Per the workflow memory, no `ch03_plan.md` is required (the previous fabricated `chXX_plan.md` files were deleted in commit `592d89e3`). The `=?=` and `~(...)` machinery in §3.2 is pre-existing language scope; no charter expansion required.
- **Language Design Authority**: **N/A**. No new guard / system predicate / body kernel / directive / type-system feature. The guards used (built-in `>`, `ground`, `=?=`, defined `channel/1`, negation `~(=?=)`) are all pre-existing in the GLP language per the book §3.2 and pre-existing in the runtime. The body kernels appearing in the inherited ch4 imports (`:=`) are pre-existing (introduced for ch2's tutorial).
- **Technology Stack**: **PASS**. All deps within Constitution-authorised stack (GLP source; Dart ^3.9.4 for REPL build; Markdown; Bash + PowerShell parity for any helper scripts).

**Result**: All applicable principles PASS or N/A. No Complexity Tracking entries required. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 research and Phase 1 design (research.md + data-model.md + contracts/ + quickstart.md), the Constitution Check is **re-validated**:

- **I. Spec-First**: still PASS. No design decision contradicts the spec; all deferred items resolved in research.md with rationale tracing back to FRs and Clarifications Q1+Q2+Q3.
- **II. No Workarounds**: still PASS. quickstart.md "On failure" section reinforces the halt-and-report posture for every plausible failure mode. The R-008 handle/1 resolution (local stub vs. body substitution) is documented as a deliberate decision with byte-exactness tradeoff annotated, not a workaround for runtime breakage.
- **III. SRSW Discipline**: still PASS. The contracts explicitly require SRSW compliance for all four `.glp` files; no `skipSRSW` or anti-spec language flag is introduced. Note: ex-02's composition with merge/3 (if R-009 picks "compose") may surface SRSW edge cases at REPL load — per FR-013 these halt and amend, never silently relax.
- **IV. FCP Reference Architecture**: still N/A. No runtime touch.
- **V. Test-First**: still PASS with caveats. Captured traces ARE the regression artifacts for this feature.
- **VI. Tutorial Charter Compliance**: still PASS. R-001 references charter §1.5; R-006 references charter scope (formal-track, Worked Examples 1–4 narrative-only out of scope per charter); R-007 documents the cross-chapter import per charter design-principles 1–2's "documented exception" clause.
- **Language Design Authority**: still N/A.
- **Technology Stack**: still PASS. R-002 confirms no new third-party deps.

**Post-design verdict**: no new violations introduced by Phase 1 design. Plan complete.

## Project Structure

### Documentation (this feature)

```text
specs/004-tutorial-ch03/
├── spec.md                            # /speckit-specify + /speckit-clarify output (existing)
├── plan.md                            # this file (/speckit-plan output)
├── research.md                        # Phase 0 output (this command)
├── data-model.md                      # Phase 1 output (this command)
├── quickstart.md                      # Phase 1 output (this command)
├── contracts/                         # Phase 1 output (this command)
│   ├── trace-file-format.md           # ex-NN-repl-trace.md structural contract
│   ├── status-block-format.md         # ch03_tutorial.md approval-gate format
│   └── glp-file-format.md             # ch-03-ex-NN-*.glp content contract
├── checklists/
│   └── requirements.md                # /speckit-specify output (existing)
├── QUARANTINE-DO-NOT-USE/             # existing — quarantined fabricated content
│   └── quarantine_004_ch03_spec.md
└── tasks.md                           # Phase 2 (/speckit-tasks — created by chained execution)
```

### Source Code (repository root)

**Constitution Option C: Tutorial chapter under charter.**

```text
olamni/tutorial/charter.md             # cited per Principle VI (existing, untouched)
olamni/tutorial/tutorial.md            # incremental top-level signpost (EXTEND ch03 row; per spec FR-006)
olamni/tutorial/ch03/
├── ch03-sources.md                    # PDF code-block index (existing, committed in 592d89e3)
├── ch03-specification-input-prompt.md # rev-eng output, no speckit ceremony (EXISTING; per spec FR-007)
├── ch03_tutorial.md                   # chapter signpost with status block (NEW; per spec FR-005)
├── spec-rev-eng-input/
│   └── ch03-DEPRECATED-spec.md        # rev-eng input copy (existing)
├── exercise-01/
│   ├── ch-03-ex-01-glp-fair-stream-merger.glp  # Program 3.1 byte-exact p 15 + %% (NEW; per FR-001)
│   ├── ch-03-ex-01-producer-consumer.glp       # producer/2 + consumer/3 byte-exact p 43 + %% (NEW; per FR-002 + Q1)
│   ├── ex-01-tutorial.md                       # learner step-through (NEW; per FR-003)
│   └── ex-01-repl-trace.md                     # verbatim captured REPL session (NEW; per FR-004)
├── exercise-02/                       # GATED — only after ex-01 approved + REPL-tested
│   ├── ch-03-ex-02-defined-guards.glp          # channel/1 + process/2 byte-exact p 34 + handle/1 stub (NEW; per FR-009 + Q2)
│   ├── ex-02-tutorial.md                       # learner step-through (NEW)
│   └── ex-02-repl-trace.md                     # verbatim captured REPL session (NEW; strict per FR-014)
└── exercise-03/                       # GATED — only after ex-02 approved + REPL-tested
    ├── ch-03-ex-03-guard-negation.glp          # lookup/3 byte-exact p 34 (both clauses) (NEW; per FR-010 + Q3)
    ├── ex-03-tutorial.md                       # learner step-through (NEW)
    └── ex-03-repl-trace.md                     # verbatim captured REPL session (NEW; strict per FR-014 — no relaxation since ch3 has no wallclock output)

# REPL build artifact (transient, not committed; reused from ch01/ch02 if still present)
glp_runtime/glp_repl.exe               # built from glp_runtime/bin/glp_repl.dart via `dart compile exe`
                                       # location and gitignore strategy: see research.md R-002 (inherited from ch01/ch02)
```

**Structure Decision**: Constitution Option C — Tutorial chapter under charter. Cites Constitution Principle VI (Tutorial Charter Compliance), `olamni/tutorial/charter.md` §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments — applies to all four `.glp` files in this chapter), and §design-principles 1–2 (section-driven; reader on §3.1/§3.2 loads matching files; ch4 §4.2.1+§4.2.2 import is the documented exception to "matching file" rule for ex-01). No multi-actor / Flutter scope (chapter 3 is REPL-only per charter §1).

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
