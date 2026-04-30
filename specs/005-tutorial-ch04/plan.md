# Implementation Plan: Olamni Tutorial — Chapter 4 (Basic Concurrent Programming)

**Branch**: `005-tutorial-ch04` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/005-tutorial-ch04/spec.md` (with 3 resolved Clarifications, 2026-04-30: Q1 grouping = Option A 10 exercises; Q2 alleged-parser-limitations both verified stale and content retired; Q3 status-block format = per-exercise 10 lines).

## Summary

Build the chapter-4 tutorial under `olamni/tutorial/ch04/`: ten runnable exercises that cover the entire ch04 of *The Art of Grassroots Logic Programming* (Shapiro, 2025) — Basic Concurrent Programming. The largest content chapter so far (~38 substantial Programs across §4.1 + §4.2 + §4.3 + §4.4), grouped per Clarifications Q1 by sub-section family.

Three group-boundary approval gates govern progression (§4.1→§4.2, §4.2→§4.3, §4.3→§4.4); within a group exercises proceed without intermediate pairwise gates (NEW pattern for ch04 vs. ch01–ch03's pairwise model). Status block in `ch04_tutorial.md` uses the per-exercise 10-line format per Q3.

Per Clarifications Q2, the two CLAUDE.md "Known REPL Limitations" (structs-in-lists; `=..` in body) were empirically verified STALE — both work in the current REPL build (`30d9953c`). ex-05's §4.2.9 `distribute_indexed/3` and ex-08's §4.3.11 `distribute_ng/3` + `copy/3` + `copy_list/3` are implemented byte-exact with no special parser-limitation handling.

Technical approach: pure documentation + GLP-source feature. Volume: ~50 files for the entire chapter (10 .glp + 20 markdown new + 1 signpost + 1 input prompt + 1 markdown extended).

## Technical Context

**Language/Version**: Dart `^3.9.4` (REPL build); GLP (~38 substantial Programs byte-exact from PDF book pp 25–43, distributed across 10 exercise files); Markdown.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency. `programs/self.glp` (root prelude — provides `:=`, comparison guards, `=..` univ operator). NO new third-party deps.
**Storage**: On-disk Markdown + 10 `.glp` source files. No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` before/after implementation. Captured REPL traces ARE the regression artifacts. Per FR-016, ch04 files NOT in `test/run_all_tests.sh`.
**Target Platform**: Windows host for development; learner artifacts platform-agnostic.
**Project Type**: Tutorial chapter under charter (Constitution Option C).
**Performance Goals**: Learner completes the entire chapter in <90 minutes (per SC-001). REPL build <30 s. Each primary demo goal completes in <1 s (except possibly §4.4 MIs which may need elevated `:limit`).
**Constraints**:
- 10 locked Programs-per-exercise distributions per Q1 — no shape-restructuring during /speckit-plan.
- Locked primary goal bindings empirically verified during /speckit-implement; mismatch is halt-and-amend per FR-013.
- Strict trace byte-equality per FR-014; no per-run-variation exception.
- Self-containment per FR-010 (each exercise's `.glp` standalone-loadable).
- Group-boundary approval gates per FR-008 + FR-009.
- Cross-chapter inversion identity contract per FR-002 + SC-007 (ex-03's producer/consumer byte-identical to ch03's import).
- Plan-then-act per FR-013.
- No fabrication per FR-012.
**Scale/Scope**: 10 exercises; ~38 byte-exact Programs; ~60–80 `%%` paraphrase comments total across all `.glp` files.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec produced via `/speckit-specify`; 3 Clarifications via `/speckit-clarify`; this plan cites all.
- **II. No Workarounds**: **PASS**. Halt-and-report posture documented at every failure mode. Q2 retraction is the canonical anti-workaround posture: empirical verification overrode the doc claim.
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. All ~38 Programs are SRSW-compliant by byte-exact construction.
- **IV. FCP Reference Architecture**: **N/A**. Documentation feature only.
- **V. Test-First Discipline**: **PASS** with caveats. Baseline 485/485 expected per ch03 ship state. Captured traces ARE regression artifacts.
- **VI. Tutorial Charter Compliance**: **PASS**. Charter §1 + §1.5 + design-principles 1–2 cited; cross-chapter inversion documented.
- **Language Design Authority**: **N/A**. No new language features.
- **Technology Stack**: **PASS**. All within Constitution-authorised stack.

**Result**: All applicable principles PASS or N/A. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 + Phase 1: all 8 principles still PASS or N/A. R-001 through R-009 in research.md trace back to spec FRs and Clarifications. Phase 1 contracts (trace-file, status-block, glp-file) extend ch01/ch02/ch03's contracts without introducing new constraints.

**Post-design verdict**: no new violations. Plan complete.

## Project Structure

### Documentation (this feature)

```text
specs/005-tutorial-ch04/
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
olamni/tutorial/tutorial.md            # incremental top-level signpost (EXTEND ch04 row)
olamni/tutorial/ch04/
├── ch04-sources.md                    # PDF code-block index (existing)
├── ch04-specification-input-prompt.md # rev-eng prompt (EXISTING)
├── ch04_tutorial.md                   # chapter signpost with 10-line status block (NEW)
├── spec-rev-eng-input/ch04-DEPRECATED-spec.md  # rev-eng input copy (existing)
├── exercise-01/  ch-04-ex-01-constants-and-gates.glp + ex-01-tutorial.md + ex-01-repl-trace.md
├── exercise-02/  ch-04-ex-02-compound-circuits.glp + ex-02-tutorial.md + ex-02-repl-trace.md
├── exercise-03/  ch-04-ex-03-producer-consumer-reverse.glp + ex-03-tutorial.md + ex-03-repl-trace.md (§4.2 group; GATED behind §4.1)
├── exercise-04/  ch-04-ex-04-merge-variants.glp + ex-04-tutorial.md + ex-04-repl-trace.md
├── exercise-05/  ch-04-ex-05-stream-operators.glp + ex-05-tutorial.md + ex-05-repl-trace.md
├── exercise-06/  ch-04-ex-06-buffered-and-monitors.glp + ex-06-tutorial.md + ex-06-repl-trace.md
├── exercise-07/  ch-04-ex-07-recursive-numerics.glp + ex-07-tutorial.md + ex-07-repl-trace.md (§4.3 group; GATED behind §4.2)
├── exercise-08/  ch-04-ex-08-recursive-list-tree.glp + ex-08-tutorial.md + ex-08-repl-trace.md
├── exercise-09/  ch-04-ex-09-metaprogramming-foundations.glp + ex-09-tutorial.md + ex-09-repl-trace.md (§4.4 group; GATED behind §4.3)
└── exercise-10/  ch-04-ex-10-advanced-meta-interpreters.glp + ex-10-tutorial.md + ex-10-repl-trace.md

# REPL build artifact (transient, not committed)
glp_runtime/glp_repl.exe
```

**Structure Decision**: Constitution Option C — Tutorial chapter under charter. Cites Constitution Principle VI, charter §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments), design-principles 1–2 (section-driven). No multi-actor / Flutter scope. Cross-chapter inversion documented per spec FR-002.

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
