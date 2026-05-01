# Implementation Plan: Olamni Tutorial — Chapter 6 (Typed Programming)

**Branch**: `007-tutorial-ch06` | **Date**: 2026-05-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/007-tutorial-ch06/spec.md` with **2 resolved Clarifications** (Q1: ex-01 source = ch04 §4.3.7 `flatten`+`flatten_acc` per Option B, ex-03 source = ch04 §4.4.4 control MI per input-prompt default; Q2: type/procedure declaration shapes deferred to /speckit-plan T006-equivalent per ch05 Q2 precedent).

## Summary

Build the chapter-6 tutorial under `olamni/tutorial/ch06/`: **five** runnable exercises, one per §6.x heading, that synthesise the chapter's content from cited byte-exact earlier-chapter PDF sources because **the ch06 PDF is a stub** (book p 53 contains only the chapter title and five section headings, no body text and no Programs).

**Source map** (locked per spec FR-003 + Clarification Q1):
- ex-01 §6.1 Difference Lists ← ch04 §4.3.7 `flatten`+`flatten_acc` (book pp 38–39)
- ex-02 §6.2 Quicksort ← ch05 §5.6 typed quicksort (book p 51)
- ex-03 §6.3 Equators: Emergency Brake ← ch04 §4.4.4 control meta-interpreter `run/5`+`suspended_run/4` (book p 42)
- ex-04 §6.4 Bidirectional Communication ← ch03 §3.2 channel ops `send`/`receive`/`new_channel`/`relay`/`make_pair` (book p 23)
- ex-05 §6.5 Buffered Communication ← ch04 §4.2.12+§4.2.13 `bb`+`bb_test` sliding-window buffer (book pp 34–35)

**Approval gates**: pairwise per FR-008 (4 gates between 5 exercises). Chapter is small enough that ch04/ch05's group gates are unnecessary; pairwise inherits from ch01–ch03 pattern. Status block in `ch06_tutorial.md` uses the per-exercise 5-line format.

**Cross-chapter relationships are NOT cross-chapter imports** — each ch06 exercise's clauses are byte-exact from their cited earlier-chapter PDF source (per FR-002), with type definitions and `procedure` declarations introduced fresh at §6.x per ch05 conventions (the literal-source mandate applies to *clauses*, not to introduced declarations). Documented in three places per FR-014: `.glp` header, signpost, top-level `tutorial.md` row footnote.

**Type-checker is operational** (inherited from ch05 R-006 + SC-006). All five exercises must pass the live type-checker after declarations are added; halt-and-amend per FR-013 if the type-checker rejects what loaded fine in the un-typed source chapter — the byte-exact clause body is locked, the declaration shape is amendable per Q2.

**Per Q2 deferral**: specific type/procedure declaration shapes are NOT locked at the spec layer; they are proposed during /speckit-plan T006-equivalent (which lands in `research.md` Phase 0 below) with project-owner approval recorded; mismatch with the analyser at /speckit-implement load is halt-and-amend per FR-013.

Technical approach: pure documentation + GLP-source feature. Volume: ~17 files for the entire chapter (5 exercise dirs × {1 `.glp` + 1 tutorial.md + 1 trace.md} + 1 chapter signpost + 1 input prompt already exists + 1 sources index already exists + 1 deprecated spec copy already exists + this plan + spec + downstream artifacts).

## Technical Context

**Language/Version**: Dart `^3.9.4` (REPL build; this Windows host has 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`); GLP (~5 byte-exact source Programs distributed across 5 `.glp` files); Markdown.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency. `programs/self.glp` (root prelude — provides built-in types `Number`/`Atom`/`Any`, `Stream(X)`/`List`/`NumList`-style parametric machinery, `:=` arithmetic kernel, `number/1` guard). NO new third-party deps.
**Storage**: On-disk Markdown + 5 `.glp` source files (one per exercise). No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` before/after implementation. Captured REPL traces ARE the regression artifacts. Per FR-016, ch06 files NOT in `test/run_all_tests.sh`.
**Target Platform**: Windows host for development; learner artifacts platform-agnostic.
**Project Type**: Tutorial chapter under charter (Constitution Option C).
**Performance Goals**: Each exercise's `.glp` loads in <5 s (per SC-002). Each primary demo goal completes in <1 s. REPL build <30 s. Quicksort ex-02 on 8-element list completes within default `:limit`. Control MI ex-03 with abort message demonstrates termination within default `:limit`. (Chapter has 5 exercises — smaller than ch04's 10 and ch05's 7; no chapter-completion-time SC defined.)
**Constraints**:
- 5 locked exercise distributions per FR-001 + spec source map — no shape-restructuring during /speckit-plan.
- Locked primary goal bindings empirically verified during /speckit-implement; mismatch is halt-and-amend per FR-013.
- Strict trace byte-equality per FR-012; no per-run-variation expected (no `now/1` / `'_output'/1` — those are ch02 territory and explicitly out of scope per Out of scope section).
- Self-containment per FR-009 (each exercise's `.glp` standalone-loadable; no shared types.glp helper file).
- Pairwise approval gates per FR-008 (4 gates between 5 exercises).
- Cross-chapter relationships per FR-014 documented as header cross-references + signpost prose + top-level footnote, NOT code imports.
- Type-checker live-pipeline requirement — pre-flight verification per FR-018 + SC-006 BEFORE any exercise begins; ch06 work halts per FR-013 against a broken type-checker.
- Per Q2 deferral: declaration shapes proposed during /speckit-plan T006-equivalent with project-owner approval recorded in `research.md` (R-007 below).
- Plan-then-act per FR-013.
- Body kernels: `:=` is permitted in any byte-exact source clause that uses it (per ch03 FR-015 amendment precedent — applies to ch04 §4.3.7 flatten_acc which does NOT use `:=`, and ch04 §4.2.12 bb which does NOT use `:=`; net result: `:=` likely does NOT appear in any ch06 `.glp`); `now/1` / `'_output'/1` MUST NOT appear (none of the source Programs use them).
**Scale/Scope**: 5 exercises (4 pairwise gates); 5 byte-exact source Programs spanning ch03 + ch04 + ch05; ~25–35 `%%` paraphrase comments total across all `.glp` files (estimate based on the source Programs' clause counts: flatten ~5 clauses + quicksort ~6 + control MI ~7 + channel ops ~6 + bb ~4 = ~28 clauses → ~28 comments + per-§6.x heading mapping notes).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec produced via `/speckit-specify` then refined through 2 Clarifications (Q1 source map for ex-01 + ex-03; Q2 declaration-shape deferral). This plan cites both. The 2-clarification count vs ch05's 12 reflects ch06's simpler scope (synthesis from earlier chapters, no new type-system content).
- **II. No Workarounds**: **PASS**. Halt-and-report posture documented at every failure mode in quickstart §"On failure". The synthesis-from-earlier-chapters approach is itself NOT a workaround — it is the spec-authorised response to the ch06 PDF stub state per FR-001 + Assumptions; if the author fills in the PDF body between now and /speckit-implement, FR-015 halt-and-report applies (do NOT silently fold native content into synthesised exercises without re-running /speckit-clarify).
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. All 5 source Programs are SRSW-compliant by byte-exact construction (they were each verified at their original chapter's load; ch01–ch05 implementations confirmed). Adding type/procedure declarations does not affect SRSW; the analyser runs SRSW BEFORE type-check per the REPL pipeline contract.
- **IV. FCP Reference Architecture**: **N/A**. Documentation feature only; no runtime/compiler/type-checker code changes.
- **V. Test-First Discipline**: **PASS** with caveats. Baseline expected per ch05 ship state (494/494 plus any drift from `claude/fix-misleading-build-line` merge state). Captured traces ARE regression artifacts per FR-016 (chapter files explicitly NOT in `run_all_tests.sh`). Type-checker pre-flight verification per FR-018 + SC-006 is itself a baseline-establishing test for ch06's typed re-presentations.
- **VI. Tutorial Charter Compliance**: **PASS**. Charter §1 (REPL-only for chs 1–6) + §1.5 (`%%` paraphrase comments — one per clause) + design-principles 1–2 (section-driven) cited. Cross-chapter relationships (synthesis from earlier chapters) documented per R-008 below as a NEW contract specific to ch06's stub-source mode; distinct from ch04's cross-chapter-inversion identity (where the same code appears in two chapters with different paraphrase context) and ch05's typed↔untyped relationship (same procedure name, different signature/clauses).
- **Language Design Authority**: **N/A**. No new guards, system predicates, body kernels, directives, or type-system features introduced. The type system + `procedure` declaration + mode marks all PRE-EXIST from ch05.
- **Technology Stack**: **PASS**. All artifacts within Constitution-authorised stack (Dart 3.9.4+, GLP, Markdown).

**Result**: All applicable principles PASS or N/A. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 + Phase 1: all 8 principles still PASS or N/A. R-001 through R-009 in research.md trace back to spec FRs and Clarifications Q1–Q2. Phase 1 contracts (trace-file, status-block, glp-file) inherit from ch01–ch05's contracts with two additions specific to ch06: (a) glp-file contract requires a "synthesis cross-reference" header block citing both the earlier-chapter source AND the §6.x heading; (b) status-block contract uses the pairwise 5-line format inherited from ch01–ch03 (NOT ch04/ch05's group format).

**Post-design verdict**: no new violations. Plan complete; proceeds to /speckit-tasks.

## Project Structure

### Documentation (this feature)

```text
specs/007-tutorial-ch06/
├── spec.md                            # /speckit-specify + /speckit-clarify (Q1, Q2) output (existing)
├── plan.md                            # this file (/speckit-plan output)
├── research.md                        # Phase 0 output (R-001..R-009)
├── data-model.md                      # Phase 1 output
├── quickstart.md                      # Phase 1 output
├── contracts/                         # Phase 1 output
│   ├── trace-file-format.md           # 5-phase positive (1 load + primary + 3 inspection)
│   ├── status-block-format.md         # per-exercise 5-line pairwise grep contract
│   └── glp-file-format.md             # 5 file specs with synthesis cross-reference header block
├── checklists/requirements.md         # /speckit-specify output (existing)
├── QUARANTINE-DO-NOT-USE/             # existing — untouched per spec Out-of-scope
└── tasks.md                           # Phase 2 (/speckit-tasks output)
```

### Source Code (repository root)

**Constitution Option C: Tutorial chapter under charter.**

```text
olamni/tutorial/charter.md             # cited per Principle VI (existing)
olamni/tutorial/tutorial.md            # incremental top-level signpost (UPDATE ch06 row + footnote)
olamni/tutorial/ch06/
├── ch06-sources.md                    # PDF code-block index — already documents stub state (existing)
├── ch06-specification-input-prompt.md # rev-eng prompt (existing)
├── ch06_tutorial.md                   # chapter signpost with 5-line status block (NEW)
├── spec-rev-eng-input/ch06-DEPRECATED-spec.md  # rev-eng input copy (existing — untouched)
├── exercise-01/  ch-06-ex-01-difference-lists.glp + ex-01-tutorial.md + ex-01-repl-trace.md          (§6.1 ← ch04 §4.3.7 flatten/flatten_acc)
├── exercise-02/  ch-06-ex-02-typed-quicksort.glp + ex-02-tutorial.md + ex-02-repl-trace.md            (§6.2 ← ch05 §5.6)
├── exercise-03/  ch-06-ex-03-equators-emergency-brake.glp + ex-03-tutorial.md + ex-03-repl-trace.md   (§6.3 ← ch04 §4.4.4 control MI)
├── exercise-04/  ch-06-ex-04-bidirectional-communication.glp + ex-04-tutorial.md + ex-04-repl-trace.md (§6.4 ← ch03 §3.2 channel ops)
└── exercise-05/  ch-06-ex-05-buffered-communication.glp + ex-05-tutorial.md + ex-05-repl-trace.md     (§6.5 ← ch04 §4.2.12+§4.2.13 bb)

# REPL build artifact (transient, not committed)
glp_runtime/glp_repl.exe
```

**Structure Decision**: Constitution Option C — Tutorial chapter under charter. Cites Constitution Principle VI, charter §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments — one per clause), design-principles 1–2 (section-driven). No multi-actor / Flutter scope. Cross-chapter relationships (synthesis-from-earlier-chapters) documented per spec FR-014 as header cross-references + signpost prose + top-level footnote; the ch06 clauses are byte-exact from ch01–ch05 PDF, with declarations introduced fresh at §6.x.

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
