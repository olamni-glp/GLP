# Contract: `ch-XX-ex-NN-<short-name>.glp` content format

**Feature**: Olamni Tutorial Chapter 1 (`002-tutorial-ch01`)
**Source**: spec.md FR-001, FR-008; research.md R-001 (comment density), R-006 (PDF source scope).

This contract defines the structure of the runnable GLP source file in each `exercise-NN/`.

## File-level structure

```
%% <filename>
%% Program <book-program-number> from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §<section>, p <page>.
%% <2-4 line block paraphrase explaining what this Program demonstrates and why>

<clause 1>  %% <one-line paraphrase from book prose>
<clause 2>  %% <one-line paraphrase from book prose>
<clause 3>  %% <one-line paraphrase from book prose>
```

## For chapter 1 specifically

**Source Program**: 1.1 Fair Stream Merger, PDF p 5.

**Header block paraphrase MUST cover**:
- Demonstrates SRSW discipline (each variable occurs exactly once as writer + once as reader).
- Three clauses: take from stream 1, take from stream 2, terminate on empty.
- Argument-swap fairness mechanism.

**Clause-by-clause paraphrase**:
- Clause 1 (recursive, take from stream 1): paraphrase the "swap to alternate" sentence from p 5–6.
- Clause 2 (recursive, take from stream 2): symmetric paraphrase.
- Clause 3 (base case): paraphrase the termination prose.

## Variable naming per exercise

Per spec FR-008:

| Exercise | Variables (replacing X, Xs, Y, Ys, Zs from PDF) |
|----------|--------------------------------------------------|
| ex-01    | `X`, `Xs`, `Y`, `Ys`, `Zs` (original from PDF)    |
| ex-02    | `First`, `RestFirst`, `Second`, `RestSecond`, `Out` |
| ex-03    | `A`, `As`, `B`, `Bs`, `Cs`                         |

Reader markers (`?` suffix) follow each variable consistently with the original Program's SRSW pattern. The structural shape of every clause is identical across exercises; only the names differ.

## Byte-identity invariant

For exercise-01: after stripping all `%%` lines and trailing whitespace, the remaining executable lines MUST be byte-identical to Program 1.1 as printed on PDF p 5 (verified by re-reading p 5 byte-exactly per spec Clarification Q1 / R-006).

For exercise-02 and exercise-03: after stripping `%%` lines AND applying the variable-rename mapping (table above), the executable structure MUST be byte-identical to exercise-01's executable structure (i.e., variant differs ONLY in identifier names).

## Forbidden content

- No type declarations (`procedure ...`). Chapter 1 precedes ch5; per charter §1 (REPL only) and per spec FR-001, no type/mode declarations.
- No external `.glp` imports / module declarations. Single-file exercise.
- No `skipSRSW` or other anti-spec language flags (Constitution Principle III).
- No author/date metadata in `%%` lines beyond what's in the header block.

## Validation procedure

When the implementer writes the file:
1. Re-read PDF p 5 to refresh byte-exact Program 1.1 (per spec Clarification Q1).
2. Type clauses verbatim into the file.
3. Add `%%` paraphrase comments per the structure above.
4. Run the file under the GLP REPL: `load <path>`. Pipeline (SRSW → PE → type-check → compile) MUST pass with zero errors (per spec SC-002).
5. If REPL reports any error, halt and report (Constitution Principle II).
