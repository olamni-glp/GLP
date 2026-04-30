# Contract — `ex-NN-repl-trace.md` Structural Format (chapter 3)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-30

This contract defines the structural format of `ex-NN-repl-trace.md` files for chapter 3. It inherits the ch01 + ch02 trace contracts and adds chapter-3-specific extensions for ex-01 (two-file load + composed-pipeline goal). All three ch03 traces use STRICT byte-equality (per FR-014); chapter 3 introduces no wallclock-derived output, so ch02's elapsed-ms relaxation does NOT apply here.

---

## Common structure (all three traces)

Every `ex-NN-repl-trace.md` MUST contain, in order:

1. **Title** — `# Exercise NN — REPL trace` (or similar; learner-facing).
2. **Preface** — 1–3 sentences (learner-targeted) stating what the trace demonstrates. OUTSIDE any code block.
3. **Phase blocks** — one fenced ```glp code block per phase. Code-block CONTENT is byte-verbatim from the actual REPL session (stdin lines + stdout responses + REPL prompt prefix `GLP>` where applicable).
4. **Per-phase annotations** — 1–2 brief lines OUTSIDE each code block, before or after the block, explaining what to expect, what it means, and why it matters.
5. **Postscript** — 1–3 sentences (learner-targeted) summarising what the trace proves and why it matters for the chapter's learning goal. OUTSIDE any code block.

---

## Phases per exercise

### ex-01 (Program 3.1 + producer/consumer composed pipeline)

**Six fenced code blocks** in this order (two `.glp` files load separately + composed primary goal + three inspection goals):

1. **Phase A — Load: Program 3.1 fair stream merger**. Stdin: `olamni/tutorial/ch03/exercise-01/ch-03-ex-01-glp-fair-stream-merger.glp`. Stdout: `✓ Loaded: …` success message.
2. **Phase B — Load: producer/consumer pair**. Stdin: `olamni/tutorial/ch03/exercise-01/ch-03-ex-01-producer-consumer.glp`. Stdout: `✓ Loaded: …` success message. Both procedures (`merge/3` from Phase A and `producer/2` + `consumer/3` from this load) coexist without procedure-redeclaration conflict.
3. **Phase C — Composed primary goal**. Stdin: `producer(A, 5), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` Stdout: `Sum = 21\n→ succeeds`.
4. **Phase D — Inspection goal 1**. Stdin: `producer(A, 0), producer(B, 0), merge(A?, B?, M), consumer(M?, 0, Sum).` Stdout: `Sum = 0\n→ succeeds`.
5. **Phase E — Inspection goal 2**. Stdin: `producer(A, 0), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` Stdout: `Sum = 6\n→ succeeds`.
6. **Phase F — Inspection goal 3**. Stdin: `producer(A, 1), producer(B, 1), merge(A?, B?, M), consumer(M?, 0, Sum).` Stdout: `Sum = 2\n→ succeeds`.

The Phase A → Phase B → Phase C sequence demonstrates the composed pipeline: load the chapter anchor (Program 3.1), load the cross-chapter import (producer + consumer), exercise both source files in one composed goal. Annotation between Phase B and Phase C explicitly tells the learner: "the goal references procedures from BOTH `.glp` files; the SRSW reader/writer pairing connects them across four roles (two producers + one merger + one consumer)."

### ex-02 (`channel/1` + `process/2` defined-guard demo)

**Five fenced code blocks** in this order:

1. **Phase A — Load: ex-02 file**. Stdin: `olamni/tutorial/ch03/exercise-02/ch-03-ex-02-defined-guards.glp`. Stdout: `✓ Loaded: …`.
2. **Phase B — Primary goal**. Stdin: `process(ch(a, b), Status).` Stdout: `Status = ok\n→ succeeds`.
3. **Phase C — Inspection goal 1**. Stdin: `process(foo, Status).` Stdout: `Status = error\n→ succeeds`.
4. **Phase D — Inspection goal 2**. Stdin: `process(ch([], []), Status).` Stdout: `Status = ok\n→ succeeds`.
5. **Phase E — Inspection goal 3**. Stdin: `process([1,2,3], Status).` Stdout: `Status = error\n→ succeeds`.

Annotation on Phase B MUST point out that the `channel/1` defined guard succeeded at `process/2` clause 1's guard site, selecting the `ok` branch. Annotation on Phase C MUST point out that `channel/1` failed (because `foo` is not a `ch(_, _)` term), so the `otherwise` fallback in clause 2 fired, binding `Status = error`. Phase D's annotation covers the empty-channel variant (still satisfies `channel/1`); Phase E's covers the list-fall-through.

### ex-03 (`lookup/3` complete with both clauses, guard negation demo)

**Five fenced code blocks** in this order:

1. **Phase A — Load: ex-03 file**. Stdin: `olamni/tutorial/ch03/exercise-03/ch-03-ex-03-guard-negation.glp`. Stdout: `✓ Loaded: …`.
2. **Phase B — Primary goal**. Stdin: `lookup(b, [(a,1),(b,2),(c,3)], V).` Stdout: `V = 2\n→ succeeds`.
3. **Phase C — Inspection goal 1**. Stdin: `lookup(a, [(a,1),(b,2),(c,3)], V).` Stdout: `V = 1\n→ succeeds`.
4. **Phase D — Inspection goal 2**. Stdin: `lookup(c, [(a,1),(b,2),(c,3)], V).` Stdout: `V = 3\n→ succeeds`.
5. **Phase E — Inspection goal 3**. Stdin: `lookup(z, [(a,1),(b,2),(c,3)], V).` Stdout: `→ fails`. The input list is fully ground; recursion descends to `lookup(z, [], V)` which is also ground; neither clause head matches; procedure deterministically fails. If the runtime produces `→ suspended` instead, that indicates a runtime anomaly and the implementer halts-and-reports per Principle II rather than capturing the suspension as a valid outcome.

Annotation on Phase B MUST explain the two-clause sequence: clause 2 fires first (negated `~(b =?= a)` succeeds, recursion descends past `(a,1)`), then clause 1 fires on the residue (positive `b =?= b` succeeds, binds V to 2). Annotation on Phase C MUST point out clause 1 fires immediately (positive branch only). Annotation on Phase E MUST refer to the §3.2 SRSW Rules for Defined Guards table on book p 24 to remind the learner that `=?=` is negatable but defined guards are not.

---

## Byte-equality contract

Per spec FR-014, ALL THREE traces use STRICT byte-equality:

| Trace file | Strict byte-equality required (modulo timestamps) | Relaxation |
|---|---|---|
| `ex-01-repl-trace.md` | YES, in all six phases | None |
| `ex-02-repl-trace.md` | YES, in all five phases | None |
| `ex-03-repl-trace.md` | YES, in all five phases | None |

**"Modulo timestamps"** means the auditor's reproducibility check ignores: the REPL banner (e.g., `GLP REPL v…`), the build wallclock line (e.g., `Built at 2026-…`), and any session-start line that is wallclock-derived. All other code-block content is compared line-for-line.

Chapter 3 has NO wallclock-derived output (no `now/1`, no `'_output'/1` per FR-015 + SC-015 — those kernels are explicitly out of scope for ch03). Therefore the ch02 FR-014 elapsed-ms relaxation does NOT apply to any ch03 trace; every trace is strict byte-equality everywhere.

---

## Annotation rules

1. Annotations MUST be brief (1–2 lines per phase). Long discussion belongs in `ex-NN-tutorial.md`.
2. Annotations MUST be OUTSIDE the fenced code blocks. The block content is byte-verbatim from the REPL; annotations are commentary.
3. Annotations MUST NOT modify or paraphrase the code-block content. They explain what the learner is seeing.
4. ex-01 Phase B → Phase C transition annotation MUST explicitly explain the cross-chapter composition: "the composed primary goal references procedures from BOTH loaded `.glp` files; SRSW pairing connects four roles (producer A, producer B, merger, consumer)".
5. ex-02 Phase B / Phase C annotations MUST explicitly identify which `process/2` clause was selected and why (the defined-guard `channel(X?)` succeeded for B, the `otherwise` fallback fired for C).
6. ex-03 Phase B annotation MUST identify the clause sequence (clause 2 fires first to descend, then clause 1 to match). Phase E's annotation MUST reference the §3.2 SRSW Rules for Defined Guards table on book p 24.

---

## Capture mechanism

Per workflow memory, traces are captured via the kernel-snapshot batch-mode pattern:

```bash
DART="/c/Users/gavri/dart-sdk/bin/dart"
printf "<file-path>\n<goal1>.\n<goal2>.\n…\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

For ex-01 specifically, BOTH `.glp` files MUST be loaded in the same REPL session (the composed primary goal references procedures from both):

```bash
printf "olamni/tutorial/ch03/exercise-01/ch-03-ex-01-glp-fair-stream-merger.glp\nolamni/tutorial/ch03/exercise-01/ch-03-ex-01-producer-consumer.glp\nproducer(A, 5), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).\n…\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill > /tmp/ex01-trace.txt 2>&1
```

The implementer captures stdout verbatim into the corresponding fenced code blocks. Any post-capture editing MUST be limited to:
- Adding the title, preface, postscript, and per-phase annotations OUTSIDE the code blocks.
- Splitting a single batch-capture into per-phase code blocks (each phase's block content is the relevant slice of the batch output).
- Removing the REPL banner / build wallclock / session-start lines that are wallclock-derived.

The implementer MUST NOT:
- Hand-construct REPL output.
- "Clean up" REPL output to match an expected shape.
- Synthesise a binding the REPL didn't produce.
- Apply any per-run-variation relaxation (none is permitted in chapter 3 — no wallclock content exists to vary).
