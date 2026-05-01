# Contract — `.glp` File Content & Comment Format (chapter 5)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-30

This contract defines the content and comment format for the 8–10 `.glp` files in chapter 5 (8 baseline + 2 extra for the negative two-`.glp` pattern). It inherits the ch01–ch04 file contracts and adapts to ch05's NEW exercise kinds: type-only / procedure-decl-only / negative.

---

## Common rules (apply to all files)

1. **Header comment block** — each file MUST begin with a `%`-prefixed comment block (5–15 lines for ch05) summarising what the file does + citing PDF source(s) + listing the Programs included + noting any relevant Formal box (5.1 / 5.2 / 5.3) + (for ex-04, ex-05) the canonical cross-chapter relationship cross-reference per R-008.
2. **Per-Program sub-header** — for multi-Program exercises, each new Program in the file is preceded by a 1–2 line `%%` sub-header naming the Program + its book sub-section reference (e.g., `%% §5.1.1 — Bit type definition`).
3. **Per-clause `%%` paraphrase comments** — each clause MUST carry one `%%` comment paraphrasing the surrounding prose from the relevant book section (charter §1.5). Helper unit-clauses + corrected-form clauses + stub-body clauses ALL get `%%` per clause.
4. **No `skipSRSW` or anti-spec language flags** — Constitution Principle III is non-negotiable.
5. **No external imports beyond `programs/self.glp`** (auto-loaded by the REPL). Per spec FR-015, ch05 has no cross-chapter imports (the cross-chapter relationships in ex-04 + ex-05 are documentation-only).
6. **Byte-exactness** — every PDF-sourced clause text MUST be byte-identical to the PDF source. Helper unit-clauses + stub-body clauses (R-012) are NOT byte-exact-from-PDF (the PDF doesn't contain them); they satisfy SRSW + type-check at REPL load and are recorded as "demonstration helpers" in the file header. The /speckit-implement verification subtask compares the file's PDF-sourced clause text (after stripping the header comment block + per-Program sub-headers + per-clause `%%` annotations + the helper layer) against the byte-exact PDF transcription.
7. **Byte-identical clause corpus — precise definition** (inherited from ch04 contract rule 7, refined for ch05):
   - Step 1: Remove the file's header comment block (every line starting with `%` at the top of the file, up to the first non-comment line).
   - Step 2: For each remaining clause, remove ANY line whose first non-whitespace character is `%` (this catches both `%`-prefix comments, `%%`-prefix paraphrase comments, and `%%`-prefix per-Program sub-headers).
   - Step 3: Trim trailing whitespace from each remaining line; preserve internal whitespace (indentation within multi-line clause bodies must match the PDF).
   - Step 4: Identify the helper layer per the file's `%% --- DEMONSTRATION HELPERS ---` marker (NEW for ch05; required in helper-bearing files). Helper-layer clauses are NOT compared to PDF.
   - Step 5: The remaining (non-helper) line sequence MUST equal the PDF clause corpus byte-for-byte.

---

## Helper-bearing files (ch05 NEW: ex-01, ex-02, ex-03)

Type-only and procedure-decl-only exercises include helper unit-clauses or a stub body BELOW a marker line that distinguishes the helper layer from the PDF-sourced layer.

**Marker convention**:

```glp
%% --- DEMONSTRATION HELPERS (not from book; per spec Q2 deferral + R-012) ---
```

This marker MUST appear AFTER all PDF-sourced declarations and BEFORE any helper unit-clause / stub body. The byte-exact verification subtask uses this marker to skip the helper layer.

The file's HEADER block MUST also acknowledge the helper layer:

```
% This file presents the §5.X PDF-sourced declarations from book pp YY. Helper
% unit-clauses below the `%% --- DEMONSTRATION HELPERS ---` marker are NOT from
% the book — they are small demonstration clauses that make the type / mode
% shape interactively exercisable in the REPL per spec Q2 + R-012. Each helper
% clause carries a `%%` paraphrase per charter §1.5.
```

**Negative-form files** (ex-07 + ex-08 failing forms) DO NOT carry the helper marker — they contain only the byte-exact PDF failing form. Their header explicitly states the file is meant to fail to load.

---

## File 1 — `exercise-01/ch-05-ex-01-type-definitions.glp` (type-only, Foundations)

**Programs**: §5.1.1 `Bit ::= 0 ; 1.` + §5.1.2 `Nat ::= 0 ; s(Nat).` + §5.1.3 `NumList ::= [] ; [Number | NumList].` + helper layer (R-012 proposed: `bit_test/1` × 2 + `nat_test/1` × 3 + `numlist_test/1` × 3).

**Header block** template:

```
% ch-05-ex-01-type-definitions.glp
%
% This file presents the §5.1.1 + §5.1.2 + §5.1.3 type definitions from book
% p 47 (PDF p 59). All type definitions are byte-exact from the PDF.
%
% Programs included:
%   §5.1.1 (p 47): Bit ::= 0 ; 1. — constant alternation
%   §5.1.2 (p 47): Nat ::= 0 ; s(Nat). — recursive Peano
%   §5.1.3 (p 47): NumList ::= [] ; [Number | NumList]. — typed list cons
%
% References Formal 5.1 (Type Definition Syntax, p 48).
%
% Helper unit-clauses below the `%% --- DEMONSTRATION HELPERS ---` marker are
% NOT from the book — they are small demonstration clauses that make each type
% interactively exercisable in the REPL per spec Q2 + research R-012. Each
% helper carries a `%%` paraphrase per charter §1.5.
```

**Validation**:
- 3 type-definition declarations (byte-exact from PDF p 47).
- 3 `%%` per-Program sub-headers.
- ~6–8 helper unit clauses below the marker.
- 6–11 `%%` paraphrase comments total (3 PDF + 3–8 helpers).
- Byte-exact verification per common rule 7 against PDF p 47, with helpers excluded via the marker.
- Helpers MUST satisfy SRSW + type-check at REPL load per FR-018 + R-012.

---

## File 2 — `exercise-02/ch-05-ex-02-built-in-types.glp` (type-only, Foundations)

**Programs**: §5.2 `List ::= [] ; [Any | List].` + helper layer (R-012 proposed: `list_test/1` × 3 + `any_test/1` × 3).

**Header block** template:

```
% ch-05-ex-02-built-in-types.glp
%
% This file presents the §5.2 universal `List` type definition + the built-in
% types prose paraphrase (Number, Any, Atom) from book p 48 (PDF p 60).
% Byte-exact from PDF.
%
% Programs included:
%   §5.2 (p 48): List ::= [] ; [Any | List]. — universal list via built-in Any
%
% References built-in types Number, Any, Atom (book p 48 prose, not encoded as
% code declarations — they are pre-existing GLP built-ins).
%
% Helper unit-clauses below the marker demonstrate the universal `List`'s ability
% to hold mixed-type elements (numbers, atoms, nested lists) and the `Any`
% discriminator's polymorphic admission criterion.
```

**Validation**:
- 1 type-definition declaration (byte-exact from PDF p 48).
- 1 `%%` per-Program sub-header.
- ~6 helper unit clauses below the marker.
- ~7 `%%` paraphrase comments total.
- Byte-exact verification per common rule 7.

---

## File 3 — `exercise-03/ch-05-ex-03-procedure-declaration.glp` (procedure-decl-only, Foundations)

**Programs**: §5.3 `procedure merge(List?, List?, List).` + 1–2 stub body clauses (R-012 proposed: 1-clause stub `merge(L?, R?, M) :- L? = [], M = R?.` with optional 2-clause expansion if the type-checker rejects the trivial form).

**Header block** template:

```
% ch-05-ex-03-procedure-declaration.glp
%
% This file presents the §5.3 moded procedure declaration from book p 48
% (PDF p 60). Byte-exact from PDF.
%
% Programs included:
%   §5.3 (p 48): procedure merge(List?, List?, List). — moded declaration
%                with `?` reader marks at positions 1 and 2 (consume mode)
%                and unmarked position 3 (produce mode).
%
% The stub body below the marker is NOT from the book — it provides minimal
% clauses to make the procedure declaration interactively exercisable in the
% REPL while preserving the declared mode shape per spec Q2 + research R-012.
%
% The full §5.4 worked typed merge/3 example with NumList type appears in ex-04.
```

**Validation**:
- 1 procedure declaration (byte-exact from PDF p 48).
- 1–2 stub body clauses below the marker.
- 2–3 `%%` paraphrase comments total.
- Byte-exact verification per common rule 7.
- Stub body MUST satisfy SRSW + type-check at REPL load.

---

## File 4 — `exercise-04/ch-05-ex-04-mode-checked-merge.glp` (full-program, Mode-checking-flow)

**Programs** (per Q4 + Q5 amendments): §5.4 `List ::= [] ; [Any | List].` (inline; the universal type from §5.2, NOT `NumList`) + `procedure merge(List?, List?, List).` + 3 clauses of typed `merge/3` worked example with Q5 `?`-additions to body's `Ys` (book p 49). Byte-exact clause text:

```glp
List ::= [] ; [Any | List].

procedure merge(List?, List?, List).

merge([X|Xs], Ys, [X?|Zs?]) :- merge(Ys?, Xs?, Zs).
merge(Xs, [Y|Ys], [Y?|Zs?]) :- merge(Xs?, Ys?, Zs).
merge([], [], []).
```

The body of clauses 1+2 carries the Q5 amendment: PDF printed `merge(Ys, Xs?, Zs)` and `merge(Xs?, Ys, Zs)`, but the page's own Body Checking annotation says `merge(Ys?, Xs?, Zs)` and `merge(Xs?, Ys?, Zs)`. The Q5 amendment uses the annotation's intent. Per FR-013 + spec Clarifications Q5, this is a pre-emptive amendment based on PDF self-inconsistency. The .glp file's `%%` paraphrase comment for clauses 1+2 explicitly documents the Q5 amendment.

**Header block** template:

```
% ch-05-ex-04-mode-checked-merge.glp
%
% This file presents the TYPED merge/3 worked example, byte-exact from book p 49
% (with Q5 `?`-additions to body per PDF annotation), §5.4 "Mode Checking" +
% Formal 5.2 "Mode Semantics".
% A related un-typed merge/3 appears in ch04 ex-04 (book §4.2.5, p 32) as an
% un-typed simple fair merger; see olamni/tutorial/ch04/exercise-04/ch-04-ex-04-merge-variants.glp.
% The two are pedagogically distinct presentations: same procedure name, the ch05
% typed form carries an explicit `procedure merge(List?, List?, List).`
% declaration with `?` reader marks (using the universal `List ::= [] ; [Any | List].`
% type from §5.2, per Q4); the ch04 untyped form has no procedure declaration at all
% (defaulting to GLP's implicit untyped behaviour). Different clause set (3 typed
% clauses in ch05 vs 4 untyped in ch04), different pedagogical focus (mode checking
% flow vs stream-merge implementations).
% This is a CROSS-CHAPTER RELATIONSHIP — not a code import. The .glp clauses below
% are byte-exact from §5.4 (with Q5 `?`-additions), NOT copies of ch04's clauses.
%
% Programs included:
%   §5.4 (p 49): NumList ::= [] ; [Number | NumList]. — type definition (duplicated inline from ex-01 per FR-010 self-containment)
%   §5.4 (p 49): procedure merge(NumList?, NumList?, NumList). — moded declaration
%   §5.4 (p 49): merge/3 — 3 clauses with `%%` mode-check walk-through annotations
%
% References Formal 5.2 (Mode Semantics, p 49). The `%%` annotations on each
% merge/3 clause walk through the head-mode proof and body-mode propagation
% steps from §5.4 prose IN ADDITION to the per-clause paraphrase per charter §1.5.
```

**Validation**:
- 1 type definition + 1 procedure declaration + 3 clauses (byte-exact from PDF p 49).
- 3 `%%` per-Program sub-headers (type def / procedure decl / clauses).
- 5 `%%` paraphrase comments + 3 walk-through annotations on merge/3 clauses (per charter §1.5 + spec FR-005 + SC-017).
- Byte-exact verification per common rule 7.
- Header MUST contain canonical R-008 cross-reference block citing ch04 ex-04.

---

## File 5 — `exercise-05/ch-05-ex-05-counter-response-slot.glp` (full-program, Mode-checking-flow)

**Programs** (per Q4 + Q6 amendments): §5.5 byte-exact from book p 50:

```glp
CounterMsg ::= clear ; up ; down ; show(Number?).
CounterStream ::= [] ; [CounterMsg | CounterStream].

procedure counter(CounterStream?, Number?).

counter([show(State?)|S], State) :-
    number(State?) |
    counter(S?, State?).
```

Per Q4: arg 2 of `counter` is `Number?` (consume mode), NOT plain `Number`. Per Q6: the clause has guard `number(State?) |` + recursive body `counter(S?, State?).`, NOT a single response-slot head clause. The `number(State?)` guard is multi-reader-permissive per Formal 4.3 (ch04), authorising `State`'s 1W + 3R appearance. Mode Involution per Formal 5.3 applies: the embedded `Number?` inside `show(...)` of `CounterMsg`'s alternation, combined with the outer consume-mode `CounterStream?`, produces a writer slot at the embedded position (consume × consume = produce per Formal 5.3 table).

**Header block** template:

```
% ch-05-ex-05-counter-response-slot.glp
%
% This file presents the §5.5 typed counter with response-slot embedded mode,
% byte-exact from book p 50, §5.5 "Embedded Modes: Response Slots" + Formal 5.3
% "Mode Involution".
% A related un-typed counter/1 + counter_loop/2 appears in ch04 ex-06 (book §4.2.14)
% as an un-typed object/monitor; see olamni/tutorial/ch04/exercise-06/ch-04-ex-06-buffered-and-monitors.glp.
% Different arity (1 → 2), different shape (no response-slot in ch04 vs response-slot
% in ch05), different pedagogical focus (objects/monitors vs embedded modes).
% This is a CROSS-CHAPTER RELATIONSHIP — not a code import.
%
% Programs included:
%   §5.5 (p 50): CounterMsg ::= clear ; up ; down ; show(Number?). — type def with embedded `?`
%   §5.5 (p 50): CounterStream ::= [] ; [CounterMsg | CounterStream].
%   §5.5 (p 50): procedure counter(CounterStream?, Number?). (per Q4: arg 2 is Number?, not plain Number)
%   §5.5 (p 50): counter([show(State?)|S], State) :- number(State?) | counter(S?, State?). (per Q6: full clause has guard + body)
%
% References Formal 5.3 (Mode Involution, p 50): consume × consume = produce.
```

**Validation**:
- 2 type definitions + 1 procedure declaration + 1 clause (byte-exact from PDF p 50).
- ~4 `%%` paraphrase comments.
- Byte-exact verification per common rule 7.
- Header MUST contain canonical R-008 cross-reference block citing ch04 ex-06.

---

## File 6 — `exercise-06/ch-05-ex-06-typed-quicksort.glp` (full-program, Flagship)

**Programs**: §5.6 `NumList` (inline, duplicated from ex-04 per FR-010) + `procedure quicksort/2` + `procedure qsort/3` + `procedure partition/4` + 6 clauses spanning the full sort algorithm (book p 51).

**Header block** template:

```
% ch-05-ex-06-typed-quicksort.glp
%
% This file presents the §5.6 typed quicksort (the chapter's flagship Program),
% byte-exact from book p 51, §5.6 "Complete Example: Typed Quicksort".
%
% Programs included:
%   §5.6 (p 51): NumList ::= [] ; [Number | NumList]. — type def (inline; duplicated from ex-01/ex-04 per FR-010 self-containment)
%   §5.6 (p 51): procedure quicksort(NumList?, NumList).
%   §5.6 (p 51): procedure qsort(NumList?, NumList?, NumList).
%   §5.6 (p 51): procedure partition(Number?, NumList?, NumList, NumList).
%   §5.6 (p 51): 6 clauses of quicksort/2 + qsort/3 + partition/4
%
% This is the chapter's flagship — it composes everything from §5.1–§5.5 into a
% complete typed Program: type definitions, procedure declarations with mode
% annotations, recursion across multiple typed predicates.
```

**Validation**:
- 1 type def + 3 procedure decls + 6 clauses = 10 declarations/clauses (byte-exact from PDF p 51).
- ~10 `%%` paraphrase comments.
- 4 `%%` per-Program sub-headers.
- Byte-exact verification per common rule 7.

---

## File 7a — `exercise-07/ch-05-ex-07-type-error-failing.glp` (negative, Negatives)

**Programs**: §5.7.1 `foo/1` failing form — load MUST FAIL with type-error message (book p 51).

**Header block** template:

```
% ch-05-ex-07-type-error-failing.glp
%
% ⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠
%
% This file presents the §5.7.1 type-error illustration from book p 51, byte-exact
% from PDF. The file's purpose is to demonstrate the type-checker's rejection
% behaviour. When loaded into the GLP REPL, the load MUST fail with a type-error
% message documenting that a non-Number value (e.g., the atom 'a') does not
% satisfy the declared Number type.
%
% Programs included:
%   §5.7.1 (p 51): foo/1 — type-error trigger
%
% See ch-05-ex-07-type-error-corrected.glp for a re-typed form that loads
% successfully.
%
% Per spec FR-014 + R-011, the captured error message in the trace is byte-equal
% to the actual REPL output, modulo any per-run-varying segments authorised at
% /speckit-implement T026/T037-equivalent.
```

**Validation**:
- 1 procedure declaration + 1 clause (byte-exact from PDF p 51).
- 2 `%%` paraphrase comments.
- Byte-exact verification per common rule 7.
- Load MUST FAIL (verifiable via the captured trace's Phase A).

## File 7b — `exercise-07/ch-05-ex-07-type-error-corrected.glp` (negative, Negatives)

**Programs**: corrected `foo/1` form — load succeeds. Exact corrected shape proposed at /speckit-implement T006-equivalent (e.g., re-typed `procedure foo(Atom).` to accept the offending value).

**Header block** template:

```
% ch-05-ex-07-type-error-corrected.glp
%
% Companion to ch-05-ex-07-type-error-failing.glp — this file presents a
% corrected form of foo/1 that LOADS SUCCESSFULLY, demonstrating the fix for
% the §5.7.1 type-error illustration.
%
% The exact corrected shape is proposed during /speckit-plan T006-equivalent
% with project-owner approval recorded in research.md. Common shapes: re-typing
% the procedure declaration to accept the offending value's type, OR fixing the
% clause body to produce a value matching the declared type.
%
% This file demonstrates that the rejection is fixable; the load succeeds with
% `✓ Loaded:` and zero errors.
```

**Validation**:
- 1 procedure declaration + 1 clause (corrected form).
- 2 `%%` paraphrase comments.
- Load MUST succeed (verifiable via the captured trace's Phase B).

---

## File 8a — `exercise-08/ch-05-ex-08-mode-error-failing.glp` (negative, Negatives)

**Programs**: §5.7.2 `bar/2` failing form — load MUST FAIL with mode-error message (book pp 51–52).

**Header block** template:

```
% ch-05-ex-08-mode-error-failing.glp
%
% ⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠
%
% This file presents the §5.7.2 mode-error illustration from book pp 51–52,
% byte-exact from PDF. When loaded into the GLP REPL, the load MUST fail with
% a mode-error message documenting that the clause's reader/writer roles
% violate the procedure declaration.
%
% Programs included:
%   §5.7.2 (pp 51–52): bar/2 — mode-error trigger
%
% See ch-05-ex-08-mode-error-corrected.glp for the corrected form
%   bar(X, Y?) :- Y := X? + 1.
% explicitly cited by the book at p 52 as the fix.
```

**Validation**:
- 1 procedure declaration + 1 clause (byte-exact from PDF pp 51–52).
- 2 `%%` paraphrase comments.
- Byte-exact verification per common rule 7.
- Load MUST FAIL.

## File 8b — `exercise-08/ch-05-ex-08-mode-error-corrected.glp` (negative, Negatives)

**Programs**: book-cited corrected form `bar(X, Y?) :- Y := X? + 1.` from book p 52.

**Header block** template:

```
% ch-05-ex-08-mode-error-corrected.glp
%
% Companion to ch-05-ex-08-mode-error-failing.glp — this file presents the
% book-cited corrected form
%   bar(X, Y?) :- Y := X? + 1.
% from book p 52. Loads SUCCESSFULLY, demonstrating the fix for the §5.7.2
% mode-error illustration.
%
% Uses the := body kernel (introduced for ch02 territory; permitted here per
% ch03 FR-015 amendment because it appears in a byte-exact PDF clause).
```

**Validation**:
- 1 procedure declaration + 1 clause (byte-exact from PDF p 52).
- 2 `%%` paraphrase comments.
- Byte-exact verification per common rule 7.
- Load MUST succeed.
- Optional Phase C of the trace exercises `bar(5, R).` ⇒ `R = 6` to demonstrate the fix actually works.

---

## Cross-file invariants

- ex-04's typed `merge/3` clauses are byte-exact from §5.4 PDF, NOT byte-identical to ch04 ex-04's untyped `merge/3` clauses. The cross-chapter RELATIONSHIP is a header citation + signpost prose, not byte equality.
- ex-05's typed `counter/2` clause is byte-exact from §5.5 PDF, NOT byte-identical to ch04 ex-06's untyped `counter/1`. Same relationship pattern.
- Each exercise's `.glp` is self-contained per FR-010; `NumList` reused in ex-04 + ex-06 is duplicated inline byte-exact (NOT in a shared `types.glp`).
- Per-clause `%%` paraphrase comments MAY differ across files even for duplicated type definitions, because each file's pedagogical context differs.
- Helper layers (ex-01, ex-02, ex-03) are exercise-specific; helper procedure names MUST NOT collide with PDF-Program procedure names from any §5.x section (R-012 rule 6).
- Negative failing-form files MUST be marked `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠` in the header block for clarity.

---

## Constitution alignment

- Principle III (SRSW Discipline) — all PDF-sourced clauses in all files are SRSW-compliant by byte-exact construction (the book's Programs are SRSW-valid; implementer copies byte-exact). Helper layers (ex-01/ex-02/ex-03) MUST also satisfy SRSW per R-012.
- Principle VI (Tutorial Charter Compliance) — `%%` per-clause comments per charter §1.5 across all files including helpers and corrected-form clauses.
- Language Design Authority — no new kernels / guards / system predicates / type-system features introduced; the type-system + mode declarations + `procedure` keyword + `Any`/`Number`/`Atom` built-ins all PRE-EXIST.
