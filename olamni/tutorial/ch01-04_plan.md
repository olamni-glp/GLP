# Chs 1–4 Plan (REPL only)

## Shared
- REPL: `cd glp_runtime/bin; dart run glp_repl.dart`; load file; run goal. → succeeds OR suspended.
- Comments paraphrase book prose. Stay close to book; refactor toward existing patterns only on close match.

## Files (code → test goal)
- ch01/ch-01-ex-01-fair-stream-merger.glp: Program 1.1 merge/3 → merge([1,2,3],[a,b],X).
- ch03/ch-03-ex-01-append-lp-and-glp.glp: LP append + GLP w/ reader/writer modes → append_glp([1,2],[3,4],Z).
- ch03/ch-03-ex-02-defined-guards-and-channel-abstractions.glp: §3.2 lookup, send/receive/new_channel, relay, make_pair, bind_response → make_pair(C1,C2),relay([m1,m2],O,C1?).
- ch04/ch-04-ex-01-from-constants-to-circuits.glp: §4.1 unit clauses → gates → nand → half_adder (ground guards) → full_adder → full_adder(1,1,1,S,C).
- ch04/ch-04-ex-02-streams-producer-consumer-reverse-merge.glp: §4.2 producer/consumer + naive reverse + reverse_acc + 4-clause merge → producer(H,5),consumer(H?,0,R).
- ch04/ch-04-ex-03-recursive-programming.glp: §4.3 — peano arithmetic (plus, times, lesseq, natural_number); integer arithmetic (double, average, abs, max); factorial (3-clause + tail-recursive fact_acc); fibonacci (O(2^N) fib + linear fib_acc); flatten/flatten_acc with `otherwise` pass-through; tree_sum on binary trees (concurrent recursive calls); insertion_sort; mergesort (mergesort + split2 + merge_sorted); non-ground stream distributor (distribute_ng + copy + copy_list, suspending on unbound subterms); tree substitution (substitute + replace). → mergesort([3,1,4,1,5,9,2,6], S).
- ch04/ch-04-ex-04-meta-trust.glp: reduce/2 + run/2 → run(merge,merge([1,2],[3,4],Z)).
- ch04/ch-04-ex-05-meta-failsafe.glp: run/4 + failed/1 catch-all.
- ch04/ch-04-ex-06-meta-control.glp: run/5 + ground control + suspended_run/4.
- ch04/ch-04-ex-07-meta-tracing-and-replay.glp: run/3 (tree) + replay/3.

## Acceptance
- All 10 files load cleanly; goals produce expected output.
