# Phase 0 Research — Olamni Tutorial Chapter 4

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)
**Date**: 2026-04-30

This document resolves the plan-level items deferred during `/speckit-clarify`. Three Clarifications were already resolved in `spec.md` (Q1: 10-exercise grouping locked; Q2: parser-limitations verified stale + content retired; Q3: status-block format = per-exercise 10 lines). The remaining decisions live here.

---

## R-001 — `%%` paraphrase comment density across the 10 `.glp` files

**Decision**: Inherit the ch01–ch03 R-001 pattern. Each `.glp` file:
- Header block (3–8 lines) summarising what the file does + citing PDF source(s) + Formal-box references where relevant
- Per-Program sub-header (1–2 lines) for each Program inside a multi-Program exercise
- One inline `%%` paraphrase comment per clause

Estimated comment counts per exercise:

| Exercise | Programs | Clauses (approx) | %% comments |
|---|---|---|---|
| ex-01 | 4.1.1, 4.1.2, 4.1.3 (logic gates) | 1 + 2 + 14 = 17 | 17 |
| ex-02 | 4.1.4 nand + 4.1.5 half_adder + 4.1.6 full_adder | 1 + 1 + 1 = 3 | 3 |
| ex-03 | 4.2.1 producer + 4.2.2 consumer + 4.2.3 naive reverse + 4.2.4 acc reverse | 2 + 2 + 2 + 1 + 2 = 9 | 9 |
| ex-04 | 4.2.5 merge + 4.2.6 dmerge + 4.2.7 merge_tree | 4 + 7 + 1 + 2 + 3 = 17 | 17 |
| ex-05 | 4.2.8 distribute + 4.2.9 distribute_indexed + 4.2.10 observer + 4.2.11 ripple-carry adder | 2 + 3 + 2 + 2 = 9 | 9 |
| ex-06 | 4.2.12 bb + 4.2.13 bb_test + 4.2.14 counter + 4.2.15 accumulator | varies; ~12 | 12 |
| ex-07 | 4.3.1–4.3.6 (Peano, integer arith, factorial, fact_acc, fib, fib_linear) | varies; ~18 | 18 |
| ex-08 | 4.3.7–4.3.12 (flatten, tree_sum, sort, mergesort, distribute_ng, substitute) | varies; ~20 | 20 |
| ex-09 | 4.4.1 reduce + 4.4.2 trust-mode run/2 | 3 + 4 = 7 | 7 |
| ex-10 | 4.4.3 fail-safe + 4.4.4 control + 4.4.5 tracing | 5 + 7 + 9 = 21 | 21 |

**Total: ~133 `%%` comments** across the 10 exercise files (revised up from the spec's ~60–80 estimate after counting clauses against `ch04-sources.md`). The implementer budgets time accordingly.

**Rationale**: Charter §1.5 mandates per-clause paraphrase; one short line per clause matches; multi-Program exercises (most of ch04) have higher clause counts than ch01–ch03's single-Program exercises but the same per-clause discipline applies.

**Alternatives considered**:
- *Skip header comment block* — violates ch01–ch03 precedent; rejected.
- *Skip `%%` per clause for sub-Program helpers* — violates charter §1.5; rejected.
- *Combine multiple short clauses' comments into one* — invents new comment-density rule; rejected.

---

## R-002 — REPL build-artifact location

**Decision**: Inherit ch01–ch03's R-002 verbatim. Build to `glp_runtime/glp_repl.exe`. Reuse if fresh; rebuild if `glp_runtime/bin/glp_repl.dart` newer than the binary. If `claude/fix-misleading-build-line` (commit `a913b3e7`) is merged before ch04 implementation begins, use `--define=GLP_BUILD_COMMIT=...`; otherwise build without (banner shows `Built from: unknown`).

**Baseline test count expected**: 485/485 (per ch03 ship state; `claude/fix-misleading-build-line` still unmerged as of session start).

**Rationale**: Established convention; binary is gitignored; no new design needed.

---

## R-003 — Top-level `olamni/tutorial/tutorial.md` update strategy

**Decision**: Inherit ch01/ch02/ch03 pattern. Flip ch04 row from `planned` → `pending review (YYYY-MM-DD)` after first exercise lands → `implemented YYYY-MM-DD` after all 10 are approved (post §4.4 group approval). Chapters 5–13 stay marked `planned`.

**Rationale**: Per spec FR-006 — incremental update.

---

## R-004 — Inspection-goal selection for all 10 exercises

**Decision**: Each exercise has THREE inspection goals chosen during /speckit-implement T006/T007-equivalent with project-owner approval per exercise. Per FR-017, the four-goal session (primary + 3 inspection) MUST collectively exercise every clause of every Program in the exercise's `.glp`.

The detailed goal lists per exercise are NOT pre-locked here (10 exercises × 4 goals = 40 goals; locking all in the spec would be overspecification). Instead, the implementing session proposes per-exercise goal sets at /speckit-implement T006 with project-owner approval recorded per-exercise in the implementation transcript. The proposal must satisfy:

1. **Primary goal**: exercises the exercise's main Program(s) end-to-end with a deterministic locked binding.
2. **Inspection goals**: each exercises a different clause / sub-Program / edge case (empty input, one-element, deepest descent, no-match, etc.) NOT covered by the primary.
3. **Coverage check**: across all 4 goals, every clause of every Program in the exercise's `.glp` is exercised.
4. **Determinism**: each goal has a deterministic locked binding; no per-run-variation expected (chapter 4 has no wallclock-derived output).
5. **No parser-limitation workarounds needed** per Q2 (both alleged limitations stale).

For multi-Program exercises with 12+ clauses (ex-04, ex-07, ex-08, ex-10), the 4-goal budget may not span every clause; in that case the implementer either (a) adds a small number of additional goals as "supplementary inspection" with explicit annotation in the trace, OR (b) selects goals that exercise the most-pedagogical clauses with explicit acknowledgment that some clauses are exercised only via recursive sub-calls of other goals. Decision recorded in implementation transcript.

**Rationale**:
- Three goals per exercise is the ch01–ch03 standard; ch04 inherits.
- Locking 40 specific goals in the spec creates massive churn risk (any goal-shape revision requires Clarifications amendment); deferring to plan/implement is appropriate.
- Coverage check (every clause exercised) is testable post-hoc against the captured trace.

**Alternatives considered**:
- *Lock all 40 goals in the spec* — overspecification; high churn risk; rejected.
- *Skip inspection goals for multi-Program exercises* — violates ch01–ch03 precedent + FR-017 every-clause coverage; rejected.

---

## R-005 — Verify Dart SDK on this Windows host

**Status**: To be verified before any REPL build attempt. Per workflow memory + ch01/ch02/ch03 precedent: Dart 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`. First action of implementation is `"$DART" --version` confirming `^3.9.4`. If absent or older, halt and report.

---

## R-006 — PDF re-read scope

**Decision**: Re-read the entire ch04 (book pp 25–43, PDF pp 37–55) byte-exactly during /speckit-implement. ~38 substantial code blocks across 4 sub-sections; per the ch01 lesson (PDF transcription drift in `ch01-sources.md`), byte-exact verification against the PDF is non-negotiable. The implementer plans implementation time accordingly.

For each exercise, re-read the relevant sub-section's prose paragraphs (for `%%` paraphrase comments) AND the byte-exact code blocks (for the `.glp` clause corpus). Formal 4.1 (p 29), Formal 4.2 (p 31), and Formal 4.3 (pp 35–36) are referenced in `%%` paraphrase comments where relevant but NOT encoded as code.

**OUT OF SCOPE for re-read**: §4.5 (if any), end-of-chapter exercises (none explicit per the deprecated spec), chapter 5+ content.

**Rationale**: Per ch01–ch03 precedent. The volume is large but the discipline is unchanged.

---

## R-007 — Cross-chapter inversion provenance

**Decision**: ex-03's `ch-04-ex-03-producer-consumer-reverse.glp` MUST contain `producer/2` + `consumer/3` clauses byte-identical to ch03's `ch-03-ex-01-producer-consumer.glp` (per spec FR-002 + SC-007). Header comment block paraphrases the `§4.2.1` + `§4.2.2` "Producers and Consumers" subsection's prose + Formal 4.2 (SRSW in Continuation Calls) — distinct from ch03's cross-chapter-import-provenance header.

**Canonical ex-03 inversion-acknowledgment block** (header):

```
%% This file presents producer/2 + consumer/3 in their NATIVE chapter-4 home,
%% byte-exact from book pp 31 (PDF p 43), §4.2.1 + §4.2.2 "Producers and Consumers".
%% These same procedures appear in ch03 ex-01 as a cross-chapter forward import
%% (see olamni/tutorial/ch03/exercise-01/ch-03-ex-01-producer-consumer.glp); the
%% byte-exact code corpus is identical, but the surrounding `%%` paraphrase context
%% differs: ch03's header cites the cross-chapter import provenance, this file's
%% header paraphrases the §4.2.1 + §4.2.2 native prose.
```

**Verifiability**: per SC-007, `diff` between the two files (modulo header + `%%` annotations) returns zero clause-text differences. Implementer runs this check during /speckit-implement.

**Rationale**: spec FR-002 + Clarifications Q1 + ch03 R-007 precedent. The byte-exact identity is a contract; the surrounding prose context is exercise-specific.

---

## R-008 — Per-exercise filename mapping

**Decision**: Locked filenames per Clarifications Q1 spec FR-001 suggested-labels:

| # | Filename |
|---|---|
| ex-01 | `ch-04-ex-01-constants-and-gates.glp` |
| ex-02 | `ch-04-ex-02-compound-circuits.glp` |
| ex-03 | `ch-04-ex-03-producer-consumer-reverse.glp` |
| ex-04 | `ch-04-ex-04-merge-variants.glp` |
| ex-05 | `ch-04-ex-05-stream-operators.glp` |
| ex-06 | `ch-04-ex-06-buffered-and-monitors.glp` |
| ex-07 | `ch-04-ex-07-recursive-numerics.glp` |
| ex-08 | `ch-04-ex-08-recursive-list-tree.glp` |
| ex-09 | `ch-04-ex-09-metaprogramming-foundations.glp` |
| ex-10 | `ch-04-ex-10-advanced-meta-interpreters.glp` |

All single `.glp` per exercise (no compose-pair needed for any ch04 exercise based on Q1's locked Programs distribution; the pedagogy is "all of one sub-section" rather than "contrast pair").

**Rationale**: Filename matches its exercise's theme; consistent hyphenation; no exercise needs the two-`.glp` pattern that ch02 ex-01 + ch03 ex-01 used.

---

## R-009 — Within-group execution order + group-boundary gate enforcement

**Decision**: Within each sub-section group, exercises proceed sequentially in order:
- §4.1 group: ex-01 → ex-02 (sequential within group)
- §4.2 group: ex-03 → ex-04 → ex-05 → ex-06 (sequential within group)
- §4.3 group: ex-07 → ex-08 (sequential within group)
- §4.4 group: ex-09 → ex-10 (sequential within group)

Group-boundary gates per FR-008: BEFORE starting any §4.2 exercise, ALL §4.1 exercises (ex-01 + ex-02) MUST be approved (status block lines `^- exercise-(01|02): approved` both present). BEFORE starting any §4.3 exercise, ALL §4.2 exercises (ex-03 through ex-06) MUST be approved. BEFORE starting any §4.4 exercise, ALL §4.3 exercises (ex-07 + ex-08) MUST be approved.

Within a group, each exercise's `.glp` write + REPL trace + tutorial happens sequentially per the plan-then-act discipline (FR-013), but the implementer does NOT pause for project-owner approval between in-group exercises — only at the group boundary. Concretely:
- Implementer writes ex-01 + verifies + writes trace + writes tutorial. STOP for the project-owner review of the §4.1 group only after ex-02 is also done. Approval flips both ex-01 + ex-02 lines together.
- Similarly for ex-03 + ex-04 + ex-05 + ex-06 (§4.2 group), ex-07 + ex-08 (§4.3), ex-09 + ex-10 (§4.4).

This is the NEW pattern for ch04 — distinct from ch01–ch03's pairwise gate model.

**Rationale**: Per Clarifications Q3 (per-exercise status block) + FR-009 (within-group exercises don't gate each other). The per-exercise status block carries 10 lines, which all flip approved at the group's approval moment (4 group-boundary flips total for the chapter).

---

## Summary of Phase 0

Nine items resolved (R-001 through R-009). All decisions traceable to spec FRs and Clarifications Q1+Q2+Q3. No `NEEDS CLARIFICATION` markers remain. R-001/R-002/R-003 inherit ch01–ch03 patterns adjusted for ch04's volume; R-004 defers per-exercise inspection goals to /speckit-implement (40-goal lock would overspecify); R-005/R-006 are supporting verifications; R-007 documents the cross-chapter inversion contract; R-008 locks filenames; R-009 specifies within-group sequencing + gate-boundary semantics. Phase 0 complete; proceed to Phase 1.
