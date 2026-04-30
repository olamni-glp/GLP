# Contract — `ex-NN-repl-trace.md` Structural Format (chapter 4)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-30

This contract defines the structural format of `ex-NN-repl-trace.md` files for chapter 4. It inherits the ch01–ch03 trace contracts. ALL TEN ch04 traces use STRICT byte-equality (per FR-014); chapter 4 introduces no wallclock-derived output, so ch02's elapsed-ms relaxation does NOT apply.

---

## Common structure (all 10 traces)

Every `ex-NN-repl-trace.md` for `NN ∈ 01..10` MUST contain, in order:

1. **Title** — `# Exercise NN — REPL trace` (or similar; learner-facing).
2. **Preface** — 1–3 sentences (learner-targeted) stating what the trace demonstrates. OUTSIDE any code block.
3. **Phase blocks** — one fenced ```glp code block per phase. Code-block CONTENT is byte-verbatim from the actual REPL session (stdin lines + stdout responses + REPL prompt prefix `GLP>` where applicable).
4. **Per-phase annotations** — 1–2 brief lines OUTSIDE each code block, before or after the block, explaining what to expect, what it means, and why it matters.
5. **Postscript** — 1–3 sentences (learner-targeted) summarising what the trace proves and why it matters for the chapter's learning goal. OUTSIDE any code block.

---

## Phase count per exercise

Each ch04 exercise has **5 phases** in its trace:

- Phase A — Load: ex-NN file
- Phase B — Primary demo goal
- Phase C — Inspection goal 1
- Phase D — Inspection goal 2
- Phase E — Inspection goal 3

If a multi-Program exercise (most of ch04) needs supplementary inspection goals to satisfy the every-clause-coverage requirement (per FR-017 + research R-004), additional phases F, G, etc. MAY be added with explicit annotation "supplementary inspection — exercises clause Q of Program P". This is an exception to the 5-phase default; the implementer documents the rationale in the trace's preface.

For ex-03 (cross-chapter inversion exercise), Phase A loads the single `.glp` file containing all four §4.2.1–§4.2.4 Programs (no separate load step for the cross-chapter inversion since it's all in one file).

---

## Per-exercise phase content (proposed; locked per-exercise during /speckit-implement T006-equivalent)

The specific primary + inspection goals + locked bindings per exercise are NOT pre-locked here (per research R-004; 40 bindings would overspecify). The implementer proposes per-exercise during /speckit-implement with project-owner approval. The proposal MUST satisfy:

1. Primary goal exercises the exercise's main Program(s) end-to-end with a deterministic locked binding.
2. The 4-goal session (or 4+ if supplementary phases needed) collectively exercises every clause of every Program in the exercise's `.glp` per FR-017.
3. Each goal has a deterministic locked binding (no per-run variation; chapter 4 has no wallclock-derived output).

Some illustrative primary goals (as guidance for the implementer; NOT locked here):

| Exercise | Illustrative primary goal | Approximate binding |
|---|---|---|
| ex-01 | `and(0, 1, R).` and `xor(1, 0, X).` | `R = 0`, `X = 1` |
| ex-02 | `full_adder(1, 1, 0, S, C).` | `S = 0`, `C = 1` |
| ex-03 | `producer(A, 5), consumer(A?, 0, Sum).` | `Sum = 15` |
| ex-04 | `merge_tree([[1], [2], [3], [4]], M).` | `M = ` some merged form |
| ex-05 | `producer(A, 3), distribute(A?, B, C), consumer(B?, 0, S1), consumer(C?, 0, S2).` | `S1 = S2 = 6` |
| ex-06 | `counter([add, add, read(X), clear, add, read(Y), done]).` | `X = 2, Y = 1` |
| ex-07 | `factorial(7, F).` and `fib_linear(20, G).` | `F = 5040`, `G = 6765` |
| ex-08 | `mergesort([3,1,4,1,5,9,2,6], S).` | `S = [1,1,2,3,4,5,6,9]` |
| ex-09 | `run(merge, merge([1,2],[3,4],Z)).` (trust-mode MI) | `Z = [1,3,2,4]` (or similar fair-merge result) |
| ex-10 | tracing MI primary then replay | trace + replay match byte-for-byte |

The ex-04 + ex-05 + ex-06 + ex-09 + ex-10 goals may need elevated `:limit` (per spec edge case "Goal sequence in a §4.4 meta-interpreter goal exceeds REPL execution limit").

---

## Byte-equality contract

Per spec FR-014, ALL TEN traces use STRICT byte-equality:

- Byte-equal modulo REPL banner / build wallclock lines / session-start lines
- No per-run-variation exception applies (no `now/1` / `'_output'/1` in any ch04 Program; no wallclock-derived output)
- Auditor reproducibility check: re-run the same goal sequence on the same `.glp` file via the same REPL build → trace content byte-equal modulo banner

---

## Annotation rules

1. Annotations MUST be brief (1–2 lines per phase). Long discussion belongs in `ex-NN-tutorial.md`.
2. Annotations MUST be OUTSIDE the fenced code blocks. The block content is byte-verbatim from the REPL; annotations are commentary.
3. Annotations MUST NOT modify or paraphrase the code-block content. They explain what the learner is seeing.
4. For multi-Program exercises (most of ch04), annotations identify which Program's clause was selected by each goal — this is the primary mechanism for the learner to understand which Program is being exercised.
5. ex-03's Phase A annotation MUST acknowledge the cross-chapter inversion: "These same `producer/2` + `consumer/3` procedures appear in ch03 ex-01 as a cross-chapter forward import; here they are presented in their NATIVE chapter-4 home with the §4.2.1 + §4.2.2 prose-paraphrase context."

---

## Capture mechanism

Per workflow memory + ch01/ch02/ch03 precedent, traces are captured via the kernel-snapshot batch-mode pattern:

```bash
DART="/c/Users/gavri/dart-sdk/bin/dart"
printf "<.glp-path>\n<goal1>.\n<goal2>.\n…\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

For exercises that may exceed the default REPL execution limit (ex-04 dynamic merge, ex-05 ripple-carry adder, ex-09 + ex-10 meta-interpreters), prepend `:limit <higher-value>` to the command sequence:

```bash
printf "<.glp-path>\n:limit 1000000\n<goal1>.\n<goal2>.\n…\n:quit\n" | "$DART" run glp_runtime/.dart_tool/repl.dill
```

The implementer captures stdout verbatim into the corresponding fenced code blocks. Any post-capture editing MUST be limited to:
- Adding the title, preface, postscript, and per-phase annotations OUTSIDE the code blocks.
- Splitting a single batch-capture into per-phase code blocks.
- Removing the REPL banner / build wallclock / session-start lines that are wallclock-derived.

The implementer MUST NOT:
- Hand-construct REPL output.
- "Clean up" REPL output to match an expected shape.
- Synthesise a binding the REPL didn't produce.
- Apply any per-run-variation relaxation (none is permitted in chapter 4).
