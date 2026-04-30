# Contract — `.glp` File Content & Comment Format (chapter 4)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-30

This contract defines the content and comment format for the 10 `.glp` files in chapter 4. It inherits the ch01–ch03 single-Program / few-Program file contracts and adapts to the chapter-4 multi-Program-per-file pattern.

---

## Common rules (apply to all 10 files)

1. **Header comment block** — each file MUST begin with a `%`-prefixed comment block (5–15 lines for ch04 due to multi-Program scope) summarising what the file does + citing PDF source(s) + listing the Programs included + noting any relevant Formal box.
2. **Per-Program sub-header** — for multi-Program exercises, each new Program in the file is preceded by a 1–2 line `%%` sub-header naming the Program + its book sub-section reference (e.g., `%% §4.1.3 — logic gates and/3, or/3, not/2, xor/3`).
3. **Per-clause `%%` paraphrase comments** — each clause MUST carry one `%%` comment paraphrasing the surrounding prose from the relevant book section (charter §1.5).
4. **No `skipSRSW` or anti-spec language flags** — Constitution Principle III is non-negotiable.
5. **No external imports beyond `programs/self.glp`** (auto-loaded by the REPL). Per spec FR-015, ch04 has no cross-chapter imports (the `producer/2` + `consumer/3` reclaim is a NATIVE presentation, not an import).
6. **Byte-exactness** — every clause text MUST be byte-identical to the PDF source. The /speckit-implement verification subtask compares the file's clause text (after stripping the header comment block + per-Program sub-headers + per-clause `%%` annotations per ch03 contract rule 7) against the byte-exact PDF transcription.
7. **Byte-identical clause corpus — precise definition** (inherited from ch03 contract rule 7):
   - Step 1: Remove the file's header comment block (every line starting with `%` at the top of the file, up to the first non-comment line).
   - Step 2: For each remaining clause, remove ANY line whose first non-whitespace character is `%` (this catches both `%`-prefix comments, `%%`-prefix paraphrase comments, and `%%`-prefix per-Program sub-headers).
   - Step 3: Trim trailing whitespace from each remaining line; preserve internal whitespace (indentation within multi-line clause bodies must match the PDF).
   - Step 4: The resulting line sequence MUST equal the PDF clause corpus byte-for-byte.
   - Per-Program sub-headers (e.g., `%% §4.1.3 — logic gates ...`) are stripped at Step 2 the same as `%%` paraphrase comments.

---

## File 1 — `exercise-01/ch-04-ex-01-constants-and-gates.glp`

**Programs**: 4.1.1 `p(a)` (1 unit clause) + 4.1.2 `q(b)/q(a)` (2 unit clauses) + 4.1.3 logic gates `and/3` + `or/3` + `not/2` + `xor/3` (14 unit clauses total).

**Header block** template:

```
% ch-04-ex-01-constants-and-gates.glp
%
% This file presents the §4.1.1 + §4.1.2 + §4.1.3 unit-clause Programs from
% "The Art of Grassroots Logic Programming" (Shapiro, 2025), book pp 25–28
% (PDF pp 37–40). All Programs in this file are byte-exact from the PDF.
%
% Programs included:
%   §4.1.1 (p 25): p(a) — single unit clause demo
%   §4.1.2 (p 27): q(b), q(a) — multi-clause committed-choice demo
%   §4.1.3 (p 28): logic gates and/3, or/3, not/2, xor/3 (14 unit clauses)
%
% No clauses with bodies; no guards; no recursion. ex-02 builds on these
% gates to construct compound circuits (nand, half_adder, full_adder).
```

**Validation**:
- 17 unit clauses total (1 + 2 + 14).
- 17 `%%` paraphrase comments (one per clause).
- 3 `%%` per-Program sub-headers.
- Byte-exact verification per common rule 7 against PDF book pp 25–28.

---

## File 2 — `exercise-02/ch-04-ex-02-compound-circuits.glp`

**Programs**: 4.1.4 `nand/3` (1 clause with body) + 4.1.5 `half_adder/4` (1 clause with body + `ground` guards on multi-readers) + 4.1.6 `full_adder/5` (1 clause composing two half_adders + or).

**Header block** template:

```
% ch-04-ex-02-compound-circuits.glp
%
% This file presents the §4.1.4–§4.1.6 compound-circuit Programs from book
% pp 29–30 (PDF pp 41–42). All Programs are byte-exact from the PDF.
%
% Programs included:
%   §4.1.4 (p 29): nand/3 — first clause-with-body, composing and/3 + not/2
%   §4.1.5 (p 29): half_adder/4 — `ground` guards on multi-reader head positions
%   §4.1.6 (p 30): full_adder/5 — compound circuit composing two half_adders + or/3
%
% References Formal 4.1 (Produces and Consumes Parameters, p 29) and Formal 4.3
% (Which Guards Enable Multiple Reader Occurrences, pp 35–36).
%
% This file STAND-ALONE — does NOT load ex-01's logic-gates file as a dependency.
% Per FR-010 self-containment, all gate procedures (and/3, or/3, not/2, xor/3)
% used here are duplicated inline from ex-01 byte-exact.
```

**Validation**:
- 3 clauses-with-bodies (nand, half_adder, full_adder) + 14 duplicated unit clauses (and/or/not/xor) = 17 clauses total.
- 17 `%%` paraphrase comments + 3 `%%` per-Program sub-headers + 1 `%%` "duplicated from ex-01 per self-containment rule" sub-header.
- Byte-exact: nand/half_adder/full_adder clauses byte-exact from book pp 29–30; duplicated and/or/not/xor clauses byte-exact from book p 28.

---

## File 3 — `exercise-03/ch-04-ex-03-producer-consumer-reverse.glp`

**Programs**: 4.2.1 `producer/2` + 4.2.2 `consumer/3` (cross-chapter inversion native home) + 4.2.3 naive `reverse/2` + `append/3` + 4.2.4 acc `reverse/2` + `reverse_acc/3`.

**Header block** template (per research R-007):

```
% ch-04-ex-03-producer-consumer-reverse.glp
%
% This file presents producer/2 + consumer/3 in their NATIVE chapter-4 home,
% byte-exact from book p 31 (PDF p 43), §4.2.1 + §4.2.2 "Producers and Consumers".
% These same procedures appear in ch03 ex-01 as a cross-chapter forward import
% (see olamni/tutorial/ch03/exercise-01/ch-03-ex-01-producer-consumer.glp); the
% byte-exact code corpus is identical, but the surrounding `%%` paraphrase context
% differs: ch03's header cites the cross-chapter import provenance, this file's
% header paraphrases the §4.2.1 + §4.2.2 native prose.
%
% Programs included:
%   §4.2.1 (p 31): producer/2 — countdown from N
%   §4.2.2 (p 31): consumer/3 — sums stream elements; uses Formal 4.2 SRSW-in-continuation-calls
%   §4.2.3 (p 31): reverse/2 naive + append/3 (O(n²))
%   §4.2.4 (p 32): reverse/2 with accumulator + reverse_acc/3 (linear)
%
% References Formal 4.2 (SRSW in Continuation Calls, p 31).
```

**Validation**:
- ~9 clauses total (2 producer + 2 consumer + 2 naive reverse + 1 append + 1 reverse-entry + 2 reverse_acc).
- producer/2 + consumer/3 clause text byte-identical to ch03's `ch-03-ex-01-producer-consumer.glp` (per FR-002 + SC-007). Verifiable via `diff` modulo headers + `%%`.

---

## File 4 — `exercise-04/ch-04-ex-04-merge-variants.glp`

**Programs**: 4.2.5 simple `merge/3` (4 clauses) + 4.2.6 `dmerge/3` + `dmerger/3` (8 clauses) + 4.2.7 `merge_tree/2` + `merge_layer/2` (5 clauses).

**Header block** + ~17 clauses + 3 sub-headers + 17 `%%` paraphrases.

---

## File 5 — `exercise-05/ch-04-ex-05-stream-operators.glp`

**Programs**: 4.2.8 `distribute/3` (2 clauses) + 4.2.9 `distribute_indexed/3` (3 clauses) + 4.2.10 `observer/3` (2 clauses) + 4.2.11 `adder/4` ripple-carry (2 clauses).

**Note (per Q2 retraction)**: `distribute_indexed/3` works correctly with structs-in-lists in REPL goals; no special handling needed.

**Header block** + 9 clauses + 4 sub-headers + 9 `%%` paraphrases.

ex-05 may need duplicated `full_adder/5` + `half_adder/4` + gates from ex-02 inline if the ripple-carry adder primary goal needs them at REPL load (per FR-010 self-containment). Implementer decides during /speckit-implement based on the locked primary goal shape.

---

## File 6 — `exercise-06/ch-04-ex-06-buffered-and-monitors.glp`

**Programs**: 4.2.12 `bb/0` sliding-window (varies; ~3 clauses) + 4.2.13 `bb_test/0` (varies; ~3 clauses) + 4.2.14 `counter/1` + `counter_loop/2` (5 clauses) + 4.2.15 `accumulator/1` + `acc_loop/2` + `client1/1` + `client2/1` + `test_acc/0` (varies; ~6 clauses).

**Header block** + ~17 clauses + 4 sub-headers + 17 `%%` paraphrases.

---

## File 7 — `exercise-07/ch-04-ex-07-recursive-numerics.glp`

**Programs**: 4.3.1 Peano (`plus/3`, `times/3`, `lesseq/2`, `natural_number/1`; varies, ~10 clauses) + 4.3.2 integer arith (`double/2`, `average/3`, `abs/2`, `max/3`; ~5 clauses) + 4.3.3 `factorial/2` (3 clauses) + 4.3.4 tail factorial + `fact_acc/3` (3 clauses) + 4.3.5 `fib/2` (3 clauses) + 4.3.6 `fib_linear/2` + `fib_acc/4` (3 clauses).

**Header block** + ~27 clauses + 6 sub-headers + 27 `%%` paraphrases.

---

## File 8 — `exercise-08/ch-04-ex-08-recursive-list-tree.glp`

**Programs**: 4.3.7 `flatten/2` + `flatten_acc/3` (4 clauses) + 4.3.8 `tree_sum/2` (2 clauses) + 4.3.9 `insertion_sort/2` + `insert/3` (5 clauses) + 4.3.10 `mergesort/2` + `split2/5` + `merge_sorted/3` (varies, ~11 clauses) + 4.3.11 `distribute_ng/3` + `copy/3` + `copy_list/3` (varies, uses `=..`; ~6 clauses) + 4.3.12 `substitute/4` + `replace/4` (varies; ~4 clauses).

**Note (per Q2 retraction)**: `=..` works in clause bodies; no special handling needed.

**Header block** + ~32 clauses + 6 sub-headers + 32 `%%` paraphrases.

---

## File 9 — `exercise-09/ch-04-ex-09-metaprogramming-foundations.glp`

**Programs**: 4.4.1 `reduce/2` programs-as-data encoding (3 unit clauses encoding the merge program) + 4.4.2 trust-mode `run/2` minimal MI (4 clauses).

**Header block** + 7 clauses + 2 sub-headers + 7 `%%` paraphrases.

---

## File 10 — `exercise-10/ch-04-ex-10-advanced-meta-interpreters.glp`

**Programs**: 4.4.3 fail-safe `run/4` (5 clauses) + 4.4.4 control `run/5` + `suspended_run/4` (7 clauses) + 4.4.5 tracing `run/3` + indexed `reduce/3` + `replay/3` (9 clauses).

**Header block** + ~21 clauses + 3 sub-headers + 21 `%%` paraphrases. ex-10 may need duplicated `reduce/2` from ex-09 inline (per FR-010); implementer decides during /speckit-implement.

---

## Cross-file invariants

- ex-03's `producer/2` + `consumer/3` clauses are byte-identical to ch03's `ch-03-ex-01-producer-consumer.glp` (per spec FR-002 + SC-007 cross-chapter inversion identity contract).
- Each exercise's `.glp` is self-contained per FR-010; duplication of shared procedures (and/or/not/xor in ex-02; reduce/2 in ex-10 if needed; etc.) is inline byte-exact.
- Per-clause `%%` paraphrase comments MAY differ across files even for duplicated clauses, because each file's pedagogical context differs.

---

## Constitution alignment

- Principle III (SRSW Discipline) — all clauses in all 10 files are SRSW-compliant by byte-exact construction (the book's Programs are SRSW-valid; implementer copies byte-exact).
- Principle VI (Tutorial Charter Compliance) — `%%` per-clause comments per charter §1.5.
- Language Design Authority — no new kernels / guards / system predicates introduced; `:=` body kernel + `=..` univ + `ground` multi-reader guards are all pre-existing.
