# Contract — `.glp` File Content & Comment Format (chapter 3)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-30

This contract defines the content and comment format for the four `.glp` files in chapter 3. It inherits the ch01 + ch02 single-file contracts and adds chapter-3-specific shape locks for (a) Program 3.1 byte-exact from p 15, (b) the cross-chapter `producer/2` + `consumer/3` import from p 31, (c) `channel/1` + `process/2` byte-exact from p 22 with a local `handle/1` stub, (d) `lookup/3` byte-exact from p 22 with both clauses (positive `=?=` and negated `~(=?=)`).

---

## Common rules (apply to all four files)

1. **Header comment block** — each file MUST begin with a `%`-prefixed comment block (3–8 lines) summarising what the file does and citing the PDF source.
2. **Per-clause `%%` comments** — each non-trivial clause MUST carry one `%%` comment paraphrasing the surrounding prose from the relevant book section. (Charter §1.5.)
3. **No `skipSRSW` or anti-spec language flags** — Constitution Principle III is non-negotiable.
4. **No external imports beyond `programs/self.glp`** (which is auto-loaded by the REPL) and the locked cross-chapter `producer/2` + `consumer/3` from PDF p 43. Per spec FR-015 + Clarifications Q1.
5. **Byte-exactness of imported clauses** — Program 3.1's three `merge/3` clauses MUST be byte-identical to PDF p 15 (per spec SC-006, the standalone-clause subset). The cross-chapter `producer/2` + `consumer/3` clauses MUST be byte-identical to PDF p 43 (per spec SC-007). The §3.2 `channel/1` + `process/2` + `lookup/3` clauses MUST be byte-identical to PDF p 34.
6. **Body kernel scope** — `:=` is permitted ONLY inside the byte-exact `producer/2` + `consumer/3` clauses (per spec FR-015 amendment). NO ch3-introduced procedure (Program 3.1's clauses, `channel/1`, `process/2`, locally-defined `handle/1`, `lookup/3`) may use `:=`, `now/1`, `'_output'/1`, or any other body kernel.
7. **Byte-identical clause corpus — precise definition**. The "byte-identical" verification (per spec SC-006 + SC-007) is performed as follows:
   - **Step 1**: Remove the file's header comment block (every line starting with `%` at the top of the file, up to the first non-comment line).
   - **Step 2**: For each remaining clause, remove ANY line whose first non-whitespace character is `%` (this catches both `%`-prefix comments and `%%`-prefix paraphrase comments, including those interspersed inside multi-line clause bodies).
   - **Step 3**: Trim trailing whitespace from each remaining line; preserve internal whitespace (indentation within multi-line clause bodies must match the PDF).
   - **Step 4**: The resulting line sequence MUST equal the PDF clause corpus byte-for-byte.
   - For multi-line clause bodies (e.g., `consumer/3` in File 2 with three body lines under the `:- ground(X?) |` guard), the verification compares each non-comment line individually; the relative order of lines must match the PDF, but `%%` annotations interspersed between body lines are stripped before comparison. This rule applies to T011 + T012 verification subtasks in tasks.md.

---

## File 1 — `exercise-01/ch-03-ex-01-glp-fair-stream-merger.glp`

**Purpose**: Program 3.1 (GLP Fair Stream Merger) byte-exact from PDF p 15. The chapter's anchor — the canonical SRSW fair merger that motivates the entire ch3 tutorial.

**Content** (illustrative — actual prose comes from the implementer rereading PDF p 15 + §3.1 prose during /speckit-implement step 3):

```
% ch-03-ex-01-glp-fair-stream-merger.glp
%% Program 3.1 (GLP Fair Stream Merger) byte-exact from "The Art of Grassroots Logic Programming"
%% (Shapiro, 2025), §3.1, p 15. The canonical example illustrating SRSW reader/writer pairs
%% (Reader/Writer pair invariant), the SO Invariant, and the fair-merge alternation via
%% argument-swap recursion. Each clause's `?` annotations identify which positions are
%% readers (consume bound writers) and which are writers (produce bindings).
%% This file is loaded into ex-01's REPL session alongside ch-03-ex-01-producer-consumer.glp
%% to form a producer-merger-consumer pipeline.

merge([X|Xs],Ys,[X?|Zs?]) :- merge(Ys?,Xs?,Zs).  %% output from first stream — head's X is forwarded to output; recursion swaps args for fairness
merge(Xs,[Y|Ys],[Y?|Zs?]) :- merge(Xs?,Ys?,Zs).  %% output from second stream — head's Y is forwarded; recursion preserves args (no swap needed; symmetric to clause 1)
merge([],[],[]).                                 %% terminate on empty streams — base case
```

**Validation rules**:
- The three clauses MUST be byte-identical to Program 3.1 on PDF p 15 after stripping the header comment block AND the per-clause `%%` annotations (per spec SC-006). Specifically, the three-line code corpus is:
  ```
  merge([X|Xs],Ys,[X?|Zs?]) :- merge(Ys?,Xs?,Zs).
  merge(Xs,[Y|Ys],[Y?|Zs?]) :- merge(Xs?,Ys?,Zs).
  merge([],[],[]).
  ```
- Header MUST cite Program 3.1 + book p 15 + §3.1 (per spec FR-001).
- File MUST be ACCEPTED by the GLP REPL with zero errors. Loading it alongside `ch-03-ex-01-producer-consumer.glp` MUST NOT cause a procedure-redeclaration conflict (only `merge/3` is defined here; producer/2 + consumer/3 live in the other file).
- File MUST NOT contain any body kernel (`:=`, `now/1`, `'_output'/1`) — Program 3.1's body uses only `merge/3` recursion with no kernel calls.

---

## File 2 — `exercise-01/ch-03-ex-01-producer-consumer.glp`

**Purpose**: Cross-chapter import of `producer/2` + `consumer/3` from PDF p 43 (book p 31, §4.2.1 + §4.2.2). Composed with Program 3.1 in ex-01's primary goal to form a producer-merger-consumer pipeline.

**Content** (illustrative; the canonical R-007 provenance lines and the byte-exact clauses):

```
% ch-03-ex-01-producer-consumer.glp
%% producer/2 byte-exact from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §4.2.1, p 31.
%% consumer/3 byte-exact from same source, §4.2.2, p 31.
%% Imported into ch03 to compose with Program 3.1 into a producer-merger-consumer pipeline that
%% demonstrates SRSW reader/writer pairing across four roles using only built-in guards (`>` and `ground`).
%% This is the only cross-chapter import permitted in ch03 per the spec's Out-of-Scope section.
%% The `:=` body kernel inside producer/2's recursive clause and consumer/3's recursive clause is
%% inherited byte-exact from the import per the spec FR-015 amendment (Clarifications Q1).

producer([], 0).                                                              %% producer base: when count is zero, the stream is empty
producer([N?|Xs?], N) :- N? > 0 | N1 := N? - 1, producer(Xs, N1?).            %% producer recursive: emit N at head, recurse on tail with N-1; built-in guard `>` ensures positive count
consumer([], Sum, Sum?).                                                      %% consumer base: when stream is empty, accumulator becomes the result via writer/reader pair Sum/Sum?
consumer([X|Xs], Sum, Result?) :- ground(X?) |                                %% consumer recursive: built-in guard `ground` waits until X is fully bound
    Sum1 := Sum? + X?,                                                        %%   compute new accumulator
    consumer(Xs?, Sum1?, Result).                                             %%   recurse on tail with new accumulator (Formal 4.2: continuation calls pass readers Xs?, Sum1?)
```

**Validation rules**:
- The four clauses (2 producer + 2 consumer) MUST be byte-identical to PDF p 43 after stripping the header comment block AND the per-clause `%%` annotations (per spec SC-007). Specifically:
  ```
  producer([], 0).
  producer([N?|Xs?], N) :- N? > 0 | N1 := N? - 1, producer(Xs, N1?).
  consumer([], Sum, Sum?).
  consumer([X|Xs], Sum, Result?) :- ground(X?) |
      Sum1 := Sum? + X?,
      consumer(Xs?, Sum1?, Result).
  ```
- Header MUST contain the canonical R-007 provenance block (six lines as documented in `research.md` R-007).
- File MUST be ACCEPTED by the GLP REPL with zero errors when loaded alone OR alongside `ch-03-ex-01-glp-fair-stream-merger.glp`.
- The `:=` operator appears inside `producer/2`'s recursive clause and `consumer/3`'s recursive clause; this is permitted by the FR-015 amendment because the surrounding clause text is byte-identical to PDF p 43.
- Built-in guards `>` (in `producer/2` recursive) and `ground` (in `consumer/3` recursive) — these are pre-existing, declared in `programs/self.glp`.

---

## File 3 — `exercise-02/ch-03-ex-02-defined-guards.glp`

**Purpose**: ex-02's defined-guard demo. Defines `channel/1` + `process/2` byte-exact from PDF p 34 (book p 22, §3.2) plus a local `handle/1` stub (per `research.md` R-008). Stand-alone — does NOT duplicate Program 3.1's `merge/3` (per `research.md` R-009).

**Content** (illustrative; final form composes per `research.md` R-008 + R-009):

```
% ch-03-ex-02-defined-guards.glp
%% This file extends the ex-01 §3.2 curriculum: ex-01 used built-in guards only (`>`, `ground`).
%% ex-02 introduces DEFINED guards from §3.2 (book p 22). A defined guard is a unit clause or
%% short procedure that the compiler unfolds at guard sites — extending the guard vocabulary
%% beyond the built-in set while remaining bound by SRSW reader-position rules.
%% channel/1 + process/2 byte-exact from "The Art of Grassroots Logic Programming"
%% (Shapiro, 2025), §3.2, p 22. Per `research.md` R-008, handle/1 is defined locally as a
%% minimal stub (the book leaves handle/1 undefined as a placeholder for downstream processing).
%% This file is STAND-ALONE (per R-009): no Program 3.1 / merge/3 duplication is required
%% because the locked primary goal `process(ch(a, b), Status).` does not exercise merge/3.

%% Defined guard: channel-shaped term test (book p 22)
channel(ch(_, _)).

%% process/2 first clause: defined-guard dispatch (book p 22). The `channel(X?)` guard unfolds
%% to a structural match against `ch(_, _)`; succeeds for ch-shaped X, falls through otherwise.
process(X, ok)    :- channel(X?) | handle(X?).
%% process/2 second clause: otherwise fallback (book p 22). When channel/1 fails on clause 1,
%% the built-in `otherwise` guard succeeds and binds Status to error.
process(_, error) :- otherwise   | true.

%% handle/1 local stub (per research.md R-008). The book uses `handle(X?)` in process/2's body
%% as a placeholder for downstream processing; ch3 ex-02's pedagogy is the defined-guard machinery,
%% not handle's behaviour, so a tautological unit clause is sufficient.
handle(_).
```

**Validation rules**:
- The `channel/1` unit clause MUST be byte-identical to `channel(ch(_, _)).` from PDF p 34 / book p 22.
- The two `process/2` clauses MUST be byte-identical to PDF p 34 / book p 22. Specifically:
  ```
  process(X, ok)    :- channel(X?) | handle(X?).
  process(_, error) :- otherwise   | true.
  ```
- The `handle/1` clause is LOCAL to this file (NOT byte-exact from book — the book leaves `handle/1` undefined). It MUST be a single tautological unit clause `handle(_).` per R-008.
- File MUST NOT define `merge/3`, `producer/2`, or `consumer/3` — those are NOT exercised by ex-02's primary or inspection goals (per R-009 stand-alone decision).
- File MUST NOT use any body kernel (`:=`, `now/1`, `'_output'/1`) — none of `channel/1`, `process/2`, or `handle/1` requires arithmetic or I/O.
- File MUST NOT load any other file as a dependency.
- File MUST be ACCEPTED by the GLP REPL with zero errors. Running `process(ch(a, b), Status).` MUST bind `Status = ok` (per spec FR-009 locked binding).

---

## File 4 — `exercise-03/ch-03-ex-03-guard-negation.glp`

**Purpose**: ex-03's guard-negation demo. Defines `lookup/3` byte-exact from PDF p 34 (book p 22, §3.2) with BOTH clauses — first clause uses positive `=?=`, second clause uses the `~(=?=)` negation form on the same operator. Stand-alone — does NOT duplicate Program 3.1's `merge/3` or ex-02's `channel/1` + `process/2` (per `research.md` R-009).

**Content** (illustrative):

```
% ch-03-ex-03-guard-negation.glp
%% This file completes the ex-01/ex-02/ex-03 §3.2 curriculum: ex-01 used built-in guards (`>`, `ground`);
%% ex-02 introduced defined guards (`channel/1`); ex-03 introduces GUARD NEGATION (`~(...)` form).
%% The `~(...)` form is restricted to negatable built-in guards per the §3.2 SRSW Rules for
%% Defined Guards table on book p 24: built-in `=?=` is negatable; defined guards (e.g., ex-02's
%% `channel/1`) are NOT negatable. ex-03 demonstrates positive `=?=` (clause 1) and negated
%% `~(=?=)` (clause 2) on the SAME operator.
%% lookup/3 byte-exact from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §3.2, p 22.
%% This file is STAND-ALONE (per R-009): no merge/3 or channel/process duplication is required
%% because the locked primary goal `lookup(b, [(a,1),(b,2),(c,3)], V).` does not exercise them.

%% lookup/3 first clause: positive equality test guard. Built-in `=?=` succeeds when Key matches
%% the head's K — clause 1 fires immediately and binds V to the head's value via writer/reader
%% pair V/V?.
lookup(Key, [(K,V)|_], V?) :- Key? =?= K? | true.
%% lookup/3 second clause: NEGATED equality test guard. The `~(...)` form negates `=?=`,
%% succeeding when Key does NOT match the head's K — clause 2 fires and the recursion descends
%% into the rest of the list.
lookup(Key, [(K,_), Rest], V?) :- ~(Key? =?= K?) | lookup(Key, Rest?, V).
```

**NOTE on the second clause's head pattern**: the book's `lookup/3` second clause head is `lookup(Key, [(K,_)|Rest], V?)` — i.e., a cons cell `[(K,_)|Rest]` where Rest is the tail. The implementer MUST re-read PDF p 34 byte-exactly during /speckit-implement to confirm whether the book uses `[(K,_)|Rest]` (cons-with-tail) or `[(K,_), Rest]` (two-element list with Rest as second element). The illustrative content above shows the more likely cons-with-tail form per typical recursion patterns; correct via byte-exact PDF re-read if needed (per R-006 + ch01's predict-and-verify lesson).

**Validation rules**:
- Both `lookup/3` clauses MUST be byte-identical to PDF p 34 / book p 22 after stripping the header comment block AND the per-clause `%%` annotations.
- File MUST NOT define `merge/3`, `producer/2`, `consumer/3`, `channel/1`, `process/2`, or `handle/1` — those are NOT exercised by ex-03's primary or inspection goals (per R-009 stand-alone decision).
- File MUST NOT use any body kernel (`:=`, `now/1`, `'_output'/1`) — `lookup/3`'s body is pure recursion with the `=?=` guard test.
- File MUST NOT load any other file as a dependency.
- File MUST be ACCEPTED by the GLP REPL with zero errors. Running `lookup(b, [(a,1),(b,2),(c,3)], V).` MUST bind `V = 2` (per spec FR-010 locked binding).
- The `~(...)` form MUST be applied to `=?=` (a built-in negatable guard) ONLY. The file MUST NOT contain `~(channel(...))` or any other defined-guard negation (per §3.2 SRSW Rules for Defined Guards table on book p 24).

---

## Cross-file invariants

- Program 3.1's `merge/3` (in File 1) is loaded ONLY in ex-01's REPL session (alongside File 2). ex-02 (File 3) and ex-03 (File 4) do NOT duplicate `merge/3` inline — the conditional-duplication rule from FR-009 / FR-010 + R-009 elects stand-alone shapes for both.
- The cross-chapter `producer/2` + `consumer/3` (in File 2) is loaded ONLY in ex-01's REPL session. ex-02 and ex-03 do NOT duplicate them.
- Per-clause `%%` paraphrase comments MAY differ across files even for the duplicated clauses (none in ch3 per R-009, but the rule is preserved for parallelism with ch02). Each file's pedagogical context is independent.
- The chapter's three locked primary goals are file-disjoint:
  - ex-01 primary references procedures from File 1 + File 2.
  - ex-02 primary references procedures from File 3 only.
  - ex-03 primary references procedures from File 4 only.

---

## Constitution alignment

- Principle III (SRSW Discipline) — all four files are SRSW-compliant. Program 3.1 is the canonical SRSW fair merger; producer/2 + consumer/3 are SRSW-compliant book examples; channel/1 + process/2 + lookup/3 are SRSW-compliant §3.2 idioms.
- Principle VI (Tutorial Charter Compliance) — `%%` per-clause comments per charter §1.5; cross-chapter import documented per `research.md` R-007.
- Language Design Authority — no new kernels introduced; `:=` (used inside the byte-exact ch4 import) is pre-existing per ch2 territory; `=?=`, `~(...)`, `>`, `ground`, `otherwise`, `channel/1` (as a defined guard mechanism) are all pre-existing in the GLP language.
