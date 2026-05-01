# Contract — `ex-NN-repl-trace.md` Structural Format (chapter 5, post-Q7+Q12)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-05-01 (Q7+Q11+Q12 binding form)

This contract defines the structural format of `ex-NN-repl-trace.md` files for chapter 5 (post-Q7+Q12). Inherits the ch01–ch04 trace contracts. ALL POSITIVE ch05 traces use STRICT byte-equality (per FR-014); chapter 5 introduces no wallclock-derived output, so ch02's elapsed-ms relaxation does NOT apply. NEGATIVE ch05 traces use byte-equality with R-011 per-run-varying-segment relaxation procedure available — but per Q11 empirical T3+T6 on REPL build `bcd59392` (2026-05-01), no per-run-varying segments observed, so **R-011 relaxation is NOT triggered** for current REPL build; full byte-equality holds for both negative-exercise error messages.

---

## Common structure (all 7 traces post-Q7+Q12)

Every `ex-NN-repl-trace.md` for `NN ∈ 01..07` (post-Q7+Q12) MUST contain, in order:

1. **Title** — `# Exercise NN — REPL trace` (or similar; learner-facing).
2. **Preface** — 1–3 sentences (learner-targeted) stating what the trace demonstrates. OUTSIDE any code block. For NEGATIVE exercises (ex-06, ex-07 post-Q7+Q12), the preface MUST explicitly note that the load failure is the demonstrated outcome (NOT a tutorial bug) per FR-005. For LOAD-ONLY exercises (ex-01, ex-02 post-Q7), the preface MUST explicitly note that the load itself is the demonstration (no goals to run; non-runnable PDF content per Q7 retraction).
3. **Phase blocks** — one fenced ```glp code block per phase. Code-block CONTENT is byte-verbatim from the actual REPL session (stdin lines + stdout responses + REPL prompt prefix `GLP>` where applicable).
4. **Per-phase annotations** — 1–2 brief lines OUTSIDE each code block, before or after the block, explaining what to expect, what it means, and why it matters.
5. **Postscript** — 1–3 sentences (learner-targeted) summarising what the trace proves and why it matters for the chapter's learning goal. OUTSIDE any code block.

---

## Phase count per exercise (ch05 has THREE shapes per Q7+Q12 binding)

### Load-only exercises (ex-01, ex-02 post-Q7+Q12): 1-phase trace

- **Phase A — Load**: ex-NN file. The trace ends here. **NO goals to run** per Q7 retraction; the load itself IS the demonstration that the type-checker accepts the byte-exact PDF code.

The trace's preface MUST explicitly note the load-only nature (per FR-017 + Q7). **No fabricated helpers per Q7** — Phase A is the entire trace; there are no Phase B/C/D/E.

### Full-program exercises (ex-03, ex-04, ex-05 post-Q7+Q12): 5-phase trace

- Phase A — Load: ex-NN file
- Phase B — Primary demo goal
- Phase C — Inspection goal 1
- Phase D — Inspection goal 2
- Phase E — Inspection goal 3

For ex-03 (§5.3+§5.4 merged per Q7; cross-chapter relationship to ch04 ex-04 untyped merge), Phase A loads the `.glp` containing the §5.3 procedure declaration + §5.4 worked typed `merge/3` example. The cross-chapter relationship is documented in the `.glp` header AND the trace's preface, NOT through a separate phase.

For ex-04 (§5.5 counter response-slot; cross-chapter relationship to ch04 ex-06 untyped counter; with Q8 minimal coverage stubs), Phase A loads the `.glp` with the response-slot clause + Q8 stubs for `[]`/`clear`/`up`/`down` exhaustiveness. Inspection goals MAY exercise the Q8 stubs (e.g., a `clear` message forwarded by the Q8 stub) to demonstrate stub behaviour.

For ex-05 (§5.6 typed quicksort flagship; with Q10 dual amendment), the four goals collectively exercise all 6 clauses + 3 procedure declarations of typed quicksort per FR-017 + SC-010. Q10 amendments (corrected qsort signature + interleaved layout) are documented in the `.glp` header.

### Negative exercises (ex-06, ex-07 post-Q7+Q12): 2-phase or 3-phase trace

- **Phase A** — Failing-form load attempt: load `ch-05-ex-NN-<error-kind>-failing.glp`. Capture the type-error or mode-error message verbatim. Annotation: `→ load failed (expected per spec; NOT a tutorial bug)`.
- **Phase B** — Corrected-form load: load `ch-05-ex-NN-<error-kind>-corrected.glp`. Capture `✓ Loaded:` + zero errors. Annotation: `→ load succeeded (the fix)`.
- **Phase C** *(optional)* — Success-confirmation goal: if the corrected form has a runnable goal demonstrating the fix actually works (e.g., for ex-07's corrected `bar(X, Y?) :- Y := X? + 1.` running `bar(5, R).` ⇒ `R = 6` per Q11 T7), include this phase. Decision per-exercise during /speckit-implement T117/T125-equivalent.

**Per Q11 empirical T3+T6 (2026-05-01, REPL build `bcd59392`):**

- ex-06 §5.7.1 type-error message is a 3-line message: `Inconsistent path: Number type requires numeric literal Path: ([|]/2, 0, output) → (a, 1, output)` (and analogous for b, c) at line 5. **No per-run-varying segments** — full byte-equality.
- ex-07 §5.7.2 mode-error message is a 2-line message: `Variable mode mismatch: writer requires ↑ (produce), got ↓ (consume) Path: (X, 0, input)` + `reader requires ↓ (consume), got ↑ (produce) Path: (Y?, 0, output)` at line 3. **No per-run-varying segments** — full byte-equality.

R-011 per-run-varying-segment relaxation is NOT triggered for current REPL build. If a future REPL build introduces per-run-varying segments at T113/T122 capture, halt-and-amend per R-011 procedure.

---

## Per-exercise phase content (proposed; locked per-exercise during /speckit-implement T-NN-PROPOSE)

The specific primary + inspection goals + locked bindings per exercise are NOT pre-locked here (per research R-004; locking 9+ bindings would overspecify). The implementer proposes per-exercise during /speckit-implement with project-owner approval. The proposal MUST satisfy:

1. Primary goal exercises the exercise's main Program(s) end-to-end (or, for load-only, the load itself is "primary" and there are no inspection goals).
2. The 4-goal session (or 1 phase for load-only, 2-3 phases for negatives) collectively exercises every clause of every Program in the exercise's `.glp` per FR-017.
3. Each goal has a deterministic locked binding (no per-run variation expected for positive exercises; chapter 5 has no wallclock-derived output).
4. For negatives, the captured error message has byte-equal full content per Q11 empirical (no per-run-varying segments observed for current REPL build); if a future build introduces them, R-011 relaxation procedure applies.
5. Load-only exercises (ex-01, ex-02 post-Q7) have NO inspection goals per Q7 retraction.

Some illustrative primary / first-inspection goals (as guidance for the implementer; NOT locked here):

| Exercise (post-Q7) | Kind | Illustrative primary OR first-inspection goal | Approximate binding |
|---|---|---|---|
| ex-01 | load-only | (no goals — load is the only phase) | `✓ Loaded:` + zero errors |
| ex-02 | load-only | (no goals — load is the only phase) | `✓ Loaded:` + zero errors |
| ex-03 | full-program | `merge([1, 3], [2, 4], M).` | `M = [1, 2, 3, 4]` (or one fair-merge interleaving) |
| ex-04 | full-program | counter response-slot exercise (per /speckit-implement T073) | a `show(State?)` produces a state value |
| ex-05 | full-program | `quicksort([3,1,4,1,5,9,2,6], S).` | `S = [1,1,2,3,4,5,6,9]` |
| ex-06 | negative | failing-form load → 3-line type-error per Q11 T3 | type-error message captured verbatim |
| ex-07 | negative | failing-form load → 2-line mode-error per Q11 T6 + `bar(5, R).` on corrected (Phase C) | mode-error capture + `R = 6` per Q11 T7 |

---

## Byte-equality contract

Per spec FR-014:

**Positive + load-only exercises (ex-01, ex-02, ex-03, ex-04, ex-05 post-Q7+Q12)**: STRICT byte-equality.
- Byte-equal modulo REPL banner / build wallclock lines / session-start lines
- No per-run-variation exception applies (no `now/1` / `'_output'/1` in any ch05 Program; no wallclock-derived output)
- Auditor reproducibility check: re-run the same goal sequence on the same `.glp` file via the same REPL build → trace content byte-equal modulo banner

**Negative exercises (ex-06, ex-07 post-Q7+Q12)**: STRICT byte-equality per Q11 empirical (current REPL build `bcd59392`).
- Phase A failing-load output: byte-equal to Q11 T3 (ex-06) / Q11 T6 (ex-07) captured 3-line / 2-line error messages
- Phase B corrected-load output: STRICT byte-equality (load-success path has no per-run-varying content)
- Phase C optional success-confirmation goal output: STRICT byte-equality (e.g., ex-07's `bar(5, R).` ⇒ `R = 6` per Q11 T7)
- R-011 relaxation NOT triggered for current build. If a future build introduces per-run-varying segments, the trace's annotation explicitly notes which segments are subject to per-run variation per R-011 amendment procedure.

---

## Annotation rules

1. Annotations MUST be brief (1–2 lines per phase). Long discussion belongs in `ex-NN-tutorial.md`.
2. Annotations MUST be OUTSIDE the fenced code blocks. The block content is byte-verbatim from the REPL; annotations are commentary.
3. Annotations MUST NOT modify or paraphrase the code-block content. They explain what the learner is seeing.
4. For multi-Program exercises (ex-03, ex-04, ex-05 post-Q7+Q12), annotations identify which Program's clause was selected by each goal — this is the primary mechanism for the learner to understand which Program is being exercised.
5. **ex-03's Phase A annotation** (post-Q7+Q12 — formerly ex-04 pre-Q7) MUST acknowledge the cross-chapter relationship per R-008: "This typed `merge/3` is the §5.4 worked-example pedagogical center for mode checking; a related un-typed `merge/3` from §4.2.5 (book p 32) appeared in ch04 ex-04 — see `olamni/tutorial/ch04/exercise-04/ch-04-ex-04-merge-variants.glp`. Same procedure name; different signature, different mode declaration, different clause set; this is a CROSS-CHAPTER RELATIONSHIP, not a code import."
6. **ex-04's Phase A annotation** (post-Q7+Q12 — formerly ex-05 pre-Q7) MUST analogously acknowledge the cross-chapter relationship to ch04 ex-06's untyped `counter/1` + `counter_loop/2`. Different arity (1→2), different shape.
7. **ex-05's Phase A annotation** (post-Q7+Q12 — formerly ex-06 pre-Q7) MUST acknowledge the Q10 dual amendment: "This typed quicksort uses (a) a corrected qsort declaration `(NumList?, NumList, NumList?)` per Q10 Issue A — the printed PDF declaration `(NumList?, NumList?, NumList)` contradicts the book's own prose and clauses; and (b) interleaved declarations-with-clauses layout per Q10 Issue B — the PDF's stacked layout fails to parse. Clause text is byte-exact PDF; only the LAYOUT and the qsort signature are amended."
8. **Negative-exercise annotations** (ex-06, ex-07 post-Q7+Q12) MUST explicitly state at Phase A: `→ load failed (expected per spec; NOT a tutorial bug)`. The trace preface ALSO carries this disclosure.
9. **Load-only annotations** (ex-01, ex-02 post-Q7+Q12) at Phase A note that the load is the entire trace AND that the type definitions are now registered with the type system. **No fabricated helpers** per Q7 retraction.

---

## Capture mechanism

Per workflow memory + ch01/ch02/ch03/ch04 precedent, traces are captured via the kernel-snapshot batch-mode pattern:

```bash
DART="/c/Users/gavri/dart-sdk/bin/dart"
printf "<.glp-path>\n<goal1>.\n<goal2>.\n…\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

For LOAD-ONLY exercises (ex-01, ex-02 post-Q7+Q12):

```bash
printf "<.glp-path>\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

For NEGATIVE exercises (ex-06, ex-07 post-Q7+Q12), the capture is two separate REPL sessions (or one combined session with both loads + `:quit`):

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
- For negative exercises with R-011-authorised relaxation (NOT triggered for current REPL build per Q11): substituting `<address>` / `<tuple-id>` placeholders for per-run-varying segments and annotating the substitution in the trace's metadata.

The implementer MUST NOT:
- Hand-construct REPL output.
- "Clean up" REPL output to match an expected shape.
- Synthesise a binding the REPL didn't produce.
- Apply any per-run-variation relaxation NOT explicitly authorised at /speckit-implement T113/T122 (positive + load-only have no relaxation; negative exercises currently have no triggered relaxation per Q11 empirical; future REPL builds may trigger R-011 procedure).
- **Add fabricated helpers** per Q7 retraction (load-only exercises ex-01+ex-02 contain ONLY byte-exact PDF text).
