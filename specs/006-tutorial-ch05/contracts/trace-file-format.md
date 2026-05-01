# Contract — `ex-NN-repl-trace.md` Structural Format (chapter 5)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-30

This contract defines the structural format of `ex-NN-repl-trace.md` files for chapter 5. It inherits the ch01–ch04 trace contracts. ALL POSITIVE ch05 traces use STRICT byte-equality (per FR-014); chapter 5 introduces no wallclock-derived output, so ch02's elapsed-ms relaxation does NOT apply to positive exercises. NEGATIVE ch05 traces (ex-07, ex-08) use byte-equality MODULO any per-run-varying segments authorised at /speckit-implement T026/T037-equivalent per R-011.

---

## Common structure (all 8 traces)

Every `ex-NN-repl-trace.md` for `NN ∈ 01..08` MUST contain, in order:

1. **Title** — `# Exercise NN — REPL trace` (or similar; learner-facing).
2. **Preface** — 1–3 sentences (learner-targeted) stating what the trace demonstrates. OUTSIDE any code block. For NEGATIVE exercises, the preface MUST explicitly note that the load failure is the demonstrated outcome (NOT a tutorial bug) per FR-005.
3. **Phase blocks** — one fenced ```glp code block per phase. Code-block CONTENT is byte-verbatim from the actual REPL session (stdin lines + stdout responses + REPL prompt prefix `GLP>` where applicable).
4. **Per-phase annotations** — 1–2 brief lines OUTSIDE each code block, before or after the block, explaining what to expect, what it means, and why it matters.
5. **Postscript** — 1–3 sentences (learner-targeted) summarising what the trace proves and why it matters for the chapter's learning goal. OUTSIDE any code block.

---

## Phase count per exercise (ch05 has THREE shapes per Q7 amendment)

### Load-only exercises (ex-01, ex-02): 1-phase trace

- Phase A — Load: ex-NN file. The trace ends here. No goals to run; the load itself IS the demonstration that the type-checker accepts the byte-exact PDF code. The trace's preface MUST explicitly note the load-only nature (per FR-017 + Q7).

### Runnable exercises (ex-03, ex-04, ex-05): 5-phase trace

- Phase A — Load: ex-NN file
- Phase B — Primary demo goal
- Phase C — Inspection goal 1
- Phase D — Inspection goal 2
- Phase E — Inspection goal 3

For ex-04 (cross-chapter relationship to ch04 untyped merge), Phase A loads the `.glp` containing the §5.4 worked typed `merge/3` example. The cross-chapter relationship is documented in the `.glp` header AND the trace's preface, NOT through a separate phase.

For ex-06 (Flagship), the four goals collectively exercise all 6 clauses + 3 procedure declarations of typed quicksort per FR-017 + SC-010.

### Type-only / Procedure-decl-only exercises (ex-01, ex-02, ex-03): 5-phase trace with adjusted Phase B semantics

- Phase A — Load: ex-NN file (the load is the primary demo per FR-017)
- Phase B — Primary demo confirmation: an inspection-style goal exercising the FIRST helper unit-clause / stub clause (acts as the "primary" since the load itself isn't a runnable goal)
- Phase C — Inspection goal 2 (different helper or type-test goal)
- Phase D — Inspection goal 3 (different helper or type-failure probe per R-012)
- Phase E — Closing remarks (optional; or a 4th inspection goal if needed for coverage)

The trace's preface for type-only / procedure-decl-only exercises MUST explicitly note that the load itself is the primary demonstration; the helpers exercise the type or mode shape via small unit-clause / stub-body queries.

### Negative exercises (ex-07, ex-08): 2-phase or 3-phase trace

- Phase A — Failing-form load attempt: load `ch-05-ex-NN-<error-kind>-failing.glp`. Capture the type-error or mode-error message verbatim. Annotation: `→ load failed (expected)`.
- Phase B — Corrected-form load: load `ch-05-ex-NN-<error-kind>-corrected.glp`. Capture `✓ Loaded:` + zero errors. Annotation: `→ load succeeded (the fix)`.
- Phase C *(optional)* — Success-confirmation goal: if the corrected form has a runnable goal demonstrating the fix actually works (e.g., for ex-08's corrected `bar(X, Y?) :- Y := X? + 1.` running `bar(5, R).` ⇒ `R = 6`), include this phase. Decision per-exercise during /speckit-implement T006-equivalent.

---

## Per-exercise phase content (proposed; locked per-exercise during /speckit-implement T006-equivalent)

The specific primary + inspection goals + locked bindings + helper shapes per exercise are NOT pre-locked here (per research R-004 + R-012; locking 24+ bindings would overspecify). The implementer proposes per-exercise during /speckit-implement with project-owner approval. The proposal MUST satisfy:

1. Primary goal exercises the exercise's main Program(s) end-to-end (or, for type-only / proc-decl-only, the load itself is "primary").
2. The 4-goal session (or 2-3 phases for negatives) collectively exercises every clause of every Program in the exercise's `.glp` per FR-017.
3. Each goal has a deterministic locked binding (no per-run variation expected for positive exercises; chapter 5 has no wallclock-derived output).
4. For negatives, the captured error message has byte-equal full content modulo per-run-varying segments authorised at T026/T037-equivalent per R-011.
5. For type-only / proc-decl-only, helpers satisfy R-012 discipline.

Some illustrative primary / first-inspection goals (as guidance for the implementer; NOT locked here):

| Exercise | Kind | Illustrative primary OR first-inspection goal | Approximate binding |
|---|---|---|---|
| ex-01 | type-only | `bit_test(0).` (Phase B) + `bit_test(1).` (Phase C) + `nat_test(s(s(0))).` (Phase D) | each succeeds |
| ex-02 | type-only | `list_test([1, two, 3.0]).` (Phase B) + `any_test(1).` (Phase C) + `any_test(two).` (Phase D) | each succeeds |
| ex-03 | proc-decl-only | `merge([], [a, b], M).` (Phase B exercising stub) + `merge([1], [2], M).` (Phase C) + alternate-clause exercise (Phase D) | each succeeds with stub binding |
| ex-04 | full-program | `merge([1, 3], [2, 4], M).` | `M = [1, 2, 3, 4]` (or one fair-merge interleaving) |
| ex-05 | full-program | counter response-slot exercise (per /speckit-plan T006) | a `show(State?)` produces a state value |
| ex-06 | full-program | `quicksort([3,1,4,1,5,9,2,6], S).` | `S = [1,1,2,3,4,5,6,9]` |
| ex-07 | negative | failing-form load | type-error message captured verbatim |
| ex-08 | negative | failing-form load + `bar(5, R).` on corrected (Phase C) | mode-error capture + `R = 6` |

---

## Byte-equality contract

Per spec FR-014:

**Positive exercises (ex-01 through ex-06)**: STRICT byte-equality.
- Byte-equal modulo REPL banner / build wallclock lines / session-start lines
- No per-run-variation exception applies (no `now/1` / `'_output'/1` in any ch05 Program; no wallclock-derived output)
- Auditor reproducibility check: re-run the same goal sequence on the same `.glp` file via the same REPL build → trace content byte-equal modulo banner

**Negative exercises (ex-07, ex-08)**: byte-equality with R-011 per-run-varying-segment relaxation.
- Phase A failing-load output: byte-equal modulo any memory-address / tuple-id / wallclock-derived segment authorised at T026-equivalent
- Phase B corrected-load output: STRICT byte-equality (load-success path has no per-run-varying content)
- Phase C optional success-confirmation goal output: STRICT byte-equality
- If R-011 relaxation triggered, the trace's annotation explicitly notes which segments are subject to per-run variation

---

## Annotation rules

1. Annotations MUST be brief (1–2 lines per phase). Long discussion belongs in `ex-NN-tutorial.md`.
2. Annotations MUST be OUTSIDE the fenced code blocks. The block content is byte-verbatim from the REPL; annotations are commentary.
3. Annotations MUST NOT modify or paraphrase the code-block content. They explain what the learner is seeing.
4. For multi-Program exercises (ex-04, ex-05, ex-06), annotations identify which Program's clause was selected by each goal — this is the primary mechanism for the learner to understand which Program is being exercised.
5. ex-04's Phase A annotation MUST acknowledge the cross-chapter relationship per R-008: "This typed `merge/3` is the §5.4 worked-example pedagogical center for mode checking; a related un-typed `merge/3` from §4.2.5 (book p 32) appeared in ch04 ex-04 — see `olamni/tutorial/ch04/exercise-04/ch-04-ex-04-merge-variants.glp`. Same procedure name; different signature, different mode declaration, different clause set; this is a CROSS-CHAPTER RELATIONSHIP, not a code import."
6. ex-05's Phase A annotation MUST analogously acknowledge the cross-chapter relationship to ch04 ex-06's untyped `counter/1`.
7. **Negative-exercise annotations** MUST explicitly state at Phase A: `→ load failed (expected per spec; NOT a tutorial bug)`. The trace preface ALSO carries this disclosure.
8. **Type-only / proc-decl-only annotations** at Phase A note that the load is the primary outcome AND that the type definitions / procedure declarations are now registered with the type system.

---

## Capture mechanism

Per workflow memory + ch01/ch02/ch03/ch04 precedent, traces are captured via the kernel-snapshot batch-mode pattern:

```bash
DART="/c/Users/gavri/dart-sdk/bin/dart"
printf "<.glp-path>\n<goal1>.\n<goal2>.\n…\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

For NEGATIVE exercises, the capture is two separate REPL sessions (or one combined session with both loads + `:quit`):

```bash
# Failing-form session
printf "<failing-.glp-path>\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
# Corrected-form session
printf "<corrected-.glp-path>\n<optional-success-goal>.\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

The implementer captures stdout verbatim into the corresponding fenced code blocks. Any post-capture editing MUST be limited to:
- Adding the title, preface, postscript, and per-phase annotations OUTSIDE the code blocks.
- Splitting a single batch-capture into per-phase code blocks.
- Removing the REPL banner / build wallclock / session-start lines that are wallclock-derived.
- For negative exercises with R-011-authorised relaxation: substituting `<address>` / `<tuple-id>` placeholders for per-run-varying segments and annotating the substitution in the trace's metadata.

The implementer MUST NOT:
- Hand-construct REPL output.
- "Clean up" REPL output to match an expected shape.
- Synthesise a binding the REPL didn't produce.
- Apply any per-run-variation relaxation NOT explicitly authorised at /speckit-implement T026/T037-equivalent (positive exercises have no relaxation; negative exercises have R-011 relaxation only when triggered by observed per-run-varying segments).
