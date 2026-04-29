# Feature Specification: Olamni Tutorial — Chapter 2 (LP/GLP Append Contrast + Body Kernels)

**Feature Branch**: `003-tutorial-ch02`
**Created**: 2026-04-28
**Status**: Draft
**Input**: User description: "Build a tutorial for chapter 2 of the GLP book. Chapter 2 is mostly theoretical; the only executable code is Example 2.1 (classical LP append, p 10). Pair it with the GLP append from chapter 4 §4.2 (pp 31–32) as a contrast piece. Three exercises with progressive body-kernel introduction: ex-01 LP/GLP append contrast (no math/IO); ex-02 introduces GLP arithmetic (`:=`); ex-03 introduces system time (`now/1`) and ground-term output (`'_output'/1`). Approval gates between exercises; thorough REPL testing required before each gate. Variation-shape choice for ex-02 and ex-03 is project-owner-approved during /speckit-plan."
**Constitution**: `.specify/memory/constitution.md` v1.2.0 — Principle I (Spec-First) requires this spec exist before any implementation begins. Because this spec touches `olamni/tutorial/**`, Principle VI requires citing `olamni/tutorial/charter.md` (cited in Assumptions). The plain-prose input prompt is `olamni/tutorial/ch02/ch02-specification-input-prompt.md`; per the Constitution and the ch01 precedent, the input prompt and this spec are separate artifacts on purpose — the prompt strips speckit ceremony, the spec adds it.

## Clarifications

### Session 2026-04-28

- Q: Does ex-02's REPL-trace byte-equality contract follow ex-01's strict rule (modulo REPL banner / build wallclock lines), inherit ex-03's SHAPE-only relaxation, or use a hybrid? → A: Strict (like ex-01) — full byte-equality modulo REPL banner / build wallclock lines. Reason: ex-02 is deterministic arithmetic on fixed inputs with no per-run variation; ex-03's relaxation exists only because elapsed-ms is wallclock-derived. Spec FR-014's exception applies ONLY to ex-03; FR-004's strict rule applies to BOTH ex-01 and ex-02.
- Q: How do ex-02 and ex-03 obtain the GLP `append/3` they build on — duplicate inline, load ex-01's file as a dependency, or use a shared helper file? → A: Duplicate `append/3` inline in each ex-02 / ex-03 `.glp` file. Reason: each exercise directory stays self-contained and grep-discoverable; the duplication is two short clauses, not real maintenance overhead; the SRSW analyser sees one program at a time, so loading two files that both define `append/3` would be a procedure-redeclaration conflict; this parallels ch01's three-exercise pattern where each exercise has its own complete `.glp`. The byte-exact provenance from PDF pp 31–32 (per FR-002) is preserved in the duplicated clauses.
- Q: When does the primary-goal binding for ex-02 / ex-03 get locked — in this spec, in `research.md` during /speckit-plan, or empirically at /speckit-implement? → A: Locked in this spec.md NOW. The project owner selects (during /speckit-clarify) the recommended shapes from the input prompt: ex-02 = `append_and_sum/3` (amended from `/4` to `/3` on 2026-04-29 per amendment Q3a below), ex-03 = `timed_append/3`. Locked primary goals + bindings:
  - **ex-02 primary goal**: `append_and_sum([1,2,3], [4,5,6], Sum).` Locked binding: `Sum = 21`. (The intermediate appended list is internal — local writer/reader pair within the clause body — and is NOT exposed in the procedure signature.)
  - **ex-03 primary goal**: `timed_append([1,2,3], [a,b,c], Zs).` Locked binding: `Zs = [1, 2, 3, a, b, c]`. Side-effect line: `elapsed_ms(N)` where N is wallclock-derived (per FR-014; SHAPE locked, value varies per run).
  /speckit-implement runs predict-and-verify against these locked bindings; mismatch is a halt-and-report bug. /speckit-plan does NOT re-decide the shape; it focuses on the inspection goals, the helper-procedure decomposition (e.g., `sum/2`), and the implementation-task ordering.
- Q3a (2026-04-29 spec amendment, post-/speckit-implement halt): The original Q3 lock was `append_and_sum/4` exposing both `Zs` and `Sum` to the caller. Implementation halted because that shape is incompatible with simple SRSW patterns: `Zs` would need to be read by the caller AND consumed internally by `sum/2` — two readers for one writer. Workarounds attempted (relay via `=`, `_copy` kernel, fused producer-consumer with `ground(X?)` guards) either failed or pedagogically diluted the chapter's arithmetic-introduction arc. → **Amended to `append_and_sum/3`** with only `Sum` exposed; intermediate appended list is local. This matches the canonical producer-consumer pattern from book p 31 (`producer(H, 5), consumer(H?, 0, R).`), where the intermediate stream is internal and only the final result is exposed. Reason: cleanest SRSW pattern (one writer, one reader for the intermediate); textbook-aligned; preserves the chapter's "consumer reads producer's stream" pedagogical claim without contraction relaxations.
- Q: What is the cross-chapter import scope for ex-02 and ex-03 — only ch 4 §4.2 GLP `append/3`, or are other later-chapter imports allowed? → A: Only ch 2 (book p 10 classical LP append) + ch 4 §4.2 GLP `append/3` + body-kernels via `programs/self.glp` (auto-resolved by /speckit-clarify auto-mode). Reason: parallels the input prompt's Out-of-Scope (which already restricts ch 4 imports to `append/3`); ex-02 / ex-03 procedures are original constructions composed of: (a) duplicated GLP `append/3` (per Q2 lock), (b) `:=` arithmetic from `self.glp`, (c) `now/1` and `'_output'/1` from `self.glp` (ex-03 only), (d) helper procedures defined locally in the same `.glp` (e.g., `sum/2` for ex-02). NO additional cross-chapter imports are permitted.
- Q: Are ch02 exercise files added to `test/run_all_tests.sh`? → A: NO (auto-resolved by /speckit-clarify auto-mode). Reason: the harness (currently 476 passing) is for language-semantics regression coverage; tutorial files are documentary artifacts under `olamni/tutorial/**`. Per the workflow memory, ch01's exercises are also not in the harness. Tutorial REPL traces are validated via the per-chapter `ex-NN-repl-trace.md` byte-equality contract (FR-004, FR-014), not via the harness. The trace capture during /speckit-implement is the equivalent of a one-shot smoke test.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Observe SRSW rejection of classical LP append (Priority: P1)

A learner who has just read §2.1 (Logic Programs) and §2.2 (Linear Logic) of *The Art of Grassroots Logic Programming* opens the chapter-2 exercise file containing classical LP `append/3` (Example 2.1, book p 10) and attempts to load it in the GLP REPL. The REPL's SRSW analyser rejects the file with a clear violation message. The learner sees, concretely, that the "No contraction" row of Formal 2.1 is enforced at load time — variables that would be reused as both writer and reader in classical LP are caught by the analyser before any goal is run.

**Why this priority**: This is the chapter's pedagogical core. Chapter 2 is mostly theoretical; the LP→GLP transition is the abstract content that the tutorial must make observable. Without seeing the rejection happen on a real file, the learner has only words; with it, they have a runtime confirmation of the linear-logic discipline.

**Independent Test**: Open `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-classical-append-LP-only.glp` in the GLP REPL and attempt to load it. The REPL responds with `Error loading: …` naming an SRSW violation; no goal-running phase is reached.

**Acceptance Scenarios**:

1. **Given** a learner who has read §2.1 + §2.2, **When** they enter the path of `ch-02-ex-01-classical-append-LP-only.glp` at the REPL prompt, **Then** the REPL produces an `Error loading: …` SRSW-violation message and does NOT print `✓ Loaded: …`.
2. **Given** the file's header comment block flags it `% INTENTIONALLY ILL-FORMED FOR GLP — illustrates classical LP contraction`, **When** the rejection happens, **Then** the file's intent and the analyser's behaviour are mutually consistent — the rejection is documented as the demonstration, not as a defect.

---

### User Story 2 - Load GLP append (imported from ch 4) and run primary + inspection goals (Priority: P1)

The same learner then opens the companion file `ch-02-ex-01-glp-append.glp`, which carries the GLP version of `append/3` byte-exact from book pp 31–32 (chapter 4, §4.2). The REPL accepts this file (no SRSW violation, no type error, no compile error), and the learner runs the primary demo goal `append([1,2,3], [a,b,c], Zs).` plus three inspection goals exercising both clauses. The contrast with User Story 1 is the chapter's punchline: same predicate, same recursion, but the SRSW annotations turn it from rejected to runnable.

**Why this priority**: A tutorial that shows only the failure case (US1) leaves the learner without a working mental model. The success case is what gives the contrast pair its pedagogical force.

**Independent Test**: Open `ch-02-ex-01-glp-append.glp` in the REPL, load it (no errors), run `append([1,2,3], [a,b,c], Zs).`, observe `Zs = [1, 2, 3, a, b, c]` and `→ succeeds`.

**Acceptance Scenarios**:

1. **Given** the GLP append file is loaded, **When** the learner runs `append([1,2,3], [a,b,c], Zs).`, **Then** the goal succeeds with the locked binding `Zs = [1, 2, 3, a, b, c]`. Empirically verified during implementation by capturing the actual REPL output; mismatch is a halt-and-report bug, not a silent fix.
2. **Given** the primary goal succeeds, **When** the learner runs the three inspection goals (`append([], [a,b,c], Zs).`, `append([1,2,3], [], Zs).`, `append([], [], Zs).`), **Then** each produces the documented binding (`Zs = [a, b, c]`, `Zs = [1, 2, 3]`, `Zs = []` respectively) and `→ succeeds`. Together with the primary goal, the four-goal session exercises BOTH clauses of the GLP append.

---

### User Story 3 - Step through a guided session for exercise-01 (Priority: P1)

The learner opens `ex-01-tutorial.md`, follows the prose step-by-step, runs each suggested REPL command, and cross-checks each result against `ex-01-repl-trace.md` — a verbatim trace captured from an actual REPL run on this repo's REPL build. The trace covers BOTH the rejection of the LP-only file and the successful load + four goals on the GLP file.

**Why this priority**: Without a guide and a captured trace, a learner cannot self-verify. The trace is the difference between "tutorial says this should happen" and "this is exactly what happened in a known-good run".

**Independent Test**: A reader can follow `ex-01-tutorial.md` start-to-finish on a fresh machine with a working GLP REPL and reproduce, line-for-line (modulo timestamps), the contents of `ex-01-repl-trace.md`.

**Acceptance Scenarios**:

1. **Given** `ex-01-tutorial.md` and `ex-01-repl-trace.md` both exist in `olamni/tutorial/ch02/exercise-01/`, **When** the learner runs the documented REPL commands in order, **Then** the actual REPL output matches `ex-01-repl-trace.md` byte-for-byte (modulo REPL banner and build wallclock lines).
2. **Given** the trace was captured by an actual REPL session, **When** an auditor inspects `ex-01-repl-trace.md`, **Then** it is verifiable as the output of a real GLP REPL run — including the verbatim SRSW-violation error message for the LP-only file.

---

### User Story 4 - Practice GLP arithmetic via ex-02 (Priority: P2, planned, gated)

After mastering exercise-01, the learner studies exercise-02, which keeps the same append-shaped problem but introduces GLP arithmetic via the `:=` operator (e.g., a procedure that appends and concurrently sums a number list). This makes concrete the SRSW promise that a downstream consumer can compute on a stream while the producer is still constructing it — the same writer/reader pairing the learner saw with lists, now with numbers.

**Why this priority**: P2 because exercise-01 already delivers the chapter's MVP (the LP→GLP contrast). ex-02 is the body-kernel curriculum's first step. Gated behind ex-01 approval because thorough REPL testing of ex-01 must precede any extension.

**Independent Test**: Once ex-02 is implemented post-approval, the learner can run the chosen arithmetic predicate against a number list and confirm it produces both the expected appended list AND the expected arithmetic result, all in one session.

**Acceptance Scenarios**:

1. **Given** ex-01 has been thoroughly REPL-tested AND approved by the project owner, **When** ex-02 is implemented, **Then** the `.glp` under `exercise-02/` defines a procedure that uses `:=` arithmetic from `programs/self.glp` and exercises at least one of `+`, `-`, `*`, `/`, `//`, `mod`, `abs`. The math kernels (`'_add'`, `'_sub'`, `_mul`, …) MUST NOT be called directly from learner-facing code.
2. **Given** ex-01 is NOT yet marked `approved` in `ch02_tutorial.md` AND the "thoroughly REPL-tested" criteria are not satisfied for ex-01, **When** anyone (human or Claude session) attempts to begin ex-02, **Then** the work MUST be blocked until both gating conditions hold.
3. **Given** ex-02's specific shape (which arithmetic predicate) is being chosen, **When** the implementing session proposes a concrete shape during /speckit-plan, **Then** the project owner approves the choice and the approval is recorded in `research.md` BEFORE any `.glp` is written.

---

### User Story 5 - Practice system time and I/O via ex-03 (Priority: P3, planned, gated)

After mastering exercise-02, the learner studies exercise-03, which adds the system clock (`now/1`) and ground-term output (`'_output'/1`) to the arithmetic foundation laid in ex-02. The chosen procedure (e.g., `timed_append/3`) captures `now(Start)` and `now(End)`, computes elapsed milliseconds via the arithmetic from ex-02, and prints the result via `'_output'/1`. The learner sees that the same SRSW discipline that governs lists and numbers also governs side-effecting kernels.

**Why this priority**: P3 because ex-01 + ex-02 already cover the chapter's core LP→GLP contrast and the first body-kernel addition; ex-03 completes the body-kernel curriculum (math + time + I/O) but is the reinforcement layer, not new chapter content. Gated behind ex-02 approval.

**Independent Test**: Once ex-03 is implemented post-approval, the learner can run the chosen timing-and-output predicate, observe `_output`-printed lines in the trace, and confirm the elapsed-ms value is non-negative and reasonable for the input size.

**Acceptance Scenarios**:

1. **Given** ex-02 has been thoroughly REPL-tested AND approved by the project owner, **When** ex-03 is implemented, **Then** the `.glp` under `exercise-03/` calls `now/1` at least twice (start + end) AND `'_output'/1` at least once with a ground term, AND reuses the `:=` arithmetic introduced in ex-02 (typically for the elapsed-time subtraction). The runtime body kernels (`_now`, `_output`) MUST NOT be called directly except via the `self.glp`-level procedures.
2. **Given** ex-03 produces side-effects (printed lines) and uses wallclock-derived elapsed times, **When** the trace is captured, **Then** `ex-03-repl-trace.md` shows the `_output`-printed lines exactly as they appeared, AND the elapsed-time annotation documents that the value "varies per run; the SHAPE matters, not the specific number" — a deliberate exception to the strict byte-equality rule from US3.
3. **Given** ex-02 is NOT yet marked `approved` in `ch02_tutorial.md` AND ex-02's "thoroughly REPL-tested" criteria are not satisfied, **When** anyone attempts to begin ex-03, **Then** the work MUST be blocked until both gating conditions hold.

---

### User Story 6 - Find chapter 2 from the chapter signpost (Priority: P2)

The learner opens `olamni/tutorial/ch02/ch02_tutorial.md` (the chapter signpost), reads a brief intro to chapter 2's theoretical content and how the tutorial bridges to runnable code via the ch-4 GLP-append import, and follows links to `exercise-01/` (and later, `exercise-02/`, `exercise-03/`). The signpost briefly explains how to use the chapter's tutorial code (where the .glp lives, how to load it, where the trace lives) and includes the date-stamped per-exercise status block.

**Why this priority**: P2 — discoverability for chapter-level navigation. Without the signpost, the learner would need to know all the file paths in advance.

**Independent Test**: Opening `ch02_tutorial.md` shows a clearly-named entry for `exercise-01/` with a one-line summary, the cross-chapter import provenance ("GLP append byte-exact from ch 4 §4.2"), build instructions for the REPL, and a status block where ex-02 / ex-03 are visibly marked as "planned, pending approval" until they are implemented.

**Acceptance Scenarios**:

1. **Given** `ch02_tutorial.md` exists, **When** the learner opens it, **Then** it lists `exercise-01/` with a one-line description, points to `ex-01-tutorial.md` as the entry point, and explains why chapter 2 imports the GLP append from ch 4.
2. **Given** ex-02 and ex-03 are not yet implemented, **When** the learner opens `ch02_tutorial.md`, **Then** ex-02 and ex-03 are visibly marked in the status block as `not yet implemented` or `pending exercise-N approval` — not silently omitted, not listed as available.

---

### User Story 7 - Find chapter 2 from the top-level index (Priority: P3)

The learner opens `olamni/tutorial/tutorial.md` and sees Chapter 2 listed alongside chapter 1 (already implemented). The top-level index is built incrementally; chapter 2's row flips from `planned` to `implemented YYYY-MM-DD` once all three exercises are approved. Chapters 3–13 stay marked `planned`.

**Why this priority**: P3 because the top-level index becomes valuable mainly as more chapters land. With only chapters 1 and 2 implemented, it's nice-to-have rather than essential.

**Independent Test**: After this spec is implemented through ex-01 (at minimum), `tutorial.md` exists and contains a row for Chapter 2 — initially `pending review` while ex-01 is in flight, then `implemented YYYY-MM-DD` once all three exercises are approved.

**Acceptance Scenarios**:

1. **Given** chapter 2's exercise-01 has been approved, **When** the top-level index is updated, **Then** `tutorial.md` lists Chapter 2 with a one-line summary and a link to `ch02_tutorial.md`. The chapter 2 row is marked `pending review` if any exercise is still in flight, or `implemented YYYY-MM-DD` once all three are approved.
2. **Given** the top-level index is updated incrementally per chapter, **When** an audit looks at the file's history, **Then** chapter 2's row is added (or its status updated) in the same logical commit as the chapter's approval.

### Edge Cases

- **Dart SDK absent on the host machine.** Implementation halts at REPL build; tutorial author reports back to the project owner before proceeding. The learner-facing tutorial documents that a working GLP REPL is a prerequisite.
- **REPL build fails (e.g., dependency / version mismatch).** Implementation halts; failing-build trace is reported to the project owner. The learner-facing tutorial does NOT contain a synthesised "expected" trace if a real one cannot be captured.
- **PDF transcription mismatch between `ch02-sources.md` and `GLP_ART.pdf` p 10 (or pp 31–32).** PDF is canonical; if the sources index has a typo, it is corrected during implementation by re-reading the PDF byte-exactly (per ch01's predict-and-verify lesson).
- **SRSW analyser rejects the LP-only file with a different error wording than expected.** Capture whatever wording the analyser actually produces; do NOT hand-construct the expected error. The exact wording is part of the trace.
- **GLP append goal binds Zs to something other than `[1, 2, 3, a, b, c]`.** Halt-and-report bug; either the prediction or the runtime is wrong. Do NOT silently overwrite the spec.
- **ex-03 elapsed-ms value is zero or negative on a fast host.** Document in the trace annotation that the SHAPE matters, not the specific number; an elapsed value of zero is acceptable for trivially small inputs.
- **`'_output'/1` callback overridden by host (Flutter / test harness) instead of stdout.** ex-03 trace assumes stdout output; if the runtime is configured otherwise, capture whichever sink the configured callback writes to.
- **Goal that suspends rather than succeeds** (e.g., `append(X?, Y?, Z).` with unbound writers). The tutorial covers `→ suspended` as a valid outcome, not a failure, in the inspection-goal walkthrough where applicable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001** `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-classical-append-LP-only.glp` MUST contain Example 2.1 from PDF p 10 of `GLP_ART.pdf` byte-exact: the two classical LP `append/3` clauses, with NO `?` reader annotations and NO header `procedure` declaration. The file MUST carry a header comment block flagging it `% INTENTIONALLY ILL-FORMED FOR GLP — illustrates classical LP contraction` and paraphrasing §2.1 + §2.2 + Formal 2.1 from the book.

- **FR-002** `olamni/tutorial/ch02/exercise-01/ch-02-ex-01-glp-append.glp` MUST contain the GLP `append/3` byte-exact from PDF pp 31–32 (chapter 4, §4.2 "List Reversal — Naive Reverse"): the base case `append([], Ys, Ys?).` and the recursive case `append([X|Xs], Ys, [X?|Zs?]) :- append(Xs?, Ys?, Zs).`. The file's header comment block MUST name the cross-chapter source ("byte-exact from book pp 31–32, used here in chapter 2 to illustrate the SRSW transition described in §2.2") and MUST carry one `%%` paraphrase comment per clause mapping the variables to their writer/reader roles.

- **FR-003** `olamni/tutorial/ch02/exercise-01/ex-01-tutorial.md` MUST guide the learner through: (a) building the REPL, (b) attempting to load the LP-only file and observing the SRSW rejection, (c) loading the GLP file successfully, (d) running the primary demo goal `append([1,2,3], [a,b,c], Zs).`, (e) running the three inspection goals selected during /speckit-plan T006, (f) cross-checking against the captured trace.

- **FR-004** `olamni/tutorial/ch02/exercise-01/ex-01-repl-trace.md` MUST be a verbatim capture of an actual REPL session run by the implementing Claude on this Windows host. It MUST cover BOTH the failed load of the LP-only file AND the successful load + four goals on the GLP file. It MUST NOT be hand-constructed or synthesised. Format: (a) 1–3 sentence learner-targeted preface stating what the trace demonstrates; (b) one fenced ```glp code block per phase (LP-only load attempt, GLP file load, primary goal, each inspection goal), each holding raw REPL stdin/stdout verbatim with prompt prefixes; (c) 1–2 brief annotation lines outside each code block; (d) 1–3 sentence learner-targeted postscript summarising the LP→GLP contrast.

- **FR-005** `olamni/tutorial/ch02/ch02_tutorial.md` MUST exist as a chapter signpost. It MUST list `exercise-01/` (with a one-line summary), MUST document the cross-chapter import from ch 4 §4.2 in plain prose, MUST visibly mark `exercise-02/` and `exercise-03/` as "planned, pending approval" while they are not yet implemented, and MUST contain the date-stamped per-exercise status block per the Status-block format in Assumptions.

- **FR-006** `olamni/tutorial/tutorial.md` MUST be updated incrementally — chapter 2's row MUST be present (alongside chapter 1) with a status reflecting current progress (`pending review` while in flight, `implemented YYYY-MM-DD` once all three exercises are approved). Chapters 3–13 stay marked `planned`.

- **FR-007** `olamni/tutorial/ch02/ch02-specification-input-prompt.md` MUST exist as plain prose describing the chapter's tutorial requirement WITHOUT speckit ceremony — no Feature Branch / Status / Constitution / FR-NNN / User Story / Given/When/Then forms in that file. It is the rev-eng input prompt that drives this very spec; it is a separate artifact from THIS spec.md.

- **FR-008** Implementation of `exercise-02/` MUST NOT begin until the project owner has approved `exercise-01/` AND the "thoroughly REPL-tested" criteria are met for ex-01 (every clause exercised, both files exercised, primary + 3 inspection goals captured in the trace). Implementation of `exercise-03/` MUST NOT begin until the project owner has approved `exercise-02/` AND the "thoroughly REPL-tested" criteria are met for ex-02. The approval gates MUST be visible in `ch02_tutorial.md` as the date-stamped status block: `- exercise-NN: <status> [<date>]` where `<status>` ∈ {`approved YYYY-MM-DD`, `pending exercise-N approval`, `not yet implemented`}. Downstream Claude sessions MUST grep this block before starting any `exercise-NN` work and MUST refuse to proceed if predecessor status is anything other than `approved`.

- **FR-009** When implemented post-approval, `exercise-02/` MUST contain a `.glp` defining `append_and_sum/3` (the locked variation shape per the Clarifications, amended from the original `/4` on 2026-04-29 per Clarifications Q3a) plus the helper `sum/2` it depends on. The procedure MUST use `:=` arithmetic from `programs/self.glp` and MUST exercise the `+` operator. The math body kernels (`'_add'`, `'_sub'`, `_mul`, `_div`, `_idiv`, `_mod`, `_abs`, …) MUST NOT be called directly from learner-facing code. The primary demo goal is `append_and_sum([1,2,3], [4,5,6], Sum).` with locked binding `Sum = 21`. The intermediate appended list is local to the clause body (one writer in the `append/3` sub-call, one reader in the `sum/2` sub-call — the canonical SRSW producer-consumer idiom). The ex-02 `.glp` MUST duplicate the GLP `append/3` from ex-01 inline (byte-exact from PDF pp 31–32, per the Clarifications) — it MUST NOT load ex-01's file as a dependency. The decomposition into `append_and_sum/3` + `sum/2` (vs. some other decomposition) is the only structural choice deferred to /speckit-plan; the public shape and binding are locked here.

- **FR-010** When implemented post-approval, `exercise-03/` MUST contain a `.glp` defining `timed_append/3` (the locked variation shape, per the Clarifications). The procedure MUST call `now/1` (declared in `self.glp`) exactly twice (once before `append/3`, once after), MUST call `'_output'/1` (declared in `self.glp`) at least once with a ground term, AND MUST compute the elapsed time via `:=` subtraction (the arithmetic introduced in ex-02). The `_now` and `_output` body kernels MUST NOT be called directly except via the `self.glp`-level procedures. The primary demo goal is `timed_append([1,2,3], [a,b,c], Zs).` with locked binding `Zs = [1, 2, 3, a, b, c]` and side-effect line `elapsed_ms(N)` (SHAPE locked; N is wallclock-derived per FR-014). The ex-03 `.glp` MUST duplicate the GLP `append/3` from ex-01 inline (byte-exact from PDF pp 31–32, per the Clarifications) — it MUST NOT load ex-01's file (or ex-02's file) as a dependency.

- **FR-011** REPL test execution MUST use the GLP REPL built from `glp_runtime/bin/glp_repl.dart` in this repo, compiled with the host Dart SDK (`^3.9.4`). Implementation MUST verify Dart presence (`dart --version`) before attempting the REPL build. Trace capture uses the kernel snapshot pattern `printf "<path>\n<goal>.\n:quit\n" | dart run glp_runtime/.dart_tool/repl.dill`.

- **FR-012** No file under `specs/003-tutorial-ch02/` (other than this `spec.md` and any further `/speckit-*`-generated artifacts) MAY be written by Claude impersonating speckit-output format. The polluted `QUARANTINE-DO-NOT-USE/quarantine_003_ch02_spec.md` remains untouched and is used as reverse-engineering INPUT only via the copy at `olamni/tutorial/ch02/spec-rev-eng-input/ch02-DEPRECATED-spec.md`.

- **FR-013** Implementation MUST plan-then-act at every step: present a numbered plan and await explicit project-owner approval before writing any file other than the plan itself. Multi-step file-writing batches MUST be paused between major artifacts (the .glp files, the trace, the tutorial, the signpost) to allow review. The variation shapes for ex-02 (`append_and_sum/4`) and ex-03 (`timed_append/3`) are LOCKED in this spec (per the Clarifications); /speckit-plan MUST NOT re-decide them, only refine subordinate decisions (helper-procedure decomposition, inspection-goal selection, task ordering). If a downstream session believes the locked shape is wrong, it MUST halt and propose a spec amendment; it MUST NOT silently substitute a different shape.

- **FR-014** Trace byte-equality contracts by exercise: `ex-01-repl-trace.md` and `ex-02-repl-trace.md` are governed by the strict rule — byte-equal modulo REPL banner / build wallclock lines (per FR-004 and the Clarifications session). `ex-03-repl-trace.md` is permitted a deliberate exception: the elapsed-ms value emitted via `'_output'(elapsed_ms(N))` is wallclock-derived and varies per run; the trace's annotation MUST document this explicitly ("varies per run; the SHAPE matters, not the specific number"), and the auditor's reproducibility check ignores the elapsed-ms VALUE while still requiring the `_output` line's STRUCTURE to be byte-equal.

- **FR-015** ex-02 and ex-03 `.glp` files MUST NOT import code from any chapter beyond ch 4 §4.2's `append/3` (per the Clarifications). The only permitted external dependencies are: (a) the duplicated GLP `append/3` from PDF pp 31–32, (b) the `:=` operator and the comparison guards declared in `programs/self.glp`, (c) `now/1` and `'_output'/1` declared in `programs/self.glp` (ex-03 only). Helper procedures (e.g., `sum/2` for ex-02) MUST be defined locally in the same `.glp` file.

- **FR-016** ch02 exercise files (the `.glp` files under `olamni/tutorial/ch02/exercise-NN/`) MUST NOT be added to `test/run_all_tests.sh` or any other Dart-test entry point (per the Clarifications). The trace capture during /speckit-implement serves as the one-shot smoke test; ongoing regression coverage is the harness's existing 476 tests, not the tutorial files.

### Key Entities

- **Exercise**: A subdirectory under `olamni/tutorial/chXX/` named `exercise-NN/`. For chapter 2, ex-01 contains TWO `.glp` files (the contrast pair) plus one `ex-NN-tutorial.md` step-through guide and one `ex-NN-repl-trace.md` verbatim REPL session; ex-02 and ex-03 each contain ONE `.glp` plus the same two markdown files.
- **Chapter Tutorial**: A directory `olamni/tutorial/chXX/` containing the chapter sources index (`chXX-sources.md`), the rev-eng-input prompt (`chXX-specification-input-prompt.md`), the chapter signpost (`chXX_tutorial.md`), the rev-eng-input copy of the deprecated spec (`spec-rev-eng-input/chXX-DEPRECATED-spec.md`), and one or more `exercise-NN/` subdirs.
- **Top-level Tutorial Index**: `olamni/tutorial/tutorial.md`. Built incrementally as chapters are approved; final completion pass when all 13 chapters are done.
- **Approval Gate**: A documented checkpoint between exercises (or between major implementation steps within an exercise) where the project owner must explicitly approve before downstream work may begin. Three gates govern this chapter: ex-02 gate (predecessor approved + REPL-tested), ex-03 gate (same with ex-02), and the variation-shape gates (the specific concrete shape for ex-02 / ex-03 must be approved before any `.glp` is written).
- **Body Kernel**: A runtime-implemented predicate in `glp_runtime/lib/runtime/body_kernels.dart` that executes inline. Tutorial code uses these via the GLP-level procedures defined in `programs/self.glp` (e.g., `:=`, `now/1`, `'_output'/1`); tutorial code MUST NOT call the kernels (`'_add'`, `_now`, `_output`, …) directly.
- **Cross-chapter Import**: A code block from a later chapter (here, ch 4 §4.2's GLP `append/3`) used inside an earlier chapter's tutorial. The header comment of the importing `.glp` documents the provenance explicitly. Chapter 2 is the only chapter where this pattern is anticipated; it is required because chapter 2's own code is too thin alone.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** A learner who has read §2.1 + §2.2 can complete exercise-01 — load both files, observe the rejection, observe the success, run the four goals, interpret the output — in under 10 minutes given a working GLP REPL.
- **SC-002** `ch-02-ex-01-classical-append-LP-only.glp` is REJECTED at load by the GLP REPL with an SRSW-violation error message; the rejection is captured verbatim in `ex-01-repl-trace.md`.
- **SC-003** `ch-02-ex-01-glp-append.glp` is ACCEPTED at load by the GLP REPL with zero errors (no SRSW violation, no type error, no compile error).
- **SC-004** The primary goal `append([1,2,3], [a,b,c], Zs).` returns the locked binding `Zs = [1, 2, 3, a, b, c]` and the REPL prints `→ succeeds`. Empirically verified during implementation; mismatch is a halt-and-report bug.
- **SC-005** `ex-01-repl-trace.md` is byte-equal (modulo REPL banner / build wallclock lines) to a fresh REPL session re-run by an auditor on the same code.
- **SC-006** The classical-LP clauses in `ch-02-ex-01-classical-append-LP-only.glp` are byte-identical to Example 2.1 on PDF p 10 (after stripping the header comment block).
- **SC-007** The GLP `append/3` clauses in `ch-02-ex-01-glp-append.glp` are byte-identical to the corresponding two clauses on PDF pp 31–32 (after stripping the header comment block and the `%%` per-clause paraphrase comments).
- **SC-008** `exercise-02/` and `exercise-03/` directories do NOT exist on disk until the corresponding approval gates are passed (verifiable via `git log` and the directory listing); attempts to create them while predecessor status is non-`approved` are blocked by the implementing session.
- **SC-009** When ex-02 is implemented, its `.glp` exercises at least one `:=` arithmetic operator from `{+, -, *, /, //, mod, abs}` and runs to completion against the chosen primary demo goal; the trace shows the math output verbatim.
- **SC-010** When ex-03 is implemented, its `.glp` calls `now/1` at least twice and `'_output'/1` at least once, AND reuses the ex-02 arithmetic; the trace shows the `_output`-printed lines verbatim with the elapsed-ms annotation documenting per-run variation.
- **SC-011** Zero files under `specs/003-tutorial-ch02/` (other than this `spec.md` and downstream `/speckit-*`-generated artifacts) carry speckit-output formatting written by Claude impersonating the speckit pipeline. The `QUARANTINE-DO-NOT-USE/` subfolder remains untouched.
- **SC-012** All three approval gates (ex-02, ex-03, variation-shape) are observable post-hoc: predecessor `exercise-NN: approved YYYY-MM-DD` lines in `ch02_tutorial.md`'s status block. The variation-shape decisions for ex-02 (`append_and_sum/4`) and ex-03 (`timed_append/3`) are locked in this spec's Clarifications and are observable directly in `spec.md` (not in `research.md`, which captures only the subordinate decompositions).
- **SC-013** When ex-02 is implemented, running `append_and_sum([1,2,3], [4,5,6], Sum).` against the loaded ex-02 `.glp` returns `Sum = 21` AND prints `→ succeeds`. (Per Clarifications Q3a, the procedure shape is `/3`; the intermediate appended list is internal.) Empirically verified during /speckit-implement; mismatch is a halt-and-report bug.
- **SC-014** When ex-03 is implemented, running `timed_append([1,2,3], [a,b,c], Zs).` against the loaded ex-03 `.glp` returns `Zs = [1, 2, 3, a, b, c]` AND emits one `'_output'`-printed line per invocation of the form `elapsed_ms(N)` where `N` is a non-negative integer. The integer value varies per run and is not constrained. (Each separate `timed_append/3` goal produces exactly one such line; multiple goals in one REPL session produce one line each, in order.)
- **SC-015** No ex-02 or ex-03 `.glp` file imports code from any chapter beyond ch 4 §4.2's `append/3`. Verifiable by inspecting the `.glp` file: only locally-defined procedures + the duplicated `append/3` + `self.glp`-declared procedures (`:=`, `now/1`, `'_output'/1`) are referenced.
- **SC-016** No ch02 tutorial `.glp` file appears in `test/run_all_tests.sh` or any other test entry point. Verifiable by `grep "olamni/tutorial/ch02" test/run_all_tests.sh` returning zero matches.

## Assumptions

- The "user" of this feature is the **learner** reading Chapter 2 of *The Art of Grassroots Logic Programming* (Shapiro, 2025). This interpretation is taken from `olamni/tutorial/charter.md` design principle 2 ("Reader on §X.Y loads the matching file/project").
- **PDF source of truth.** `GLP_ART.pdf` p 10 is the canonical Example 2.1 (classical LP append). `GLP_ART.pdf` pp 31–32 is the canonical GLP `append/3`. If `olamni/tutorial/ch02/ch02-sources.md` shows a slightly different transcription (e.g., a missing `?` annotation), the PDF wins and is corrected by re-reading byte-exactly during implementation.
- **REPL availability.** The host machine has a working Dart SDK (`^3.9.4`); the implementing Claude session verifies `dart --version` before attempting to build `glp_runtime/bin/glp_repl.dart` into an executable. If Dart is absent, implementation halts and the project owner is consulted.
- **Charter governance.** `olamni/tutorial/charter.md` governs grouping, file-naming, step-by-step alignment, and per-chapter scope per Constitution Principle VI. The cross-chapter import from ch 4 §4.2 is explicitly documented in the input prompt and in the importing file's header comment.
- **Body kernel availability.** The runtime kernels for arithmetic (`_add`, `_sub`, `_mul`, `_div`, `_idiv`, `_mod`, `_abs`), system time (`_now`), and ground-term output (`_output`) are wired up in `glp_runtime/lib/runtime/body_kernels.dart` and exposed at the GLP level by `programs/self.glp` (via `:=`, `now/1`, `'_output'/1`). The tutorial USES these but does NOT reimplement them. If a kernel is missing or behaves differently than `body_kernels.dart` describes, the implementing session halts and reports.
- **Top-level `tutorial.md` already exists** with chapter 1's row from the ch01 implementation; ch02's row is added/updated by this spec's implementation. Subsequent chapters extend it.
- **Approval gate is human-only.** The project owner explicitly approves each step; no automated gating mechanism is required at this layer (the gate is procedural, enforced by the implementing Claude session).
- **Status-block format** (single source of truth, repeated in `ch02_tutorial.md`):
  ```
  ## Exercise status

  - exercise-01: <status> [<date>]
  - exercise-02: <status> [<date or empty>]
  - exercise-03: <status> [<date or empty>]
  ```
  `<status>` ∈ {`approved YYYY-MM-DD`, `pending exercise-N approval`, `not yet implemented`}.
- **Variation-shape choice is downstream.** The specific concrete shape for ex-02's arithmetic predicate (e.g., `append_and_sum/4` vs `append_with_running_total/4` vs `length_via_append/3`) and for ex-03's timing-and-output predicate (e.g., `timed_append/3` vs `traced_append/3` vs `bench_append_and_sum/4`) is chosen during /speckit-plan, not in this spec. The spec mandates the kernel-coverage requirements (FR-009, FR-010); the plan picks the shape and records the project owner's approval in `research.md`.
- **Out of scope.** Definitions 2.1–2.10 and 2.11–2.12 (formal-track material), Example 2.2 (resource interpretation, narrative-only), the chapter-4 `reverse/2` and `reverse_acc/3` definitions BEYOND the GLP `append/3` import, the trigonometric / logarithmic / exponential math kernels, the time guards `wait/1` and `wait_until/1`, the mutual-reference / multi-way-merge kernels, madGLP `_send`, and any chapter beyond 2 — all out of scope for this spec.
