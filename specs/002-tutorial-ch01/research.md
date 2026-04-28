# Phase 0 Research — Olamni Tutorial Chapter 1

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)
**Date**: 2026-04-28

This document resolves the four plan-level items deferred during `/speckit-clarify`, plus the supporting unknowns surfaced during plan-template fill.

---

## R-001 — `%%` paraphrase comment density and style for `ch-01-ex-01-fair-stream-merger.glp`

**Decision**: Block-comment header (3–6 lines) summarising what Program 1.1 does and citing PDF p 5 §1.6, plus **one inline `%%` comment per clause** paraphrasing the surrounding prose. Total per-clause comment ≤ 1 short line. Total file ≤ ~20 lines including blanks.

**Rationale**:
- Charter §1.5 mandates "every clause carries a `%%` comment paraphrasing the matching paragraph of the book". One per clause matches.
- Heavy commentary pushes the file beyond skimming length and dilutes the SRSW-discipline punchline (the variables themselves teach the lesson).
- A short header puts the file in context for a learner who arrives via the chapter signpost without re-reading the book.
- Constitution Principle VI requires charter compliance; this is the minimal compliant comment density.

**Alternatives considered**:
- *No comments, just code* — violates charter §1.5.
- *Comment on every variable occurrence* — over-commented; dilutes signal.
- *Verbatim prose paragraph as block comment* — too long; not a paraphrase; risks copyright issues.

**Concrete shape** (illustrative, NOT to be hand-written into the .glp by the implementer; the actual prose comes from the implementer rereading p 5 prose during step 3 of the Ordered Actions):

```
%% ch-01-ex-01-fair-stream-merger.glp
%% Program 1.1 from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §1.6, p 5.
%% Demonstrates the SRSW discipline: each variable occurs exactly once as a writer
%% and once as a reader, alternation produced by argument swap in the recursive call.

merge([X|Xs],Ys,[X?|Zs?]) :- merge(Ys?,Xs?,Zs).  %% take from stream 1; swap so stream 2 is consumed next
merge(Xs,[Y|Ys],[Y?|Zs?]) :- merge(Xs?,Ys?,Zs).  %% take from stream 2; swap so stream 1 is consumed next
merge([],[],[]).                                 %% both streams empty: terminate
```

Note: clause SRSW notation (`X?` vs `X`) is canonical from PDF p 5 — the implementer re-reads p 5 byte-exactly per spec Clarification Q1 / Ordered Action 3 to ensure no transcription drift.

---

## R-002 — REPL build-artifact location and gitignore strategy

**Decision**: Build the REPL executable to **`glp_runtime/glp_repl.exe`** (next to the source, under `glp_runtime/`). Add `glp_runtime/glp_repl.exe` and `glp_runtime/glp_repl` (Linux/macOS form) to the repo-root `.gitignore`. Document the build command in `quickstart.md` and in `ex-01-tutorial.md` so a learner can rebuild on their own host.

**Rationale**:
- Co-locating the binary with its source (`glp_runtime/bin/glp_repl.dart`) is the standard Dart project convention; it avoids a stray binary at the repo root.
- Gitignoring the binary keeps the repo platform-agnostic (a `.exe` from Windows is useless on macOS / Linux; binaries are large and churn on every Dart upgrade).
- The build command is deterministic and short (`dart compile exe`), so requiring learners to build it adds <30 seconds and ensures they're running a binary built against their local Dart SDK version.

**Alternatives considered**:
- *Build to repo root `./glp_repl.exe`* — pollutes top-level listing.
- *Build to a tempdir per session* — fine for CI but worse for interactive iteration; harder for a learner to find.
- *Commit the binary* — bloats the repo; cross-platform incompatible; violates Constitution Technology Stack policy on declared deps.

**Implementation note**: Before writing the `.gitignore` entry, the implementer MUST verify the file does not already gitignore `glp_repl.*` somewhere else (search the existing `.gitignore`). If a sibling pattern exists, harmonise rather than duplicate.

---

## R-003 — Top-level `olamni/tutorial/tutorial.md` initial structure

**Decision**: One-page Markdown with four sections: (1) brief intro to the Olamni Tutorial, (2) status table per chapter (chapter number, title, link, status: implemented / in-progress / planned), (3) prerequisites (working GLP REPL, references to charter and spec workflow), (4) "how to use this tutorial" (one-paragraph guidance on the section-driven model and the per-exercise approval gates). For this first invocation, only chapter 1 is filled in; chapters 2–13 appear in the table as "planned" rows pointing at their existing `chXX-sources.md` files.

**Rationale**:
- A status table makes the incremental build cadence visible at a glance — a learner sees both "what's ready" and "what's coming".
- Including planned chapters as table rows (not silently omitting them) signals the full chapter scope and avoids future edits surprising a returning reader.
- The `chXX-sources.md` files already exist for all 13 chapters (committed in `592d89e3`), so the planned-chapter rows can link to real artifacts.
- One file, not multiple; matches the spec's FR-005 ("`tutorial.md` MUST contain ... an entry added for Chapter 1").

**Alternatives considered**:
- *Pure list of completed chapters, no planned entries* — silently hides the future scope; violates the "no surprise" pedagogical goal.
- *Per-part split (Part I / II / III index files)* — over-engineering for 13 chapters; charter implies a single index.
- *Auto-generate from `chXX-sources.md` headers* — adds tooling complexity for a one-page markdown file; YAGNI.

**Schema (illustrative, see contract `data-model.md` for normative form)**:

```markdown
# Olamni Tutorial — *The Art of Grassroots Logic Programming*

A self-paced tutorial accompanying Shapiro (2025). Each chapter has 1–N exercises.
Build the REPL once: `dart compile exe glp_runtime/bin/glp_repl.dart -o glp_runtime/glp_repl.exe`.
Then load the per-chapter `.glp` files and follow each `ex-NN-tutorial.md` step-through.

## Chapter status

| # | Chapter | Tutorial entry | Status |
|---|---|---|---|
| 1 | Introduction | [ch01_tutorial.md](ch01/ch01_tutorial.md) | ✅ implemented (2026-04-28) |
| 2 | Logic Programs and Linear Logic | [ch02-sources.md](ch02/ch02-sources.md) | ⏳ planned |
| ... | ... | ... | ⏳ planned |
| 13 | (bonus, Python actors) | [ch13-sources.md](ch13/ch13-sources.md) | ⏳ planned (scenario TBD) |

## Prerequisites
- Dart SDK ^3.9.4
- The GLP REPL built from this repo (see above)
- A copy of *The Art of Grassroots Logic Programming* PDF for cross-reference

## How to use this tutorial
Section-driven (chs 1–6) — one `.glp` per substantial Program. Use-case-driven (chs 7–13) — one project per use case. Per chapter, exercise-01 is the canonical version, exercise-02 / -03 are renamed-variable variants gated behind exercise-01 approval. See `olamni/tutorial/charter.md` for the full design rationale.
```

---

## R-004 — Inspection-goal selection for exercise-01

**Decision**: Capture **3 inspection goals** in `ex-01-repl-trace.md` after the primary goal, in the following order:
1. **Asymmetric — first stream longer**: `merge([1,2,3,4], [a], Xs).` — observes that surplus elements of one stream are appended after alternation exhausts the other.
2. **Empty stream**: `merge([], [a, b, c], Xs).` — observes the first-clause-fails / second-clause-succeeds path; binds `Xs` to the right-hand stream straight through.
3. **Both empty (base case)**: `merge([], [], Xs).` — observes the third clause; binds `Xs = []`.

Each is presented in `ex-01-tutorial.md` as a "now try this" exploratory prompt with brief annotation explaining what the learner should observe and what it teaches.

**Rationale**:
- Three goals match spec FR-002 ("2–3 exploratory inspection goals").
- Selected goals exercise each of the three clauses of Program 1.1 (the two recursive cases via the asymmetric goal; the base case via the both-empty goal). Coverage of all clauses is the most pedagogically dense use of three goals.
- Each goal is **deterministic and short-running** — fits the <5 min learner budget (SC-001).
- Each goal **exposes a different SRSW reader/writer pattern** — the asymmetric one shows leftover-stream forwarding, the empty one shows clause selection, the base case shows termination.
- Per spec Clarification Q1 / FR-002, these are proposed by the implementer for project-owner approval BEFORE running. The implementer presents them in the same shape as the primary goal proposal.

**Alternatives considered**:
- *Suspended-on-unbound-reader* (`merge(X?, Y?, Z).`) — pedagogically interesting (shows `→ suspended`) but invites confusion at this stage; chapter 4 §4.2 already covers stream suspension. Defer to ch04.
- *Type-error attempts* — Program 1.1 has no type declarations (chapter precedes ch5); type-error illustration belongs to ch05 §5.7.
- *Two goals only* — leaves the third clause uncovered.
- *Five+ goals* — exceeds spec FR-002's 2–3 cap; risks over-saturation.

**Verification gate**: implementer presents these three goals to the project owner for explicit approval BEFORE running them under the REPL (per spec FR-011, Plan-then-act). User may override the selection.

---

## Supporting research

### R-005 — Verify Dart SDK on this Windows host

**Status**: To be verified before any REPL build attempt. Constitution requires Dart `^3.9.4`.

**Plan**: First action of implementation is `dart --version`. If absent or below 3.9.4, halt and report (per spec Edge Cases — "Dart SDK absent on the host machine").

**Note**: This is a runtime verification step, not a research conclusion. Recorded here so the implementer doesn't skip it.

### R-006 — PDF re-read scope

**Decision**: Re-read PDF p 5 byte-exactly for Program 1.1 itself; ALSO re-read p 5–6 prose surrounding the program (the §1.6 introduction + the sentences immediately after the program block, before Formal 1.1) to draw paraphrase comments from. Formal 1.1 box on p 6 is OUT OF SCOPE per charter (formal-track material).

**Rationale**:
- Re-reading just the code without the prose context produces sterile paraphrase-comments.
- Re-reading the whole chapter would over-broaden the input and risks importing material from §1.7 / §1.8 (Security, Book Overview) that doesn't belong to this exercise.
- p 5 + first half of p 6 is the natural "Program 1.1 zone" per the chapter layout.

**Alternatives considered**:
- *p 5 only* — paraphrase comments would lose the surrounding "alternately selected … due to argument swap" sentence which is the most pedagogically valuable.
- *Whole chapter* — too broad; bleeds across exercise scopes.

---

## Summary of Phase 0

All four plan-level deferrals (R-001 through R-004) have decisions recorded with rationale and alternatives. R-005 / R-006 are supporting verifications for the implementation step. No `NEEDS CLARIFICATION` markers remain. Phase 0 complete; proceed to Phase 1.
