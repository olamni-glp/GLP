# Implementation Plan: Olamni Tutorial — Chapter 5 (Types and Modes)

**Branch**: `006-tutorial-ch05` | **Date**: 2026-05-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/006-tutorial-ch05/spec.md` with **12 resolved Clarifications** (Q1 grouping locked = Option A 8 → **AMENDED post-Q7 to 7 exercises** because §5.3 cannot stand alone; Q2 helper-stub deferral **RETRACTED per Q7** — no fabricated helpers; Q3 status-block format = per-exercise **7 lines post-Q7**; Q4 §5.4 type is `List` and §5.5 arg 2 is `Number?` per byte-exact PDF re-read; Q5 **RETRACTED 2026-05-01** — body text byte-exact PDF as printed; Q6 §5.5 counter has full guard+body; Q7 grouping amendment + helper retraction; Q8 minimal coverage stubs for §5.5 with documented Q-amendment provenance; Q9 sustainable process improvement; Q10 §5.6 dual amendment — qsort declaration corrected per prose+clauses + interleaved layout; Q11 empirical verification log against REPL build `bcd59392`; Q12 internal-consistency cleanup binding post-Q7 numbering).

## Summary

Build the chapter-5 tutorial under `olamni/tutorial/ch05/`: **seven** runnable+load-only+negative exercises that cover the entire ch05 of *The Art of Grassroots Logic Programming* (Shapiro, 2025) — Types and Modes. Compact content chapter (~10 substantial PDF code blocks across §5.1 + §5.2 + §5.3 + §5.4 + §5.5 + §5.6 + §5.7), grouped per Clarifications Q1+Q7 by sub-section family.

**Three group-boundary approval gates** govern progression (Foundations→Mode-checking-flow, Mode-checking-flow→Flagship, Flagship→Negatives); within a group exercises proceed without intermediate pairwise gates (inheriting ch04's group-gate pattern, NOT ch01–ch03 pairwise). Status block in `ch05_tutorial.md` uses the per-exercise 7-line format per Q3 (post-Q7 renumbering).

**Three exercise kinds operate under post-Q7 numbering:** ex-01 + ex-02 are **load-only** (§5.1 + §5.2 type definitions only — non-runnable PDF content; the LOAD itself IS the demonstration; **no fabricated helpers** per Q7 retraction; 1-phase trace); ex-03 + ex-04 + ex-05 are **full-program** (§5.3+§5.4 worked merge merged per Q7 / §5.5 counter response-slot with Q8 minimal coverage stubs / §5.6 typed quicksort with Q10 dual amendment; 5-phase trace = load + primary + 3 inspection goals); ex-06 + ex-07 are **negative** (§5.7.1 type-error + §5.7.2 mode-error; failing-form `.glp` MUST FAIL TO LOAD with documented error per Q11 empirical capture; two-`.glp` failing+corrected pattern; 2–3-phase trace).

**ch05 is the first chapter where the type-checker stage of the REPL pipeline does meaningful work** on tutorial code. Per FR-018 + R-006, a pre-flight type-checker operational verification (positive case loads + negative case rejected) MUST pass before any Foundations exercise begins; if broken, ch05 work halts per FR-013. Empirical R-006 verification was captured 2026-04-30 (research.md Appendix A) — re-verified against current REPL build at /speckit-implement T001.

Per Clarifications Q11 (empirical verification log on REPL build `bcd59392`, 2026-05-01): all eight test cases (T1–T7) confirm spec decisions are sound; full byte-equality holds for both negative-exercise error messages (no per-run-varying segments observed; R-011 relaxation NOT triggered); §5.6 typed quicksort requires both Q10 amendments (corrected qsort signature `(NumList?, NumList, NumList?)` AND interleaved layout — stacked layout fails to parse).

**Cross-chapter relationships (NOT cross-chapter imports):** ex-03 typed `merge/3` cross-references ch04 ex-04's untyped `merge/3` (same name, different signature, different clause set); ex-04 typed `counter/2` cross-references ch04 ex-06's untyped `counter/1`+`counter_loop/2` (different arity, different shape). The clauses in ch05 are byte-exact from §5.4/§5.5 PDF, NOT byte-identical to ch04's clauses.

Technical approach: pure documentation + GLP-source feature. Volume: ~25 files for the entire chapter (7 exercise dirs × {1–2 `.glp` + 1 tutorial.md + 1 trace.md} + 1 signpost + 1 input prompt already exists + 1 sources index already exists + 1 deprecated spec copy already exists + this spec.md and downstream artifacts).

## Technical Context

**Language/Version**: Dart `^3.9.4` (REPL build; this Windows host has 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`); GLP (~10 substantial Programs byte-exact from PDF book pp 47–52, distributed across 7 exercise dirs and 9 `.glp` files including the two-file pattern for ex-06 + ex-07); Markdown.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency. `programs/self.glp` (root prelude — provides built-in types `Number`/`Atom`/`Any`, `Stream(X)`/`List`/`NumList`-style parametric machinery, `:=` arithmetic kernel, `number/1` guard). NO new third-party deps.
**Storage**: On-disk Markdown + 9 `.glp` source files (7 single-form + 2 corrected-form for negative two-file pattern). No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` before/after implementation. Captured REPL traces ARE the regression artifacts. Per FR-016, ch05 files NOT in `test/run_all_tests.sh`.
**Target Platform**: Windows host for development; learner artifacts platform-agnostic.
**Project Type**: Tutorial chapter under charter (Constitution Option C).
**Performance Goals**: Learner completes the entire chapter in <60 minutes (per SC-001; smaller than ch04's 90 because content volume is smaller). REPL build <30 s. Each primary demo goal completes in <1 s. Type-checker rejects negative-exercise failing forms in <1 s. Quicksort flagship (ex-05) on 8-element list completes well within default `:limit`.
**Constraints**:
- 7 locked exercise distributions per Q1+Q7 — no shape-restructuring during /speckit-plan.
- Locked primary goal bindings empirically verified during /speckit-implement; mismatch is halt-and-amend per FR-013.
- Strict trace byte-equality per FR-014; per Q11 empirical T3+T6, no per-run-variation observed for either negative exercise; R-011 relaxation NOT triggered for current REPL build.
- Self-containment per FR-010 (each exercise's `.glp` standalone-loadable; `NumList` reused inline in ex-05 — no shared types.glp helper file).
- Group-boundary approval gates per FR-008 + FR-009.
- Cross-chapter relationships per FR-002 + SC-007 documented as header cross-references + signpost prose, NOT code imports.
- **No fabricated helpers per Q7 retraction of Q2/R-012**; non-runnable book content yields 1-phase load-only exercises.
- **Type-checker live-pipeline requirement** — pre-flight R-006 verification per FR-018 + SC-012 BEFORE any Foundations work; ch05 work halts per FR-013 against a broken type-checker.
- **Q10 §5.6 dual amendment** locked: qsort declaration `(NumList?, NumList, NumList?)` + interleaved declarations-with-clauses layout; both required to load (Q11 T4a/T4b/T4c/T4d empirical confirmation).
- **Q8 minimal coverage stubs** locked for §5.5 counter exhaustiveness; explicitly labeled `%% Q8 minimal coverage stub` to distinguish from retracted-helper framing.
- Plan-then-act per FR-013.
- No fabrication per FR-012 + SC-011.
- Body kernel `:=` permitted ONLY in byte-exact PDF clauses that use it (specifically: ex-07 §5.7.2 corrected `bar(X, Y?) :- Y := X? + 1.`); `now/1`, `'_output'/1` MUST NOT appear (SC-015).
**Scale/Scope**: 7 exercises (4 sub-section groups, 3 group-boundary gates); ~10 byte-exact Programs; ~20–30 `%%` paraphrase comments total across all `.glp` files (R-001 estimate revised down post-Q7 retraction of helper layer; was ~35–45 pre-Q7).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec produced via `/speckit-specify` then refined through 12 Clarifications (3 from initial /speckit-clarify session 2026-04-30 + Q4–Q12 added during /speckit-plan, /speckit-implement, and post-implement empirical verification). This plan cites all 12. Q7 + Q10 + Q11 + Q12 represent the canonical anti-fabrication / byte-exact PDF / empirical-verification posture: when implementation hit reality, the spec was amended (audit-trail-preserving) rather than the implementation freelanced.
- **II. No Workarounds**: **PASS**. Halt-and-report posture documented at every failure mode in quickstart §"On failure". Q7's retraction of Q2/R-012 fabricated helpers is the canonical anti-workaround amendment: helpers were eliminated in favour of 1-phase load-only exercises rather than worked-around to make the type-checker accept them. Q10's §5.6 dual amendment treats the book-internal qsort-typo + stacked-layout-incompatibility as a halt-and-amend with documented provenance, NOT a silent correction.
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. All ~10 Programs are SRSW-compliant by byte-exact construction. Q5 retraction confirmed empirically that the §5.4 PDF body already has `?` on Ys/Xs as printed; no body amendment needed. Q8 minimal coverage stubs satisfy SRSW + type-check at REPL load (verifiable at /speckit-implement T071-equivalent).
- **IV. FCP Reference Architecture**: **N/A**. Documentation feature only; no runtime/compiler/type-checker code changes.
- **V. Test-First Discipline**: **PASS** with caveats. Baseline expected per ch04 ship state (485/485 plus any drift). Captured traces ARE regression artifacts per FR-016 (chapter files explicitly NOT in `run_all_tests.sh`). R-006 type-checker pre-flight verification is itself a baseline-establishing test for ch05's type-system content.
- **VI. Tutorial Charter Compliance**: **PASS**. Charter §1 (REPL-only for chs 1–6) + §1.5 (`%%` paraphrase comments — one per clause) + design-principles 1–2 (section-driven) cited. Cross-chapter relationships (typed↔untyped) documented per R-008 canonical block; distinct from ch04's cross-chapter-inversion identity contract.
- **Language Design Authority**: **N/A**. No new guards, system predicates, body kernels, directives, or type-system features introduced. The type system + `procedure` declaration + mode marks + `:=` arithmetic + `number/1` guard all PRE-EXIST. ch05 is the first chapter where the type-checker stage produces non-trivial output; the stage itself is untouched.
- **Technology Stack**: **PASS**. All artifacts within Constitution-authorised stack (Dart 3.9.4+, GLP, Markdown).

**Result**: All applicable principles PASS or N/A. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 + Phase 1: all 8 principles still PASS or N/A. R-001 through R-012 in research.md trace back to spec FRs and Clarifications Q1–Q12. Phase 1 contracts (trace-file, status-block, glp-file) extend ch01/ch02/ch03/ch04's contracts with three NEW additions: (a) trace-file's negative 2–3-phase structure for ex-06 + ex-07; (b) glp-file's two-`.glp` pattern for ex-06 + ex-07 + Q8-stub `%% --- Q8 MINIMAL COVERAGE STUBS ---` marker for ex-04 + Q10 amendment header for ex-05; (c) status-block contract amended to per-exercise 7-line post-Q7 grep contract. The pre-Q7 R-001 helper-layer marker `%% --- DEMONSTRATION HELPERS ---` is RETRACTED per Q7; no helper marker appears in any ch05 `.glp`.

**Post-design verdict**: no new violations. Plan complete; proceeds to /speckit-tasks.

## Project Structure

### Documentation (this feature)

```text
specs/006-tutorial-ch05/
├── spec.md                            # /speckit-specify + /speckit-clarify (Q1–Q12) output (existing)
├── plan.md                            # this file (/speckit-plan output)
├── research.md                        # Phase 0 output (R-001..R-012); post-Q7 cleanup applied during /speckit-analyze
├── data-model.md                      # Phase 1 output; post-Q7 cleanup applied during /speckit-analyze
├── quickstart.md                      # Phase 1 output; post-Q7 cleanup applied during /speckit-analyze
├── contracts/                         # Phase 1 output
│   ├── trace-file-format.md           # 5-phase positive / 1-phase load-only / 2–3-phase negative
│   ├── status-block-format.md         # per-exercise 7-line post-Q7 grep contract
│   └── glp-file-format.md             # 7 file specs + 2 extras for negative two-.glp pattern
├── checklists/requirements.md         # /speckit-specify output (existing)
├── QUARANTINE-DO-NOT-USE/             # existing — untouched per FR-012
└── tasks.md                           # Phase 2 (/speckit-tasks output); regenerated post-Q7+Q12
```

### Source Code (repository root)

**Constitution Option C: Tutorial chapter under charter.**

```text
olamni/tutorial/charter.md             # cited per Principle VI (existing)
olamni/tutorial/tutorial.md            # incremental top-level signpost (UPDATE ch05 row)
olamni/tutorial/ch05/
├── ch05-sources.md                    # PDF code-block index (existing)
├── ch05-specification-input-prompt.md # rev-eng prompt (EXISTING)
├── ch05_tutorial.md                   # chapter signpost with 7-line status block (NEW)
├── spec-rev-eng-input/ch05-DEPRECATED-spec.md  # rev-eng input copy (existing — untouched)
├── exercise-01/  ch-05-ex-01-type-definitions.glp + ex-01-tutorial.md + ex-01-repl-trace.md          (Foundations; load-only — §5.1)
├── exercise-02/  ch-05-ex-02-built-in-types.glp + ex-02-tutorial.md + ex-02-repl-trace.md            (Foundations; load-only — §5.2)
├── exercise-03/  ch-05-ex-03-mode-checked-merge.glp + ex-03-tutorial.md + ex-03-repl-trace.md        (Mode-checking-flow; full-program — §5.3+§5.4 merged per Q7; cross-chapter ↔ ch04 ex-04 untyped merge)
├── exercise-04/  ch-05-ex-04-counter-response-slot.glp + ex-04-tutorial.md + ex-04-repl-trace.md     (Mode-checking-flow; full-program — §5.5; with Q8 coverage stubs; cross-chapter ↔ ch04 ex-06 untyped counter)
├── exercise-05/  ch-05-ex-05-typed-quicksort.glp + ex-05-tutorial.md + ex-05-repl-trace.md           (Flagship; full-program — §5.6; with Q10 dual amendment)
├── exercise-06/  ch-05-ex-06-type-error-failing.glp + ch-05-ex-06-type-error-corrected.glp + ex-06-tutorial.md + ex-06-repl-trace.md     (Negatives; negative two-.glp — §5.7.1)
└── exercise-07/  ch-05-ex-07-mode-error-failing.glp + ch-05-ex-07-mode-error-corrected.glp + ex-07-tutorial.md + ex-07-repl-trace.md     (Negatives; negative two-.glp — §5.7.2)

# REPL build artifact (transient, not committed)
glp_runtime/glp_repl.exe
```

**Structure Decision**: Constitution Option C — Tutorial chapter under charter. Cites Constitution Principle VI, charter §1 (REPL-only for chs 1–6), §1.5 (`%%` paraphrase comments — one per clause), design-principles 1–2 (section-driven). No multi-actor / Flutter scope. Cross-chapter relationships (typed↔untyped) documented per spec FR-002 as header cross-references + signpost prose; the ch05 clauses are byte-exact from §5.4/§5.5 PDF, NOT byte-identical to ch04 — distinct from ch04's cross-chapter-inversion identity contract.

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
