# Contract — `.glp` file format (ch06)

**Path**: `olamni/tutorial/ch06/exercise-NN/ch-06-ex-NN-<short-name>.glp`.

**Inherited from ch01–ch05** with ONE ch06-specific addition: a synthesis cross-reference header block (per R-008 + FR-014 first documentation site).

## File structure

Each `.glp` file MUST contain, in this order:

1. **Header comment block** (lines starting with `%%`) — see "Header block contract" below.
2. **Type definition(s)** introduced fresh at §6.x per Q2 deferral (shape locked at /speckit-implement T006-equivalent).
3. **`procedure` declaration(s)** introduced fresh at §6.x per Q2 deferral (shape locked at /speckit-implement T006-equivalent).
4. **Clauses byte-exact from the cited earlier-chapter PDF source** (per FR-002 + FR-003), each preceded by ONE `%%` paraphrase comment per FR-005.

For ex-02 specifically (typed quicksort from ch05 §5.6), the type definitions and procedure declarations are ALSO byte-exact from the source chapter (because ch05 §5.6 was already typed in its origin chapter, including ch05's Q10 dual amendments — corrected qsort declaration `(NumList?, NumList, NumList?)` + interleaved layout). For ex-01, ex-03, ex-04, ex-05, the source chapter was un-typed and the declarations are introduced fresh per Q2.

## Header block contract (NEW for ch06 per R-008)

Every `.glp` file MUST have a header comment block of the form:

```
%% ch06 ex-NN — <§6.x heading text>
%% Source: <earlier chapter §-section>, book pp <page-range>, Program <identifier from chXX-sources.md>.
%% Synthesised from <earlier chapter source> because the ch06 PDF chapter (book p 53) is a stub —
%%   only the title and five section headings exist; no body text and no native Programs.
%% Type definitions and `procedure` declarations are introduced fresh at §6.x per ch05 conventions
%%   (or, for ex-02, are byte-exact from ch05 §5.6 which was already typed).
```

Concrete example for ex-01:

```
%% ch06 ex-01 — §6.1 Difference Lists
%% Source: ch04 §4.3.7, book pp 38–39, Programs flatten/2 + flatten_acc/3.
%% Synthesised from ch04 §4.3.7 because the ch06 PDF chapter (book p 53) is a stub —
%%   only the title and five section headings exist; no body text and no native Programs.
%% Type definitions and `procedure` declarations are introduced fresh at §6.1 per ch05 conventions.
%% Per /speckit-clarify Q1 (option B): the flatten-with-accumulator pattern is closer in
%%   pedagogical shape to the difference-list idiom than ch04 §4.2.3+§4.2.4 reverse/reverse_acc.
```

For ex-02 specifically, the header notes that declarations are byte-exact from ch05:

```
%% ch06 ex-02 — §6.2 Quicksort
%% Source: ch05 §5.6, book p 51, Program 5.6 typed quicksort.
%% Synthesised from ch05 §5.6 because the ch06 PDF chapter (book p 53) is a stub —
%%   only the title and five section headings exist; no body text and no native Programs.
%% Type definitions, procedure declarations, AND clauses are byte-exact from ch05 §5.6
%%   (including ch05 Q10 dual amendments: corrected qsort declaration `(NumList?, NumList, NumList?)`
%%   + interleaved layout — both required to load per ch05 Q11 empirical verification).
```

## Per-clause `%%` paraphrase comments (FR-005, charter §1.5)

Every clause MUST be preceded by a `%%` paraphrase comment of the matching paragraph or sentence in the book. For ch06 exercises, the paraphrase MAY come from EITHER:
- The earlier-chapter source's paraphrase (e.g., ch04's prose for `flatten/2`), OR
- A ch06-§6.x-specific re-framing (e.g., "this is the difference-list idiom under §6.1's framing").

The implementer chooses based on which framing is more pedagogically useful at /speckit-implement T-equivalent.

## Byte-exact mandate scope

Per FR-002 + Q2 clarification, the byte-exact mandate applies to:
- ✓ The clause text (head, guard, body) of each clause from the cited PDF source.
- ✗ The type definitions introduced fresh at §6.x (NOT byte-exact — chosen at T006-equivalent).
- ✗ The `procedure` declarations introduced fresh at §6.x (NOT byte-exact — chosen at T006-equivalent).
- ✗ The header comment block (NOT byte-exact — synthesis explanation written for ch06).
- ✗ Per-clause `%%` paraphrase comments (NOT byte-exact — paraphrase is a writer's choice).

For ex-02 only, ALL of the above are byte-exact from ch05 §5.6 because ch05's Q10 amendments locked the declaration shapes.

## File-count contract (FR-009)

Each exercise dir contains exactly THREE files:
- `ch-06-ex-NN-<short-name>.glp` (single GLP source).
- `ex-NN-tutorial.md`.
- `ex-NN-repl-trace.md`.

NO two-`.glp`-file pattern (unlike ch02 ex-01 / ch05 ex-06 + ex-07). All 5 ch06 exercises are positive (load cleanly + run successfully); no negative-form contrast required.

## SRSW + type-check verification (FR-018, SC-006)

Each `.glp` file MUST pass:
1. SRSW analyser at REPL load (inherited automatic verification — fails the load if violated).
2. Live type-checker at REPL load (per ch05 R-006 inheritance — operational from ch05 onward).
3. Compilation + execution of the locked primary demo goal + 3 inspection goals.

Mismatch at any step is halt-and-amend per FR-013. The byte-exact source clauses are LOCKED — only the introduced declarations are amendable.

## Inherited from ch01–ch05

This contract inherits from `specs/006-tutorial-ch05/contracts/glp-file-format.md` with the synthesis cross-reference header block as the ch06-specific addition per R-008.
