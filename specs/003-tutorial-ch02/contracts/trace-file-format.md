# Contract — `ex-NN-repl-trace.md` Structural Format (chapter 2)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-28

This contract defines the structural format of `ex-NN-repl-trace.md` files for chapter 2. It inherits the ch01 trace contract verbatim and adds a chapter-2-specific extension for ex-01 (two-file load attempt) and ex-03 (elapsed-ms relaxation per FR-014).

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

### ex-01 (LP/GLP append contrast)

**Six fenced code blocks** in this order:

1. **Phase A — Load attempt: LP-only file**. Stdin: `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-classical-append-LP-only.glp`. Stdout: `Error loading: …` SRSW-violation message captured verbatim.
2. **Phase B — Load: GLP file**. Stdin: `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-glp-append.glp`. Stdout: `✓ Loaded: …` success message.
3. **Phase C — Primary goal**. Stdin: `append([1,2,3], [a,b,c], Zs).` Stdout: `Zs = [1, 2, 3, a, b, c]\n→ succeeds`.
4. **Phase D — Inspection goal 1**. Stdin: `append([], [a,b,c], Zs).` Stdout: `Zs = [a, b, c]\n→ succeeds`.
5. **Phase E — Inspection goal 2**. Stdin: `append([1,2,3], [], Zs).` Stdout: `Zs = [1, 2, 3]\n→ succeeds`.
6. **Phase F — Inspection goal 3**. Stdin: `append([], [], Zs).` Stdout: `Zs = []\n→ succeeds`.

The Phase A → Phase B sequence is the LP→GLP contrast made observable. Annotation between A and B explicitly tells the learner: "you just watched the SRSW analyser do its job."

### ex-02 (`append_and_sum/3`)

**Five fenced code blocks** in this order. (Procedure shape amended from `/4` to `/3` on 2026-04-29 per spec Clarifications Q3a; the intermediate appended list is internal and not displayed.)

1. **Phase A — Load: ex-02 file**. Stdin: `olamni/tutorial/ch02/exercise-02/ch-02-ex-02-append-and-sum.glp`. Stdout: `✓ Loaded: …`.
2. **Phase B — Primary goal**. Stdin: `append_and_sum([1,2,3], [4,5,6], Sum).` Stdout: `Sum = 21\n→ succeeds`.
3. **Phase C — Inspection goal 1**. Stdin: `append_and_sum([], [4,5,6], Sum).` Stdout: `Sum = 15\n→ succeeds`.
4. **Phase D — Inspection goal 2**. Stdin: `append_and_sum([1,2,3], [], Sum).` Stdout: `Sum = 6\n→ succeeds`.
5. **Phase E — Inspection goal 3**. Stdin: `append_and_sum([], [], Sum).` Stdout: `Sum = 0\n→ succeeds`.

### ex-03 (`timed_append/3`)

**Five fenced code blocks** in this order:

1. **Phase A — Load: ex-03 file**. Stdin: `olamni/tutorial/ch02/exercise-03/ch-02-ex-03-timed-append.glp`. Stdout: `✓ Loaded: …`.
2. **Phase B — Primary goal**. Stdin: `timed_append([1,2,3], [a,b,c], Zs).` Stdout: `elapsed_ms(N)` (where N is wallclock-derived; SHAPE locked, value varies per run) on its own line FROM `'_output'/1` — appears BEFORE the binding line — followed by `Zs = [1, 2, 3, a, b, c]\n→ succeeds`.
3. **Phase C — Inspection goal 1**. Stdin: `timed_append([], [], Zs).` Stdout: `elapsed_ms(N)` (typically N=0 or 1) followed by `Zs = []\n→ succeeds`.
4. **Phase D — Inspection goal 2**. Stdin: `timed_append([1,2,3,4,5,6,7,8,9,10], [a,b,c,d,e,f,g,h,i,j], Zs).` Stdout: `elapsed_ms(N)` (typically N in 1..5) followed by `Zs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, a, b, c, d, e, f, g, h, i, j]\n→ succeeds`.
5. **Phase E — Inspection goal 3**. Stdin: `timed_append([1], [a], Zs).` Stdout: `elapsed_ms(N)` followed by `Zs = [1, a]\n→ succeeds`.

---

## Byte-equality contract

Per spec FR-014, byte-equality contracts vary by exercise:

| Trace file | Strict byte-equality required (modulo timestamps) | Relaxation |
|---|---|---|
| `ex-01-repl-trace.md` | YES, in all six phases | None |
| `ex-02-repl-trace.md` | YES, in all five phases | None |
| `ex-03-repl-trace.md` | YES for the `Zs = …` bindings, the `→ succeeds` lines, and the `elapsed_ms(...)` STRUCTURE | The N value inside `elapsed_ms(N)` MAY vary per run; the trace's annotation MUST document this with the phrase "varies per run; the SHAPE matters, not the specific number" |

**"Modulo timestamps"** for ex-01 and ex-02 means the auditor's reproducibility check ignores: the REPL banner (e.g., `GLP REPL v…`), the build wallclock line (e.g., `Built at 2026-…`), and any session-start line that is wallclock-derived. All other code-block content is compared line-for-line.

For ex-03, the auditor additionally ignores the integer literal inside `elapsed_ms(N)` while still requiring the surrounding structure (`elapsed_ms(`, `)`, `→ succeeds`, `Zs = ...`) to be byte-equal.

---

## Annotation rules

1. Annotations MUST be brief (1–2 lines per phase). Long discussion belongs in `ex-NN-tutorial.md`.
2. Annotations MUST be OUTSIDE the fenced code blocks. The block content is byte-verbatim from the REPL; annotations are commentary.
3. Annotations MUST NOT modify or paraphrase the code-block content. They explain what the learner is seeing.
4. ex-01 Phase A → Phase B transition annotation MUST explicitly explain the contrast: "the analyser rejected the classical LP version (Phase A) and accepted the GLP version (Phase B); this is the LP→GLP transition the chapter introduces in §2.2 made observable at the REPL".
5. ex-03 Phase B annotation MUST contain the elapsed-ms relaxation phrase per the byte-equality table above.

---

## Capture mechanism

Per workflow memory, traces are captured via the kernel-snapshot batch-mode pattern:

```bash
DART="/c/Users/gavri/dart-sdk/bin/dart"
printf "<file-path>\n<goal1>.\n<goal2>.\n…\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

The implementer captures stdout verbatim into the corresponding fenced code blocks. Any post-capture editing MUST be limited to:
- Adding the title, preface, postscript, and per-phase annotations OUTSIDE the code blocks.
- Splitting a single batch-capture into per-phase code blocks (each phase's block content is the relevant slice of the batch output).
- Removing the REPL banner / build wallclock / session-start lines that are wallclock-derived.

The implementer MUST NOT:
- Hand-construct REPL output.
- "Clean up" REPL output to match an expected shape.
- Synthesise a binding the REPL didn't produce.
