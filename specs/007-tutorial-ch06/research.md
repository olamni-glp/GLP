# Research — ch06 (Typed Programming)

**Phase 0 output**. All NEEDS CLARIFICATION items from Technical Context resolved here. Cites spec.md (FR-NNN, SC-NNN, Q1, Q2) and CLAUDE.md.

## R-001 — Per-`.glp` `%%` paraphrase comment volume

**Decision**: ~25–35 `%%` paraphrase comments total across the 5 `.glp` files. Estimate per file:
- ex-01 flatten/flatten_acc: ~5 clauses → ~5 comments
- ex-02 typed quicksort: ~6 clauses → ~6 comments
- ex-03 control MI: ~7 clauses (run/5 has 5 + suspended_run/4 has 2) → ~7 comments
- ex-04 channel ops: ~6 clauses (send + receive + new_channel + 3 relay) → ~6 comments
- ex-05 bb sliding-window: ~4 clauses (bb + producer + consumer + bb_test) → ~4 comments

Plus per-file synthesis cross-reference header block (3 lines minimum per FR-014) and per-§6.x heading mapping notes.

**Rationale**: charter §1.5 mandates one paraphrase comment per clause. Counts derived from each source program's clause count as documented in `ch01-sources.md` through `ch05-sources.md`. Final count verified at /speckit-implement.

**Alternatives considered**: per-line comments (rejected — too dense for the synthesis-narrative purpose); chapter-level prose only (rejected — violates charter §1.5).

## R-002 — REPL build state

**Decision**: Use the REPL build verified at end of ch05 ship (build commit `bcd59392 Back-merge main into develop after v2026.05.01 release` per ch05 Q11 empirical log). At /speckit-implement T001-equivalent, rebuild against current main with `--define=GLP_BUILD_COMMIT=...` and re-verify type-checker pre-flight (R-006 below).

**Rationale**: ch05 Q11 confirmed the type-checker is operational and produces stable error messages on this build. ch06 inherits without re-verification unless the REPL build has materially changed (which is checked at T001).

**Alternatives considered**: rebuilding with `--define` skipped (rejected — banner shows `Built from: unknown`, defeats provenance verification); using a tagged release exe (acceptable but the workflow memory's pattern uses fresh per-checkout builds).

## R-003 — Top-level `tutorial.md` update strategy

**Decision**: Incremental update per FR-011: ch06's row flips from `planned` to `pending review (YYYY-MM-DD)` when ex-01 lands; `implemented YYYY-MM-DD` when all 5 are approved. The row's footnote (per FR-014 third documentation site) explains: "ch06 PDF page is a stub; tutorial content synthesised from ch01–ch05 sources per /speckit-clarify Q1."

**Rationale**: Inherits ch01–ch05 incremental-update pattern. The footnote is the new ch06-specific addition.

**Alternatives considered**: batch-update at chapter completion only (rejected — loses visibility into in-flight state).

## R-004 — Per-exercise inspection-goal selection

**Decision**: **Deferred to /speckit-implement T006/T007-equivalent** with project-owner approval recorded in this `research.md` at that point. Each exercise's primary demo goal + 3 inspection goals are proposed, and locked bindings empirically verified against the actual REPL on this Windows host before any `.glp` is written for that exercise.

**Rationale**: Inherits ch01–ch05 deferral pattern (ch01 R-004, ch02 ex-02/ex-03 shape selection, ch03 R-007, ch04 R-007, ch05 Q2). The project owner reviews each exercise's goal set before commit; halt-and-amend per FR-013 for any binding mismatch.

**Alternatives considered**: locking goals at the spec layer (rejected — ch05 Q2 retracted helper-locking under exactly this rationale; the empirical-verification window at /speckit-implement is the cheaper validation point).

## R-005 — Cross-platform Dart verification

**Decision**: Dart 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`. Verified at session start (already done earlier in this conversation — see CLAUDE.md §2 environment detection). Re-verified at /speckit-implement T001 against the constitution requirement (Dart `^3.9.4`).

**Rationale**: Inherited from ch01–ch05; no change for ch06.

## R-006 — Type-checker live-pipeline pre-flight verification (inherited from ch05 R-006)

**Decision**: Before any ex-NN work begins at /speckit-implement, the implementer MUST verify the live type-checker stage of the REPL pipeline is operational by running the same two-step regression that ch05 R-006 established:
1. **Positive case**: load any ch05 byte-exact `.glp` (e.g., `olamni/tutorial/ch05/exercise-05/ch-05-ex-05-typed-quicksort.glp`) — MUST report `✓ Loaded:` with no errors.
2. **Negative case**: load any ch05 negative-exercise failing-form `.glp` (e.g., `olamni/tutorial/ch05/exercise-06/ch-05-ex-06-type-error-failing.glp`) — MUST report the documented type-error message and refuse the load.

If the type-checker is broken (positive case fails OR negative case loads cleanly), ch06 work HALTS per FR-013 and the implementer reports the regression. Do NOT proceed against a broken type-checker.

**Rationale**: ch06 inherits ch05's type-system content and assumes the type-checker is operational. ch05 R-006 established this verification as the precondition for any chapter-with-types work; ch06 reuses the same gate without modification.

**Alternatives considered**: skipping the pre-flight (rejected — ch05's R-006 was added precisely because the type-checker stage's operational state had to be verified before chapter content depended on it; skipping would re-introduce the silent-failure mode that R-006 was designed to prevent).

## R-007 — Per-Q2 deferred declaration shapes — sketch and approval window

**Decision**: Per Clarification Q2, type definitions and `procedure` declaration shapes for each exercise are NOT spec-locked; they are proposed during /speckit-implement T006-equivalent (one per exercise) with project-owner approval recorded as a row appended to this R-007 table. Each declaration MUST itself satisfy SRSW + the live type-checker at REPL load (FR-018); halt-and-amend per FR-013 if rejected.

**Sketch (illustrative — final shape locked at T006)**:

| Exercise | Source clauses | Sketch declaration | Notes |
|---|---|---|---|
| ex-01 | ch04 §4.3.7 `flatten/2` + `flatten_acc/3` | `NestedList ::= [] ; [Atom \| NestedList] ; [NestedList \| NestedList].` + `procedure flatten(NestedList?, List).` + `procedure flatten_acc(NestedList?, List?, List).` | NestedList is recursive; List is the universal `[Any \| List]` from ch05 §5.2. |
| ex-02 | ch05 §5.6 typed quicksort | **byte-exact from ch05** including ch05 Q10 dual-amendment (corrected qsort declaration `(NumList?, NumList, NumList?)` + interleaved layout) — declarations are part of the byte-exact ch05 source so they need NO re-derivation. | Only ch06 exercise where the source was already typed in its origin chapter. |
| ex-03 | ch04 §4.4.4 control MI `run/5` + `suspended_run/4` | `Control ::= suspend ; resume ; abort.` + `ControlStream ::= [] ; [Control \| ControlStream].` + a MINIMAL `Goal` type sufficient ONLY for the abort demo (e.g., `Goal ::= goal_atom(Atom) ; conj(Goal, Goal).` or even smaller). + `procedure run(Goal?, ControlStream?, ...).` + `procedure suspended_run(Goal?, ControlStream?, ...).` | Goal type is the highest declaration-shape risk in ch06; at T092-PROPOSE the implementer MUST propose the SMALLEST `Goal` type that satisfies the abort demo and defer richer Goal types (conjunction, disjunction, body kernels) to ch07+. The control-MI clauses use Goal opaquely (no destructuring on Goal alternatives in run/5 / suspended_run/4 themselves), so a minimal Goal type that the type-checker accepts is sufficient. |
| ex-04 | ch03 §3.2 channel ops | `Channel ::= ch(Stream, Stream?).` (ch05 §5.5 form) + `procedure send(Any?, Channel?, Channel).` + `procedure receive(Any, Channel?, Channel).` + `procedure new_channel(Channel, Channel).` + `procedure relay(...).` + `procedure make_pair(Channel, Channel).` | Channel form is the canonical one from ch05 §5.5 (typed-glp-manual.md §5). |
| ex-05 | ch04 §4.2.12+§4.2.13 `bb`+`bb_test` | `Stream ::= [] ; [Number \| Stream].` + `procedure bb().` + `procedure producer(Number?, Stream).` + `procedure consumer(Stream?, Number).` + `procedure bb_test().` | Producer/consumer types parametrise on Number for the bounded-buffer demo. |

**Rationale**: Inherits ch05 Q2 deferral. The sketch above is for /speckit-implement guidance only — the implementer MUST re-verify each declaration shape against the live type-checker at T006 before any `.glp` is written.

**Alternatives considered**: locking the sketch as authoritative (rejected — would re-introduce the spec-vs-type-checker conflict mode that ch05 Q4/Q7/Q10 documented).

## R-008 — Cross-chapter relationship contract (NEW for ch06; distinct from ch04's inversion + ch05's typed↔untyped)

**Decision**: ch06's cross-chapter relationship is **synthesis-from-earlier-chapters**: each ch06 exercise's clauses are byte-exact from a cited earlier-chapter PDF source, with type/procedure declarations introduced fresh at §6.x.

This contract is distinct from:
- **ch04's cross-chapter inversion** (ch03 imported `producer/2`+`consumer/3` from ch04 §4.2.1+§4.2.2; ch04 reclaims them as native — *same code, two homes*).
- **ch05's typed↔untyped relationship** (ch05 §5.4 typed `merge/3` cross-references ch04 §4.2.5 untyped `merge/3` — *same procedure name, different signature/clauses*).
- **ch02's cross-chapter forward import** (ch02 imports ch04 §4.2 GLP `append/3` byte-exact — *same code as a forward reference*).

The synthesis-from-earlier-chapters contract for ch06 documents:
1. **`.glp` header block** (per FR-004): MUST cite the earlier-chapter source (chapter, section, page, Program identifier from `chXX-sources.md`) AND the §6.x heading. MUST explicitly state "synthesised from <source> because the ch06 PDF chapter is a stub" (or equivalent prose).
2. **Chapter signpost `ch06_tutorial.md`** (per FR-010 + FR-014): MUST contain plain prose explaining the synthesis approach for the chapter as a whole AND a per-exercise synthesis-source line.
3. **Top-level `tutorial.md` row footnote** (per FR-014): MUST state "ch06 content synthesised from ch01–ch05 sources per /speckit-clarify Q1" or equivalent.

**Rationale**: ch06 is the first chapter where the PDF is a stub; the synthesis approach is novel for the tutorial set and needs an explicit contract distinct from the existing cross-chapter relationship types. The three-site documentation requirement (FR-014) ensures a learner encountering ch06 from any entry point (top-level index, chapter signpost, individual `.glp`) understands the synthesis status.

**Alternatives considered**: documenting only in the chapter signpost (rejected — a learner who jumps straight to a `.glp` from a search would miss the context); documenting only in `.glp` headers (rejected — a learner browsing the top-level index would miss why ch06's row has a footnote).

## R-009 — Filename conventions (locked per workflow memory)

**Decision**: Per workflow memory file-naming dialect:
- Chapter signpost: `ch06_tutorial.md` (underscore between `ch06` and `tutorial`).
- Per-exercise tutorial: `ex-NN-tutorial.md` (hyphens).
- Per-exercise REPL trace: `ex-NN-repl-trace.md` (hyphens).
- GLP source: `ch-06-ex-NN-<short-name>.glp` (hyphens throughout). Locked short names:
  - ex-01: `ch-06-ex-01-difference-lists.glp`
  - ex-02: `ch-06-ex-02-typed-quicksort.glp`
  - ex-03: `ch-06-ex-03-equators-emergency-brake.glp`
  - ex-04: `ch-06-ex-04-bidirectional-communication.glp`
  - ex-05: `ch-06-ex-05-buffered-communication.glp`

**Rationale**: Inherits ch01–ch05 conventions. Short names match the §6.x heading text directly (no creative naming); the implementer does not have license to deviate.

**Alternatives considered**: ch01–ch04 had some flexibility in short names (e.g., ch01 used `merge`, ch04 ex-04 used `merge-variants`); ch06's stub-source nature makes the §6.x heading text the canonical naming source — minimises ambiguity for /speckit-implement.

## Appendix A — pre-implement verification checklist

Run BEFORE T001 of /speckit-implement:
- [ ] `git status` — branch is `007-tutorial-ch06`, working tree clean except for spec/plan/research/data-model/contracts/quickstart artefacts.
- [ ] `dart --version` — reports `^3.9.4` or later (currently 3.10.1).
- [ ] REPL build: `dart compile exe glp_runtime/bin/glp_repl.dart --define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')" -o glp_runtime/glp_repl.exe` — succeeds with no warnings.
- [ ] REPL banner verified: `Built from: <commit>` matches `Repo HEAD: <commit>` (no STALE BINARY warning).
- [ ] R-006 type-checker pre-flight (positive + negative cases) — both pass per the documented procedure above.
- [ ] Baseline test run: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — passes at the ch05 ship state baseline (494/494 expected; record any drift).
