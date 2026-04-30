---

description: "Task list for Olamni Tutorial Chapter 4 — Basic Concurrent Programming"
---

# Tasks: Olamni Tutorial — Chapter 4 (Basic Concurrent Programming)

**Input**: Design documents from `specs/005-tutorial-ch04/`
**Prerequisites**: plan.md, spec.md (with 3 Clarifications Q1+Q2+Q3), research.md (R-001..R-009), data-model.md, contracts/ (3 files), quickstart.md
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V. All ~38 ch04 Programs are SRSW-compliant by byte-exact construction (Principle III). Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI.

**Tests**: Captured REPL traces ARE the regression artifacts. No new Dart unit tests. Per FR-016, ch04 files NOT in `test/run_all_tests.sh`. Baseline `bash test/run_all_tests.sh` MUST pass before AND after implementation per Principle V (485/485 expected per ch03 ship state).

**Organization**: Tasks grouped by user story per spec.md AND by sub-section group (NEW for ch04 — group-boundary gates per FR-008+FR-009). US1+US2+US3+US4 (P1+P2) cover the four sub-section groups; US5 (P1) covers per-exercise traces+tutorials interleaved with each US1–4 group; US6 (P2) covers chapter signpost; US7 (P3) covers top-level index.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1..US7); composite labels like [US1+US5] for tasks spanning stories.

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verify Dart SDK: `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. Set `DART="/c/Users/gavri/dart-sdk/bin/dart"`.
- [ ] T002 Verify or rebuild REPL exe at `glp_runtime/glp_repl.exe`. If `claude/fix-misleading-build-line` merged, use `--define=GLP_BUILD_COMMIT=...`; else build without (record in research.md).
- [ ] T003 Verify `.gitignore` covers `glp_runtime/glp_repl*` and `glp_runtime/.dart_tool/` (inherited from ch01).
- [ ] T004 Record baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — expect 485/485 PASS. Record actual baseline number.
- [ ] T005 Verify spec inputs: `specs/005-tutorial-ch04/spec.md`, `olamni/tutorial/ch04/ch04-specification-input-prompt.md`, `olamni/tutorial/ch04/ch04-sources.md`, `olamni/tutorial/ch04/spec-rev-eng-input/ch04-DEPRECATED-spec.md` all exist.

**Checkpoint**: Phase 1 complete — Dart, REPL, baseline, spec inputs all verified.

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T006 Re-read `GLP_ART.pdf` book pp 25–43 (PDF pp 37–55) byte-exactly for ALL ch04 source code blocks + relevant prose. Note any drift vs `ch04-sources.md`; correct sources file BEFORE proceeding. Per ch01 R-006 lesson, this is non-negotiable for all ~38 Programs.
- [ ] T007 Confirm subordinate decisions with project owner (auto-mode-approved during /speckit-plan):
  - R-008 filenames: locked per research.md (10 filenames listed).
  - R-009 within-group sequencing + group-boundary gate enforcement: per FR-009.
  - Per-exercise inspection-goal selection: deferred to T-NN-PROPOSE within each exercise's task block (per R-004).

**Checkpoint**: Phase 2 complete — PDF re-read done; subordinate decisions confirmed.

---

## Phase 3: Group §4.1 — User Story 1 (Constants + Compound Circuits, P1)

**Predecessor gate**: Chapter signpost exists (created during this group's work).

### ex-01 (Programs with Constants + Logic Gates)

- [ ] T010 [US1] Create `olamni/tutorial/ch04/exercise-01/`.
- [ ] T011 [US1] Write `ch-04-ex-01-constants-and-gates.glp` per contracts/glp-file-format.md File 1: 4.1.1 `p(a)` + 4.1.2 `q(b)/q(a)` + 4.1.3 logic gates (17 unit clauses byte-exact from book pp 25–28).
- [ ] T012 [US1] Verify load: `printf "<path>\n:quit\n" | $DART run repl.dill` → `✓ Loaded:`. If rejected, HALT.
- [ ] T013 [US1] Propose 1 primary + 3 inspection goals to project owner (auto-mode-approved). Examples: primary `and(0, 1, R).` → `R = 0`; inspections `or(1, 0, X)`, `not(1, N)`, `xor(1, 1, X)`.
- [ ] T014 [US1] Run 4-goal session + capture verbatim. Verify locked bindings.
- [ ] T015 [US5] Write `ex-01-repl-trace.md` per contracts/trace-file-format.md (5 phases). Strict byte-equality.
- [ ] T016 [US5] Write `ex-01-tutorial.md` — learner step-through.

### ex-02 (Compound Circuits)

- [ ] T020 [US1] Create `olamni/tutorial/ch04/exercise-02/`.
- [ ] T021 [US1] Write `ch-04-ex-02-compound-circuits.glp` per contracts/glp-file-format.md File 2: 4.1.4 `nand/3` + 4.1.5 `half_adder/4` + 4.1.6 `full_adder/5` + duplicated logic gates from ex-01 (per FR-010 self-containment). 17 clauses total. References Formal 4.1 + Formal 4.3.
- [ ] T022 [US1] Verify load. If rejected, HALT.
- [ ] T023 [US1] Propose primary + 3 inspection goals. Example: primary `full_adder(1, 1, 0, S, C).` → `S = 0, C = 1`.
- [ ] T024 [US1] Run 4-goal session + capture.
- [ ] T025 [US5] Write `ex-02-repl-trace.md`.
- [ ] T026 [US5] Write `ex-02-tutorial.md`.

### Chapter signpost + top-level index (interleaved with §4.1 group)

- [ ] T030 [US6] Write `olamni/tutorial/ch04/ch04_tutorial.md` per contracts/status-block-format.md initial state (10 status lines). Document cross-chapter inversion + group-boundary gate model.
- [ ] T031 [US6] Verify status block grep-friendly: `grep -E "^- exercise-NN:" ch04_tutorial.md` returns 10 matches.
- [ ] T032 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch04 row from `planned` to `pending review (YYYY-MM-DD)`. Link target → `ch04/ch04_tutorial.md`.

### §4.1 group approval gate (Phase 3 exit)

- [ ] T040 [US1+US5+US6+US7] Run baseline tests: 485/485 PASS expected.
- [ ] T041 [US1+US5+US6+US7] Show §4.1 group diff to project owner. Wait for approval.
- [ ] T042 [US1+US5+US6+US7] On approval: edit `ch04_tutorial.md` status block to flip BOTH `exercise-01: approved YYYY-MM-DD` AND `exercise-02: approved YYYY-MM-DD` (group-atomic). Commit `implement(ch04): §4.1 group landed`.

**Checkpoint**: §4.1 group approved; §4.2 group unblocked.

---

## Phase 4: Group §4.2 — User Story 2 (Streams, P1)

**Predecessor gate**: §4.1 group approved (`grep -cE "^- exercise-(01|02): approved" ch04_tutorial.md` returns 2). HALT if not.

### ex-03 (producer + consumer + reverse — cross-chapter inversion native home)

- [ ] T050 [US2] Pre-flight gate check: `grep -cE "^- exercise-(01|02): approved" ch04_tutorial.md` MUST return 2.
- [ ] T051 [US2] Create `olamni/tutorial/ch04/exercise-03/`.
- [ ] T052 [US2] Write `ch-04-ex-03-producer-consumer-reverse.glp` per contracts/glp-file-format.md File 3. CRITICAL: producer/2 + consumer/3 byte-identical to ch03's `ch-03-ex-01-producer-consumer.glp` per FR-002+SC-007.
- [ ] T053 [US2] Verify cross-chapter inversion identity: `diff` ch03's producer/consumer clauses against ch04 ex-03 modulo headers + `%%`. Zero clause-text differences.
- [ ] T054 [US2] Verify load.
- [ ] T055 [US2] Propose primary + 3 inspection goals. Example: primary `producer(A, 5), consumer(A?, 0, Sum).` → `Sum = 15`.
- [ ] T056 [US2] Run 4-goal session + capture.
- [ ] T057 [US5] Write `ex-03-repl-trace.md` (Phase A annotation MUST acknowledge cross-chapter inversion per contracts/trace-file-format.md).
- [ ] T058 [US5] Write `ex-03-tutorial.md`.

### ex-04 (Merge Variants)

- [ ] T060 [US2] Create `olamni/tutorial/ch04/exercise-04/`.
- [ ] T061 [US2] Write `ch-04-ex-04-merge-variants.glp` per contracts/glp-file-format.md File 4: 4.2.5 simple merge + 4.2.6 dmerge/dmerger + 4.2.7 merge_tree/merge_layer (~17 clauses).
- [ ] T062 [US2] Verify load.
- [ ] T063 [US2] Propose primary + 3 inspection goals. May need elevated `:limit`. Example: primary `merge_tree([[1], [2], [3], [4]], M).` → some merged form.
- [ ] T064 [US2] Run 4-goal session + capture.
- [ ] T065 [US5] Write `ex-04-repl-trace.md`.
- [ ] T066 [US5] Write `ex-04-tutorial.md`.

### ex-05 (Stream Operators — incl. distribute_indexed)

- [ ] T070 [US2] Create `olamni/tutorial/ch04/exercise-05/`.
- [ ] T071 [US2] Write `ch-04-ex-05-stream-operators.glp` per contracts/glp-file-format.md File 5: 4.2.8 distribute + 4.2.9 distribute_indexed + 4.2.10 observer + 4.2.11 ripple-carry adder (9 ch04-§4.2 clauses). **Self-containment decision (per FR-010)**: the ripple-carry `adder/4` primary call chain reaches `full_adder/5` → `half_adder/4` → logic gates. T073's locked primary goal determines whether these sub-procedures are exercised. If the primary OR any inspection goal exercises `adder/4`, the ex-05 `.glp` MUST duplicate `full_adder/5` + `half_adder/4` + `and/3` + `or/3` + `not/2` + `xor/3` from ex-02 byte-exact inline (~17 additional clauses; total ~26 clauses for ex-05). If `adder/4` is omitted from all 4 goals (unusual but valid), no duplication needed (~9 clauses total). Decision recorded with the T073 goal lock.
- [ ] T072 [US2] Verify load. Note: per Q2 retraction, distribute_indexed works fine with structs-in-lists.
- [ ] T073 [US2] Propose primary + 3 inspection goals. Example primary: `producer(A, 3), distribute(A?, B, C), consumer(B?, 0, S1), consumer(C?, 0, S2).` → `S1 = S2 = 6`. May need elevated `:limit`.
- [ ] T074 [US2] Run 4-goal session + capture.
- [ ] T075 [US5] Write `ex-05-repl-trace.md`.
- [ ] T076 [US5] Write `ex-05-tutorial.md`.

### ex-06 (Buffered Communication + Monitors)

- [ ] T080 [US2] Create `olamni/tutorial/ch04/exercise-06/`.
- [ ] T081 [US2] Write `ch-04-ex-06-buffered-and-monitors.glp` per contracts/glp-file-format.md File 6: 4.2.12 bb + 4.2.13 bb_test + 4.2.14 counter/counter_loop + 4.2.15 accumulator/acc_loop/clients (~17 clauses).
- [ ] T082 [US2] Verify load.
- [ ] T083 [US2] Propose primary + 3 inspection goals. Example primary: `counter([add, add, read(X), clear, add, read(Y), done]).` → `X = 2, Y = 1`.
- [ ] T084 [US2] Run 4-goal session + capture.
- [ ] T085 [US5] Write `ex-06-repl-trace.md`.
- [ ] T086 [US5] Write `ex-06-tutorial.md`.

### §4.2 group approval gate (Phase 4 exit)

- [ ] T090 [US2+US5] Run baseline tests: 485/485 PASS.
- [ ] T091 [US2+US5] Show §4.2 group diff (4 exercises). Wait for approval.
- [ ] T092 [US2+US5] On approval: flip ex-03..ex-06 status block lines all to `approved YYYY-MM-DD` atomically. Commit `implement(ch04): §4.2 group landed`.

**Checkpoint**: §4.2 group approved; §4.3 group unblocked.

---

## Phase 5: Group §4.3 — User Story 3 (Recursive Programming, P2)

**Predecessor gate**: §4.2 group approved.

### ex-07 (Recursive Numerics)

- [ ] T100 [US3] Pre-flight gate: `grep -cE "^- exercise-(03|04|05|06): approved" ch04_tutorial.md` MUST return 4.
- [ ] T101 [US3] Create `olamni/tutorial/ch04/exercise-07/`.
- [ ] T102 [US3] Write `ch-04-ex-07-recursive-numerics.glp` per contracts/glp-file-format.md File 7: 4.3.1 Peano + 4.3.2 integer arith + 4.3.3 factorial + 4.3.4 fact_acc + 4.3.5 fib + 4.3.6 fib_linear (~27 clauses).
- [ ] T103 [US3] Verify load.
- [ ] T104 [US3] Propose primary + 3 inspection goals. Examples: primary `factorial(7, F).` → `F = 5040`; inspection `fib_linear(20, G).` → `G = 6765`.
- [ ] T105 [US3] Run 4-goal session + capture.
- [ ] T106 [US5] Write `ex-07-repl-trace.md`.
- [ ] T107 [US5] Write `ex-07-tutorial.md`.

### ex-08 (Recursive List/Tree)

- [ ] T110 [US3] Create `olamni/tutorial/ch04/exercise-08/`.
- [ ] T111 [US3] Write `ch-04-ex-08-recursive-list-tree.glp` per contracts/glp-file-format.md File 8: 4.3.7 flatten + 4.3.8 tree_sum + 4.3.9 insertion_sort + 4.3.10 mergesort + 4.3.11 distribute_ng (uses `=..`) + 4.3.12 substitute (~32 clauses).
- [ ] T112 [US3] Verify load. Per Q2 retraction, distribute_ng's `=..` in body works fine.
- [ ] T113 [US3] Propose primary + 3 inspection goals. Example primary: `mergesort([3,1,4,1,5,9,2,6], S).` → `S = [1,1,2,3,4,5,6,9]`.
- [ ] T114 [US3] Run 4-goal session + capture.
- [ ] T115 [US5] Write `ex-08-repl-trace.md`.
- [ ] T116 [US5] Write `ex-08-tutorial.md`.

### §4.3 group approval gate (Phase 5 exit)

- [ ] T120 [US3+US5] Run baseline tests: 485/485 PASS.
- [ ] T121 [US3+US5] Show §4.3 group diff. Wait for approval.
- [ ] T122 [US3+US5] On approval: flip ex-07 + ex-08 status block lines atomically. Commit `implement(ch04): §4.3 group landed`.

**Checkpoint**: §4.3 group approved; §4.4 group unblocked.

---

## Phase 6: Group §4.4 — User Story 4 (Metaprogramming, P2)

**Predecessor gate**: §4.3 group approved.

### ex-09 (Metaprogramming Foundations)

- [ ] T130 [US4] Pre-flight gate: `grep -cE "^- exercise-(07|08): approved" ch04_tutorial.md` MUST return 2.
- [ ] T131 [US4] Create `olamni/tutorial/ch04/exercise-09/`.
- [ ] T132 [US4] Write `ch-04-ex-09-metaprogramming-foundations.glp` per contracts/glp-file-format.md File 9: 4.4.1 reduce/2 (3 unit clauses encoding merge) + 4.4.2 trust-mode run/2 (4 clauses).
- [ ] T133 [US4] Verify load.
- [ ] T134 [US4] Propose primary + 3 inspection goals. Example primary (trust-mode MI): `run(merge, merge([1,2],[3,4],Z)).` → `Z = [1,3,2,4]` (or fair-merge result). May need elevated `:limit`.
- [ ] T135 [US4] Run 4-goal session + capture.
- [ ] T136 [US5] Write `ex-09-repl-trace.md`.
- [ ] T137 [US5] Write `ex-09-tutorial.md`.

### ex-10 (Advanced Meta-Interpreters)

- [ ] T140 [US4] Create `olamni/tutorial/ch04/exercise-10/`.
- [ ] T141 [US4] Write `ch-04-ex-10-advanced-meta-interpreters.glp` per contracts/glp-file-format.md File 10: 4.4.3 fail-safe run/4 + 4.4.4 control run/5 + suspended_run/4 + 4.4.5 tracing run/3 + indexed reduce/3 + replay/3 (~21 clauses; may need duplicated reduce/2 from ex-09 inline per FR-010).
- [ ] T142 [US4] Verify load.
- [ ] T143 [US4] Propose primary + 3 inspection goals. Example: primary tracing MI then replay matches byte-for-byte. May need elevated `:limit`.
- [ ] T144 [US4] Run 4-goal session + capture.
- [ ] T145 [US5] Write `ex-10-repl-trace.md`.
- [ ] T146 [US5] Write `ex-10-tutorial.md`.

### §4.4 group approval gate + chapter complete (Phase 6 exit)

- [ ] T150 [US4+US5] Run baseline tests: 485/485 PASS.
- [ ] T151 [US4+US5] Show §4.4 group diff. Wait for approval.
- [ ] T152 [US4+US5+US7] On approval (chapter complete):
  - Flip ex-09 + ex-10 status block lines atomically.
  - Edit `olamni/tutorial/tutorial.md` ch04 row from `pending review (…)` to `implemented YYYY-MM-DD`.
  - Commit `implement(ch04): chapter complete — §4.4 group + top-level index flip`.

**Checkpoint**: All 4 groups approved; chapter 4 complete.

---

## Phase 7: Polish & Cross-Cutting

- [ ] T160 [P] No-fabrication audit: verify all files under `specs/005-tutorial-ch04/` are proper `/speckit-*` outputs. Per FR-012 + SC-011.
- [ ] T161 [P] Cross-chapter inversion identity check (final): `diff` ex-03's producer/consumer clauses against ch03's import. Zero clause-text differences. Per SC-007.
- [ ] T162 [P] Cross-chapter scope check: grep all 10 ch04 `.glp` files for procedure names from other chapters. Should match only ch04 native + cross-chapter inversion duplicates.
- [ ] T163 [P] Test harness exclusion check: `grep "olamni/tutorial/ch04" test/run_all_tests.sh` MUST return 0 matches. Per FR-016 + SC-014.
- [ ] T164 [P] Body-kernel scope check: `grep -E "now\\(|'_output'" olamni/tutorial/ch04/exercise-*/*.glp` MUST return 0 matches. `:=` permitted only inside byte-exact PDF clauses. Per SC-015.
- [ ] T165 [P] §3.2 guard species observability NOT required for ch04 (curriculum-axis is sub-section content, not guard species). Skip ch03's SC-016.
- [ ] T166 Final baseline test pass: 485/485 PASS expected.
- [ ] T167 Trace reproducibility check: re-run all 10 traces; diff against committed `.md` files modulo banner. All 10 strict byte-equality per FR-014.
- [ ] T168 [P] Walk-through verification (soft): SC-001 90-min budget logged as known follow-up.
- [ ] T169 Commit + push branch `005-tutorial-ch04`. Per Constitution multi-Claude protocol — `git add` SPECIFIC files only.
- [ ] T170 Provide merge instructions to project owner per workflow memory mandatory format.

**Checkpoint**: Chapter 4 fully delivered, audited, and ready for merge.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001..T005 sequential.
- **Foundational (Phase 2)**: T006 + T007 — required before any user story.
- **§4.1 group (Phase 3)**: T010..T042 sequential within group; signpost + top-level interleaved.
- **§4.2 group (Phase 4)**: T050..T092; gated on Phase 3 approval.
- **§4.3 group (Phase 5)**: T100..T122; gated on Phase 4 approval.
- **§4.4 group (Phase 6)**: T130..T152; gated on Phase 5 approval.
- **Polish (Phase 7)**: T160..T170; T160-T165 + T168 [P] independent.

### Approval Gates

| Gate | Blocks | Set by |
|---|---|---|
| §4.1 group approval (T042) | T050+ (Phase 4) | T042 itself, after T041 |
| §4.2 group approval (T092) | T100+ (Phase 5) | T092 itself, after T091 |
| §4.3 group approval (T122) | T130+ (Phase 6) | T122 itself, after T121 |
| §4.4 group approval (T152) | (chapter complete) | T152 itself, after T151 |

### Parallel Opportunities

- **Phase 7**: T160-T165 + T168 [P] — different files, independent grep audits.
- Most tasks within an exercise are sequential (write file → verify load → propose goals → run goals → write trace → write tutorial).
- Within a sub-section group, exercises are sequential (per R-009).
- Across sub-section groups: NO parallelism (gated).

---

## Implementation Strategy

### MVP First (§4.1 group only)

1. Phase 1 (T001..T005).
2. Phase 2 (T006..T007).
3. Phase 3 (T010..T042) — §4.1 group complete + signpost + top-level index.
4. **STOP and VALIDATE**: §4.1 is fully usable for a learner. ex-01 + ex-02 cover the chapter's foundational unit-clause + compound-circuit content.

### Incremental Delivery by Group

5. Phase 4 (§4.2 group) — biggest group, 4 exercises with the chapter's centerpiece (streams).
6. Phase 5 (§4.3 group) — recursive programming.
7. Phase 6 (§4.4 group) — metaprogramming, completes the chapter.
8. Phase 7 (polish + commit).

### Total Wall-Clock Estimate

- Phase 1+2: 30 min (Dart verify, REPL build, baseline test ~14 min, PDF re-read).
- Phase 3 (§4.1): 30–45 min (2 exercises, ~17 + 17 clauses).
- Phase 4 (§4.2): 90–120 min (4 exercises, ~9 + 17 + 9 + 17 clauses + cross-chapter inversion verify).
- Phase 5 (§4.3): 60–90 min (2 exercises, ~27 + 32 clauses — biggest per-exercise).
- Phase 6 (§4.4): 45–60 min (2 exercises, ~7 + 21 clauses — metaprogramming may need elevated `:limit`).
- Phase 7: 30 min (polish + commit + merge instructions).

**Total**: ~5–7 hours with auto-mode approvals at group boundaries; longer if pairwise approvals at every step.

---

## Notes

- [P] tasks = different files, no shared deps — parallelisable.
- [Story] label maps tasks to spec.md user stories (US1..US7).
- US1+US2+US3+US4 are gated cross-group per FR-008+FR-009 group-boundary model.
- US5 (per-exercise traces+tutorials) interleaves with each group; trace+tutorial happen immediately after the corresponding `.glp` file is written + 4-goal session captured.
- Per Q2 retraction, alleged parser limitations are STALE — no special handling for distribute_indexed (ex-05) or distribute_ng (ex-08). If they fail at REPL load, that's a runtime regression — halt-and-report, NOT work-around.
- Per FR-013 + Constitution Principle II: any obstacle (Dart absent, REPL build fail, binding mismatch, byte-exact transcription drift, cross-chapter inversion identity violation) → HALT and report.
- Per FR-012: Claude does NOT write speckit-format `spec.md`-style files. T160 verifies this.
- Per FR-015 + SC-015: `:=` permitted only inside byte-exact PDF clauses; `now/1` and `'_output'/1` MUST NOT appear.
- Commit cadence: 4 group-approval commits + 1 polish/final commit = 5 commits total. `git add` SPECIFIC files per multi-Claude protocol.
- Constitution Principle V: baseline tests at T004 + T040 + T090 + T120 + T150 + T166 (6 baseline checks total). All must show 485/485 PASS.
