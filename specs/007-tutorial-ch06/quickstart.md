# Quickstart — ch06 (Typed Programming) implementer's guide

**Phase 1 output**. Sequential implementation order with halt-and-report rules. Cites spec.md FR-NNN, plan.md, research.md R-NNN, and contracts/.

## Pre-flight (run BEFORE T001)

Per research.md Appendix A, verify:

1. **Branch + tree state**: `git status` — branch is `007-tutorial-ch06`; working tree contains only spec/plan/research/data-model/contracts/quickstart artefacts (no stray `.glp` or trace files).
2. **Dart**: `dart --version` reports `^3.9.4` or later (3.10.1 on this Windows host).
3. **REPL build**: rebuild with `--define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')"` per workflow memory; verify banner `Built from: <commit>` matches `Repo HEAD: <commit>`.
4. **R-006 type-checker pre-flight**: load a known-good ch05 typed `.glp` (positive) AND a known-bad ch05 negative-form `.glp` (negative); confirm positive loads cleanly + negative is rejected with the documented error. **HALT per FR-013 if either case fails.**
5. **Baseline test run**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — passes at the ch05 ship state baseline (494/494 expected). Record any drift.
6. **PDF stub state re-verified**: read book p 53 of `GLP_ART.pdf` byte-exactly. Confirm only the chapter title + 5 section headings exist (no body, no Programs). HALT per FR-015 if the author has filled in any body text.

## Implementation order (5 exercises sequential, pairwise-gated)

### exercise-01 — §6.1 Difference Lists

1. **Re-read source**: `chXX-sources.md` for ch04 + book pp 38–39 of `GLP_ART.pdf`. Confirm `flatten/2` + `flatten_acc/3` clauses byte-exactly.
2. **T006-equivalent (declaration locking)**: propose type definition (sketch in R-007: `NestedList ::= [] ; [Atom | NestedList] ; [NestedList | NestedList].`) + `procedure flatten(NestedList?, List).` + `procedure flatten_acc(NestedList?, List?, List).`. Project owner approves; record the locked shape as a row appended to research.md R-007. Iterate if type-checker rejects.
3. **T006-equivalent (goal locking)**: propose primary demo goal + 3 inspection goals. Examples: primary `flatten([[1,2],[3,[4,5]]], Out).` → `Out = [1,2,3,4,5]`; inspection 1 `flatten([], Out).` → `Out = []` (base case); inspection 2 `flatten([[1]], Out).` → `Out = [1]` (singleton); inspection 3 `flatten([1,2,3], Out).` → `Out = [1,2,3]` (flat input). Project owner approves; locked bindings recorded.
4. **Write `.glp`**: assemble per `contracts/glp-file-format.md` — header block + locked declarations + byte-exact clauses with `%%` paraphrase comments.
5. **REPL verification**: load + run all 4 goals; capture trace verbatim. Bindings MUST match locked values. **HALT per FR-013 if any binding mismatches.**
6. **Write `ex-01-tutorial.md` + `ex-01-repl-trace.md`** per `contracts/trace-file-format.md`.
7. **Update `ch06_tutorial.md` status block**: `exercise-01: files written` initially; `pending review` when complete.
8. **Project owner reviews + approves**: status block flips to `exercise-01: approved YYYY-MM-DD`. Cross-chapter relationship 3 sites verified (header, signpost, top-level footnote).
9. **Gate satisfied**: ex-02 work may begin.

### exercise-02 — §6.2 Quicksort

1. **Re-read source**: `ch05-sources.md` Program 5.6 + book p 51. Confirm clauses + ch05's Q10 dual-amendment declarations byte-exactly. **NO new declaration-locking step needed** (declarations are byte-exact from ch05 §5.6 per `contracts/glp-file-format.md` ex-02 exception).
2. **T006-equivalent (goal locking only)**: propose primary + 3 inspection goals. Examples: primary `quicksort([3,1,4,1,5,9,2,6], Sorted).` → `Sorted = [1,1,2,3,4,5,6,9]`; inspection 1 `quicksort([], S).` → `S = []`; inspection 2 `quicksort([5], S).` → `S = [5]`; inspection 3 `quicksort([3,1,2], S).` → `S = [1,2,3]`. Approval recorded.
3. **Write `.glp`**: byte-exact clauses + declarations from ch05 §5.6 (including Q10 amendments) + ch06-specific header block + `%%` paraphrase comments. The header notes "type defs + proc decls + clauses ALL byte-exact from ch05 §5.6 (including Q10 dual amendments)".
4. **REPL verification + tutorial + trace + status block + approval** as ex-01.
5. **Gate satisfied**: ex-03 work may begin.

### exercise-03 — §6.3 Equators: Emergency Brake

1. **Re-read source**: `ch04-sources.md` §4.4.4 + book p 42. Confirm `run/5` + `suspended_run/4` control-MI clauses byte-exactly.
2. **T006-equivalent (declaration locking)**: propose `Goal ::= ...`, `Control ::= suspend ; resume ; abort.`, `ControlStream ::= [] ; [Control | ControlStream].`, plus `procedure run(Goal?, ControlStream?, …).`. The Goal type is non-trivial; the implementer may reuse ch05's encoding patterns or propose a minimal Goal type sufficient for the demo. Approval recorded.
3. **T006-equivalent (goal locking)**: propose primary + 3 inspection goals. The primary MUST demonstrate the emergency-brake semantics: a goal running under the control MI receives an `abort` message on the control stream and halts. Examples (illustrative — final selection at T006): primary `run(some_goal, [abort], …).` shows abort terminates the computation; inspection 1 shows `[suspend]` → suspends; inspection 2 shows `[resume]` after suspend → resumes; inspection 3 shows `[]` → goal runs to completion. Approval recorded.
4. **Write `.glp`**: locked declarations + byte-exact clauses + header block citing the synthesis explanation (FR-014 + R-008). The header explicitly states that "Equators: Emergency Brake" is approximated by the control-MI's abort message per /speckit-clarify Q1 — the input prompt's analogue is retained.
5. **REPL verification + tutorial + trace + status block + approval** as ex-01.
6. **Gate satisfied**: ex-04 work may begin.

### exercise-04 — §6.4 Bidirectional Communication

1. **Re-read source**: `ch03-sources.md` §3.2 + book p 23. Confirm `send/3` + `receive/3` + `new_channel/2` + `relay/3` + `make_pair/2` clauses byte-exactly.
2. **T006-equivalent (declaration locking)**: propose `Channel ::= ch(Stream, Stream?).` (canonical ch05 §5.5 form per typed-glp-manual.md §5) + `procedure send(Any?, Channel?, Channel).` + `procedure receive(Any, Channel?, Channel).` + `procedure new_channel(Channel, Channel).` + `procedure relay(Stream?, Stream, Channel?).` + `procedure make_pair(Channel, Channel).`. Approval recorded.
3. **T006-equivalent (goal locking)**: propose primary + 3 inspection goals demonstrating bidirectional message flow. Approval recorded.
4. **Write `.glp` + REPL verification + tutorial + trace + status block + approval** as ex-01.
5. **Gate satisfied**: ex-05 work may begin.

### exercise-05 — §6.5 Buffered Communication

1. **Re-read source**: `ch04-sources.md` §4.2.12+§4.2.13 + book pp 34–35. Confirm `bb/0` + `producer/2` + `consumer/2` + `bb_test/0` clauses byte-exactly.
2. **T006-equivalent (declaration locking)**: propose `Stream ::= [] ; [Number | Stream].` + `procedure bb().` + `procedure producer(Number?, Stream).` + `procedure consumer(Stream?, Number).` + `procedure bb_test().`. Approval recorded.
3. **T006-equivalent (goal locking)**: propose primary `bb_test.` + 3 inspection goals (e.g., partial-buffer state, producer-only, consumer-only). Approval recorded.
4. **Write `.glp` + REPL verification + tutorial + trace + status block + approval** as ex-01.
5. **Chapter complete**: top-level `tutorial.md` row flips to `implemented YYYY-MM-DD`; ch06 footnote already in place from ex-01 lands.

## On failure

Per FR-013 and Constitution Principle II:
- Type-checker rejects the locked declarations → propose declaration-shape amendment; project owner approves; iterate. The byte-exact source clauses are LOCKED, the declarations are amendable per Q2.
- REPL binding mismatches the locked binding → STOP. Re-verify the byte-exact transcription against the PDF. If transcription is correct, the locked binding was wrong; propose binding amendment; project owner approves; update spec/plan/research as appropriate (Q-amendment per ch02–ch05 precedent).
- ch06 PDF body has been filled in by the author (FR-015) → STOP. Report. Do NOT silently fold native content into synthesised exercises.
- Source `chXX-sources.md` has drifted from the PDF → STOP. Report. Update the sources file with the correct byte-exact text BEFORE writing the ch06 `.glp`.
- R-006 type-checker pre-flight fails → STOP. Report. Do NOT proceed against a broken type-checker.

## Status block evolution

Throughout implementation, `ch06_tutorial.md` carries:

```
## Exercise status

- exercise-01: <evolves: not yet implemented → files written → pending review → approved YYYY-MM-DD>
- exercise-02: <same evolution; gated on ex-01 approved>
- exercise-03: <same evolution; gated on ex-02 approved>
- exercise-04: <same evolution; gated on ex-03 approved>
- exercise-05: <same evolution; gated on ex-04 approved>
```

Per FR-008 + `contracts/status-block-format.md`, ex-(N+1) work begins only after ex-N is `approved`.

## Top-level index update

Per FR-011 + R-003: when ex-01 lands, flip ch06 row in `olamni/tutorial/tutorial.md` from `planned` to `pending review (YYYY-MM-DD)` and add the synthesis footnote (R-008 third site). When ex-05 is approved, flip to `implemented YYYY-MM-DD` (footnote remains).

## Numbered step list (53 steps total — same shape as ch05 quickstart)

This conceptual numbering is for the learner's mental model of the implementation flow. **The authoritative implementation tracker is `tasks.md` (T001–T124)**; the conceptual numbering below is parallel-but-not-identical to the T-task numbering and SHOULD NOT be used for status tracking.

1–10: pre-flight (verifying environment + R-006 + PDF stub state).
11–18: ex-01 (re-read, lock decl + goals, write, verify, tutorial, trace, status-block, approval).
19–26: ex-02 (same shape; declarations are byte-exact, no T006 lock step).
27–34: ex-03.
35–42: ex-04.
43–50: ex-05.
51–53: chapter-completion (top-level index update, final review, commit-ready state).
