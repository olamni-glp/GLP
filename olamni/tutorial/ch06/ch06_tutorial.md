# Chapter 6 — Typed Programming

Companion files for *The Art of Grassroots Logic Programming*, Chapter 6.

The book draft contains only a TOC page for ch 6 (§6.1–§6.5 as headings, no body). Per Udi's direction, each TOC heading becomes a tutorial file, sourcing material from where the topic actually appears elsewhere in the book or in `programs/typed_book/`.

## Examples

### `ch-06-ex-01-difference-lists.glp` — §6.1 Difference Lists

The (List, Hole) idiom: an open-tailed list paired with a writer at its tail, enabling O(1) append. Material from `programs/typed_book/recursive/list_processing/dl_append.glp`.

### `ch-06-ex-02-quicksort-revisited.glp` — §6.2 Quicksort

Typed/moded quicksort using the accumulator pattern: `quicksort/2` calls `qsort/3` with an accumulator, which calls `partition/4` to split around a pivot. Material from book §5.6 "Complete Example: Typed Quicksort" (book p 51) and `programs/typed_book/recursive/list_processing/quicksort.glp`.

### `ch-06-ex-03-equators-emergency-brake.glp` — §6.3 Equators: Emergency Brake

The equator mechanism for many-to-one signalling: an `'_equator'(E, C)` structure in which the writer `E` becomes equal to the constant `C` once the equator is "fired"; the `equator(X?)` guard succeeds and relaxes SRSW like `ground`; the `'_equator'(X)` body kernel performs the binding. Material from `docs/naming-conventions.md` (Equators table) and `programs/typed_book/meta/enhanced/abortable_meta.glp` (working example: an abortable meta-interpreter that halts when its equator is fired).

### `ch-06-ex-04-bidirectional-communication.glp` — §6.4 Bidirectional Communication

Embedded-mode reply variables for request/reply over a single channel: a message such as `show(Number?)` carries a hole the server fills, allowing a client to receive a reply without a separate channel. Material from book §5.5 (response-slot pattern) and `programs/typed_book/streams/`.

### `ch-06-ex-05-buffered-communication.glp` — §6.5 Buffered Communication

A bounded sliding-window buffer where the consumer pre-allocates a fixed number of slots and the producer fills them, with `known/1` gating consumption and natural back-pressure. Material from book §4.2 "Buffered Communication / Sliding Window Buffer" (book p 34: `bb`, `bb_test`).

## How to run

```bash
cd glp_runtime/bin
dart run glp_repl.dart
```

Each file's header comment states its load path and demo goal.
