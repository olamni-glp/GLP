# Contract — `.glp` File Content & Comment Format (chapter 5, post-Q7+Q12)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-05-01 (post-Q7+Q4+Q5+Q6+Q8+Q10+Q11+Q12 binding form)

This contract defines the content and comment format for the **9 `.glp`** files in chapter 5 (7 baseline files for the 7 post-Q7+Q12 exercises + 2 extra corrected-form files for the negative two-`.glp` pattern in ex-06 + ex-07). Inherits the ch01–ch04 file contracts and adapts to ch05's TWO post-Q7 exercise kinds: **load-only** (ex-01, ex-02) and **negative** (ex-06, ex-07). Three other exercises are **full-program** (ex-03, ex-04, ex-05).

---

## Common rules (apply to all files)

1. **Header comment block** — each file MUST begin with a `%`-prefixed comment block (5–15 lines) summarising what the file does + citing PDF source(s) + listing the Programs included + noting any relevant Formal box (5.1 / 5.2 / 5.3) + (for ex-03, ex-04) the canonical cross-chapter relationship cross-reference per R-008 + (for ex-05) the Q10 dual amendment provenance + (for ex-06+ex-07 failing forms) the `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠` marker.
2. **Per-Program sub-header** — for multi-Program exercises, each new Program in the file is preceded by a 1–2 line `%%` sub-header naming the Program + its book sub-section reference (e.g., `%% §5.1.1 — Bit type definition`).
3. **Per-clause `%%` paraphrase comments** — each clause MUST carry one `%%` comment paraphrasing the surrounding prose from the relevant book section (charter §1.5). Q8 minimal coverage stub clauses + corrected-form clauses ALL get `%%` per clause. **NO fabricated demonstration helpers** per Q7 retraction.
4. **No `skipSRSW` or anti-spec language flags** — Constitution Principle III is non-negotiable.
5. **No external imports beyond `programs/self.glp`** (auto-loaded by the REPL). Per spec FR-015, ch05 has no cross-chapter imports (the cross-chapter relationships in ex-03 + ex-04 are documentation-only).
6. **Byte-exactness** — every PDF-sourced clause text MUST be byte-identical to the PDF source. Q8 minimal coverage stubs (in ex-04 only) are NOT byte-exact-from-PDF (the PDF doesn't contain them — they exist solely to satisfy type-checker exhaustiveness on `CounterMsg`'s alternatives `[]`/`clear`/`up`/`down`); they satisfy SRSW + type-check at REPL load and are recorded under a distinct `%% --- Q8 MINIMAL COVERAGE STUBS ---` marker. Q10 amendments to ex-05 alter the LAYOUT (interleaved decls-with-clauses) and the qsort SIGNATURE only; the clause TEXT remains byte-exact PDF. The /speckit-implement verification subtask compares the file's PDF-sourced clause text (after stripping the header comment block + per-Program sub-headers + per-clause `%%` annotations + the Q8 stub layer where present) against the byte-exact PDF transcription.
7. **Byte-identical clause corpus — precise definition** (inherited from ch04 contract rule 7, refined for ch05 post-Q7+Q12):
   - Step 1: Remove the file's header comment block (every line starting with `%` at the top of the file, up to the first non-comment line).
   - Step 2: For each remaining clause, remove ANY line whose first non-whitespace character is `%` (this catches both `%`-prefix comments, `%%`-prefix paraphrase comments, and `%%`-prefix per-Program sub-headers).
   - Step 3: Trim trailing whitespace from each remaining line; preserve internal whitespace (indentation within multi-line clause bodies must match the PDF, except for ex-05 where Q10 Issue B authorises layout interleaving).
   - Step 4: For ex-04 (post-Q7+Q12), identify the Q8-stub layer per the file's `%% --- Q8 MINIMAL COVERAGE STUBS ---` marker. Q8-stub-layer clauses are NOT compared to PDF (they exist for type-checker exhaustiveness, not faithful PDF transcription).
   - Step 5: For ex-05 (post-Q7+Q12), the qsort declaration is the Q10-corrected form `(NumList?, NumList, NumList?)` (NOT the printed `(NumList?, NumList?, NumList)`); this single-line amendment is documented in the header AND in the inline `%%` paraphrase comment on the qsort declaration. Layout interleaving (Q10 Issue B) is also documented.
   - Step 6: The remaining (non-Q8-stub) line sequence MUST equal the PDF clause corpus byte-for-byte (with Q10's qsort signature swap and layout interleaving as the only authorised deviations for ex-05).

---

## Q8 minimal coverage stubs (ch05 NEW, ex-04 only — NOT to be confused with retracted-Q2 helpers)

Per Q8 + Q11 T5 empirical, ex-04 (§5.5 counter response-slot post-Q7+Q12) requires minimal coverage stubs for `CounterMsg`'s `[]`/`clear`/`up`/`down` alternatives because the byte-exact PDF form (showing only the `show` clause) fails to load with `counter argument 1: uncovered alternative "[]"`. Q8 minimal coverage stubs are NOT helpers in the retracted-Q2 sense — they are **minimal completions for type-checker exhaustiveness** with documented Q-amendment provenance.

**Marker convention** (NEW for ch05; appears in ex-04 ONLY):

```glp
%% --- Q8 MINIMAL COVERAGE STUBS (type-checker exhaustiveness; book p 50 shows only the show clause; per spec Q8 amendment) ---
```

This marker MUST appear AFTER the byte-exact PDF show-clause and BEFORE any Q8 stub clause. The byte-exact verification subtask uses this marker to skip the Q8-stub layer.

The file's HEADER block MUST also acknowledge the Q8 stubs:

```
% This file presents the §5.5 counter response-slot from book p 50 byte-exact, plus
% Q8 minimal coverage stubs for the uncovered CounterMsg alternatives ([]/clear/up/down)
% per spec Q8 amendment. The Q8 stubs are NOT fabricated helpers (per Q7 retraction);
% they are minimal completions required for the type-checker's exhaustiveness check
% to pass. Each Q8 stub clause carries a `%%` paraphrase per charter §1.5 explicitly
% labelled `%% Q8 minimal coverage stub`.
```

**Permitted Q8 stub shapes** (proposed at /speckit-implement T071-equivalent with project-owner approval; SRSW + type-check valid):
- `counter([], _).` — empty-stream termination
- `counter([clear|S], _) :- counter(S?, 0).` — no-op forwarding (or with state reset)
- `counter([up|S], State) :- N := State? + 1 | counter(S?, N?).` — increment forwarding
- `counter([down|S], State) :- N := State? - 1 | counter(S?, N?).` — decrement forwarding

**No other ch05 file uses the Q8 marker.** Per Q7 retraction, **no `%% --- DEMONSTRATION HELPERS ---` marker** appears in any ch05 file.

---

## Q10 dual amendment (ch05 NEW, ex-05 only)

Per Q10 + Q11 T4a/T4b/T4c/T4d empirical, ex-05 (§5.6 typed quicksort post-Q7+Q12) requires two amendments to load:

**Q10 Issue A — qsort declaration corrected**:
- PDF prints: `procedure qsort(NumList?, NumList?, NumList).` (consume/consume/produce)
- Book's prose + body call + clause heads agree on: `procedure qsort(NumList?, NumList, NumList?).` (consume/produce/consume)
- ex-05 declares the **corrected form**. The `%%` paraphrase comment on the qsort declaration documents the Q10 amendment with provenance.

**Q10 Issue B — interleaved layout**:
- PDF stacks all three procedure decls (`quicksort/2`, `qsort/3`, `partition/4`) at the top of §5.6, then all six clauses below
- REPL parser requires immediate-clause-after-decl (per Q11 T2 empirical: `[syntax] Procedure declaration … must be immediately followed by its clauses`)
- ex-05 **interleaves** declarations with their respective clauses

The file's HEADER block MUST explicitly document both Q10 amendments with provenance:

```
% Q10 dual amendment (ex-05 / §5.6 only):
%   Issue A — qsort declaration: PDF prints `procedure qsort(NumList?, NumList?, NumList).`
%             which contradicts the book's own prose ("qsort: consumes list, produces
%             accumulator head, consumes accumulator tail") + body call shape + clause
%             head shapes. This file declares the prose-consistent form
%             `procedure qsort(NumList?, NumList, NumList?).` per Q10 amendment.
%             Empirically confirmed: Q11 T4d shows the printed declaration causes
%             mode-mismatch errors at clause heads + body atoms.
%   Issue B — layout: PDF stacks the three procedure declarations at the top of §5.6
%             and clauses below. The REPL parser requires immediate-clause-after-decl,
%             so declarations and clauses are interleaved per Q10 amendment.
%             Empirically confirmed: Q11 T4a + T4b show stacked layout fails to parse.
% Clause text remains byte-exact PDF; only the LAYOUT and the qsort SIGNATURE are
% amended. Pedagogical content (typed sort algorithm, mode declarations, recursion)
% is preserved exactly.
```

---

## File 1 — `exercise-01/ch-05-ex-01-type-definitions.glp` (load-only, Foundations)

**Programs** (post-Q7 — NO helpers per Q7 retraction): §5.1.1 `Bit ::= 0 ; 1.` + §5.1.2 `Nat ::= 0 ; s(Nat).` + §5.1.3 `NumList ::= [] ; [Number | NumList].` byte-exact from book p 47.

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
% This is a LOAD-ONLY exercise per Q7 — type definitions are non-runnable book
% content. The load itself IS the demonstration that the type-checker accepts
% the byte-exact PDF code. No fabricated helpers per Q7 retraction (the pre-Q7
% Q2/R-012 helper authorisation has been retracted on grounds of literal-source
% mandate).
```

**Validation**:
- Exactly 3 type-definition declarations (byte-exact from PDF p 47).
- 3 `%%` per-Program sub-headers OR 3 `%%` per-declaration paraphrase comments (charter §1.5 — one short paraphrase line per declaration).
- **NO helper layer.** **NO `%% --- DEMONSTRATION HELPERS ---` marker** (Q7 retraction).
- 3 `%%` paraphrase comments total.
- Byte-exact verification per common rule 7 against PDF p 47, with NO helpers to exclude.

---

## File 2 — `exercise-02/ch-05-ex-02-built-in-types.glp` (load-only, Foundations)

**Programs** (post-Q7 — NO helpers per Q7 retraction): §5.2 `List ::= [] ; [Any | List].` + prose-paraphrase comments referencing built-in types `Number` / `Any` / `Atom`.

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
% This is a LOAD-ONLY exercise per Q7. No fabricated helpers per Q7 retraction.
```

**Validation**:
- Exactly 1 type-definition declaration (byte-exact from PDF p 48).
- 1 `%%` paraphrase comment.
- **NO helper layer.** **NO `%% --- DEMONSTRATION HELPERS ---` marker** (Q7 retraction).
- Byte-exact verification per common rule 7.

---

## File 3 — `exercise-03/ch-05-ex-03-mode-checked-merge.glp` (full-program, Mode-checking-flow)

**Programs** (post-Q7+Q4+Q5+Q12 — §5.3 + §5.4 merged per Q7): inline `List ::= [] ; [Any | List].` (universal type from §5.2 per Q4 — duplicated inline per FR-010 self-containment, NOT `NumList`) + `procedure merge(List?, List?, List).` byte-exact from PDF p 49 + 3 clauses byte-exact from PDF p 49 (Q5 RETRACTED — body text is byte-exact PDF as printed; the printed PDF on p 49 already shows `merge(Ys?, Xs?, Zs)` and `merge(Xs?, Ys?, Zs)` per Q11 T1 empirical confirmation; no `?`-additions needed).

```glp
List ::= [] ; [Any | List].

procedure merge(List?, List?, List).
merge([X|Xs], Ys, [X?|Zs?]) :- merge(Ys?, Xs?, Zs).
merge(Xs, [Y|Ys], [Y?|Zs?]) :- merge(Xs?, Ys?, Zs).
merge([], [], []).
```

**Header block** template:

```
% ch-05-ex-03-mode-checked-merge.glp
%
% This file presents the §5.3 procedure declaration + §5.4 typed merge/3 worked
% example, byte-exact from book p 49 (per Q11 T1 empirical confirmation; Q5 was
% RETRACTED 2026-05-01 — no `?`-additions, body text is byte-exact PDF as printed).
% §5.3 and §5.4 are MERGED into this single exercise per Q7 because the §5.3
% procedure declaration alone does not parse without immediate clauses (Q11 T2
% empirical confirmation).
%
% Cross-chapter relationship (per FR-002 + R-008): A related un-typed merge/3
% appears in ch04 ex-04 (book §4.2.5, p 32) as an un-typed simple fair merger;
% see olamni/tutorial/ch04/exercise-04/ch-04-ex-04-merge-variants.glp.
% The two are pedagogically distinct presentations: same procedure name; the ch05
% typed form carries an explicit `procedure merge(List?, List?, List).` declaration
% with `?` reader marks (using the universal `List ::= [] ; [Any | List].` type
% from §5.2 per Q4 — duplicated inline per FR-010 self-containment); the ch04
% untyped form has no procedure declaration at all (defaulting to GLP's implicit
% untyped behaviour). Different clause set (3 typed clauses in ch05 vs 4 untyped
% in ch04), different pedagogical focus (mode checking flow vs stream-merge
% implementations). This is a CROSS-CHAPTER RELATIONSHIP — not a code import.
% The .glp clauses below are byte-exact from §5.4 PDF, NOT copies of ch04's clauses.
%
% Programs included:
%   §5.2 (p 48): List ::= [] ; [Any | List]. — universal type (duplicated inline per FR-010)
%   §5.3 (p 48): procedure merge(List?, List?, List). — moded declaration
%   §5.4 (p 49): merge/3 — 3 clauses with `%%` mode-check walk-through annotations
%
% References Formal 5.2 (Mode Semantics, p 49). The `%%` annotations on each
% merge/3 clause walk through the head-mode proof and body-mode propagation
% steps from §5.4 prose IN ADDITION to the per-clause paraphrase per charter §1.5.
```

**Validation**:
- 1 type definition + 1 procedure declaration + 3 clauses (byte-exact from PDF p 49).
- 3 `%%` per-Program sub-headers + 5 `%%` paraphrase comments + 3 walk-through annotations on merge/3 clauses (per charter §1.5 + spec FR-005 + SC-017).
- Byte-exact verification per common rule 7.
- Header MUST contain canonical R-008 cross-reference block citing ch04 ex-04.
- **NO helper layer.** No Q8 stub marker (Q8 stubs are ex-04 only).

---

## File 4 — `exercise-04/ch-05-ex-04-counter-response-slot.glp` (full-program, Mode-checking-flow; with Q8 minimal coverage stubs)

**Programs** (post-Q7+Q4+Q6+Q8+Q12): byte-exact §5.5 from book p 50:

```glp
CounterMsg ::= clear ; up ; down ; show(Number?).
CounterStream ::= [] ; [CounterMsg | CounterStream].

procedure counter(CounterStream?, Number?).

counter([show(State?)|S], State) :-
    number(State?) |
    counter(S?, State?).

%% --- Q8 MINIMAL COVERAGE STUBS (type-checker exhaustiveness; book p 50 shows only the show clause; per spec Q8 amendment) ---
%% Q8 minimal coverage stub for CounterMsg's empty-stream termination.
counter([], _).
%% Q8 minimal coverage stub for clear alternative — no-op forwarding.
counter([clear|S], State) :- counter(S?, State?).
%% Q8 minimal coverage stub for up alternative — no-op forwarding.
counter([up|S], State) :- counter(S?, State?).
%% Q8 minimal coverage stub for down alternative — no-op forwarding.
counter([down|S], State) :- counter(S?, State?).
```

(Specific Q8 stub shapes — no-op forwarding vs increment/decrement — proposed at /speckit-implement T071-equivalent with project-owner approval. Above is a permitted shape; alternate shapes per "Permitted Q8 stub shapes" section above are also acceptable as long as they satisfy SRSW + type-check at REPL load.)

Per Q4: arg 2 of `counter` is `Number?` (consume mode), NOT plain `Number`. Per Q6: the show clause has guard `number(State?) |` + recursive body `counter(S?, State?).`, NOT a single response-slot head clause. The `number(State?)` guard is multi-reader-permissive per Formal 4.3 (ch04), authorising `State`'s 1W + 3R appearance. Mode Involution per Formal 5.3 applies: the embedded `Number?` inside `show(...)` of `CounterMsg`'s alternation, combined with the outer consume-mode `CounterStream?`, produces a writer slot at the embedded position (consume × consume = produce per Formal 5.3 table).

**Header block** template:

```
% ch-05-ex-04-counter-response-slot.glp
%
% This file presents the §5.5 typed counter with response-slot embedded mode,
% byte-exact from book p 50 (per Q4 + Q6 amendments), §5.5 "Embedded Modes:
% Response Slots" + Formal 5.3 "Mode Involution".
%
% Cross-chapter relationship (per FR-002 + R-008): A related un-typed counter/1
% + counter_loop/2 appears in ch04 ex-06 (book §4.2.14) as an un-typed
% object/monitor; see olamni/tutorial/ch04/exercise-06/ch-04-ex-06-buffered-and-monitors.glp.
% Different arity (1 → 2), different shape (no response-slot in ch04 vs response-slot
% in ch05), different pedagogical focus (objects/monitors vs embedded modes).
% This is a CROSS-CHAPTER RELATIONSHIP — not a code import.
%
% Q8 amendment (per spec): book p 50 shows ONLY the show response-slot clause;
% the type-checker requires exhaustive coverage of all CounterMsg alternatives
% (clear, up, down, show) plus the empty-stream case (Q11 T5 empirical:
% `counter argument 1: uncovered alternative "[]"`). The Q8 minimal coverage
% stubs below are NOT fabricated helpers per Q7 retraction; they are minimal
% completions for type-checker exhaustiveness with documented Q-amendment
% provenance, marked `%% --- Q8 MINIMAL COVERAGE STUBS ---`.
%
% Programs included:
%   §5.5 (p 50): CounterMsg ::= clear ; up ; down ; show(Number?). — type def with embedded `?`
%   §5.5 (p 50): CounterStream ::= [] ; [CounterMsg | CounterStream].
%   §5.5 (p 50): procedure counter(CounterStream?, Number?). (per Q4: arg 2 is Number?, not plain Number)
%   §5.5 (p 50): counter([show(State?)|S], State) :- number(State?) | counter(S?, State?). (per Q6: full clause has guard + body)
%   Q8 stubs: counter([], _) + counter([clear|S], State) + counter([up|S], State) + counter([down|S], State)
%
% References Formal 5.3 (Mode Involution, p 50): consume × consume = produce.
```

**Validation**:
- 2 type definitions + 1 procedure declaration + 1 byte-exact PDF clause + 4 Q8 stub clauses (byte-exact PDF section verifiable per common rule 7 with Q8 marker excluded).
- ~8 `%%` paraphrase comments (4 PDF + 4 Q8-stub).
- Byte-exact verification per common rule 7 against PDF p 50, with Q8 stubs excluded via the `%% --- Q8 MINIMAL COVERAGE STUBS ---` marker.
- Header MUST contain canonical R-008 cross-reference block citing ch04 ex-06.
- Q8 stubs MUST satisfy SRSW + type-check at REPL load.

---

## File 5 — `exercise-05/ch-05-ex-05-typed-quicksort.glp` (full-program, Flagship; with Q10 dual amendment)

**Programs** (post-Q7+Q10+Q12): inline `NumList ::= [] ; [Number | NumList].` (duplicated inline from ex-01 per FR-010 self-containment) + 3 procedure decls + 6 clauses byte-exact from book p 51, with Q10 dual amendment applied (corrected qsort signature per Q10 Issue A + interleaved layout per Q10 Issue B):

```glp
NumList ::= [] ; [Number | NumList].

procedure quicksort(NumList?, NumList).
quicksort(Unsorted, Sorted?) :- qsort(Unsorted?, Sorted, []).

procedure qsort(NumList?, NumList, NumList?).      %% Q10 corrected per prose + clauses; printed PDF shows `(NumList?, NumList?, NumList)` which contradicts the book's own prose + body call + clause heads
qsort([X|Unsorted], Sorted?, Rest) :- partition(Unsorted?, X?, Smaller, Larger), qsort(Smaller?, Sorted, [X?|Sorted1?]), qsort(Larger?, Sorted1, Rest?).
qsort([], Rest?, Rest).

procedure partition(NumList?, Number?, NumList, NumList).
partition([X|Xs], A, Smaller?, [X?|Larger?]) :- X? >= A? | partition(Xs?, A?, Smaller, Larger).
partition([X|Xs], A, [X?|Smaller?], Larger?) :- X? < A? | partition(Xs?, A?, Smaller, Larger).
partition([], A, [], []) :- number(A?) | true.
```

(Exact body shapes of `qsort/3` recursive clause + `partition/4` clauses are byte-exact PDF p 51; only the qsort signature swap and the interleaved layout are amendments. Implementer re-reads PDF byte-exact at /speckit-implement T092 to verify.)

**Header block** template:

```
% ch-05-ex-05-typed-quicksort.glp
%
% This file presents the §5.6 typed quicksort (the chapter's flagship Program),
% byte-exact from book p 51 with Q10 dual amendment, §5.6 "Complete Example:
% Typed Quicksort".
%
% Q10 dual amendment (ex-05 / §5.6 only):
%   Issue A — qsort declaration: PDF prints `procedure qsort(NumList?, NumList?, NumList).`
%             which contradicts the book's own prose ("qsort: consumes list, produces
%             accumulator head, consumes accumulator tail") + body call shape + clause
%             head shapes. This file declares the prose-consistent form
%             `procedure qsort(NumList?, NumList, NumList?).` per Q10 amendment.
%             Empirically confirmed: Q11 T4d shows the printed declaration causes
%             mode-mismatch errors at clause heads + body atoms.
%   Issue B — layout: PDF stacks the three procedure declarations at the top of §5.6
%             and clauses below. The REPL parser requires immediate-clause-after-decl,
%             so declarations and clauses are interleaved per Q10 amendment.
%             Empirically confirmed: Q11 T4a + T4b show stacked layout fails to parse;
%             Q11 T4c shows interleaved + corrected loads cleanly.
% Clause text remains byte-exact PDF; only the LAYOUT and the qsort SIGNATURE are
% amended. Pedagogical content (typed sort algorithm, mode declarations, recursion)
% is preserved exactly.
%
% Programs included:
%   §5.6 (p 51): NumList ::= [] ; [Number | NumList]. — type def (inline; duplicated from ex-01 per FR-010 self-containment)
%   §5.6 (p 51): procedure quicksort(NumList?, NumList).
%   §5.6 (p 51): procedure qsort(NumList?, NumList, NumList?). — Q10-corrected
%   §5.6 (p 51): procedure partition(NumList?, Number?, NumList, NumList).
%   §5.6 (p 51): 6 clauses of quicksort/2 + qsort/3 + partition/4
%
% This is the chapter's flagship — it composes everything from §5.1–§5.5 into a
% complete typed Program: type definitions, procedure declarations with mode
% annotations, recursion across multiple typed predicates.
```

**Validation**:
- 1 type def + 3 procedure decls (1 with Q10-corrected signature) + 6 clauses (byte-exact PDF p 51 with Q10 layout interleaving applied).
- ~10 `%%` paraphrase comments + 1 Q10-amendment provenance comment on the qsort declaration.
- Byte-exact verification per common rule 7 with Q10 deviations documented (qsort signature swap + interleaved layout — both authorised at spec layer).
- Header MUST contain Q10 dual amendment provenance block.

---

## File 6a — `exercise-06/ch-05-ex-06-type-error-failing.glp` (negative, Negatives)

**Programs**: §5.7.1 `foo/1` failing form — load MUST FAIL with type-error message (book p 51, byte-exact). Per Q11 T3 empirical (REPL build `bcd59392`, 2026-05-01), the load fails with 3-line message:

```
Inconsistent path: Number type requires numeric literal Path: ([|]/2, 0, output) → (a, 1, output) at line 5
```

(plus analogous lines for `b` and `c`; full byte-equality holds — no per-run-varying segments).

```glp
procedure foo(NumList).
foo([a, b, c]).
```

**Header block** template:

```
% ch-05-ex-06-type-error-failing.glp
%
% ⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠
%
% This file presents the §5.7.1 type-error illustration from book p 51, byte-exact
% from PDF. The file's purpose is to demonstrate the type-checker's rejection
% behaviour. When loaded into the GLP REPL, the load MUST fail with a type-error
% message documenting that a non-Number value (e.g., the atom 'a') does not
% satisfy the declared NumList type (whose element type is Number).
%
% Programs included:
%   §5.7.1 (p 51): procedure foo(NumList).
%   §5.7.1 (p 51): foo([a, b, c]). — the type-error trigger
%
% See ch-05-ex-06-type-error-corrected.glp for a re-typed form that loads
% successfully.
%
% Per spec FR-014 + Q11 T3 empirical, the captured error message is byte-equal
% to the actual REPL output for the current REPL build (`bcd59392`); no per-run-varying
% segments were observed; full byte-equality holds; R-011 relaxation NOT triggered.
% If a future REPL build introduces per-run-varying segments, R-011's halt-and-amend
% procedure applies.
```

**Validation**:
- Exactly 1 procedure declaration + 1 clause (byte-exact from PDF p 51).
- 2 `%%` paraphrase comments.
- Byte-exact verification per common rule 7.
- Load MUST FAIL with the Q11 T3 captured message (verifiable via the captured trace's Phase A).

## File 6b — `exercise-06/ch-05-ex-06-type-error-corrected.glp` (negative, Negatives)

**Programs**: corrected `foo/1` form — load succeeds. Exact corrected shape proposed at /speckit-implement T114-equivalent with project-owner approval (book p 51 does NOT cite a specific corrected form; common shapes: re-typing the procedure declaration to accept the offending value's type, OR fixing the clause body to produce a value matching the declared type).

**Header block** template:

```
% ch-05-ex-06-type-error-corrected.glp
%
% Companion to ch-05-ex-06-type-error-failing.glp — this file presents a
% corrected form of foo/1 that LOADS SUCCESSFULLY, demonstrating the fix for
% the §5.7.1 type-error illustration.
%
% The exact corrected shape is proposed during /speckit-implement T114-equivalent
% with project-owner approval recorded in the per-exercise tutorial. Common shapes:
% re-typing the procedure declaration to accept the offending value's type (e.g.,
% if `procedure foo(List).` accepts atom values), OR fixing the clause body to
% produce a value matching the declared NumList type (e.g., `foo([1, 2, 3]).`).
%
% This file demonstrates that the rejection is fixable; the load succeeds with
% `✓ Loaded:` and zero errors.
```

**Validation**:
- 1 procedure declaration + 1 clause (corrected form; project-owner-approved).
- 2 `%%` paraphrase comments.
- Load MUST succeed (verifiable via the captured trace's Phase B).

---

## File 7a — `exercise-07/ch-05-ex-07-mode-error-failing.glp` (negative, Negatives)

**Programs**: §5.7.2 `bar/2` failing form — load MUST FAIL with mode-error message (book pp 51–52, byte-exact). Per Q11 T6 empirical, the load fails with 2-line message:

```
Variable mode mismatch: writer requires ↑ (produce), got ↓ (consume) Path: (X, 0, input)
reader requires ↓ (consume), got ↑ (produce) Path: (Y?, 0, output) at line 3
```

(full byte-equality holds — no per-run-varying segments).

```glp
procedure bar(Number?, Number).
bar(X?, Y).
```

**Header block** template:

```
% ch-05-ex-07-mode-error-failing.glp
%
% ⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠
%
% This file presents the §5.7.2 mode-error illustration from book pp 51–52,
% byte-exact from PDF. When loaded into the GLP REPL, the load MUST fail with
% a mode-error message documenting that the clause's reader/writer roles
% violate the procedure declaration (X is declared consume but appears as
% reader X? in clause head; Y is declared produce but appears as writer Y in
% clause head).
%
% Programs included:
%   §5.7.2 (pp 51–52): procedure bar(Number?, Number).
%   §5.7.2 (pp 51–52): bar(X?, Y). — the mode-error trigger
%
% See ch-05-ex-07-mode-error-corrected.glp for the book-cited corrected form
%   bar(X, Y?) :- Y := X? + 1.
% from book p 52 which loads successfully (Q11 T7 empirical).
```

**Validation**:
- 1 procedure declaration + 1 clause (byte-exact from PDF pp 51–52).
- 2 `%%` paraphrase comments.
- Byte-exact verification per common rule 7.
- Load MUST FAIL with the Q11 T6 captured message.

## File 7b — `exercise-07/ch-05-ex-07-mode-error-corrected.glp` (negative, Negatives)

**Programs**: book-cited corrected form `bar(X, Y?) :- Y := X? + 1.` from book p 52, byte-exact.

```glp
procedure bar(Number?, Number).
bar(X, Y?) :- Y := X? + 1.
```

**Header block** template:

```
% ch-05-ex-07-mode-error-corrected.glp
%
% Companion to ch-05-ex-07-mode-error-failing.glp — this file presents the
% book-cited corrected form
%   bar(X, Y?) :- Y := X? + 1.
% from book p 52, byte-exact. Loads SUCCESSFULLY (Q11 T7 empirical),
% demonstrating the fix for the §5.7.2 mode-error illustration.
%
% Uses the := body kernel (introduced for ch02 territory; permitted here per
% ch03 FR-015 amendment because it appears in a byte-exact PDF clause).
```

**Validation**:
- 1 procedure declaration + 1 clause (byte-exact from PDF p 52).
- 2 `%%` paraphrase comments.
- Byte-exact verification per common rule 7.
- Load MUST succeed (per Q11 T7).
- Optional Phase C of the trace exercises `bar(5, R).` ⇒ `R = 6` to demonstrate the fix actually works.

---

## Cross-file invariants

- ex-03's typed `merge/3` clauses (post-Q7+Q12) are byte-exact from §5.4 PDF, NOT byte-identical to ch04 ex-04's untyped `merge/3` clauses. The cross-chapter RELATIONSHIP is a header citation + signpost prose, not byte equality.
- ex-04's typed `counter/2` clause (post-Q7+Q12) is byte-exact from §5.5 PDF, NOT byte-identical to ch04 ex-06's untyped `counter/1`. Same relationship pattern. Q8 stubs are NOT cross-chapter related.
- Each exercise's `.glp` is self-contained per FR-010; `NumList` reused in ex-01 + ex-05 is duplicated inline byte-exact (NOT in a shared `types.glp`); `List` is duplicated inline in ex-02 + ex-03 (NOT shared).
- Per-clause `%%` paraphrase comments MAY differ across files even for duplicated type definitions, because each file's pedagogical context differs.
- **NO `%% --- DEMONSTRATION HELPERS ---` marker** in any ch05 file (Q7 retraction).
- **`%% --- Q8 MINIMAL COVERAGE STUBS ---` marker appears in ex-04 ONLY** (Q8 amendment).
- Negative failing-form files MUST be marked `⚠ THIS FILE IS MEANT TO FAIL TO LOAD ⚠` in the header block for clarity.

---

## Constitution alignment

- Principle III (SRSW Discipline) — all PDF-sourced clauses in all files are SRSW-compliant by byte-exact construction (the book's Programs are SRSW-valid; implementer copies byte-exact). Q8 minimal coverage stubs (ex-04 only) MUST also satisfy SRSW (they are no-op forwarding clauses with simple writer/reader pair structure).
- Principle VI (Tutorial Charter Compliance) — `%%` per-clause comments per charter §1.5 across all files including Q8 stubs and corrected-form clauses.
- Language Design Authority — no new kernels / guards / system predicates / type-system features introduced; the type-system + mode declarations + `procedure` keyword + `Any`/`Number`/`Atom` built-ins + `:=` body kernel + `number/1` guard all PRE-EXIST.
