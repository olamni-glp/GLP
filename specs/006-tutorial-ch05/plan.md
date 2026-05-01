# Implementation Plan: Olamni Tutorial — Chapter 5 (Types and Modes)

**Branch**: `006-tutorial-ch05` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/006-tutorial-ch05/spec.md` (with 3 resolved Clarifications, 2026-04-30: Q1 grouping = Option A 8 exercises with locked exercise list; Q2 helper-stub shapes = deferred to /speckit-plan T006-equivalent with permitted-shape sketch; Q3 status-block format = per-exercise 8 lines; plus 4 pre-resolved decisions: negative-exercise split / group-boundary gates / type-checker live pipeline / parser-limitations stale).

## Summary

Build the chapter-5 tutorial under `olamni/tutorial/ch05/`: eight runnable exercises that cover the entire ch05 of *The Art of Grassroots Logic Programming* (Shapiro, 2025) — Types and Modes. Substantially smaller volume than ch04 (~10 substantial PDF code blocks across 7 sub-sections vs. ch04's ~38) but pedagogically dense — every block introduces a new concept (type-def `::=` form, recursive type, list type, built-in `Any`, procedure declaration with `?` reader marks, mode checking flow, embedded modes, typed flagship algorithm, type errors, mode errors).

ch05 is the first chapter where the third stage of the REPL pipeline (`SRSW → PE → type-check → compile → execute`) does meaningful work on the chapter's tutorial code. Previous chapters' code was implicitly `Any`-typed. ch05's code carries explicit `T ::= …` definitions and `procedure` declarations that the type-checker validates.

Three group-boundary approval gates govern progression (Foundations §5.1+§5.2+§5.3 → Mode-checking-flow §5.4+§5.5 → Flagship §5.6 → Negatives §5.7); within a group exercises proceed without intermediate pairwise gates (inherited from ch04). Status block in `ch05_tutorial.md` uses the per-exercise 8-line format per Q3.

ch05 introduces a new exercise shape — **type-definition-only** + **procedure-declaration-only** + **negative-load-test** — none present in ch01–ch04. Per Q2, helpers for ex-01/ex-02/ex-03 are proposed and approved during /speckit-plan T006-equivalent within the implement phase. Per FR-018, the type-checker stage of the REPL pipeline is verified operational at /speckit-implement T001-equivalent before any §5.7 negative exercise begins.

Cross-chapter relationships (NOT imports) link ex-04's typed `merge/3` to ch04's untyped `merge/3` and ex-05's typed `counter/2` to ch04's untyped `counter/1`. Each ch05 exercise carries its own byte-exact PDF code; no cross-chapter import.

Technical approach: pure documentation + GLP-source feature. Volume: ~30 files for the entire chapter (8 .glp baseline + up to 2 extra for negative two-file pattern = 8–10 .glp + 16 markdown new + 1 signpost + 1 input prompt existing + 1 markdown extended).

## Technical Context

**Language/Version**: Dart `^3.9.4` (REPL build); GLP (~10 substantial Programs byte-exact from PDF book pp 47–52, distributed across 8 exercise files + helper unit-clauses for ex-01/ex-02/ex-03); Markdown.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency. `programs/self.glp` (root prelude — provides `:=` arithmetic for §5.7.2 corrected `bar/2`). NO new third-party deps.
**Storage**: On-disk Markdown + 8–10 `.glp` source files. No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` before/after implementation. Captured REPL traces ARE the regression artifacts. Per FR-016, ch05 files NOT in `test/run_all_tests.sh`.
**Target Platform**: Windows host for development; learner artifacts platform-agnostic.
**Project Type**: Tutorial chapter under charter (Constitution Option C).
**Performance Goals**: Learner completes the entire chapter in <60 minutes (per SC-001). REPL build <30 s. Each positive primary demo goal completes in <1 s. Each negative load attempt fails-fast (<1 s) with deterministic error message.
**Constraints**:
- 8 locked Programs-per-exercise distributions per Q1 — no shape-restructuring during /speckit-plan.
- Locked primary goal bindings empirically verified during /speckit-implement; mismatch is halt-and-amend per FR-013.
- Strict trace byte-equality per FR-014; no per-run-variation exception for positive exercises. Negative-exercise per-run-varying segments (memory addresses, tuple-ids in error messages) authorised via /speckit-implement T026/T037-equivalent if and only if observed.
- Self-containment per FR-010 (each exercise's `.glp` standalone-loadable; `NumList` reused in §5.4 + §5.6 duplicated inline).
- Group-boundary approval gates per FR-008 + FR-009 (3 gates).
- Cross-chapter relationship contract per FR-002 + SC-007 (typed `merge/3` ↔ ch04 untyped; typed `counter/2` ↔ ch04 untyped — RELATIONSHIPS, not byte-identical imports).
- Plan-then-act per FR-013.
- No fabrication per FR-012.
- Type-checker operational per FR-018 + SC-012.
**Scale/Scope**: 8 exercises; ~10 byte-exact Programs; ~20–30 `%%` paraphrase comments total across all `.glp` files; 3 helper-clause families (ex-01/ex-02/ex-03) proposed during T006-equivalent.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec produced via `/speckit-specify`; 3 Clarifications via `/speckit-clarify`; this plan cites all.
- **II. No Workarounds**: **PASS**. Halt-and-report posture documented at every failure mode (FR-013, FR-018). Negative-exercise contract is NOT a workaround — the load failure IS the demonstrated outcome per spec; treating it as success-by-failure is by-design.
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. All ~10 PDF Programs are SRSW-compliant by byte-exact construction. Helper unit-clauses + procedure-decl stub (Q2 deferral) MUST satisfy SRSW + type-check at REPL load; mismatch is halt-and-amend per FR-013.
- **IV. FCP Reference Architecture**: **N/A**. Documentation feature only. The REPL's type-checker is exercised as a black-box validator; no FCP heap mechanism is touched.
- **V. Test-First Discipline**: **PASS** with caveats. Baseline expected from ch04 ship state (485/485+ ; ch04 added new sections to run_all_tests.sh). Captured traces ARE regression artifacts. Type-checker verification at FR-018 is itself a baseline-establishing test.
- **VI. Tutorial Charter Compliance**: **PASS**. Charter §1 (REPL-only for chs 1–6) + §1.5 (per-clause `%%` paraphrase comments) + design-principles 1–2 (section-driven) cited. Cross-chapter relationships (typed ↔ untyped) documented per spec FR-002 + signpost prose.
- **Language Design Authority**: **N/A**. No new language features. The type system + mode declarations + `procedure` keyword + `Any`/`Number`/`Atom` built-ins all PRE-EXIST; ch05 merely TEACHES them.
- **Technology Stack**: **PASS**. All within Constitution-authorised stack.

**Result**: All applicable principles PASS or N/A. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 + Phase 1: all 8 principles still PASS or N/A. R-001 through R-009 in research.md trace back to spec FRs and Clarifications. Phase 1 contracts (trace-file, status-block, glp-file) extend ch04's contracts with negative-exercise additions (2-phase trace structure for negative; helper-clause discipline rule for type-only/proc-decl-only).

**Post-design verdict**: no new violations. Plan complete.

## Project Structure

### Documentation (this feature)

```text
specs/006-tutorial-ch05/
├── spec.md                            # /speckit-specify + /speckit-clarify output (existing)
├── plan.md                            # this file (/speckit-plan output)
├── research.md                        # Phase 0 output
├── data-model.md                      # Phase 1 output
├── quickstart.md                      # Phase 1 output
├── contracts/                         # Phase 1 output
│   ├── trace-file-format.md
│   ├── status-block-format.md
│   └── glp-file-format.md
├── checklists/requirements.md         # /speckit-specify output (existing)
├── QUARANTINE-DO-NOT-USE/             # existing
└── tasks.md                           # Phase 2 (/speckit-tasks output)
```

### Source Code (repository root)

**Constitution Option C: Tutorial chapter under charter.**

```text
olamni/tutorial/charter.md             # cited per Principle VI (existing)
olamni/tutorial/tutorial.md            # incremental top-level signpost (EXTEND ch05 row)
olamni/tutorial/ch05/
├── ch05-sources.md                    # PDF code-block index (existing)
├── ch05-specification-input-prompt.md # rev-eng prompt (EXISTING)
├── ch05_tutorial.md                   # chapter signpost with 8-line status block (NEW)
├── spec-rev-eng-input/ch05-DEPRECATED-spec.md  # rev-eng input copy (existing)
├── exercise-01/  ch-05-ex-01-type-definitions.glp + ex-01-tutorial.md + ex-01-repl-trace.md          (Foundations group)
├── exercise-02/  ch-05-ex-02-built-in-types.glp + ex-02-tutorial.md + ex-02-repl-trace.md            (Foundations group)
├── exercise-03/  ch-05-ex-03-procedure-declaration.glp + ex-03-tutorial.md + ex-03-repl-trace.md     (Foundations group)
├── exercise-04/  ch-05-ex-04-mode-checked-merge.glp + ex-04-tutorial.md + ex-04-repl-trace.md         (Mode-checking-flow group; GATED behind Foundations)
├── exercise-05/  ch-05-ex-05-counter-response-slot.glp + ex-05-tutorial.md + ex-05-repl-trace.md      (Mode-checking-flow group)
├── exercise-06/  ch-05-ex-06-typed-quicksort.glp + ex-06-tutorial.md + ex-06-repl-trace.md            (Flagship group; GATED behind Mode-checking-flow)
├── exercise-07/  ch-05-ex-07-type-error{-failing,-corrected}.glp + ex-07-tutorial.md + ex-07-repl-trace.md  (Negatives group; GATED behind Flagship; two-.glp pattern)
└── exercise-08/  ch-05-ex-08-mode-error{-failing,-corrected}.glp + ex-08-tutorial.md + ex-08-repl-trace.md  (Negatives group; two-.glp pattern)

# REPL build artifact (transient, not committed)
glp_runtime/glp_repl.exe
```

**Structure Decision**: Constitution Option C — Tutorial chapter under charter. Cites Constitution Principle VI, charter §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments), design-principles 1–2 (section-driven). No multi-actor / Flutter scope. Cross-chapter relationships (typed↔untyped) documented per spec FR-002 + signpost prose. Negative exercises ex-07 + ex-08 use the two-`.glp` pattern (failing form + corrected form) per FR-001's "up to 2 .glp" allowance.

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
