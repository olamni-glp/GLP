# Ch 6 Plan (REPL only)

## Shared
- The book draft has only a TOC page for ch 6 (§6.1–§6.5 listed at p 53; no body). Per Udi: build one tutorial file per TOC heading and source the material from where each topic actually appears in the book or in `programs/typed_book/`.
- REPL: `cd glp_runtime/bin; dart run glp_repl.dart`; load file; run goal.

## Files (TOC heading → source material → demo goal)
- ch06/ch-06-ex-01-difference-lists.glp: §6.1 Difference Lists — source `programs/typed_book/recursive/list_processing/dl_append.glp`; (List, Hole) idiom with O(1) append. → dl_append demo.
- ch06/ch-06-ex-02-quicksort-revisited.glp: §6.2 Quicksort — source book §5.6 "Complete Example: Typed Quicksort" (book p 51) + `programs/typed_book/recursive/list_processing/quicksort.glp`; typed/moded `quicksort` + `qsort` + `partition`. → quicksort([3,1,4,1,5,9,2,6], S).
- ch06/ch-06-ex-03-equators-emergency-brake.glp: §6.3 Equators — source `docs/naming-conventions.md` (table defining `'_equator'(E, C)` structure, `equator(X?)` guard, `'_equator'(X)` body kernel) + `programs/typed_book/meta/enhanced/abortable_meta.glp` (working example using equator for abort). → abortable meta-interpreter demo binding the equator to halt computation.
- ch06/ch-06-ex-04-bidirectional-communication.glp: §6.4 Bidirectional Communication — source book §5.5 response-slot pattern + `programs/typed_book/streams/`; embedded-mode reply variable (e.g., `show(Number?)`) for request/reply over a single channel. → simple bidirectional client/server demo.
- ch06/ch-06-ex-05-buffered-communication.glp: §6.5 Buffered Communication — source book §4.2 "Buffered Communication / Sliding Window Buffer" (book p 34: `bb`, `bb_test`, paired `consumer`/`producer` with `known/1` guard); bounded buffer of pre-allocated slots. → bb_test.

## Acceptance
- Each file loads cleanly; demo goal succeeds.
