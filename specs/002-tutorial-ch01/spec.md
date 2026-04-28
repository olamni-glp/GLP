# Feature Specification: Olamni Tutorial — Chapter 1 (Fair Stream Merger)

**Feature Branch**: `002-tutorial-ch01`
**Created**: 2026-04-28
**Status**: Draft
**Input**: User description: "Build a tutorial for chapter 1 of the GLP book — Program 1.1 Fair Stream Merger. Three exercise variants planned (original, semantic, single-letter variable names) with approval gates between them."
**Constitution**: `.specify/memory/constitution.md` v1.1.0 — Principle I (Spec-First) requires this spec exist before any implementation begins. Because this spec touches `olamni/tutorial/**`, Principle VI requires citing `olamni/tutorial/charter.md` (cited in Assumptions). No `chNN_plan.md` exists yet under the new workflow; plans are produced downstream by `/speckit-plan`.

## Clarifications

### Session 2026-04-28

- Q: For `merge([1,2,3],[a,b],Xs).`, what is the canonical expected `Xs` binding? → A: Predict-and-verify. The spec LOCKS the predicted binding `Xs = [1, a, 2, b, 3]` (derived from the book's p 5 prose: "alternately selected … due to argument swap"; first clause consumes from stream 1, swap means stream 2 is consumed next, ending with stream-1 residue). The implementing Claude session MUST also empirically verify this by capturing the actual REPL output. If the REPL produces a different binding, the implementer halts and reports the discrepancy as a bug (either the prediction or the REPL behaviour is wrong); does NOT silently overwrite the spec.
- Q: How is approval of an exercise signalled to downstream sessions? → A: Status block in `ch01_tutorial.md` with one date-stamped line per exercise. Format: `- exercise-NN: <status> [<date>]` where `<status>` is one of `approved`, `pending` (current exercise awaiting approval), `not yet implemented` (gated future exercise). Example: `- exercise-01: approved 2026-04-29` / `- exercise-02: pending exercise-01 approval` / `- exercise-03: not yet implemented`. Downstream sessions MUST grep this block before starting any exercise-NN work; absent or non-`approved` status for the predecessor blocks the next implementation.
- Q: What is the format of `ex-NN-repl-trace.md` and how should "modulo timestamps" be defined for the byte-equality check? → A: Markdown structured as **(1) brief preface** stating in 1–3 sentences what the trace aims to demonstrate from a learner perspective; **(2) one fenced code block per phase** (load file, primary goal, each inspection goal) containing the raw REPL stdin/stdout verbatim with the REPL's prompt prefix included; **(3) one or two short annotation lines** between or after each code block explaining what the learner should expect to see, what it means, and why it matters — kept brief and clearly separated from the verbatim code-block content; **(4) brief postscript** in 1–3 sentences explaining what the trace demonstrates and why it is important for the chapter's learning goal. The captured stdin/stdout inside code blocks MUST remain byte-verbatim. "Modulo timestamps" = any REPL banner / build wallclock / session-start line that is wallclock-derived (auditor reproducibility check ignores those specific lines, compares all other code-block content line-for-line).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load and run Program 1.1 in the GLP REPL (Priority: P1)

A learner who has just read §1.4 (Concurrent Logic Programming), §1.5 (Single-Reader/Single-Writer Insight), and §1.6 (A First GLP Program) of *The Art of Grassroots Logic Programming* opens the chapter-1 exercise file, loads it into the GLP REPL, runs the canonical demo goal, and sees a fair interleaving of two streams. This grounds the SRSW concept they just read about in directly observable behaviour.

**Why this priority**: Program 1.1 is the first GLP program in the book; its fair-merge dataflow is the foundational illustration of SRSW that every later chapter builds on. A learner who can't run this can't proceed.

**Independent Test**: Open `olamni/tutorial/ch01/exercise-01/ch-01-ex-01-fair-stream-merger.glp` in the GLP REPL, load it (no SRSW / type / compile errors), run `merge([1,2,3],[a,b],Xs).`, observe a fair interleaving (e.g., `Xs = [1,a,2,b,3]`) and `→ succeeds`.

**Acceptance Scenarios**:

1. **Given** a learner who has read §1.4–§1.6, **When** they load `ch-01-ex-01-fair-stream-merger.glp` in the REPL and run `merge([1,2,3],[a,b],Xs).`, **Then** the goal succeeds and `Xs` is bound to `[1, a, 2, b, 3]` (the locked binding per the Clarifications). The implementer additionally verifies this binding empirically by capturing the actual REPL output; any discrepancy is a halt-and-report bug, not a silent fix.
2. **Given** the canonical goal succeeds, **When** the learner runs additional inspection goals proposed in `ex-01-tutorial.md` (e.g., asymmetric inputs, a single-stream case), **Then** each goal produces the documented outcome — succeed with the expected binding, suspend on an unbound reader, or fail per SRSW semantics.

---

### User Story 2 - Step through a guided session for exercise-01 (Priority: P1)

The learner opens `ex-01-tutorial.md`, follows the prose step-by-step, runs each suggested REPL command, and cross-checks each result against `ex-01-repl-trace.md` — a verbatim trace captured from an actual REPL run on this repo's REPL build. This gives the learner a known-good reference to compare against.

**Why this priority**: Without a guide and a captured trace, a learner cannot self-verify. The trace is the difference between "tutorial says this should happen" and "this is exactly what happened in a known-good run".

**Independent Test**: A reader can follow `ex-01-tutorial.md` start-to-finish on a fresh machine with a working GLP REPL and reproduce, line-for-line, the contents of `ex-01-repl-trace.md`.

**Acceptance Scenarios**:

1. **Given** `ex-01-tutorial.md` and `ex-01-repl-trace.md` both exist in `olamni/tutorial/ch01/exercise-01/`, **When** the learner runs the documented REPL commands in order, **Then** the actual REPL output matches `ex-01-repl-trace.md` byte-for-byte (modulo timestamps).
2. **Given** the trace was captured by an actual REPL session, **When** an auditor inspects `ex-01-repl-trace.md`, **Then** it is verifiable as the output of a real GLP REPL run (not a synthesised expected output).

---

### User Story 3 - Find chapter 1 from the chapter signpost (Priority: P2)

The learner opens `olamni/tutorial/ch01/ch01_tutorial.md` (the chapter signpost), reads a brief intro to chapter 1, and follows links to `exercise-01/` (and later, `exercise-02/`, `exercise-03/`). The signpost also briefly explains how to use the chapter's tutorial code (where the .glp lives, how to load it, where the trace lives).

**Why this priority**: Discoverability for chapter-level navigation. P2 because US1 and US2 are usable on their own once the file paths are known, but a chapter index makes the chapter usable as a unit.

**Independent Test**: Opening `ch01_tutorial.md` shows a clearly-named entry for `exercise-01/` with a one-line summary, and instructions for the REPL build are either embedded or linked.

**Acceptance Scenarios**:

1. **Given** `ch01_tutorial.md` exists, **When** the learner opens it, **Then** it lists `exercise-01/` with a one-line description and points to `ex-01-tutorial.md` as the entry point for that exercise.
2. **Given** ex-02 and ex-03 are not yet implemented, **When** the learner opens `ch01_tutorial.md`, **Then** ex-02 and ex-03 are visibly marked as "planned, pending approval" — not silently omitted, not listed as available.

---

### User Story 4 - Find chapter 1 from the top-level index (Priority: P3)

The learner opens `olamni/tutorial/tutorial.md` and sees Chapter 1 listed, possibly alongside whichever other chapters have been completed. The top-level index is built incrementally, so chapter 1 may be the only entry.

**Why this priority**: P3 because the top-level index becomes valuable only as more chapters complete. For a single-chapter scope it's nice-to-have.

**Independent Test**: After this spec is implemented, `olamni/tutorial/tutorial.md` exists and contains an entry pointing to `ch01_tutorial.md`.

**Acceptance Scenarios**:

1. **Given** chapter 1 has been implemented and approved, **When** the top-level index is updated as part of this work, **Then** `tutorial.md` lists Chapter 1 with a one-line summary and a link to `ch01_tutorial.md`.

---

### User Story 5 - Practice variable renaming via ex-02 and ex-03 (Priority: P3, planned, gated)

After mastering exercise-01, the learner studies exercise-02 (semantic names: `First`, `RestFirst`, `Second`, `RestSecond`, `Out`) and exercise-03 (mathematical names: `A`, `As`, `B`, `Bs`, `Cs`) to internalize that GLP semantics depend on the reader/writer pairing under SRSW, not on variable names.

**Why this priority**: P3 because ex-01 already delivers the core MVP; ex-02 and ex-03 are pedagogical reinforcement, not new capability. Gated behind approval to ensure ex-01 is solid before extending.

**Independent Test**: Once ex-02 / ex-03 are implemented post-approval, the learner can run the same `merge` goal against each variant and confirm identical outputs (modulo variable-name presentation).

**Acceptance Scenarios**:

1. **Given** ex-01 has been approved by the project owner, **When** ex-02 is implemented, **Then** the .glp under `exercise-02/` uses exactly the variable names `First, RestFirst, Second, RestSecond, Out` (and runs to the same outcome as ex-01 for identical inputs).
2. **Given** ex-02 has been approved by the project owner, **When** ex-03 is implemented, **Then** the .glp under `exercise-03/` uses exactly the variable names `A, As, B, Bs, Cs` (and runs to the same outcome).
3. **Given** ex-01 is NOT yet marked `approved` in the `ch01_tutorial.md` status block, **When** anyone (human or Claude session) attempts to implement ex-02, **Then** the work MUST be blocked: the implementer reads the status line `- exercise-01: pending …` (or `not yet implemented`), refuses to proceed, and reports back to the project owner asking for explicit approval.

### Edge Cases

- **Dart SDK absent on the host machine.** Implementation halts at REPL build; tutorial author reports back to the project owner before proceeding. The learner-facing tutorial documents that a working GLP REPL is a prerequisite.
- **REPL build fails (e.g., dependency / version mismatch).** Implementation halts; failing-build trace is reported to the project owner. The learner-facing tutorial does NOT contain a synthesised "expected" trace if a real one cannot be captured.
- **PDF transcription mismatch between `ch01-sources.md` and `GLP_ART.pdf` p 5.** PDF p 5 is canonical; if the sources index has a typo, it is corrected during implementation by re-reading the PDF byte-exactly.
- **Goal that suspends rather than succeeds** (e.g., `merge(X?, Y?, Z).` with unbound writers). The tutorial covers `→ suspended` as a valid outcome, not a failure, in the inspection-goal walkthrough.
- **One input stream empty.** `merge([], [a,b], Xs).` should bind `Xs = [a,b]` and succeed; `merge([], [], Xs).` should bind `Xs = []` and succeed. Both are useful inspection goals.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001** `olamni/tutorial/ch01/exercise-01/ch-01-ex-01-fair-stream-merger.glp` MUST contain Program 1.1 verbatim from PDF p 5 of `GLP_ART.pdf`. Comments MAY paraphrase prose from §1.4–§1.6, but MUST NOT alter the executable clauses.
- **FR-002** `olamni/tutorial/ch01/exercise-01/ex-01-tutorial.md` MUST guide the learner through: (a) loading the .glp in the REPL, (b) running the primary goal `merge([1,2,3],[a,b],Xs).`, (c) running the 3 inspection goals selected in `research.md` R-004 — `merge([1,2,3,4], [a], Xs).` (asymmetric), `merge([], [a, b, c], Xs).` (empty stream), `merge([], [], Xs).` (base case) — to interrogate the result, (d) cross-checking against the captured trace.
- **FR-003** `olamni/tutorial/ch01/exercise-01/ex-01-repl-trace.md` MUST be a verbatim capture of an actual REPL session run by the implementing Claude on this Windows host. It MUST NOT be hand-constructed or synthesised. Format MUST follow the Clarifications: (a) 1–3 sentence learner-targeted preface stating what the trace demonstrates; (b) one fenced code block per phase (file load, primary goal, each inspection goal), each holding raw REPL stdin/stdout verbatim with prompt prefixes; (c) 1–2 brief annotation lines outside the code blocks explaining for the learner what to expect, what it means, why it matters; (d) 1–3 sentence learner-targeted postscript summarising what the trace proved and why. Annotations MUST be brief and MUST NOT modify code-block content. The trace MUST be reproducible by another learner running the same .glp file under the same REPL build.
- **FR-004** `olamni/tutorial/ch01/ch01_tutorial.md` MUST exist as a chapter signpost. It MUST list `exercise-01/` (with a one-line summary), and MUST visibly mark `exercise-02/` and `exercise-03/` as "planned, pending approval" while they are not yet implemented.
- **FR-005** `olamni/tutorial/tutorial.md` MUST be updated incrementally — for this spec's invocation, it MUST contain (or have an entry added for) Chapter 1 only, with a final completion pass scheduled after all 13 chapters are done.
- **FR-006** `olamni/tutorial/ch01/ch01-specification-input-prompt.md` MUST be written as plain prose describing the chapter's tutorial requirement WITHOUT speckit ceremony — no Feature Branch / Status / Constitution / FR-NNN / User Story / Given/When/Then forms in that file. It is the rev-eng input prompt that drives this very spec; it is a separate artifact from THIS spec.md.
- **FR-007** Implementation of `exercise-02/` MUST NOT begin until the project owner has approved `exercise-01/`. Implementation of `exercise-03/` MUST NOT begin until the project owner has approved `exercise-02/`. The approval gates MUST be visible in `ch01_tutorial.md` as a date-stamped status block: `- exercise-NN: <status> [<date>]` where `<status>` ∈ {`approved`, `pending <predecessor> approval`, `not yet implemented`}. Downstream Claude sessions MUST grep this block before starting any `exercise-NN` work and MUST refuse to proceed if the predecessor's status is anything other than `approved`.
- **FR-008** When implemented post-approval, `exercise-02/` MUST use exactly the variable names `First`, `RestFirst`, `Second`, `RestSecond`, `Out` (mapping respectively to `X`, `Xs`, `Y`, `Ys`, `Zs` from Program 1.1). When implemented post-approval, `exercise-03/` MUST use exactly `A`, `As`, `B`, `Bs`, `Cs`.
- **FR-009** REPL test execution MUST use the GLP REPL built from `glp_runtime/bin/glp_repl.dart` in this repo, compiled with the host Dart SDK. Implementation MUST verify Dart presence (`dart --version`) before attempting the REPL build.
- **FR-010** No file under `specs/0NN-tutorial-chXX/` MAY be written by Claude impersonating speckit-output format; spec.md is produced by `/speckit-specify` only. This rule applies to all 13 chapters going forward.
- **FR-011** Implementation MUST plan-then-act at every step: present a numbered plan and await explicit approval from the project owner before writing any file other than the plan itself. Multi-step file-writing batches MUST be paused between major artifacts (the .glp, the trace, the tutorial, the signpost) to allow review.

### Key Entities

- **Exercise**: A subdirectory under `olamni/tutorial/chXX/` named `exercise-NN/`. Contains exactly one `.glp` source file, one `ex-NN-tutorial.md` step-through guide, and one `ex-NN-repl-trace.md` verbatim REPL session.
- **Chapter Tutorial**: A directory `olamni/tutorial/chXX/` containing the chapter sources index (`chXX-sources.md`), the rev-eng-input prompt (`chXX-specification-input-prompt.md`), the chapter signpost (`chXX_tutorial.md`), the rev-eng-input copy of the deprecated spec (`spec-rev-eng-input/chXX-DEPRECATED-spec.md`), and one or more `exercise-NN/` subdirs.
- **Top-level Tutorial Index**: `olamni/tutorial/tutorial.md`. Built incrementally as chapters are approved. Final pass when all 13 chapters are done.
- **Approval Gate**: A documented checkpoint between exercises (or between major implementation steps within an exercise) where the project owner must explicitly approve before downstream work may begin.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** A learner who has read §1.4–§1.6 can complete exercise-01 — load the file, run the primary goal, interpret the output — in under 5 minutes given a working GLP REPL.
- **SC-002** `ch-01-ex-01-fair-stream-merger.glp` loads in the GLP REPL with zero errors (no SRSW violation, no type error, no compile error).
- **SC-003** The primary goal `merge([1,2,3],[a,b],Xs).` returns the locked binding `Xs = [1, a, 2, b, 3]` and the REPL prints `→ succeeds`. Empirically verified during implementation by capturing the actual REPL output; mismatch is a halt-and-report bug per the Clarifications.
- **SC-004** `ex-01-repl-trace.md` is byte-equal (modulo timestamps) to a fresh REPL session re-run by an auditor on the same code, demonstrating that the trace was captured from a real run.
- **SC-005** The executable clauses in `ch-01-ex-01-fair-stream-merger.glp` are byte-identical to Program 1.1 on PDF p 5 (after stripping the `%%` paraphrase comments).
- **SC-006** Zero files under `specs/002-tutorial-ch01/` (other than this `spec.md` and any further `/speckit-*`-generated artifacts) carry speckit-output formatting written by Claude. The `QUARANTINE-DO-NOT-USE/` subfolder remains untouched.
- **SC-007** `exercise-02/` and `exercise-03/` directories do NOT exist on disk until the corresponding approval gate is passed (verifiable via `git log` and the directory listing).

## Assumptions

- The "user" of this feature is the **learner** reading Chapter 1 of *The Art of Grassroots Logic Programming* (Shapiro, 2025). This interpretation is taken from `olamni/tutorial/charter.md` design principle 2 ("Reader on §X.Y loads the matching file/project").
- **PDF source of truth.** `GLP_ART.pdf` p 5 is the canonical Program 1.1. If `olamni/tutorial/ch01/ch01-sources.md` shows a slightly different transcription (e.g., a missing `?` annotation), the PDF wins and is corrected by re-reading byte-exactly during implementation.
- **REPL availability.** The host machine has a working Dart SDK; the implementing Claude session verifies `dart --version` before attempting to build `glp_runtime/bin/glp_repl.dart` into an executable. If Dart is absent, implementation halts and the project owner is consulted.
- **Charter governance.** `olamni/tutorial/charter.md` governs grouping, file-naming, step-by-step alignment, and per-chapter scope per Constitution Principle VI.
- **No `ch01_plan.md` exists yet.** Under the new workflow, per-chapter plans are produced by `/speckit-plan` downstream from this spec — they are not pre-existing inputs. The earlier (fabricated) `ch01_plan.md` was deleted in commit `592d89e3` and quarantined work in commit `146f430c`.
- **Top-level `tutorial.md` does not yet exist.** It is created (or extended) as part of this spec's implementation, listing Chapter 1 only. Subsequent chapters extend it.
- **Approval gate is human-only.** The project owner explicitly approves each step; no automated gating mechanism is required at this layer (the gate is procedural, enforced by the implementing Claude session).
- **Out of scope.** End-of-chapter exercises from the book (Chapter 1 has none), Formal-track boxes (e.g., Formal 1.1 on p 6), companion repo cross-references beyond what is needed for this exercise, and any work for chapters 2–13 — all out of scope for this spec.
