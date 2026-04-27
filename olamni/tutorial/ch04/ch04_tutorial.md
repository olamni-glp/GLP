# Chapter 4 — Basic Concurrent Programming

Companion files for *The Art of Grassroots Logic Programming*, Chapter 4.

§4.1 and §4.2 are each delivered as a single narrative file (per Udi's grouping rule for early chapters). §4.4 keeps each meta-interpreter as its own file with comments, since the four `run/N` predicates have distinct arities.

## Examples

### `ch-04-ex-01-from-constants-to-circuits.glp` — §4.1

All of §4.1 woven into one narrative: unit clauses, conjunctive goal modes, first-clause commit, logic-gate truth tables (`and`/`or`/`not`/`xor`), `nand` with body, and `half_adder`/`full_adder` using `ground` guards for double-reader inputs.

### `ch-04-ex-02-streams-producer-consumer-reverse-merge.glp` — §4.2

All of §4.2: `producer/2` and `consumer/3` running concurrently on a counted stream, naive `reverse/2` with `append/3`, accumulator `reverse_acc/3`, and the four-clause fair `merge/3` whose two empty-tail base cases enable single-step drain when one input closes.

### `ch-04-ex-03-recursive-programming.glp` — §4.3

All of §4.3 in one file: Peano arithmetic (`plus`, `times`, `lesseq`, `natural_number`), integer arithmetic (`double`, `average`, `abs`, `max`), recursive numeric functions (3-clause `factorial` and tail-recursive `fact_acc`; tree-recursive `fib` of complexity O(2^N) and linear `fib_acc`), flattening nested lists (`flatten`/`flatten_acc` with an `otherwise` pass-through clause), binary trees (`tree_sum` whose two recursive calls spawn concurrently), insertion sort, merge sort (`mergesort` + `split2` + `merge_sorted`), the non-ground stream distributor (`distribute_ng` with `copy`/`copy_list` demonstrating suspension on unbound subterms), and tree substitution (`substitute` + `replace`).

### `ch-04-ex-04-meta-trust.glp` — §4.4 trust mode

Trust-mode meta-interpreter `run/2` from §4.4, plus the `reduce/2` clause-as-data encoding it consumes. Demonstrates programs-as-data, the fork/halt/cross-module/reduce kernels, and how modular goals `M # G` switch interpreter context.

### `ch-04-ex-05-meta-failsafe.glp` — §4.4 fail-safe

Fail-safe meta-interpreter `run/4` with short-circuit failure reporting via a difference-list output stream, and the `reduce(A, failed(A?)) :- otherwise | true.` catch-all that the object program must include.

### `ch-04-ex-06-meta-control.glp` — §4.4 control

Control meta-interpreter `run/5` with a ground control stream shared across forked processes, supporting `suspend`/`resume`/`abort` via a separate `suspended_run/4` predicate. Shows how ground-stream sharing relaxes SRSW.

### `ch-04-ex-07-meta-tracing-and-replay.glp` — §4.4 tracing

Tracing meta-interpreter `run/3` that builds an execution tree with `copy/3` to freeze each reduction, plus `replay/3` that re-executes deterministically by reduction index.

## How to run

From the repo root:

```bash
cd glp_runtime/bin
dart run glp_repl.dart
```

Sample loads:

```
load ../../olamni/tutorial/ch04/ch-04-ex-01-from-constants-to-circuits.glp
half_adder(1, 1, S, C).
```

Expected: `S = 0`, `C = 1`, succeeds.

```
load ../../olamni/tutorial/ch04/ch-04-ex-02-streams-producer-consumer-reverse-merge.glp
producer(H, 5), consumer(H?, 0, R).
```

Expected: `R = 15`, succeeds (sum of 5+4+3+2+1).

For each meta-interpreter (ex-04 through ex-07), see the file's header comment block for the corresponding `run/N` invocation.

## Pattern source in the repo

- §4.1 circuits: `programs/typed_book/constants/` (gates, half-adder, full-adder).
- §4.2 streams: `programs/typed_book/recursive/list_processing/` (append, reverse, merge).
- §4.4 meta: `programs/typed_book/meta/` (or `programs/OLD typed book/meta/` if not yet ported).
