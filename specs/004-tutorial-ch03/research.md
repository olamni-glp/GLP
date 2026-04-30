# Phase 0 Research — Olamni Tutorial Chapter 3

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)
**Date**: 2026-04-30

This document resolves the plan-level items deferred during `/speckit-clarify`, plus the supporting unknowns surfaced during plan-template fill. Three Clarifications were already resolved in `spec.md` (Q1: ch4 exemplar locked; Q2: §3.2 defined-guard idiom locked; Q3: §3.2 negation idiom locked). The remaining decisions live here.

---

## R-001 — `%%` paraphrase comment density across the four `.glp` files

**Decision**: Per-file pattern matches ch01's R-001 and ch02's R-001 — block-comment header (3–8 lines) summarising what the program does and citing the PDF source, plus **one inline `%%` comment per clause** paraphrasing the surrounding prose. Applies to ALL four `.glp` files:

- `ch-03-ex-01-glp-fair-stream-merger.glp` — header summarises Program 3.1's role in §3.1 (the canonical SRSW fair merger), cites PDF p 15 byte-exact provenance, and paraphrases §3.1 prose on Reader/Writer pairs + SO Invariant + GLP operational semantics. Three clauses → three `%%` comments mapping each clause's variables to writer/reader roles (clause 1: output from first stream; clause 2: output from second stream; clause 3: terminate on empty streams).
- `ch-03-ex-01-producer-consumer.glp` — header carries the canonical cross-chapter provenance lines from R-007 (below) plus a one-line explanation of why a chapter-3 file contains chapter-4 code. Four clauses (two from `producer/2` + two from `consumer/3`) → four `%%` comments. The producer clauses paraphrase book p 31's "producer that counts down from N" prose; the consumer clauses paraphrase the "consumer that sums stream elements" prose plus Formal 4.2 ("SRSW in Continuation Calls", book p 31) regarding `Xs?, Sum1?` reader-passing.
- `ch-03-ex-02-defined-guards.glp` — header explains the ex-01 → ex-02 progression (adding §3.2 defined guards), cites PDF p 34 / book p 22 byte-exact provenance for `channel/1` + `process/2`, and notes the local `handle/1` stub (per R-008 below). Four clauses (`channel/1` unit clause + `process/2` two clauses + `handle/1` stub) → four `%%` comments. The `channel/1` paraphrase explains "this unit clause defines what counts as a channel-shaped term"; the `process/2` paraphrases explain "first clause guarded by the defined guard `channel(X?)`; second clause uses `otherwise` as the fallback"; the `handle/1` paraphrase notes "minimal stub satisfying the body call; book leaves `handle/1` as a placeholder for downstream processing".
- `ch-03-ex-03-guard-negation.glp` — header explains the ex-02 → ex-03 progression (adding §3.2 guard negation `~(=?=)`), cites PDF p 34 / book p 22 byte-exact provenance for `lookup/3`, and notes the SRSW Rules table on book p 24 distinguishing negatable from non-negatable guards. Two clauses → two `%%` comments. Clause 1 paraphrase: "first clause uses `=?=` in positive form; built-in negatable guard"; clause 2 paraphrase: "second clause uses the `~(...)` negation form on the same `=?=` operator; recursion descends only when the negated guard succeeds".

**Rationale**: Same as ch01 / ch02 R-001 — charter §1.5 mandates per-clause paraphrase; one short line per clause matches; heavy commentary dilutes the §3.2 lesson. Extending to four files is a mechanical scale-out, not a new design decision.

**Alternatives considered**:
- *Skip header comment* — violates the chapter-1 / chapter-2 precedent and loses the §3.2 curriculum framing; rejected.
- *No `%%` per clause for the inherited ch4 procedures* — reasonable to argue byte-exact imports don't need re-paraphrasing, but charter §1.5 is per-clause; better to be consistent and not invent file-level exceptions; rejected.
- *Include the §3.2 SRSW Rules for Defined Guards table (p 24) as a comment block in ex-03* — adds bulk without clause-paraphrase utility; the trace annotation references the table by location instead; rejected.

---

## R-002 — REPL build-artifact location

**Decision**: Inherit ch01 + ch02's R-002 verbatim. Build to `glp_runtime/glp_repl.exe`. Reuse the binary if it already exists from a prior session AND the source has not changed (verifiable via `dart --version` parity and `git status glp_runtime/bin/glp_repl.dart`). Otherwise rebuild. If `claude/fix-misleading-build-line` (commit `a913b3e7`) is merged into main when ch03 work begins, the build command MUST include `--define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')"`; otherwise build without the flag and record the omission in the final implementation report.

**Baseline test-count consequence**: with `claude/fix-misleading-build-line` merged, the unified test suite contains 494 tests (476 pre-existing + 9 AOT smoke checks from section Q + 9 stale-binary regression checks from section R per workflow memory). Without the merge, only the AOT smoke checks (9) are present (Section R was added by the same branch), giving 485 total. The implementer at T004 records the actual baseline number observed; tasks T021 / T032 / T043 / T051 then expect identical-to-T004 rather than the literal numbers 494 / 485. This conditional is the unavoidable consequence of the unmerged-branch state at session start; resolution is for the project owner to merge `claude/fix-misleading-build-line` BEFORE ch03 implementation begins (which collapses the conditional to a single 494/494 expectation).

**Rationale**: Established convention from ch01 / ch02; the binary is gitignored already. No new design needed; this entry exists only to make the inheritance explicit and to flag the build-provenance-fix-flag conditional.

**Alternatives considered**: As in ch01 / ch02 R-002. None re-evaluated.

---

## R-003 — Top-level `olamni/tutorial/tutorial.md` update strategy

**Decision**: The file already exists from ch01 + ch02 implementations with chapter 1 row marked `implemented 2026-04-28` and chapter 2 row marked `implemented 2026-04-29`. For ch03, the implementation flips chapter 3's row from `planned` to `pending review (YYYY-MM-DD)` after ex-01 lands and to `implemented YYYY-MM-DD` after all three exercises are approved. Chapters 4–13 remain `planned` rows pointing at their `chXX-sources.md` files. No structural change to the file.

**Rationale**: Per spec FR-006 — incremental update, not a rewrite. The row for chapter 3 already exists (added during ch01's implementation as a planned entry); we only update its status field and link target.

**Alternatives considered**:
- *Rewrite the whole file each chapter* — wasteful and invites churn; rejected.
- *Defer the update until all 13 chapters are done* — violates the "incremental" rule from spec FR-006; learner using the index after ch03 lands would miss the new chapter; rejected.

---

## R-004 — Inspection-goal selection across all three exercises

**Decision**: Each exercise has THREE inspection goals after the primary demo goal. Goals exercise different clauses; selections proposed for project-owner approval at /speckit-implement T006 BEFORE running.

**ex-01** (Program 3.1 + producer/consumer composed pipeline) — primary `producer(A, 5), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` → `Sum = 21`.

The primary goal already exercises ALL THREE clauses of Program 3.1's `merge/3` (clauses 1 + 2 alternate via the swap-args trick when both streams have elements; clause 3 fires when both are empty), both clauses of `producer/2` (recursive while N>0; base when N=0), and both clauses of `consumer/3` (recursive while stream non-empty; base when stream empty). Per FR-018 the primary alone satisfies "all three clauses of Program 3.1 exercised". The inspection goals therefore cover edge cases AND deepen the producer/consumer base-case coverage:

1. `producer(A, 0), producer(B, 0), merge(A?, B?, M), consumer(M?, 0, Sum).` → `Sum = 0`. Both producer base clauses fire immediately; `merge` clause 3 fires once on the empty pair; `consumer` base fires immediately. Pedagogical: minimal pipeline; everything reaches the base case in one step.
2. `producer(A, 0), producer(B, 3), merge(A?, B?, M), consumer(M?, 0, Sum).` → `Sum = 6`. Producer A's base fires immediately (A=[]); producer B runs the recursive branch three times before hitting base; `merge`'s swap-args trick turns initial `merge([], [3,2,1], M)` into clause-2-driven recursion via swap (clause 1 fires with swapped order). Pedagogical: stream-asymmetry — fairness as graceful handling of one-empty-from-start.
3. `producer(A, 1), producer(B, 1), merge(A?, B?, M), consumer(M?, 0, Sum).` → `Sum = 2`. Smallest "all clauses fire at least once" goal: each producer fires recursive once + base once; `merge` clauses 1 + 2 + 3 each fire once; `consumer` recursive fires twice + base fires once. Pedagogical: the smallest non-trivial trace where the fairness alternation is observable.

**ex-02** (`channel/1` + `process/2` defined-guard demo) — primary `process(ch(a, b), Status).` → `Status = ok`.

Primary exercises `process/2` clause 1 (channel guard succeeds) + `channel/1` unit clause + `handle/1` stub. Inspection goals cover the fallback branch and ground-vs-non-ground variations:

1. `process(foo, Status).` → `Status = error`. `foo` is a constant, not a `ch(_, _)` term, so `channel(foo?)` fails; clause 1 fails; clause 2 (`otherwise`) fires. Pedagogical: clearest "guard fails, fallback selects" demonstration.
2. `process(ch([], []), Status).` → `Status = ok`. The argument is a `ch` term with empty-list args, still satisfies `channel/1` unit clause's structural pattern. Pedagogical: the defined guard matches the SHAPE, not the contents.
3. `process([1,2,3], Status).` → `Status = error`. The argument is a list (not `ch(_,_)` shape), `channel/1` doesn't match, fallback fires. Pedagogical: confirms the defined guard discriminates by shape; reinforces that defined guards are NOT type-conversion-aware.

**ex-03** (`lookup/3` complete with both clauses, guard negation demo) — primary `lookup(b, [(a,1),(b,2),(c,3)], V).` → `V = 2`.

Primary exercises BOTH clauses: clause 2 fires first (negated `~(b =?= a)` succeeds, recursion descends past `(a,1)`), then clause 1 fires on the residue (`b =?= b` succeeds, binds V to 2). Inspection goals cover the immediate-match case, the deepest-match case, and the no-match (fail) case:

1. `lookup(a, [(a,1),(b,2),(c,3)], V).` → `V = 1`. Clause 1 fires immediately on first element. Pedagogical: positive-branch-only path.
2. `lookup(c, [(a,1),(b,2),(c,3)], V).` → `V = 3`. Clause 2 fires twice (descend past `(a,1)` and `(b,2)`), then clause 1 fires on `(c,3)`. Pedagogical: longest descent; emphasises that the negated branch's recursion is the engine of search.
3. `lookup(z, [(a,1),(b,2),(c,3)], V).` → `→ fails`. After clause 2 descends three times, the next call is `lookup(z, [], V)` and neither clause head matches an empty list. The input list is fully ground at the call site, so the empty residue is ground, no suspension condition exists, and the procedure deterministically fails. Pedagogical: confirms the procedure terminates rather than infinitely recurses on a no-match input. If the runtime produces `→ suspended` instead of `→ fails`, the implementer halts-and-reports per Principle II — this is a runtime anomaly, not a benign per-run variation.

**Rationale**:
- Three goals per exercise matches spec's "three inspection goals" requirement (per FR-009 / FR-010 / FR-018).
- Each goal exercises a distinct clause / sub-procedure or a distinct edge case.
- ex-01's primary already covers all three Program 3.1 clauses (per FR-018), so inspection goals can deepen producer/consumer coverage and surface stream-asymmetry behaviour.
- ex-02's three inspection goals exercise both `process/2` clauses (clause 1 in primary + inspection 2; clause 2 in inspections 1 + 3) and confirm the `channel/1` defined guard discriminates by shape.
- ex-03's three inspection goals exercise both `lookup/3` clauses (clause 1 alone in inspection 1; clause 2 followed by clause 1 in primary + inspection 2; clause 2 followed by no-match in inspection 3).
- All goals are deterministic in the SHAPE of their output (no wallclock-derived values, since ch3 inherits no `now/1` / `'_output'/1` per FR-015 + SC-015).

**Alternatives considered**:
- *Suspended-on-unbound-reader inspection goals* — pedagogically interesting but invite confusion; defer to ch04 where stream suspension is the chapter topic.
- *Type-error attempts* — out of scope; the chapter doesn't introduce types (chs 5+).
- *Five+ goals per exercise* — exceeds "three" rule; risks over-saturation and inflates the trace.
- *No-match input for ex-03 that's NOT in the key-value list at all* — the chosen `z` does this cleanly; alternatives like an out-of-list integer key would behave the same way.

**Verification gate**: implementer presents these goal sets to the project owner for explicit approval BEFORE running them under the REPL (per spec FR-013, plan-then-act). Project owner may override.

---

## R-005 — Verify Dart SDK on this Windows host

**Status**: To be verified before any REPL build attempt. Constitution requires Dart `^3.9.4`. Per workflow memory, the Windows host has Dart 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe` (not on PATH).

**Plan**: First action of implementation is `"/c/Users/gavri/dart-sdk/bin/dart" --version`. If absent or below 3.9.4, halt and report (per spec Edge Cases — "Dart SDK absent on the host machine"). If present, set `DART="/c/Users/gavri/dart-sdk/bin/dart"` for the session.

**Note**: This is a runtime verification step, not a research conclusion. Recorded here so the implementer doesn't skip it.

---

## R-006 — PDF re-read scope

**Decision**: Re-read PDF p 27 (book p 15) byte-exactly for Program 3.1 + surrounding §3.1 prose; PDF p 43 (book p 31) byte-exactly for `producer/2` + `consumer/3` + Formal 4.2 prose; PDF p 34 (book p 22) byte-exactly for `channel/1` + `process/2` + `lookup/3` + surrounding §3.2 prose; PDF p 36 (book p 24) for the SRSW Rules for Defined Guards table referenced in ex-03 trace annotations. Definitions 3.1–3.6, Propositions 3.7 / 3.8 / 3.10, Lemma 3.9, Formal 3.1 Circular Term Semantics + Example 3.1 (book p 20), Worked Examples 1–4 (book pp 18–19), §3.3 Exercises (book p 24), §3.2 channel-abstraction primitives `send/3` / `receive/3` / `new_channel/2` / `relay/3` / `make_pair/2` / `bind_response/3` (reserved for ch8), and any chapter-4 content beyond `producer/2` + `consumer/3` are OUT OF SCOPE per charter and per spec Out-of-Scope.

**Rationale**:
- Re-reading just the code without the prose context produces sterile paraphrase-comments.
- Chapter 3 is partially theoretical (§3.1 formal semantics) and partially mechanical (§3.2 guards), so the prose IS the chapter's substance for header-comment material.
- Cross-chapter import: only the immediate code-block prose on book p 31 (the "Producers and Consumers" subsection plus Formal 4.2 plus the producer/consumer definitions themselves) is needed; the surrounding §4.2 stream-merging / list-reversal material is out of scope.
- Per ch01's predict-and-verify lesson, drift can sneak in (`ch01-sources.md` had `[X?|Zs]` instead of `[X?|Zs?]`); byte-exact re-reading is non-negotiable.
- For ex-02, the `channel/1` + `process/2` definition lives next to many other §3.2 idioms (the channel-abstraction primitives, `bind_response/3`, etc.); careful PDF re-read ensures we transcribe ONLY the locked Q2 idioms and not adjacent material.

**Alternatives considered**:
- *Trust `ch03-sources.md` and `ch04-sources.md` without re-reading* — explicitly rejected by the ch01 lesson. Sources files are convenience indexes; the PDF is canonical.
- *Re-read all of chapter 3 + chapter 4* — too broad; bleeds into other chapters' scope.
- *Re-read only the code blocks, not the surrounding prose* — produces mechanical, learner-unfriendly comments.

---

## R-007 — Cross-chapter import provenance documentation

**Decision**: The single `.glp` file in ex-01 that contains the cross-chapter import (`ch-03-ex-01-producer-consumer.glp`) MUST carry a header comment block with the following provenance lines, byte-exact:

```
%% producer/2 byte-exact from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §4.2.1, p 31.
%% consumer/3 byte-exact from same source, §4.2.2, p 31.
%% Imported into ch03 to compose with Program 3.1 into a producer-merger-consumer pipeline that
%% demonstrates SRSW reader/writer pairing across four roles using only built-in guards (`>` and `ground`).
%% This is the only cross-chapter import permitted in ch03 per the spec's Out-of-Scope section.
%% The `:=` body kernel inside producer/2's recursive clause and consumer/3's recursive clause is
%% inherited byte-exact from the import per the spec FR-015 amendment (Clarifications Q1).
```

The `ch03_tutorial.md` signpost ALSO documents this cross-chapter import in plain prose (per spec FR-005), so a learner who skips the `.glp` header still encounters the explanation.

ex-02 and ex-03 `.glp` files MAY duplicate `producer/2` + `consumer/3` inline only if the chosen composition exercises them (per R-009 below; R-009 picks STAND-ALONE for both, so no duplication is required). If duplication WERE required by a future amendment, the same provenance lines apply to those duplicates.

**Rationale**:
- Spec FR-002 + FR-009 + FR-010 + FR-015 + Clarifications Q1 all reference the cross-chapter import; the actual provenance text needs a single canonical formulation so it doesn't drift across files.
- A learner reading the `.glp` file in isolation must understand WHY a chapter-3 file contains a chapter-4 definition; the header explains it.
- Charter §design-principles 2 says "reader on §X.Y loads the matching file"; this is the documented exception, and the header makes the exception self-explanatory.
- The body-kernel-inheritance line is added (vs. ch02's R-007) because ch03 has the explicit FR-015 amendment that permits `:=` in inherited code while forbidding it in ch3-introduced code; the header pre-empts confusion about why this file contains `:=` while ex-02 / ex-03 files do not.

**Alternatives considered**:
- *Provenance only in the signpost, not in the `.glp`* — fails the "self-explanatory `.glp`" goal; the file should make sense on its own.
- *Provenance only in the `.glp`, not in the signpost* — fails the "discoverable from the chapter index" goal; the signpost is where a learner first lands.
- *Different provenance text per file* — invites drift; the canonical block above is reused verbatim if any duplication is ever required.
- *Skip the body-kernel-inheritance line* — would leave a learner wondering why this file contains `:=` while the others don't; explicitly addressed for clarity.

---

## R-008 — `handle/1` resolution for ex-02

**Decision**: Define `handle/1` locally as a single-clause stub `handle(_).` in `ch-03-ex-02-defined-guards.glp`, immediately after the `channel/1` + `process/2` clauses. The book's `process/2` body call `handle(X?)` resolves to this local stub. `process/2` itself is preserved byte-exact from book p 22 — no body substitution.

Concrete file shape:

```glp
%% [header block per R-001 + R-007]

%% Defined guard: channel-shaped term test (book p 22)
channel(ch(_, _)).

%% process/2 first clause: defined-guard dispatch (book p 22)
process(X, ok)    :- channel(X?) | handle(X?).
%% process/2 second clause: otherwise fallback (book p 22)
process(_, error) :- otherwise   | true.

%% handle/1 local stub — book leaves handle/1 undefined as a placeholder for downstream
%% processing; ch03 ex-02's pedagogy is the defined-guard machinery, not handle's behaviour.
handle(_).
```

**Rationale**:
- Preserves byte-exactness of `process/2` (per FR-002 / SC-007 spirit; ex-02's procedures are byte-exact-or-stub-defined).
- Local stub is a single line — minimal addition, clearly documented in the `%%` paraphrase comment.
- Body substitution (replace `handle(X?)` with `true`) would break byte-exactness; even with a header annotation, that creates audit ambiguity ("which line is byte-exact, which isn't?").
- The stub `handle(_).` succeeds for any single argument — equivalent to `true` semantically when called with `handle(X?)` from `process/2`'s body, but preserves the procedure-call structure.

**Alternatives considered**:
- *Body substitution `process(X, ok) :- channel(X?) | true.`* — deviates from byte-exact; rejected per FR-002 spirit.
- *Define `handle/1` to do something pedagogically meaningful* (e.g., echo the channel) — adds scope creep; the chapter's pedagogy is already the defined-guard demonstration; rejected.
- *Use the channel-relay `relay/3` from §3.2 as `handle/1`'s body* — pulls in another §3.2 idiom (out of scope per spec Out-of-Scope; reserved for ch8); rejected.
- *No `handle/1` definition at all (let the goal fail)* — would make the primary goal `process(ch(a, b), Status).` fail (clause 1 selected, body fails, procedure fails), violating the locked binding `Status = ok`; rejected.

**Verification gate**: implementer presents this stub choice to the project owner for explicit approval BEFORE writing the file (per spec FR-013, plan-then-act). Project owner may override (e.g., choose body substitution instead).

---

## R-009 — Composition decisions for ex-02 and ex-03

**Decision**: Both ex-02 and ex-03 are STAND-ALONE — neither composes with Program 3.1's `merge/3` nor with the ch4 producer/consumer pair.

**ex-02 stand-alone shape**: `ch-03-ex-02-defined-guards.glp` contains ONLY:
- `channel/1` byte-exact (1 unit clause)
- `process/2` byte-exact (2 clauses)
- `handle/1` local stub (1 unit clause, per R-008)

Total: 4 clauses. The primary goal `process(ch(a, b), Status).` and the three inspection goals (per R-004) reference only `process/2` (which calls `channel/1` and `handle/1` in its body). Program 3.1's `merge/3` is NOT duplicated inline.

**ex-03 stand-alone shape**: `ch-03-ex-03-guard-negation.glp` contains ONLY:
- `lookup/3` byte-exact (2 clauses)

Total: 2 clauses. The primary goal `lookup(b, [(a,1),(b,2),(c,3)], V).` and the three inspection goals (per R-004) reference only `lookup/3`. Neither Program 3.1's `merge/3` nor ex-02's `channel/1` + `process/2` are duplicated inline.

**Rationale**:
- The locked primary goals (per Q2 and Q3) reference ONLY the locked procedures — no composition required to satisfy the spec's substantive requirements.
- Stand-alone files are the simplest possible shape that satisfies FR-009 (ex-02: introduces a defined guard at a guard position) and FR-010 (ex-03: uses `~(...)` form on a §3.2-listed negatable guard). Adding composition increases code volume + clause count + paraphrase-comment volume without pedagogical gain.
- The conditional-duplication rule (FR-009 / FR-010 "MUST duplicate ONLY IF the chosen composition exercises them") naturally selects no-duplication when stand-alone is chosen.
- Each exercise's REPL session becomes minimal-load: ex-02 loads one file with 4 clauses; ex-03 loads one file with 2 clauses. Easier traces, easier auditor verification.
- The §3.2 curriculum still progresses cleanly across the three exercises: ex-01 demonstrates built-in guards in a multi-procedure composition (rich); ex-02 introduces defined guards in a focused 4-clause file (focused); ex-03 introduces guard negation in a focused 2-clause file (most focused). The "focus narrows" trajectory mirrors the §3.2 prose's own structure (built-in / defined / negation each get progressively more specific examples).

**Alternatives considered**:
- *ex-02 composes with merge/3 via a routing helper* (e.g., `wrap_and_dispatch/3` that wraps merge's output in `ch(...)` and passes to `process/2`) — adds a synthetic helper procedure NOT in the book; bloats the file; the resulting primary goal would no longer match the locked Q2 shape `process(ch(a, b), Status).`; rejected.
- *ex-03 composes with merge/3 by treating merge's output as a key-value list* — would require coercing `merge/3`'s integer output into `(K,V)` pairs, which requires arithmetic/structure-building helpers beyond §3.2's vocabulary; rejected.
- *ex-03 reuses ex-02's `channel/1` + `process/2`* (curriculum-compounds variant) — possible but the locked Q3 primary goal `lookup(b, [(a,1),(b,2),(c,3)], V).` doesn't reference channel/process; reusing them would require an additional composed primary OR adding inspection goals that exercise process/2 alongside lookup/3; introduces complexity without §3.2 curriculum gain (negation is the new content; defined-guard repetition isn't pedagogical); rejected.
- *Each exercise duplicates Program 3.1's `merge/3` even when not exercised* (consistent-shape variant) — produces dead code in ex-02 / ex-03 files; violates spirit of self-containment (which is about reproducibility of the EXERCISED behaviour, not about consistent file shape); rejected.

**Verification gate**: implementer presents this stand-alone choice for both ex-02 and ex-03 to the project owner for explicit approval BEFORE writing those files (per spec FR-013, plan-then-act). Project owner may override (e.g., elect a curriculum-compounds composition for ex-03 reusing ex-02's defined guard machinery).

---

## Summary of Phase 0

Nine items resolved (R-001 through R-009). All decisions traceable to spec FRs, SCs, and Clarifications Q1+Q2+Q3. No `NEEDS CLARIFICATION` markers remain. R-005 / R-006 / R-007 are supporting verifications; R-001 / R-002 / R-003 / R-004 inherit ch01 / ch02 patterns adjusted for the ch03 file count + locked shapes; R-008 (handle/1 stub) and R-009 (stand-alone composition for both ex-02 and ex-03) are new for ch03's §3.2 guard curriculum. Phase 0 complete; proceed to Phase 1.
