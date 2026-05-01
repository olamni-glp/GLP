# Feature Specification: Olamni Tutorial — Chapter 6 (Typed Programming)

**Feature Branch**: `007-tutorial-ch06`
**Created**: 2026-05-01
**Status**: Draft
**Input**: User description: "Build a tutorial for chapter 6 of the GLP book — 'Typed Programming.' The PDF chapter is a stub: only the title and five section headings (§6.1 Difference Lists / §6.2 Quicksort / §6.3 Equators: Emergency Brake / §6.4 Bidirectional Communication / §6.5 Buffered Communication), no body text, no Programs. Synthesise the chapter from chapters 1–5: one exercise per §6.x heading, each re-presenting the closest matching Program already established in an earlier chapter, with type and `procedure` declarations added on top per ch05 conventions. Five exercises total; pairwise approval gates between them (chapter is small enough that ch04/ch05's group gates are unnecessary). Source map: ex-01 §6.1 ← ch04 §4.2.3+§4.2.4 `reverse`+`reverse_acc` (accumulator-passing as the difference-list analogue); ex-02 §6.2 ← ch05 §5.6 typed quicksort byte-exact; ex-03 §6.3 ← ch04 §4.4.4 control meta-interpreter `run/5`+`suspended_run/4` (the abort control-stream message IS the emergency-brake demonstration); ex-04 §6.4 ← ch03 §3.2 channel ops `send`+`receive`+`new_channel`+`relay`+`make_pair`; ex-05 §6.5 ← ch04 §4.2.12+§4.2.13 `bb`+`bb_test` sliding-window buffer. Byte-exact code from cited earlier-chapter PDF source; type/procedure declarations added are NOT byte-exact (they are introduced fresh at §6.x per ch05 conventions). Each exercise gets its own `.glp` + `tutorial.md` + `repl-trace.md`; chapter signpost `ch06_tutorial.md` carries status block + plain-prose synthesis explanation. Cross-chapter relationship documented in three places (`.glp` header, signpost, top-level `tutorial.md`). Plain-prose input prompt at `olamni/tutorial/ch06/ch06-specification-input-prompt.md` drives this spec."
**Constitution**: `.specify/memory/constitution.md` v1.2.0 — Principle I (Spec-First) requires this spec exist before implementation. Because this spec touches `olamni/tutorial/**`, Principle VI requires citing `olamni/tutorial/charter.md` (cited in Assumptions). The plain-prose input prompt is `olamni/tutorial/ch06/ch06-specification-input-prompt.md`; per ch01–ch05 precedent, the input prompt and this spec are separate artifacts on purpose — the prompt strips speckit ceremony, the spec adds it.

## Clarifications

### Session 2026-05-01

- Q: For the synthesis analogues for ex-01 (Difference Lists) and ex-03 (Equators: Emergency Brake), should we accept the input prompt's choices (ch04 reverse/reverse_acc + ch04 control MI), or pick different sources? → A: Accept ex-03's analogue (ch04 §4.4.4 control meta-interpreter `run/5`+`suspended_run/4`); for ex-01, use **ch04 §4.3.7 `flatten`+`flatten_acc`** (book pp 38–39) instead — the flatten-with-accumulator is closer in pedagogical shape to the difference-list idiom than reverse/reverse_acc. The cross-reference to ex-01 in the input prompt is superseded by this clarification.

- Q: Should specific type definitions and `procedure` declaration shapes (introduced fresh at §6.x on top of byte-exact source clauses) be locked at the spec layer, or deferred to /speckit-plan T006-equivalent? → A: **Defer to /speckit-plan T006-equivalent**, per ch05 Q2 precedent. The implementer proposes specific declaration shapes during /speckit-plan; the project owner approves; decisions are recorded in `research.md`. Each declaration MUST itself satisfy SRSW + the live type-checker at REPL load (per FR-018 verification); mismatch with the analyser at load is halt-and-amend per FR-013 (the declaration shape is amendable; the byte-exact source clause body is locked). Reasoning: locking declaration shapes at the spec layer risks ch05-style halt-and-amend cycles (Q4 `NumList`→`List`, Q7 §5.3+§5.4 merger, Q10 qsort declaration) where spec-locked shapes conflicted with the type-checker. Empirical verification at /speckit-implement is the cheaper validation point.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Difference Lists exercise (Priority: P1)

A learner who has just finished reading §6.1 in the book opens `olamni/tutorial/ch06/exercise-01/`, reads the tutorial, loads the `.glp` in the REPL, runs the primary demo goal plus three inspection goals, and observes the flatten-with-accumulator pattern (drawn from ch04 §4.3.7 `flatten/2` + `flatten_acc/3`) re-presented as the difference-list idiom under the §6.1 banner.

**Why this priority**: §6.1 is the chapter's first heading; the synthesis-from-earlier-chapter pattern is established here and re-used in every subsequent §6.x exercise.

**Independent Test**: Load `ch-06-ex-01-difference-lists.glp` in a fresh REPL, run the primary goal, observe the locked binding. Independent of ex-02..ex-05.

**Acceptance Scenarios**:

1. **Given** the learner has built the REPL per the chapter signpost, **When** they load the ex-01 `.glp` file, **Then** the file loads with `✓ Loaded:` and no SRSW or type-check errors.
2. **Given** the file is loaded, **When** the learner runs the primary demo goal, **Then** the REPL prints the locked binding byte-exactly as captured in `ex-01-repl-trace.md`.
3. **Given** the learner reads the `.glp` header comment, **When** they look for the cross-chapter source citation, **Then** the header explicitly names ch04 §4.3.7 (book pp 38–39) as the origin and §6.1 as the §-section under which it is re-presented.

---

### User Story 2 - Typed Quicksort exercise (Priority: P1)

A learner who has just finished reading §6.2 opens `olamni/tutorial/ch06/exercise-02/`, loads the `.glp`, and observes the typed quicksort algorithm (byte-exact from ch05 Program 5.6, p 51) re-presented under the §6.2 banner.

**Why this priority**: §6.2 is the cleanest direct match — ch05 §5.6 IS the typed quicksort the chapter heading names. This exercise validates that re-presenting an earlier-chapter typed Program under a ch06 §-heading works end-to-end with no semantic gap.

**Independent Test**: Load `ch-06-ex-02-typed-quicksort.glp` in a fresh REPL, run `quicksort([3,1,4,1,5,9,2,6], Sorted).` (or the locked primary goal selected at /speckit-plan), observe `Sorted = [1, 1, 2, 3, 4, 5, 6, 9]`.

**Acceptance Scenarios**:

1. **Given** the learner has built the REPL, **When** they load the ex-02 `.glp` file, **Then** the file loads cleanly and the typed quicksort procedure declarations + clauses pass the live type-checker.
2. **Given** the file is loaded, **When** the learner runs the primary sort goal, **Then** the binding matches `ex-02-repl-trace.md` byte-exactly.
3. **Given** the file is loaded, **When** the learner runs the three inspection goals, **Then** every clause of `quicksort/2`, `qsort/3`, and `partition/4` is exercised by at least one of the four goals.

---

### User Story 3 - Equators: Emergency Brake exercise (Priority: P1)

A learner who has just finished reading §6.3 opens `olamni/tutorial/ch06/exercise-03/`, loads the `.glp`, runs the primary demo goal, sends the `abort` message on the control stream, and observes the control meta-interpreter (drawn from ch04 §4.4.4 `run/5` + `suspended_run/4`, book p 42) halting an in-flight computation under the §6.3 banner.

**Why this priority**: §6.3's "Emergency Brake" semantics — mutual termination via a shared control message — is the synthesis analogue's central pedagogical point; without an abort-able example, the §6.3 heading has no demonstration.

**Independent Test**: Load `ch-06-ex-03-equators-emergency-brake.glp` in a fresh REPL, start a long-running goal under the control meta-interpreter with an abort message queued, observe the goal halts when the abort arrives.

**Acceptance Scenarios**:

1. **Given** the learner has built the REPL, **When** they load the ex-03 `.glp` file, **Then** the file loads cleanly with the typed control-meta-interpreter procedures registered.
2. **Given** the file is loaded, **When** the learner runs the primary control-stream demo goal, **Then** the abort message terminates the in-flight computation and the trace shows the suspended state.
3. **Given** the learner reads the `.glp` header, **When** they look for the cross-chapter citation, **Then** the header explicitly names ch04 §4.4.4 (book p 42) as the origin and §6.3 as the §-section under which it is re-presented.

---

### User Story 4 - Bidirectional Communication exercise (Priority: P1)

A learner who has just finished reading §6.4 opens `olamni/tutorial/ch06/exercise-04/`, loads the `.glp`, allocates a channel pair via `new_channel/2`, sends a value through one end, receives it on the other, and observes bidirectional message flow under the §6.4 banner.

**Why this priority**: §6.4's bidirectional channel pattern is foundational for chapters 7+ (concurrent programming, multi-agent systems) — this exercise establishes the typed channel idiom that those chapters build on.

**Independent Test**: Load `ch-06-ex-04-bidirectional-communication.glp` in a fresh REPL, run the primary `new_channel`+`send`+`receive` goal, observe the value crossing the channel pair.

**Acceptance Scenarios**:

1. **Given** the learner has built the REPL, **When** they load the ex-04 `.glp` file, **Then** the typed `Channel` definition + `send/3` + `receive/3` + `new_channel/2` + `relay/3` + `make_pair/2` clauses load cleanly.
2. **Given** the file is loaded, **When** the learner runs the primary bidirectional-message goal, **Then** the message crosses the channel and the locked binding matches the trace.
3. **Given** the file is loaded, **When** the learner runs the inspection goals, **Then** every channel-op clause (send, receive, new_channel, relay) is exercised.

---

### User Story 5 - Buffered Communication exercise (Priority: P1)

A learner who has just finished reading §6.5 opens `olamni/tutorial/ch06/exercise-05/`, loads the `.glp`, runs the bounded-buffer demo (ch04 §4.2.12 `bb/0` + §4.2.13 `bb_test/0`, book pp 34–35), and observes a producer–consumer pair sharing a sliding-window buffer under the §6.5 banner.

**Why this priority**: §6.5 closes the chapter; without it the chapter is incomplete. Buffered communication is a direct match in ch04, so the synthesis is straightforward.

**Independent Test**: Load `ch-06-ex-05-buffered-communication.glp` in a fresh REPL, run `bb_test.`, observe the bounded-buffer producer–consumer pair completing and printing the captured values.

**Acceptance Scenarios**:

1. **Given** the learner has built the REPL, **When** they load the ex-05 `.glp` file, **Then** the typed `bb`/`bb_test`/`producer`/`consumer` clauses load cleanly.
2. **Given** the file is loaded, **When** the learner runs `bb_test.`, **Then** the captured output matches `ex-05-repl-trace.md` byte-exactly (modulo any wallclock-derived elements explicitly annotated as varying per run).
3. **Given** the learner reads the chapter signpost, **When** they look for the §6.5 entry, **Then** it explicitly cross-references ch04 §4.2.12 + §4.2.13 (book pp 34–35) as the source.

---

### Edge Cases

- **PDF stub state changes between sessions**: if the author fills in the ch06 PDF body between the spec and the implement phase, the implementer halts and asks whether to fold native PDF content into the synthesised exercises (potentially superseding the synthesis sources).
- **Earlier-chapter source has drifted**: if the byte-exact re-read of a ch01–ch05 source program reveals drift from the cited `chXX-sources.md`, the implementer halts per FR-013 and proposes a Clarifications amendment rather than silently picking one form.
- **Type declaration introduces a SRSW or mode-check failure**: if adding type/procedure declarations to a ch01–ch05 byte-exact body causes the live type-checker to reject what loaded fine in the source chapter, the implementer halts and proposes a declaration amendment (the byte-exact clause body is locked; only the introduced declarations are amendable).
- **Equators idiom interpretation gap**: the literal "equator" idiom in GLP literature refers to a mutual-termination guard pair, distinct from the control-MI's abort message. The input prompt selected the control MI as the closest analogue available in ch01–ch05; if the project owner judges the gap too wide, ex-03 is renegotiated during /speckit-clarify.
- **Difference-list idiom interpretation gap**: literal difference lists use an explicit `(Front, Back)` pair representation; ch04's `flatten_acc` (per Q1) uses single-accumulator threading, which is the spirit but not the literal data shape. The Q1 clarification preferred `flatten`+`flatten_acc` over `reverse`+`reverse_acc` because the nested-list flattening exposes more difference-list-style structure manipulation, but the gap to a literal `(Front, Back)` pair remains.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chapter MUST deliver exactly five exercises, one per §6.x heading (§6.1 Difference Lists, §6.2 Quicksort, §6.3 Equators: Emergency Brake, §6.4 Bidirectional Communication, §6.5 Buffered Communication).
- **FR-002**: Each exercise's GLP code body MUST be byte-exact from the cited earlier-chapter PDF source; the literal-source mandate inherited from ch01–ch05 applies to the *clauses*. Type definitions and `procedure` declarations introduced fresh at §6.x are NOT byte-exact (they are added on top per ch05 conventions) — this exception is explicitly authorised.
- **FR-003**: The cited source programs are: ex-01 ← ch04 §4.3.7 `flatten`+`flatten_acc` (book pp 38–39, per Q1 clarification); ex-02 ← ch05 §5.6 (book p 51); ex-03 ← ch04 §4.4.4 (book p 42); ex-04 ← ch03 §3.2 (book p 23); ex-05 ← ch04 §4.2.12 + §4.2.13 (book pp 34–35). The implementer re-reads each source PDF page byte-exactly during /speckit-implement before writing the corresponding `.glp`.
- **FR-004**: Each exercise's `.glp` file MUST carry a header comment block citing both the original earlier-chapter PDF source AND the §6.x heading under which it is re-presented; the synthesis-from-earlier-chapter status MUST be stated explicitly in the header.
- **FR-005**: Each clause in each `.glp` file MUST carry a `%%` paraphrase comment per charter §1.5.
- **FR-006**: Each exercise MUST have one primary demo goal plus three inspection goals (chosen during /speckit-plan with project-owner approval), collectively exercising every clause of every Program in the exercise.
- **FR-007**: Each goal's binding MUST be locked (proposed at /speckit-plan, empirically verified at /speckit-implement against the actual REPL on this Windows host); mismatch is halt-and-report per the ch01–ch05 precedent.
- **FR-008**: Pairwise approval gates govern exercise sequencing: `exercise-NN: approved YYYY-MM-DD` MUST be present in `ch06_tutorial.md`'s status block before exercise-(NN+1) work begins.
- **FR-009**: Each exercise MUST produce three artefacts under `olamni/tutorial/ch06/exercise-NN/`: `ch-06-ex-NN-<short-name>.glp`, `ex-NN-tutorial.md`, `ex-NN-repl-trace.md`.
- **FR-010**: The chapter signpost `ch06_tutorial.md` (note underscore) MUST carry a brief intro to the chapter's stub-source-and-synthesis nature, build instructions, links to the five exercises with one-line summaries, and a status block with one line per exercise.
- **FR-011**: The top-level `olamni/tutorial/tutorial.md` MUST be updated incrementally — ch06's row flips from `planned` to `pending review (YYYY-MM-DD)` once any exercise lands and to `implemented YYYY-MM-DD` once all five are approved.
- **FR-012**: Each `ex-NN-repl-trace.md` MUST be byte-equal to the actual REPL output modulo REPL banner / build wallclock lines (no per-run-variation relaxation expected for ch06; if any wallclock-derived element appears, the trace's annotation MUST mark it "varies per run; the SHAPE matters, not the specific number" per the ch02 FR-014 precedent).
- **FR-013**: The implementing session MUST halt and report on any discrepancy between the cited PDF source and the as-loaded REPL behaviour; no silent spec rewrite, no "robustness" workarounds. Spec amendments during /speckit-implement go through a documented Q-amendment per the ch02–ch05 precedent.
- **FR-014**: The cross-chapter relationship MUST be documented in three places per exercise: (a) the `.glp` header comment block; (b) the chapter signpost's plain prose; (c) the top-level `tutorial.md` row carries a footnote stating that ch06's content is synthesised from earlier chapters because the PDF chapter is a stub.
- **FR-015**: The implementing session MUST re-read the ch06 PDF page (book p 53) byte-exactly during /speckit-implement to confirm the stub state has not changed between sessions; if the author has filled in body text, the implementer halts per FR-013.
- **FR-016**: Per the ch01–ch05 tutorial-chapter exception (CLAUDE.md §11), per-chapter `.glp` files under `olamni/tutorial/ch06/` are NOT added to `test/run_all_tests.sh`; the captured REPL traces ARE the regression artefacts.
- **FR-017**: The synthesis analogues for ex-01 (Difference Lists ← ch04 §4.3.7 `flatten`+`flatten_acc` per Q1 clarification) and ex-03 (Equators: Emergency Brake ← ch04 §4.4.4 control meta-interpreter) are approximate, not literal — the input prompt's original ex-01 choice (ch04 §4.2.3+§4.2.4 reverse/reverse_acc) is superseded by Q1. The approximate-analogue status MUST be stated explicitly in each affected `.glp` header per FR-004 + FR-014.
- **FR-018**: The added type and `procedure` declarations MUST be consistent with ch05's mode-checking flow and pass the live type-checker (which is operational from ch05 onward). Per Q2 clarification, specific declaration shapes are deferred to /speckit-plan T006-equivalent with project-owner approval recorded in `research.md` (ch05 Q2 precedent); mismatch with the analyser at load is halt-and-amend per FR-013 — the declaration shape is amendable, the byte-exact source clause body is locked.

### Key Entities

- **Exercise**: a self-contained tutorial unit identified by `exercise-NN` (NN ∈ 01..05), comprising one `.glp` source file, one tutorial markdown file, and one REPL trace markdown file. Each exercise corresponds to exactly one §6.x heading.
- **Source Program**: the earlier-chapter byte-exact PDF block (one per exercise) from which the exercise's clause body is transcribed.
- **Approval Gate**: a state predicate `exercise-NN: approved YYYY-MM-DD` in the status block; gates ex-(NN+1) work. Four gates total (between ex-01→ex-02, ex-02→ex-03, ex-03→ex-04, ex-04→ex-05).
- **Cross-chapter Relationship**: the documented link between a ch06 exercise and its earlier-chapter source, recorded in the `.glp` header, the chapter signpost, and the top-level tutorial index.
- **Chapter Signpost**: `olamni/tutorial/ch06/ch06_tutorial.md` (note underscore) — chapter-level navigation page; carries the status block, build instructions, exercise links, synthesis explanation.
- **Top-level Index**: `olamni/tutorial/tutorial.md` — chapter-by-chapter entry point; ch06's row is updated incrementally as exercises land.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All five exercises (ex-01..ex-05) MUST be approved (`exercise-NN: approved YYYY-MM-DD` present in `ch06_tutorial.md`'s status block) for the chapter to be considered complete.
- **SC-002**: Each exercise's `.glp` file MUST load in the REPL within 5 seconds on this Windows host (Dart 3.10.1, kernel-snapshot-driven REPL) — the same load-time budget inherited from ch01–ch05.
- **SC-003**: 100% of each exercise's REPL trace MUST be byte-equal to a fresh re-run on the same REPL build, modulo banner / wallclock lines and any explicitly annotated varies-per-run segments.
- **SC-004**: The chapter signpost MUST list all five exercises with one-line summaries each, in §6.x section order, so a learner can locate any exercise from its section number by visual scan (structural test — verifying the signpost contains 5 numbered entries with §6.x cross-references; no timing measurement).
- **SC-005**: 100% of exercise `.glp` files MUST cross-reference both their earlier-chapter source AND the §6.x heading under which they are re-presented (FR-014 verified).
- **SC-006**: 100% of exercise `.glp` files MUST pass the live type-checker (the third stage of the REPL pipeline, operational from ch05 onward) — no silent type errors slipping past the load step.

## Assumptions

- The plain-prose input prompt at `olamni/tutorial/ch06/ch06-specification-input-prompt.md` faithfully captures the project owner's intent for the chapter; this spec encodes that prompt's content into speckit ceremony without altering the substantive scope.
- The ch06 PDF page (book p 53) remains a stub at /speckit-implement time. If the author fills in body text between now and then, FR-015's halt-and-report applies.
- The REPL infrastructure (Dart 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`, kernel snapshot pattern, AOT exe build with `--define=GLP_BUILD_COMMIT=...`) is inherited from ch01–ch05 and operational; the implementing session verifies a baseline test run before any /speckit-implement task begins.
- The live type-checker (REPL pipeline stage 3) is operational; ch05 R-006 verified this at the start of ch05 implement and ch06 inherits without re-verification unless the REPL build has changed.
- Charter §1 (REPL-only for chapters 1–6) applies — no Flutter project, no module structure, no exported types. Cited per Constitution Principle VI.
- The Constitution `.specify/memory/constitution.md` is at v1.2.0 (the version cited in ch05's spec); if it has bumped between ch05 and ch06, /speckit-clarify or /speckit-plan reconciles.
- Pairwise approval gates (rather than ch04/ch05's group gates) are appropriate for a 5-exercise chapter — the chapter is small enough that group gates would conflate too many decisions per gate.
- Cross-chapter source programs in ch01–ch05 are stable as of 2026-05-01 (ch05 was completed 2026-05-01; ch01–ch04 earlier). Re-reading the cited `chXX-sources.md` files plus the byte-exact PDF pages catches any drift.
- The ch01–ch05 tutorial-chapter exception (per CLAUDE.md §11) extends to ch06 — its `.glp` files are NOT added to `test/run_all_tests.sh`; the captured REPL traces are the regression artefacts (FR-016).
- The synthesis-from-earlier-chapters approach is the only viable way to produce a runnable ch06 tutorial given the PDF stub state; the alternative (waiting for the author to fill in the chapter) is out of scope.
- The polluted speckit-output `olamni/tutorial/ch06/spec-rev-eng-input/ch06-DEPRECATED-spec.md` is rev-eng input only and is NOT authoritative; this spec supersedes it.
