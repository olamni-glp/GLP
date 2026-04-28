# Contract: `ex-NN-repl-trace.md` format

**Feature**: Olamni Tutorial Chapter 1 (`002-tutorial-ch01`)
**Source**: spec.md FR-003; spec.md Clarifications Q3.

This contract defines the structure of every `ex-NN-repl-trace.md` produced by tutorial implementation.

## File-level structure

```
# <one-line title naming the exercise and chapter>

<preface>                # 1–3 sentences, learner-targeted, what this trace demonstrates

## <Phase 1 heading>

<brief annotation>       # 1–2 short lines outside the code block

```glp
<verbatim REPL stdin/stdout for phase 1>
```

## <Phase 2 heading>

<brief annotation>

```glp
<verbatim REPL stdin/stdout for phase 2>
```

...

## <Phase N heading>

<brief annotation>

```glp
<verbatim REPL stdin/stdout for phase N>
```

<postscript>             # 1–3 sentences, learner-targeted, what this trace proved and why
```

## Phases

For exercise-01 specifically (per research.md R-004), exactly **5 phases**:

1. **Build/load** — `dart compile exe` invocation (if not already done) + REPL invocation + `load <path>` command + REPL acknowledgement.
2. **Primary goal** — `merge([1,2,3],[a,b],Xs).` and the captured response (predicted: `Xs = [1, a, 2, b, 3]`).
3. **Inspection goal 1** (asymmetric) — `merge([1,2,3,4], [a], Xs).` and response.
4. **Inspection goal 2** (empty stream) — `merge([], [a, b, c], Xs).` and response.
5. **Inspection goal 3** (base case) — `merge([], [], Xs).` and response.

If the implementer's actual REPL output for phase 2 differs from the predicted binding, implementation HALTS per spec Clarification Q1 — do NOT silently re-write the spec.

## Code-block invariants

- Use ` ```glp ` for the fence language tag (Markdown fenced code block).
- Each line inside a code block is byte-verbatim from the REPL stdin or stdout.
- The REPL prompt prefix is included as printed (e.g., `> merge(...).`, or whatever prefix the local REPL emits).
- No comments are added INSIDE the code block. Annotations belong OUTSIDE, between the heading and the code block (or after).

## Annotation invariants

- Each annotation is **brief**: 1–2 short sentences max.
- Each annotation is **learner-targeted**: explain what to expect, what it means, why it matters — in plain language, no implementation jargon.
- Annotations MUST NOT modify what the code block records. Annotations are commentary; the code block is the artifact.

## "Modulo timestamps" definition

For SC-004's byte-equality auditor check:
- Lines matching the REPL banner / build wallclock (e.g., a `[2026-04-28 10:42:15] ...` style header, or `Dart SDK x.y.z` version banner) are **excluded** from the byte-equality comparison.
- All other code-block content is included.
- Auditors comparing two traces produced from the same `.glp` file MUST find them byte-identical excluding those banner lines.

## What this contract is NOT

- Not a contract on the REPL implementation itself (the REPL is in `glp_runtime/bin/glp_repl.dart`; its output format is whatever it is).
- Not a contract on the exact predicted binding (that's in the spec at `spec.md` SC-003; this format file just says "include the actual output").
- Not a contract on Markdown rendering (MUST be valid Markdown but no specific renderer is targeted).
