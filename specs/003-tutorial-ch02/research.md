# Phase 0 Research — Olamni Tutorial Chapter 2

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)
**Date**: 2026-04-28

This document resolves the plan-level items deferred during `/speckit-clarify`, plus the supporting unknowns surfaced during plan-template fill. Five Clarifications were already resolved in `spec.md`; the remaining decisions live here.

---

## R-001 — `%%` paraphrase comment density across the four `.glp` files

**Decision**: Per-file pattern matches ch01's R-001 — block-comment header (3–8 lines) summarising what the program does and citing the PDF source, plus **one inline `%%` comment per clause** paraphrasing the surrounding prose. Applies to ALL four `.glp` files:

- `ch-02-ex-01-classical-append-LP-only.glp` — header MUST flag the file `% INTENTIONALLY ILL-FORMED FOR GLP — illustrates classical LP contraction`. Per-clause comments paraphrase §2.1 prose explaining classical LP semantics. Two clauses → two `%%` comments.
- `ch-02-ex-01-glp-append.glp` — header MUST cite the cross-chapter source ("byte-exact from book pp 31–32, used here in chapter 2 to illustrate the SRSW transition described in §2.2"). Per-clause comments map variables to writer/reader roles per Formal 2.1. Two clauses → two `%%` comments.
- `ch-02-ex-02-append-and-sum.glp` — header explains the ex-01 → ex-02 progression (adding GLP arithmetic). Per-clause comments cover all clauses of `append/3` (duplicated inline) AND of locally-defined `sum/2` AND of the top-level `append_and_sum/4`. Approximately 5 clauses → 5 `%%` comments.
- `ch-02-ex-03-timed-append.glp` — header explains the ex-02 → ex-03 progression (adding system time + I/O). Per-clause comments cover the duplicated `append/3` AND the locally-defined `timed_append/3` body. Approximately 3 clauses → 3 `%%` comments.

**Rationale**: Same as ch01 R-001 — charter §1.5 mandates per-clause paraphrase; one short line per clause matches; heavy commentary dilutes the SRSW lesson. Extending to four files is a mechanical scale-out, not a new design decision.

**Alternatives considered**:
- *Skip header comment* — violates the chapter-1 precedent and loses the LP→GLP-contrast framing for the LP-only file; rejected.
- *No `%%` per clause for the duplicated `append/3` in ex-02 / ex-03* — reasonable to argue duplicated code doesn't need re-paraphrasing, but charter §1.5 is per-clause; better to be consistent and not invent file-level exceptions; rejected.
- *Reference the ex-01 paraphrase by inclusion in ex-02 / ex-03 header* — possible, but cross-file references make the file harder to read in isolation; rejected.

---

## R-002 — REPL build-artifact location

**Decision**: Inherit ch01's R-002 verbatim. Build to `glp_runtime/glp_repl.exe`. Reuse the binary if it already exists from ch01's session and the source has not changed (verifiable via `dart --version` parity and `git status glp_runtime/bin/glp_repl.dart`). Otherwise rebuild.

**Rationale**: Established convention from ch01; the binary is gitignored already. No new design needed; this entry exists only to make the inheritance explicit.

**Alternatives considered**: As in ch01 R-002. None re-evaluated.

---

## R-003 — Top-level `olamni/tutorial/tutorial.md` update strategy

**Decision**: The file already exists from ch01's implementation with chapter 1 row marked `implemented 2026-04-28`. For ch02, the implementation flips chapter 2's row from `planned` to `pending review (YYYY-MM-DD)` after ex-01 lands and to `implemented YYYY-MM-DD` after all three exercises are approved. Chapters 3–13 remain `planned` rows pointing at their `chXX-sources.md` files. No structural change to the file.

**Rationale**: Per spec FR-006 — incremental update, not a rewrite. The row for chapter 2 already exists (added during ch01's implementation as a planned entry); we only update its status field and link target.

**Alternatives considered**:
- *Rewrite the whole file each chapter* — wasteful and invites churn; rejected.
- *Defer the update until all 13 chapters are done* — violates the "incremental" rule from spec FR-006; learner using the index after ch02 lands would miss the new chapter; rejected.

---

## R-004 — Inspection-goal selection across all three exercises

**Decision**: Each exercise has THREE inspection goals after the primary demo goal. Goals exercise different clauses; selections proposed for project-owner approval at /speckit-implement T006 BEFORE running.

**ex-01** (LP/GLP append contrast) — primary `append([1,2,3], [a,b,c], Zs).` → `Zs = [1, 2, 3, a, b, c]`.

1. `append([], [a,b,c], Zs).` — exercises base clause `append([], Ys, Ys?)`. Result: `Zs = [a, b, c]`. Pedagogical: shows that the second-argument writer/reader pair forwards the right-hand list directly.
2. `append([1,2,3], [], Zs).` — exercises recursive descent terminating in the base. Result: `Zs = [1, 2, 3]`. Pedagogical: shows recursion bottoms out cleanly when the first list runs dry.
3. `append([], [], Zs).` — exercises base clause alone, both lists empty. Result: `Zs = []`. Pedagogical: minimal termination behaviour.

**ex-02** (`append_and_sum/4`) — primary `append_and_sum([1,2,3], [4,5,6], Zs, Sum).` → `Zs = [1,2,3,4,5,6]`, `Sum = 21`.

1. `append_and_sum([], [4,5,6], Zs, Sum).` — first list empty. Result: `Zs = [4,5,6]`, `Sum = 15`. Pedagogical: `append/3`'s base + `sum/2`'s recursion working together when the appender does no work.
2. `append_and_sum([1,2,3], [], Zs, Sum).` — second list empty. Result: `Zs = [1,2,3]`, `Sum = 6`. Pedagogical: full append-recursion + sum on the residue.
3. `append_and_sum([], [], Zs, Sum).` — both empty. Result: `Zs = []`, `Sum = 0`. Pedagogical: `sum/2`'s base case, end-to-end.

**ex-03** (`timed_append/3`) — primary `timed_append([1,2,3], [a,b,c], Zs).` → `Zs = [1,2,3,a,b,c]` plus `'_output'(elapsed_ms(N))` shape-locked, value varies.

1. `timed_append([], [], Zs).` — degenerate case. Result: `Zs = []` plus an `elapsed_ms(N)` line where N is typically 0 or 1. Pedagogical: confirms `_output` fires even on trivial input.
2. `timed_append([1,2,3,4,5,6,7,8,9,10], [a,b,c,d,e,f,g,h,i,j], Zs).` — larger input. Result: `Zs = [1..10, a..j]` plus an `elapsed_ms(N)` line where N is typically 1–5. Pedagogical: confirms elapsed scales (loosely) with input size; reinforces FR-014's "shape matters, not value".
3. `timed_append([1], [a], Zs).` — minimal non-empty. Result: `Zs = [1, a]` plus `elapsed_ms(N)`. Pedagogical: smallest non-trivial trace.

**Rationale**:
- Three goals per exercise matches spec's "three inspection goals" requirement.
- Each goal exercises a distinct clause / sub-procedure.
- ex-02's goals also exercise `sum/2`'s clauses (base + recursive).
- ex-03's goals span trivial / typical / minimal-non-trivial inputs to give the learner a feel for elapsed-ms variability.
- All goals are deterministic in the SHAPE of their output (modulo elapsed-ms in ex-03).

**Alternatives considered**:
- *Suspended-on-unbound-reader inspection goals* — pedagogically interesting but invite confusion; defer to ch04 where stream suspension is the chapter topic.
- *Type-error attempts* — out of scope; the chapter doesn't introduce types (chs 5+).
- *Five+ goals per exercise* — exceeds "three" rule; risks over-saturation and inflates the trace.
- *Different goal sets across the three exercises* — considered, but parallel structure makes the trace files easy to scan and reinforces that the "same problem shape" is being amplified.

**Verification gate**: implementer presents these goal sets to the project owner for explicit approval BEFORE running them under the REPL (per spec FR-013, plan-then-act). Project owner may override.

---

## R-005 — Verify Dart SDK on this Windows host

**Status**: To be verified before any REPL build attempt. Constitution requires Dart `^3.9.4`. Per workflow memory, the Windows host has Dart 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe` (not on PATH).

**Plan**: First action of implementation is `"/c/Users/gavri/dart-sdk/bin/dart" --version`. If absent or below 3.9.4, halt and report (per spec Edge Cases — "Dart SDK absent on the host machine"). If present, set `DART="/c/Users/gavri/dart-sdk/bin/dart"` for the session.

**Note**: This is a runtime verification step, not a research conclusion. Recorded here so the implementer doesn't skip it.

---

## R-006 — PDF re-read scope

**Decision**: Re-read PDF p 10 byte-exactly for Example 2.1 (classical LP append) and PDF pp 31–32 byte-exactly for the GLP `append/3` (chapter 4 §4.2). ALSO re-read surrounding prose: §2.1 + §2.2 + Formal 2.1 (book pp 9–14) for the ex-01 header comments; ch 4 §4.2 prose immediately around the GLP append definition (book pp 31–32) for the cross-chapter import provenance comment. Definitions 2.1–2.10, Definitions 2.11–2.12, Example 2.2 (resource interpretation), and any chapter-4 content beyond GLP `append/3` are OUT OF SCOPE per charter and per spec Out-of-Scope.

**Rationale**:
- Re-reading just the code without the prose context produces sterile paraphrase-comments.
- Chapter 2 is mostly theoretical, so the prose IS the chapter's substance — header comments draw from it heavily.
- Cross-chapter import: only the immediate code-block prose on pp 31–32 (the line "This is O(n²)" plus the GLP-append definition itself) is needed; the surrounding `reverse/2` and `reverse_acc/3` material is out of scope.
- Per ch01's predict-and-verify lesson, drift can sneak in (`ch01-sources.md` had `[X?|Zs]` instead of `[X?|Zs?]`); byte-exact re-reading is non-negotiable.

**Alternatives considered**:
- *Trust `ch02-sources.md` without re-reading* — explicitly rejected by the ch01 lesson. Sources files are convenience indexes; the PDF is canonical.
- *Re-read all of chapter 2 + chapter 4* — too broad; bleeds into other chapters' scope.
- *Re-read only the code blocks, not the surrounding prose* — produces mechanical, learner-unfriendly comments.

---

## R-007 — Cross-chapter import provenance documentation

**Decision**: Each `.glp` file that contains the GLP `append/3` (ex-01's `ch-02-ex-01-glp-append.glp`, ex-02's `ch-02-ex-02-append-and-sum.glp`, ex-03's `ch-02-ex-03-timed-append.glp`) MUST carry a header comment block with the following provenance line, byte-exact:

```
%% GLP append/3 byte-exact from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §4.2, pp 31–32.
%% Imported into ch02 to illustrate the SRSW transition described in §2.2 (Linear Logic, Formal 2.1).
%% This is the only cross-chapter import permitted in ch02 per the spec's Out-of-Scope section.
```

The `ch02_tutorial.md` signpost ALSO documents this cross-chapter import in plain prose (per spec FR-005), so a learner who skips the `.glp` header still encounters the explanation.

**Rationale**:
- Spec FR-002 + FR-009 + FR-010 + FR-015 all reference the cross-chapter import; the actual provenance text needs a single canonical formulation so it doesn't drift across files.
- A learner reading the `.glp` file in isolation must understand WHY a chapter-2 file contains a chapter-4 definition; the header explains it.
- Charter §design-principles 2 says "reader on §X.Y loads the matching file"; this is the documented exception, and the header makes the exception self-explanatory.

**Alternatives considered**:
- *Provenance only in the signpost, not in the `.glp`* — fails the "self-explanatory `.glp`" goal; the file should make sense on its own.
- *Provenance only in the `.glp`, not in the signpost* — fails the "discoverable from the chapter index" goal; the signpost is where a learner first lands.
- *Different provenance text per file* — invites drift; the canonical block above is reused verbatim.

---

## R-008 — `sum/2` and `append_and_sum/3` decomposition for ex-02 (amended 2026-04-29)

**Decision** (amended): ex-02's `.glp` defines three procedures:

1. **`append/3`** — duplicated inline byte-exact from PDF pp 31–32 (per Clarification Q2).
2. **`sum/2`** — accumulator-free recursion over a number list, using `:=` on the recursive call's result. Two clauses:
   - `sum([], 0).`
   - `sum([X|Xs], Total?) :- sum(Xs?, Subtotal), Total := Subtotal? + X?.`
   (Note: head pattern `[X|Xs]` writers; body uses `Xs?` reader, `X?` reader. Single writer-reader pair per variable.)
3. **`append_and_sum/3`** — top-level procedure that composes `append/3` and `sum/2`. One clause:
   - `append_and_sum(A, B, Sum?) :- append(A?, B?, Zs), sum(Zs?, Sum).`

**Rationale** (amended):
- Three procedures is the minimum decomposition that exercises both `append/3` AND `:=` arithmetic; it's pedagogically the cleanest split.
- `sum/2` is naive (non-tail-recursive) deliberately — the chapter is about introducing `:=`, not about optimal recursion (that's ch 4 §4.3.4 territory).
- `append_and_sum/3` is the canonical producer-consumer idiom (book p 31): the intermediate stream `Zs` is local — written once by the `append/3` sub-call, read once by the `sum/2` sub-call. SRSW satisfied without any guard relaxation.
- The amendment from `/4` to `/3` (2026-04-29 per Clarifications Q3a) was forced by the empirical SRSW analysis during /speckit-implement: exposing both `Zs` and `Sum` on the public signature requires two readers of `Zs` (caller's reader + `sum/2`'s reader), which is contraction. The amendment preserves the chapter's pedagogical claim ("consumer reads producer's stream") via the local `Zs` binding instead of through the public signature.
- The locked binding for `append_and_sum([1,2,3], [4,5,6], Sum)` is `Sum = 21` — verifiable by hand: 1+2+3+4+5+6 = 21.

**Alternatives considered**:
- *Original `/4` shape with both Zs and Sum exposed* — incompatible with simple SRSW; would require either a `ground` guard relaxation, a fused producer-consumer pattern with per-element `ground(X?)` guards, or a `_copy` body kernel (none exposed in self.glp). Rejected on 2026-04-29 after empirical halt during /speckit-implement.
- *Tail-recursive `sum/2`* with accumulator — pedagogically denser but introduces an accumulator parameter that isn't in the chapter's scope; rejected.
- *Inline `sum` clauses inside `append_and_sum`* — collapses the natural decomposition; harder to read; rejected.
- *Use `accumulator` from `programs/typed_book/streams/objects_monitors/`* — out of scope per FR-015 (no cross-chapter imports beyond ch4 append); rejected.

---

## R-009 — `timed_append/3` body shape for ex-03

**Decision**: ex-03's `.glp` defines two procedures:

1. **`append/3`** — duplicated inline byte-exact from PDF pp 31–32 (per Clarification Q2). Same definition as in ex-02.
2. **`timed_append/3`** — top-level procedure composing the timing kernels with `append/3`. One clause:
   - `timed_append(A, B, Zs?) :- now(Start), append(A?, B?, Zs), now(End), ground(Zs?) | Elapsed := End? - Start?, '_output'(elapsed_ms(Elapsed?)).`

The `ground(Zs?)` guard is critical: it fires the `now(End)` capture and the `_output` call AFTER `append/3` has fully bound `Zs`. Without it, `now(End)` would race with the `append` recursion and capture an early time.

**Rationale**:
- Single-clause `timed_append/3` keeps the program simple while exercising both `now/1` calls AND `:=` AND `'_output'/1`.
- The `ground/1` guard is the canonical way in GLP to wait for a stream to be fully bound before reading from it as a single value (per `programs/self.glp` definition + book ch 4 conventions). It is NOT a new feature — it is pre-existing in the runtime.
- The body kernel calls go in the body (after the guard `|`), per the standard guard/body separation.
- `Elapsed := End? - Start?` reuses ex-02's arithmetic (per FR-010 — math from ex-02 MUST be reused).
- `'_output'(elapsed_ms(Elapsed?))` formats the result as a structured term (`elapsed_ms/1`) rather than a bare number, so the trace's `_output` line is `elapsed_ms(N)` — easy to grep and self-documenting.

**Alternatives considered**:
- *No `ground/1` guard* — produces a race; `now(End)` could fire before `append/3` finishes. Wrong behaviour. Rejected.
- *Two-clause `timed_append/3`* — overkill for one demonstrable behaviour; rejected.
- *Inline arithmetic without the `:=` operator (e.g., direct `_sub` call)* — violates FR-010 (kernels MUST NOT be called directly); rejected.
- *Output as bare number `'_output'(Elapsed?)`* — less self-documenting in the trace; rejected.

---

## Summary of Phase 0

Nine items resolved (R-001 through R-009). All decisions traceable to spec FRs and Clarifications. No `NEEDS CLARIFICATION` markers remain. R-005 / R-006 / R-007 are supporting verifications; R-001 / R-002 / R-003 / R-004 inherit ch01 patterns; R-008 / R-009 are new for ch02's body-kernel curriculum. Phase 0 complete; proceed to Phase 1.
