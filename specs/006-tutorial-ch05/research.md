# Phase 0 Research — Olamni Tutorial Chapter 5

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)
**Date**: 2026-04-30

This document resolves the plan-level items deferred during `/speckit-clarify`. Three Clarifications were already resolved in `spec.md` (Q1: 8-exercise grouping locked = Option A; Q2: helper-stub shapes deferred to /speckit-plan T006-equivalent with permitted-shape sketch; Q3: status-block format = per-exercise 8 lines). The remaining decisions live here.

---

## R-001 — `%%` paraphrase comment density across the 8 `.glp` files

**Decision**: Inherit the ch01–ch04 R-001 pattern. Each `.glp` file:
- Header block (3–8 lines) summarising what the file does + citing PDF source(s) + Formal-box references where relevant
- Per-Program sub-header (1–2 lines) for each Program inside a multi-Program exercise
- One inline `%%` paraphrase comment per clause (including helper unit-clauses for ex-01/ex-02/ex-03 + the corrected forms for ex-07/ex-08)

Estimated comment counts per exercise (PDF clause counts + helper allowance):

| Exercise | Programs | PDF clauses | Helper clauses | Total %% |
|---|---|---|---|---|
| ex-01 | §5.1 `Bit`/`Nat`/`NumList` (3 type defs) | 3 type-def lines (each treated as one declaration with one `%%`) | ~3–6 helper unit clauses (Q2) | ~6–9 |
| ex-02 | §5.2 `List`/`Any` | 1 type-def + ~prose | ~3–6 helper unit clauses (Q2) | ~4–7 |
| ex-03 | §5.3 `procedure merge(List?, List?, List).` | 1 procedure decl | 1–2 stub body clauses (Q2) | ~2–3 |
| ex-04 | §5.4 worked typed merge | 1 type def + 1 procedure decl + 3 clauses + walk-through annotations | 0 (full Program) | 5 + walk-through |
| ex-05 | §5.5 counter response-slot | 2 type defs + 1 procedure decl + 1 clause | 0 (full Program) | 4 |
| ex-06 | §5.6 typed quicksort | 1 type def + 3 procedure decls + 6 clauses | 0 (full Program) | 10 |
| ex-07 | §5.7.1 `foo/1` failing form + corrected form (two-.glp) | ~1–2 clauses each file | 0 | ~2–4 |
| ex-08 | §5.7.2 `bar/2` failing form + corrected form (two-.glp) | 1 clause failing + 1 clause `bar(X, Y?) :- Y := X? + 1.` corrected | 0 | ~2–3 |

**Total: ~35–45 `%%` comments** across the 8 exercise files (revised up from the spec's ~20–30 estimate after counting clauses + helpers + walk-through annotations against `ch05-sources.md`). The §5.4 worked-example exercise (ex-04) carries `%%` annotations that additionally walk through the head/body mode-check steps from §5.4 prose IN ADDITION to the per-clause paraphrase per FR-017 + SC-017.

**Rationale**: Charter §1.5 mandates per-clause paraphrase; one short line per clause matches; type-only / procedure-decl-only exercises with helper unit-clauses get `%%` per helper. The §5.4 walk-through annotations are additive, not replacement, per spec.

**Alternatives considered**:
- *Skip header comment block* — violates ch01–ch04 precedent; rejected.
- *Skip `%%` per helper unit-clause* — helpers are part of the file's content; charter §1.5 applies to every clause; rejected.
- *Combine walk-through into single block-comment* — violates per-clause discipline; rejected.

---

## R-002 — REPL build-artifact location

**Decision**: Inherit ch01–ch04's R-002 verbatim. Build to `glp_runtime/glp_repl.exe`. Reuse if fresh; rebuild if `glp_runtime/bin/glp_repl.dart` newer than the binary. If `claude/fix-misleading-build-line` (tag `v2026.04.29-3`) is merged before ch05 implementation begins, use `--define=GLP_BUILD_COMMIT=...`; otherwise build without (banner shows `Built from: unknown`).

**Baseline test count expected**: per ch04 ship state. Verified at /speckit-implement T001-equivalent.

**Rationale**: Established convention; binary is gitignored; no new design needed.

---

## R-003 — Top-level `olamni/tutorial/tutorial.md` update strategy

**Decision**: Inherit ch01/ch02/ch03/ch04 pattern. Flip ch05 row from `planned` → `pending review (YYYY-MM-DD)` after first exercise lands → `implemented YYYY-MM-DD` after all 8 are approved (post Negatives group approval). Chapters 6–13 stay marked `planned`.

**Rationale**: Per spec FR-006 — incremental update.

---

## R-004 — Inspection-goal selection for all 8 exercises

**Decision**: Each positive exercise (ex-01 through ex-06) has THREE inspection goals chosen during /speckit-implement T006/T007-equivalent with project-owner approval per exercise. Per FR-017, the four-goal session (primary + 3 inspection) MUST collectively exercise every clause of every Program in the exercise's `.glp` (or, for type-only / procedure-decl-only exercises, every helper unit-clause / stub body clause).

For type-only exercises (ex-01, ex-02): the "primary demo goal" is the load itself (the file loads with type-check passing). The three inspection goals exercise the locked helper unit-clauses.

For the procedure-decl-only exercise (ex-03): the primary is also the load itself; inspection goals exercise the stub body's mode shape.

For NEGATIVE exercises (ex-07, ex-08): the trace structure has 2–3 phases (load-attempt-of-failing-form + optional load-of-corrected-form + optional one-success-goal-on-corrected). NO inspection goals beyond the load attempts; there is no successful binding to inspect on the failing form.

The detailed goal lists per positive exercise are NOT pre-locked here. The implementing session proposes per-exercise goal sets at /speckit-implement T006 with project-owner approval recorded per-exercise. The proposal must satisfy:

1. **Primary goal**: exercises the exercise's main Program(s) end-to-end with a deterministic locked binding (or, for type-only/proc-decl-only, the load itself).
2. **Inspection goals**: each exercises a different clause / sub-Program / edge case NOT covered by the primary.
3. **Coverage check**: across all 4 goals (or, for negatives, across the 2–3 phases), every clause / helper / stub of every Program in the exercise's `.glp` is exercised.
4. **Determinism**: each goal has a deterministic locked binding; no per-run-variation expected for positive exercises (chapter 5 has no wallclock-derived output). For negative exercises, error-message byte-equality holds modulo per-run-varying segments authorised at /speckit-implement T026/T037-equivalent.
5. **Type-checker awareness**: each goal MUST satisfy SRSW + type-check at REPL load. For ex-01/ex-02/ex-03 (helper-bearing) the helper bodies' type-correctness is verified at /speckit-plan T006-equivalent before file write.

**Rationale**:
- Three goals per positive exercise is the ch01–ch04 standard; ch05 inherits.
- Negative exercises legitimately have fewer phases (no successful binding to inspect).
- Locking specific goals + helper shapes in the spec creates churn risk (any goal-shape revision requires Clarifications amendment per Q5/Q7/Q9 ch04 precedent); deferring to plan/implement is appropriate.

**Alternatives considered**:
- *Lock all goals + helper shapes in the spec* — overspecification; high churn risk per ch04 Q5/Q7/Q9 precedent; rejected.
- *Skip inspection goals for type-only exercises* — violates FR-017; rejected.

---

## R-005 — Verify Dart SDK on this Windows host

**Status**: To be verified before any REPL build attempt. Per workflow memory + ch01/ch02/ch03/ch04 precedent: Dart 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`. First action of implementation is `"$DART" --version` confirming `^3.9.4`. If absent or older, halt and report.

---

## R-006 — Type-checker operational status verification

**Decision**: Per spec FR-018, the implementer MUST verify at /speckit-implement T001-equivalent that the type-checker stage of the REPL pipeline is operational on a known-good positive type-definition AND correctly REJECTS a known-bad type-error case before proceeding to ex-07 + ex-08 (the negative exercises).

**Concrete verification protocol**:
1. Build / reuse fresh REPL binary per R-002.
2. Construct a 2-line test file (do NOT forward-reference ex-07; ex-07 is implemented in Phase 6, AFTER this verification):
   - Positive case: A minimal byte-exact ch05 type def — recommend `Bit ::= 0 ; 1.` (which is also the first declaration in ex-01). Write to a scratch file (e.g., `/tmp/r006-positive.glp` or a temp filename). Load. Expect `✓ Loaded:` + zero errors.
   - Negative case: An inline minimal type-error trigger constructed at this task (NOT ex-07's PDF form, which doesn't exist on disk yet). Recommended construction: `procedure foo(Number).` declaration + `foo(a).` clause asserting a non-`Number` atom satisfies `Number`. Write to a scratch file (e.g., `/tmp/r006-negative.glp`). Load. Expect a type-error message documenting the type mismatch.
   - **NOTE**: ex-07's actual PDF form is verified separately at T113 once ex-07 is transcribed; T006a / R-006 only verifies the type-checker's general operational status, not ex-07-specific behaviour.
3. If positive case fails (false-negative): halt per FR-013. ch05 work does not proceed.
4. If negative case succeeds (false-positive): halt per FR-013. ch05 work does not proceed.
5. If both behave correctly: record the captured positive load output + the captured negative error message in `research.md` Appendix A (created at /speckit-implement T001-equivalent).

**Timing**: This verification runs BEFORE the Foundations group's first exercise write — ch05's type-system content is meaningless without a working type-checker. If the type-checker is broken, the entire chapter is blocked.

**Re-verification trigger**: If the REPL build is rebuilt mid-implementation (e.g., after `glp_runtime/lib/` changes or a newer base-branch merge), repeat R-006 before continuing.

**Rationale**: Per spec FR-018 + SC-012. ch05 is the first chapter where the type-checker does meaningful work; assuming it works without verification risks compounding failures across all 8 exercises.

---

## R-007 — PDF re-read scope

**Decision**: Re-read the entire ch05 (book pp 47–52, PDF pp 59–64) byte-exactly during /speckit-implement. ~10 substantial code blocks across 7 sub-sections; per the ch01 lesson (PDF transcription drift in `chXX-sources.md`), byte-exact verification against the PDF is non-negotiable.

For each exercise, re-read the relevant sub-section's prose paragraphs (for `%%` paraphrase comments) AND the byte-exact code blocks (for the `.glp` clause corpus). Formal 5.1 (p 48), Formal 5.2 (p 49), and Formal 5.3 (p 50) are referenced in `%%` paraphrase comments where relevant but NOT encoded as code.

Special attention required for ch05's syntactic novelties:
- `?` reader marks in procedure declarations (single character; must be byte-exact)
- `;` alternation separators in type defs
- `|` list-cons separators in list-typed alternatives
- Whitespace around `;` and `|` (do NOT normalise — match PDF exactly)
- Multi-alternative ordering (do NOT reorder — match PDF exactly)
- Embedded `?` within structures (e.g., `show(Number?)` inside `CounterMsg` definition; consume-mode-inside-produce-mode)

**OUT OF SCOPE for re-read**: §5.8 Summary + Exercises (book exercises out of scope per charter §1), chapter 6+ content.

**Rationale**: Per ch01–ch04 precedent. Volume is small (~10 blocks vs ch04's ~38) but per-character precision matters more than ever because new syntactic forms are introduced.

---

## R-008 — Cross-chapter relationship documentation contract

**Decision**: ex-04's `ch-05-ex-04-mode-checked-merge.glp` and ex-05's `ch-05-ex-05-counter-response-slot.glp` MUST cross-reference their ch04 untyped predecessors in their header comment block, using the canonical provenance line shape established in ch03 R-007.

**Canonical ex-04 cross-reference block** (header) — UPDATED per Q4:

```
%% This file presents the TYPED merge/3 worked example, byte-exact from book p 49,
%% §5.4 "Mode Checking" + Formal 5.2 "Mode Semantics".
%% A related un-typed merge/3 appears in ch04 ex-04 (book §4.2.5, p 32) as an
%% un-typed simple fair merger; see olamni/tutorial/ch04/exercise-04/ch-04-ex-04-merge-variants.glp.
%% The two are pedagogically distinct presentations: same procedure name, the
%% ch05 typed form carries an explicit `procedure merge(List?, List?, List).`
%% declaration with `?` reader marks (using the universal `List ::= [] ; [Any | List].`
%% type from §5.2); the ch04 untyped form has no procedure declaration at all
%% (defaulting to GLP's implicit untyped behaviour). Different clause set (3 typed
%% clauses in ch05 vs 4 untyped in ch04), different pedagogical focus (mode checking
%% flow vs stream-merge implementations). This is a CROSS-CHAPTER RELATIONSHIP — not
%% a code import. The .glp clauses below are byte-exact from §5.4 PDF (with Q5
%% amendment applied to body's `Ys` → `Ys?`/`Ys?` per PDF annotation), NOT copies of
%% ch04's clauses.
```

**Canonical ex-05 cross-reference block** (header): analogous, citing ch04 ex-06 (`§4.2.14 counter/1 + counter_loop/2`) as the un-typed predecessor and noting different arity (1 → 2) and different shape (no response-slot in ch04 vs response-slot in ch05).

**Verifiability**: per SC-007, header grep returns the canonical cross-reference; the .glp clauses themselves are byte-exact PDF (NOT byte-identical to ch04's). The signpost `ch05_tutorial.md` MUST also document the relationships in plain prose per FR-005.

**Rationale**: spec FR-002 + SC-007 + ch03 R-007 precedent. The relationship is a pedagogical bridge for learners arriving from ch04; the byte-exact-from-ch05-PDF discipline avoids the ch04 cross-chapter-inversion identity contract (which required byte-IDENTICAL clauses to ch03's import).

---

## R-009 — Per-exercise filename mapping

**Decision**: Locked filenames per Clarifications Q1 spec FR-001 suggested-labels:

| # | Filename(s) |
|---|---|
| ex-01 | `ch-05-ex-01-type-definitions.glp` |
| ex-02 | `ch-05-ex-02-built-in-types.glp` |
| ex-03 | `ch-05-ex-03-procedure-declaration.glp` |
| ex-04 | `ch-05-ex-04-mode-checked-merge.glp` |
| ex-05 | `ch-05-ex-05-counter-response-slot.glp` |
| ex-06 | `ch-05-ex-06-typed-quicksort.glp` |
| ex-07 | `ch-05-ex-07-type-error-failing.glp` + `ch-05-ex-07-type-error-corrected.glp` (two-.glp pattern) |
| ex-08 | `ch-05-ex-08-mode-error-failing.glp` + `ch-05-ex-08-mode-error-corrected.glp` (two-.glp pattern) |

Single `.glp` per positive exercise (ex-01 through ex-06); two `.glp` per negative exercise (ex-07 + ex-08) per spec FR-001's "up to 2 .glp" allowance and the negative-load-test contract from spec FR-017.

**Rationale**: Filename matches its exercise's theme; consistent hyphenation; negative two-file pattern matches ch02 ex-01 + ch03 ex-01 precedent (failing form + corrected form).

---

## R-010 — Within-group execution order + group-boundary gate enforcement

**Decision**: Within each sub-section group, exercises proceed sequentially in order:
- **Foundations group**: ex-01 → ex-02 → ex-03 (sequential within group)
- **Mode-checking-flow group**: ex-04 → ex-05 (sequential within group)
- **Flagship group**: ex-06 (only one exercise; no within-group order)
- **Negatives group**: ex-07 → ex-08 (sequential within group)

Group-boundary gates per FR-008: BEFORE starting any Mode-checking-flow exercise (ex-04+), ALL Foundations exercises (ex-01 + ex-02 + ex-03) MUST be approved (status block lines `^- exercise-(01|02|03): approved` all 3 present). BEFORE starting the Flagship exercise (ex-06), ALL Mode-checking-flow exercises (ex-04 + ex-05) MUST be approved. BEFORE starting any Negatives exercise (ex-07+), the Flagship exercise (ex-06) MUST be approved.

Within a group, each exercise's `.glp` write + REPL trace + tutorial happens sequentially per the plan-then-act discipline (FR-013), but the implementer does NOT pause for project-owner approval between in-group exercises — only at the group boundary. Concretely:
- Implementer writes ex-01 + verifies + writes trace + writes tutorial. Continues to ex-02 + ex-03 in the same group. STOP for the project-owner review of the Foundations group only after ex-03 is also done. Approval flips ex-01 + ex-02 + ex-03 lines together.
- Similarly for ex-04 + ex-05 (Mode-checking-flow group), ex-06 (Flagship; trivially one-exercise group), ex-07 + ex-08 (Negatives group).

Additional verification at the Foundations→Mode-checking-flow gate: the type-checker R-006 verification is re-confirmed (the REPL build hasn't changed since T001-equivalent, so this is typically a no-op, but explicit for safety).

**Rationale**: Inherited from ch04 R-009. Per Clarifications Q3 (per-exercise status block) + FR-009 (within-group exercises don't gate each other). The per-exercise status block carries 8 lines, which all flip approved at the group's approval moment (4 group-boundary flips total for the chapter — Foundations, Mode-checking-flow, Flagship single-line flip, Negatives).

---

## R-011 — Negative-exercise trace structure + per-run-varying segment handling

**Decision**: Per spec FR-014, FR-017, SC-009, the negative exercises ex-07 + ex-08 have a distinct trace structure from positive exercises:

**Standard negative trace (2-phase)**:
- Phase 1: Attempt to load the failing-form `.glp`. Capture the type-error or mode-error message verbatim. Document `→ load failed (expected)` annotation.
- Phase 2: Attempt to load the corrected-form `.glp`. Capture `✓ Loaded:` + zero errors. Document `→ load succeeded (the fix)` annotation.

**Optional 3rd phase** (negative-with-success-confirmation): IF the corrected form has a runnable goal that confirms the fix actually works (e.g., for ex-08's corrected `bar(X, Y?) :- Y := X? + 1.`, run `bar(5, R).` ⇒ `R = 6`), include a third phase exercising that goal. Decision per-exercise during /speckit-implement T006-equivalent.

**Per-run-varying segment handling**: At /speckit-implement T026/T037-equivalent (when the failing-form load is first attempted), inspect the captured error message for any of:
- Memory address (e.g., `0x7ff8b1234567`)
- Tuple-id / cell-id (e.g., `cell #4321`)
- Wallclock-derived line number ranges (unlikely but possible)
- Random nonce / hash

If ANY such segment is observed:
1. Halt per FR-013.
2. Propose a Clarifications amendment to spec.md adding a per-run-variation relaxation analogous to ch02's FR-014 amendment (e.g., `<address>` placeholder substituted for the per-run-varying segment in the locked trace, with annotation `varies per run; the SHAPE matters, not the specific number`).
3. Project-owner approves the relaxation; the relaxation is recorded in spec Clarifications + this R-011.
4. Resume implementation with the relaxed byte-equality.

If NO such segment is observed: full byte-equality holds for the captured error message; lock it into the trace.

**Rationale**: Per spec FR-014 + Edge Case "Negative-exercise error contains per-run-varying segment". The relaxation mechanism exists precisely for type-checker error messages whose format the implementer cannot predict in advance.

---

## R-012 — Helper unit-clause / stub body design discipline (Q2 deferral)

**Decision**: Per Clarifications Q2, helper unit-clauses for ex-01 + ex-02 and the procedure-decl stub body for ex-03 are designed during /speckit-implement T006-equivalent with project-owner approval per exercise. R-012 documents the design discipline so the implementer can propose shapes consistently.

**Discipline**:

1. **Helpers MUST themselves satisfy SRSW + type-check at REPL load.** A helper unit-clause that violates SRSW or type-check turns ex-01/ex-02/ex-03 into accidental negative exercises.

2. **Helpers MUST exercise the type / mode shape, not invent new logic.** For ex-01's `Bit ::= 0 ; 1.`: a `bit_test/1` family of unit clauses, one per allowed alternative (`bit_test(0).` + `bit_test(1).`), is appropriate. A helper that defines `bit_double/2` doing arithmetic is OFF-THEME and rejected.

3. **Helpers MUST be small.** Target 1–4 unit clauses per type def, 1–2 stub body clauses for the procedure-decl exercise. Not exceeding 6 total clauses across the helper layer of any single exercise.

4. **Helpers carry `%%` paraphrase comments per charter §1.5**, but the comment paraphrases the type/mode-shape concept being demonstrated, not a non-existent book paragraph.

5. **Helpers may include a deliberate type-failure probe** for ex-01/ex-02 (e.g., for `Bit`: the trace's third inspection goal `bit_test(2).` — which is NOT a unit clause but a goal that probes the type-checker's rejection of a non-`Bit` value at goal-submission time). Whether to include such a probe is per-exercise-decided at T006-equivalent. If included: the probe's expected outcome (failure or specific rejection message) is locked at T006 + verified at T026.

6. **Helpers do NOT shadow PDF Programs.** The helper namespace (e.g., `bit_test/1`) must not collide with any procedure name from §5.4 / §5.5 / §5.6 / §5.7 (none in scope; ch05 uses `merge/3`, `counter/2`, `quicksort/2`, `qsort/3`, `partition/4`, `foo/1`, `bar/2`).

7. **Helpers documented in `ex-NN-tutorial.md` as "demonstration helpers, not from the book".** The learner should not confuse a helper with a PDF Program; the tutorial explicitly distinguishes them.

**Concrete proposed shapes** (subject to project-owner approval at T006-equivalent):

- **ex-01 helpers**: `bit_test(0).` + `bit_test(1).` (Bit) + `nat_test(0).` + `nat_test(s(0)).` + `nat_test(s(s(0))).` (Nat) + `numlist_test([]).` + `numlist_test([1]).` + `numlist_test([1, 2, 3]).` (NumList). Total 8 unit clauses. Plus three inspection goals exercise each family (1 per type-def).

- **ex-02 helpers**: `list_test([]).` + `list_test([1]).` + `list_test([1, two, 3.0]).` (List with mixed `Any` content) + `any_test(1).` + `any_test(two).` + `any_test([nested, list]).` (Any discrimination across `Number`/`Atom`/list). Total 6 unit clauses. Plus three inspection goals exercise each.

- **ex-03 stub** (multiple candidate shapes; implementer presents at T031a; SRSW shape preferred):
  - **Candidate A (preferred — SRSW-clean head-pattern shape)**: `merge([], R?, R).` (1-clause: when left input is empty, the output IS the right input — head pattern-matches `L = []` and ties writer position 3 directly to `R`'s reader-of-the-right-input via head unification; no body needed). This shape avoids the M-writer-in-both-head-and-body issue that ch04 Q5 surfaced as SRSW-violating.
  - **Candidate B (analogous to original spec input)**: `merge(L?, R?, M) :- L? = [], M = R?.` (1-clause stub with body unification). **WARNING**: this shape has M as a writer in head and as a writer being assigned in body — analogous to ch04 Q5/Q7/Q9 spec-locked shapes that conflicted with SRSW analyser at load. Likely needs amendment if the analyser flags it.
  - **Candidate C (2-clause if a single clause is judged insufficient)**: extend Candidate A with `merge([H|T], R?, [H|MT]) :- merge(T?, R?, MT).` (recursive non-empty case; head-pattern match on left input).

  The implementer's first attempt at /speckit-implement T031a SHOULD be Candidate A. If Candidate A is rejected at REPL load (unexpected — it's the canonical GLP merge shape; would indicate either a R-012 helper-discipline issue or a real type-checker regression), halt-and-amend per FR-013 and try Candidate B or C.

These concrete shapes are PROPOSALS. The implementer presents them at T006-equivalent and project owner approves OR adjusts. The implementer does NOT write any helper-bearing `.glp` file before T006-equivalent approval per FR-013.

**Rationale**: Per Clarifications Q2 + FR-013 plan-then-act + FR-018 type-checker verification. The discipline guards against accidental helpers that would fail SRSW/type-check at load (turning Foundations exercises into broken builds) or stray off-theme into helper logic that obscures the type/mode pedagogy.

---

## Appendix A — R-006 Type-Checker Verification (captured 2026-04-30)

REPL build: `2362202d Merge pull request #2 from olamni-glp/005-tutorial-ch04` (banner shows Build line; not unknown). Baseline tests: 485/485 PASS (one transient flake on first run; clean on second).

### A.1 Positive case (load succeeds)

Input file `positive.glp`:
```glp
% R-006 positive test: minimal type definition
Bit ::= 0 ; 1.
```

Captured REPL output (relevant lines):
```
GLP> ✓ Loaded: C:/Users/gavri/AppData/Local/Temp/r006/positive.glp
GLP> Goodbye!
```

→ Type-checker accepts the byte-exact §5.1.1 type def. ✓

### A.2 Negative case (load fails with type error)

Input file `negative.glp`:
```glp
% R-006 negative test: type-error trigger
procedure foo(Number).
foo(a).
```

Captured REPL output (relevant lines):
```
GLP> Error loading C:/Users/gavri/AppData/Local/Temp/r006/negative.glp: Exception: Type checking failed:
  Head of foo is not well-typed:
  Inconsistent path: Number type requires numeric literal
  Path: (a, 0, output) at line 3
GLP> Goodbye!
```

→ Type-checker correctly REJECTS a non-`Number` value claimed for a `Number`-declared procedure argument. ✓

### A.3 Conclusions

- R-006 PASSED — type-checker stage of REPL pipeline is operational.
- Error message format observed: `Type checking failed: Head of <proc> is not well-typed: Inconsistent path: <type> type requires <constraint>; Path: (<value>, <pos>, output) at line <N>`. Structurally stable (no memory address, no tuple-id, no wallclock). R-011 per-run-varying relaxation unlikely to be needed for ex-07; full byte-equality should hold.
- ex-05 path resolution lesson: `/tmp/` paths do NOT resolve under this Windows REPL build; use Windows-style path `C:/Users/gavri/AppData/Local/Temp/...` or absolute Windows path `C:\\Users\\...`.

ch05 work proceeds.

---

## Summary of Phase 0

Twelve items resolved (R-001 through R-012). All decisions traceable to spec FRs and Clarifications Q1+Q2+Q3 + the four pre-resolved decisions (negative-exercise split, group-gate model from ch04, type-checker live-pipeline, parser-limitations stale). No `NEEDS CLARIFICATION` markers remain.

R-001 inherits ch01–ch04 paraphrase pattern adjusted for ch05's helper-bearing exercises. R-002 / R-003 inherit verbatim. R-004 defers per-exercise inspection goals to /speckit-implement (overspecification risk). R-005 verifies Dart. R-006 introduces the type-checker operational verification (NEW for ch05). R-007 PDF re-read scope. R-008 cross-chapter relationship contract (NEW shape for ch05; distinct from ch04's cross-chapter-inversion identity contract). R-009 locks filenames including the two-.glp pattern for ex-07 + ex-08. R-010 within-group sequencing + 3-gate boundary semantics. R-011 negative-exercise trace structure + per-run-varying segment handling (NEW for ch05). R-012 helper unit-clause / stub body design discipline (NEW for ch05; deferred per Q2 with concrete proposed shapes documented).

Phase 0 complete; proceed to Phase 1.
