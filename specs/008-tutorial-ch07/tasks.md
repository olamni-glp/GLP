---

description: "Task list for Olamni Tutorial Chapter 7 — Module System"
---

# Tasks: Olamni Tutorial — Chapter 7 (Module System)

**Input**: Design documents from `specs/008-tutorial-ch07/`
**Prerequisites**: plan.md, spec.md (with **5 Clarifications Q1..Q5**), research.md (R-001..R-012), data-model.md, contracts/ (5 files), quickstart.md
**Constitution**: `.specify/memory/constitution.md` v1.2.0. Phase 1 (Setup) MUST include the baseline REPL-suite run per Principle V AND the R-006 type-checker operational verification per FR-018 (inherited from ch05/ch06) AND the NEW project-loader pre-flight via Section F pass AND the NEW Flutter SDK pre-flight per R-005. All cluster project files inherit SRSW-correctness from canonical `programs/cssg_modules/` (Principle III). Tasks under `olamni/tutorial/**` cite `olamni/tutorial/charter.md` per Principle VI; tasks under `glp_multiagent/lib/main_olamni_ch07_*.dart` cite charter §2.2.

**Tests**: Captured REPL traces + Flutter traces ARE regression artifacts for the per-exercise tutorials. **NEW for ch07**: Section R is added to `test/run_all_tests.sh` per FR-014 + Q-FR014a — explicit override of the CLAUDE.md §11 tutorial-chapter exception. Baseline `bash test/run_all_tests.sh` MUST pass at 485/485 BEFORE implementation; MUST pass at 495/495 (485 + 10 new R cases) AFTER implementation.

**Organization**: Tasks grouped by phase per `quickstart.md`. User stories per spec.md (US1 = cluster A REPL ex-01..ex-05, US2 = cluster A Flutter ex-06, US3 = cluster B REPL ex-07..ex-11, US4 = cluster B Flutter ex-12, US5 = test mirror Section R, US6 = chapter signpost, US7 = top-level index). Pairwise gates within each cluster + 1 cluster-boundary gate per FR-008 + `contracts/status-block-format.md`.

**Pairwise-gate authority**: `grep -E "^- exercise-0NN: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch07/ch07_tutorial.md` MUST return ≥1 match before ex-(NN+1) work begins WITHIN the same cluster. 10 within-cluster gates (5 in cluster A: ex-01→02..ex-05→06; 5 in cluster B: ex-07→08..ex-11→12).

**Cluster-boundary-gate authority**: `grep -E "^- cluster-A: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch07/ch07_tutorial.md` MUST return 1 before any cluster B work (specifically before T-equivalent for ex-07) begins. Auxiliary check: 6 cluster-A exercise lines all approved.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Different file, no dependencies on incomplete tasks → can run in parallel.
- **[Story]**: User story this task belongs to (US1..US7).

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verify Dart SDK: `"/c/Users/gavri/dart-sdk/bin/dart" --version`, confirm `^3.9.4`. Set `DART="/c/Users/gavri/dart-sdk/bin/dart"`.
- [ ] T001b Verify Flutter SDK (NEW for ch07): `flutter --version` reports a working SDK. If absent, HALT per FR-013 + R-005.
- [ ] T002 Verify or rebuild REPL exe at `glp_runtime/glp_repl.exe`. Use `--define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')"`. Verify banner `Built from: <commit>` matches `Repo HEAD: <commit>` (no STALE BINARY warning).
- [ ] T003 Verify `.gitignore` covers `glp_runtime/glp_repl*` and `glp_runtime/.dart_tool/` (inherited from ch01–ch06).
- [ ] T004 Record baseline test pass: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — record actual baseline (485/485 expected from ch06 ship state commit `be473849`). MUST include Section F (CSSG Modules) PASS — this is the project-loader pre-flight per R-006.
- [ ] T005 Verify spec inputs: `specs/008-tutorial-ch07/spec.md`, `olamni/tutorial/ch07/ch07-sources.md`, `olamni/tutorial/ch07/spec-rev-eng-input/ch07-DEPRECATED-spec.md` exist. Note: `olamni/tutorial/ch07/ch07-specification-input-prompt.md` does NOT yet exist per FR-018 + VR-12 — flag as TODO at T005b below.
- [ ] **T005b** Author `olamni/tutorial/ch07/ch07-specification-input-prompt.md` per /speckit-analyze finding F6 + spec FR-018 + VR-12. Plain prose describing the chapter's tutorial requirement WITHOUT speckit ceremony (no Feature Branch / Status / Constitution / FR-NNN / User Story / Given/When/Then forms). The file is the rev-eng input prompt that drives `specs/008-tutorial-ch07/spec.md`; reverse-engineer its content from the existing spec.md User Story summaries + Q1..Q5 clarification topics + chapter scope per `ch07-sources.md`. No speckit ceremony per workflow memory's "no-fabrication" rule. **HALT per FR-013 if the project owner indicates the input prompt should be authored by them rather than reverse-engineered.**
- [ ] **T006a** R-006 type-checker operational verification per FR-018 against CURRENT REPL build (inherited from ch05/ch06 R-006): (a) load a known-good ch06 typed `.glp` (e.g., `olamni/tutorial/ch06/exercise-02/ch-06-ex-02-typed-quicksort.glp`); confirm `✓ Loaded:` + zero errors. (b) load a known-bad ch05 negative-form `.glp` (e.g., `olamni/tutorial/ch05/exercise-06/ch-05-ex-06-type-error-failing.glp`); confirm load FAILS with the documented type-error message. If positive case fails OR negative case loads cleanly → HALT per FR-013. Append both captured outputs to research.md Appendix A.
- [ ] **T006b** Project-loader operational verification (NEW for ch07): confirm Section F (CSSG Modules) of `test/run_all_tests.sh` passes in the T004 baseline run. If Section F regresses, HALT per FR-013 — the project loader is the cluster A + cluster B load mechanism.
- [ ] **T006c** Verify canonical `programs/cssg_modules/` state: `ls programs/cssg_modules/ programs/cssg_modules/ui/` confirms 6 expected files (`self.glp`, `agent.glp`, `boot.glp`, `mad_boot.glp` at top + `ui/{mediator.glp, actors.glp}`). HALT if any expected file is missing OR an unexpected file appears.
- [ ] **T006d** Re-read `programs/cssg_modules/boot.glp` to confirm cluster A's pruning surface per R-010 (canonical line ranges) is still accurate. HALT + amend R-010 if canonical has shifted.

**Checkpoint**: Phase 1 complete — Dart, Flutter, REPL build, baseline tests, type-checker pre-flight, project-loader pre-flight, canonical state verified.

---

## Phase 2: Foundational (Spec amendments + subordinate decisions)

- [ ] **T007** Record spec amendments (per /speckit-analyze remediation; auto-mode-approved): edit `specs/008-tutorial-ch07/spec.md` Clarifications session 2026-05-01 to add:
  - **Q1a** (cluster A keeps `ui/{mediator.glp, actors.glp}` byte-exact + only `boot.glp` is pruned per R-002).
  - **Q-FR003a** (FR-003 file listing corrected — no `ui/self.glp`, includes `mad_boot.glp` per R-002).
  - **Q-FR014a** (FR-014 Section letter R not S per R-007).
  - **Q4a** (ex-12 play subset = play1+play2+play3+play4+play5 per R-012).
- [ ] **T008** Confirm subordinate decisions (auto-mode-approved during /speckit-plan):
  - R-002 cluster A shape per Q1a: cluster A's project files are byte-exact for all 4 of `{self.glp, agent.glp, ui/mediator.glp, ui/actors.glp}` + DERIVED for `boot.glp` per R-010.
  - R-008 cross-chapter relationship contract: multimodule-project-derivation; documented in 4 sites per FR-014 (`.glp` header per file, signpost prose, top-level footnote, Section R header comment).
  - R-009 filenames + cluster project subdirs + Flutter pairings per `contracts/glp-file-format.md` + `contracts/test-mirror-format.md`.
  - R-010 cluster A `boot.glp` pruning content: removed sections (4-agent actor decls + friend-to-friend network3/3 clauses + network2/2 + plays 4–7 + fplays 4–7) + retained sections (3-agent actor decls + cold-call network3/3 + base case + local utilities + plays 1–3 + fplays 1–3).
  - R-011 Flutter pairing content: cluster A clone with `_projectDir = '../olamni/tutorial/ch07/simple-multimodule'` + `_bootFileName = 'boot.glp'` + 3-agent panels; cluster B clone with `_projectDir = '../olamni/tutorial/ch07/cssg-modules'` + `_bootFileName = 'mad_boot.glp'` + 4-agent panels (byte-exact from canonical).
  - R-012 ex-12 play subset per Q4a: play1+play2+play3+play4+play5.
  - R-004 inspection actions: deferred to T-PROPOSE within each exercise task block; each exercise has primary action + 0–3 inspection actions per the structure documented in research.md.

**Checkpoint**: Phase 2 complete — spec amendments recorded; subordinate decisions confirmed.

---

## Phase 3: Cluster project files (Foundational for both clusters; blocks all per-exercise work)

- [ ] T010 [P] [US1+US3] Create `olamni/tutorial/ch07/simple-multimodule/ui/` + `olamni/tutorial/ch07/cssg-modules/ui/` directories. Confirm parent `olamni/tutorial/ch07/` exists.
- [ ] T011 [P] [US1] Copy canonical `programs/cssg_modules/{self.glp, agent.glp, ui/mediator.glp, ui/actors.glp}` to `olamni/tutorial/ch07/simple-multimodule/{self.glp, agent.glp, ui/mediator.glp, ui/actors.glp}` (4 files). Add the ch07 byte-exact header block at the top of each file per `contracts/glp-file-format.md` Header block contract.
- [ ] T012 [P] [US3] Copy canonical `programs/cssg_modules/{self.glp, agent.glp, ui/mediator.glp, ui/actors.glp, boot.glp, mad_boot.glp}` to `olamni/tutorial/ch07/cssg-modules/...` (6 files). Add the ch07 byte-exact header block at the top of each file. Cluster B is byte-exact for ALL 6 files.
- [ ] T013 [US1] DERIVE cluster A's `boot.glp` from canonical per R-010: read `programs/cssg_modules/boot.glp`; remove the documented line ranges (4-agent actor decls + friend-to-friend network3/3 + network2/2 + plays 4–7 + fplays 4–7); retain the documented sections; add the ch07 DERIVED header block per `contracts/glp-file-format.md`. Save to `olamni/tutorial/ch07/simple-multimodule/boot.glp`.
- [ ] T014 [US1] Verify cluster A's project loads via REPL: `printf "%s\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | dart run glp_runtime/.dart_tool/repl.dill 2>&1 | grep -E "✓ Loaded:"` returns ≥5 matches (one per cluster A file). HALT per FR-013 if any module fails to load.
- [ ] T015 [US3] Verify cluster B's project loads via REPL: same pattern with `cssg-modules/`. ≥6 `✓ Loaded:` matches. HALT per FR-013 if any module fails.

**Checkpoint**: Phase 3 complete — both cluster projects exist + load cleanly.

---

## Phase 4: Test mirror (Section R)

- [ ] T020 [US5] Append Section R to `test/run_all_tests.sh` per `contracts/test-mirror-format.md`. Sub-block R-1 (4 cases: cluster A project load + 3 plays); sub-block R-2 (6 cases: per-file diff against canonical for cluster B's 6 files). Section R header comment per R-008's 4th documentation site (cite spec FR-014 + Q-FR014a).
- [ ] T021 [US5] Run baseline + Section R: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` → expect 495/495 (485 + 10 new). HALT per FR-013 if any new case fails OR any pre-existing case regresses.

**Checkpoint**: Phase 4 complete — Section R lives in `test/run_all_tests.sh`; 495/495 passes.

---

## Phase 5: Flutter pairings (Both clusters; blocks ex-06 + ex-12)

- [ ] T030 [P] [US2] Create `glp_multiagent/lib/main_olamni_ch07_simple_multimodule.dart` per R-011: clone `glp_multiagent/lib/main_cssg_mad_modules.dart`; modify (a) `_projectDir = '../olamni/tutorial/ch07/simple-multimodule'`; (b) `_bootFileName = 'boot.glp'` (cluster A's pruned boot, NOT mad_boot); (c) `_agentInfos` to 3-agent panel layout (Alice/Bob/Charlie); (d) `_cssgSpawnConfigs` to 3-isolate spawn config; (e) header comment block per FR-020 citing template + retarget + spec FR cross-reference.
- [ ] T031 [P] [US4] Create `glp_multiagent/lib/main_olamni_ch07_cssg.dart` per R-011: clone `glp_multiagent/lib/main_cssg_mad_modules.dart`; modify (a) `_projectDir = '../olamni/tutorial/ch07/cssg-modules'`; (b) `_bootFileName = 'mad_boot.glp'` (byte-exact from canonical); (c) `_agentInfos` byte-exact from canonical (4-agent Alice/Carol/Bob/Dave); (d) `_cssgSpawnConfigs` byte-exact from canonical; (e) header comment block per FR-020.
- [ ] T032 [US2+US4] Verify both Flutter pairings build: `cd glp_multiagent && flutter clean && flutter pub get && flutter build <platform>` (per CLAUDE.md §18). HALT per FR-017 if either build fails. (Manual launch happens during ex-06 + ex-12 Flutter exercise tasks below.)

**Checkpoint**: Phase 5 complete — both Flutter pairings exist + build cleanly. Manual launch deferred to ex-06 + ex-12.

---

## Phase 6: Cluster A — User Story 1 — ex-01 §7.1–§7.2 project structure / load demo (P1)

**Predecessor gate**: Phase 3 complete + Phase 5 T030 complete (cluster A Flutter pairing exists, blocks for ex-06 not ex-01) — actually only Phase 3 is required for ex-01.

- [ ] T040 [US1] Create `olamni/tutorial/ch07/exercise-01/`.
- [ ] **T041-PROPOSE** [US1] Per R-004 deferral, propose primary action (cluster A's project load demo + the per-module `✓ Loaded:` observation) + 0–2 inspection actions (e.g., `:listing` if supported; cross-reference to entry-point alias generation `play1 :- boot:play1.`). Show to project owner; await approval; record locked actions + bindings in `ex-01-tutorial.md` (or in an exercise-local notes section).
- [ ] T042 [US1] REPL load + verify primary action; capture trace verbatim per `contracts/trace-file-format.md` Phase A. Bindings/observations MUST match locked values; mismatch is HALT per FR-013.
- [ ] T043 [US1] Write `ex-01-repl-trace.md` per `contracts/trace-file-format.md` (Phase A + 0–2 additional phases). Strict byte-equality per FR-012.
- [ ] T044 [US1] Write `ex-01-tutorial.md` — learner step-through. Walks through reading the cluster A project files + loading + observing per-module `✓ Loaded:` + R-008 multimodule-project-derivation cross-reference.
- [ ] T045 [US1] Update `ch07_tutorial.md` status block: `exercise-01: files written` initially; `pending review` when complete.

### Chapter signpost + top-level index (interleaved with ex-01)

- [ ] T046 [US6] Write `olamni/tutorial/ch07/ch07_tutorial.md` per `contracts/status-block-format.md` initial state (13 status lines: 12 exercise + 1 cluster-A). Document: chapter is the transition chapter (charter §2.2 cited); two-cluster pedagogy paragraph; Section R test integration paragraph (FR-010); per-exercise links + one-line summaries (cluster-tagged); R-008 4-site documentation explanation; build instructions for BOTH REPL and Flutter; multimodule-project-derivation explanation (R-008 second site).
- [ ] T047 [US6] Verify status block grep-friendly: `grep -cE "^- exercise-(0[1-9]|1[0-2]):" ch07_tutorial.md` returns 12; `grep -cE "^- cluster-A:" ch07_tutorial.md` returns 1.
- [ ] T048 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch07 row from `planned` to `pending review (YYYY-MM-DD)`. Add R-008 third-site footnote: "ch07 is the transition chapter to use-case-driven multimodule projects per charter §2.2; cluster B's `cssg-modules/` is byte-exact-equivalent to `programs/cssg_modules/` enforced by Section R of `test/run_all_tests.sh`". Add the "How to use this tutorial" section footnote per R-003 + R-008 (cite ch07 as the concrete transition example). Link target → `ch07/ch07_tutorial.md`.

### ex-01 approval gate (Phase 6 exit)

- [ ] T049 [US1+US6+US7] Run baseline tests: PASS expected (495/495). Section R passes the load+play cases.
- [ ] T050 [US1+US6+US7] Show ex-01 diff to project owner. Wait for approval. (Auto-mode candidate.)
- [ ] T051 [US1+US6+US7] On approval: edit `ch07_tutorial.md` status block to flip `exercise-01` line to `approved YYYY-MM-DD`. Commit `implement(ch07): ex-01 cluster A project structure + load demo` (commits may batch per chapter-final precedent).

**Checkpoint**: ex-01 approved. Gate-grep `grep -E "^- exercise-01: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch07_tutorial.md` returns 1. ex-02 unblocked.

---

## Phase 7: Cluster A — User Story 1 — ex-02 §7.3 procedure declarations (P1)

**Predecessor gate**: ex-01 approved. HALT if 0.

- [ ] T060 [US1] Pre-flight gate check.
- [ ] T061 [US1] Create `olamni/tutorial/ch07/exercise-02/`.
- [ ] **T062-PROPOSE** [US1] Propose primary action (decl-kind inspection: load cluster A; demonstrate `boot.glp` reaches `agent#agent/4` (exported) but cannot reach `agent#merge/3` (private)) + 1–2 inspection actions (e.g., REPL goal that exercises an exported procedure; REPL goal that fails on a private procedure call from outside the module). Lock + verify.
- [ ] T063 [US1] REPL session; capture trace.
- [ ] T064 [US1] Write `ex-02-repl-trace.md` + `ex-02-tutorial.md`.
- [ ] T065 [US1] Status block flip + show diff + approve + commit (deferred to chapter-final).

**Checkpoint**: ex-02 approved. ex-03 unblocked.

---

## Phase 8: Cluster A — User Story 1 — ex-03 §7.4 ancestor-scoped types (P1)

**Predecessor gate**: ex-02 approved.

- [ ] T070 [US1] Pre-flight gate check.
- [ ] T071 [US1] Create `olamni/tutorial/ch07/exercise-03/`.
- [ ] **T072-PROPOSE** [US1] Propose primary action (ancestor-scoping inspection: types defined in `simple-multimodule/self.glp` resolving from `agent.glp` and `boot.glp` without imports per Formal 7.1) + 1–2 inspection actions. Lock + verify.
- [ ] T073 [US1] REPL session; capture trace.
- [ ] T074 [US1] Write `ex-03-repl-trace.md` + `ex-03-tutorial.md`.
- [ ] T075 [US1] Status block flip + diff + approve + commit deferred.

**Checkpoint**: ex-03 approved. ex-04 unblocked.

---

## Phase 9: Cluster A — User Story 1 — ex-04 §7.5 procedure-renaming + entry-point aliases (P1)

**Predecessor gate**: ex-03 approved.

- [ ] T080 [US1] Pre-flight gate check.
- [ ] T081 [US1] Create `olamni/tutorial/ch07/exercise-04/`.
- [ ] **T082-PROPOSE** [US1] Propose primary action (procedure-renaming inspection per §7.5: observe `agent:agent/4`, `boot:play1/0`, etc., namespace + entry-point alias `play1 :- boot:play1.` resolving a top-level `play1.` call) + 1 inspection action exhibiting cross-module call resolution. Lock + verify.
- [ ] T083 [US1] REPL session; capture trace.
- [ ] T084 [US1] Write `ex-04-repl-trace.md` + `ex-04-tutorial.md`.
- [ ] T085 [US1] Status block flip + diff + approve + commit deferred.

**Checkpoint**: ex-04 approved. ex-05 unblocked.

---

## Phase 10: Cluster A — User Story 1 — ex-05 end-to-end play1 + §7.6 dynamic linking ref (P1)

**Predecessor gate**: ex-04 approved.

- [ ] T090 [US1] Pre-flight gate check.
- [ ] T091 [US1] Create `olamni/tutorial/ch07/exercise-05/`.
- [ ] **T092-PROPOSE** [US1] Propose primary action (load cluster A + run `play1.` end-to-end; observe `→ succeeds` or `→ suspended` per CLAUDE.md §11+§12) + 0–1 inspection action (e.g., re-run with explicit channel state inspection, or annotate which §7.x mechanics from ex-01..ex-04 were exercised). Lock + verify.
- [ ] T093 [US1] REPL session; capture trace.
- [ ] T094 [US1] Write `ex-05-repl-trace.md` + `ex-05-tutorial.md`. The tutorial cross-references which prior cluster A exercises' mechanics were exercised (per `contracts/trace-file-format.md` postscript rule).
- [ ] T095 [US1] Status block flip + diff + approve + commit deferred.

**Checkpoint**: ex-05 approved. ex-06 unblocked. (NOT cluster boundary — that's after ex-06.)

---

## Phase 11: Cluster A — User Story 2 — ex-06 Flutter setup walkthrough (P1)

**Predecessor gate**: ex-05 approved + Phase 5 T032 complete (cluster A Flutter pairing builds).

- [ ] T100 [US2] Pre-flight gate check.
- [ ] T101 [US2] Create `olamni/tutorial/ch07/exercise-06/`.
- [ ] **T102-MANUAL-TEST** [US2] Per FR-017 + R-011 + `contracts/flutter-trace-format.md`: manually run `cd glp_multiagent && flutter clean && flutter pub get && flutter build <platform>` for cluster A's Flutter pairing; launch the app; observe each of plays 1, 2, 3 running in the Flutter window with the expected per-play UI behaviour (play1 both-accept; play2 Alice-accepts-Charlie-rejects; play3 both-reject); capture the platform log file content for each play. HALT per FR-013 + FR-017 if any play fails to launch or behave correctly. Capture `ex-06-flutter-trace.md` from this manually-tested run; do NOT synthesise.
- [ ] T103 [US2] Write `ex-06-tutorial.md` per `contracts/flutter-trace-format.md` Structure: Phase A pre-flight + Phase B build + Phase C launch + Phase D per-play (3 sub-sections) + Phase E recommended clean-session block per FR-005 (b). Postscript references the §7.x mechanics + cluster A Flutter pairing source file.
- [ ] T104 [US2] Status block flip + diff + approve.

### Cluster boundary gate (Phase 11 exit)

- [ ] **T105** [US2+US6] Verify auxiliary check: `grep -cE "^- exercise-0[1-6]: approved" ch07_tutorial.md` returns 6 (all 6 cluster A exercises approved).
- [ ] **T106** [US6] Edit `ch07_tutorial.md` status block: flip `cluster-A: not yet satisfied` → `cluster-A: approved YYYY-MM-DD` (date = ex-06's approval date OR strictly later).
- [ ] T107 Run baseline tests: PASS expected (495/495).
- [ ] T108 Commit `implement(ch07): cluster A complete (6 exercises) — Module System §7.1–§7.6 mechanics + Flutter setup walkthrough` (commits may batch).

**Checkpoint**: cluster A complete. Cluster boundary gate satisfied. Cluster B work unblocked.

---

## Phase 12: Cluster B — User Story 3 — ex-07 project structure walkthrough (P1)

**Predecessor gate**: cluster-A boundary gate satisfied (`grep -E "^- cluster-A: approved" ch07_tutorial.md` returns 1).

- [ ] T120 [US3] Pre-flight cluster-boundary gate check.
- [ ] T121 [US3] Create `olamni/tutorial/ch07/exercise-07/`.
- [ ] **T122-PROPOSE** [US3] Propose primary action (cluster B's larger project load demo: 40 types in `self.glp`, 13 private procs in `agent.glp`, 3 private procs in `ui/mediator.glp`, 16 exported actors in `ui/actors.glp`, 7 plays in `boot.glp` per FR-007 + spec US3 acceptance scenario 1) + 0–2 inspection actions (e.g., per-module `✓ Loaded:` summary). Lock + verify.
- [ ] T123 [US3] REPL session; capture trace.
- [ ] T124 [US3] Write `ex-07-repl-trace.md` + `ex-07-tutorial.md`.
- [ ] T125 [US3] Status block flip + diff + approve.

**Checkpoint**: ex-07 approved. ex-08 unblocked.

---

## Phase 13: Cluster B — User Story 3 — ex-08 cold-call befriending plays 1–3 (P1)

**Predecessor gate**: ex-07 approved.

- [ ] T130 [US3] Pre-flight gate check.
- [ ] T131 [US3] Create `olamni/tutorial/ch07/exercise-08/`.
- [ ] **T132-PROPOSE** [US3] Propose primary action (load cluster B + run `play1.`, `play2.`, `play3.` in sequence; trace records each play's outcome per CLAUDE.md §12 `→ succeeds`/`→ suspended` semantics + FR-007 (a) cold-call befriending) + 0–1 inspection action. Lock + verify.
- [ ] T133 [US3] REPL session (3-play sequence); capture trace.
- [ ] T134 [US3] Write `ex-08-repl-trace.md` + `ex-08-tutorial.md`.
- [ ] T135 [US3] Status block flip + diff + approve.

**Checkpoint**: ex-08 approved. ex-09 unblocked.

---

## Phase 14: Cluster B — User Story 3 — ex-09 friend-mediated/CSSG accept+reject plays 4–5 (P1)

**Predecessor gate**: ex-08 approved.

- [ ] T140 [US3] Pre-flight gate check.
- [ ] T141 [US3] Create `olamni/tutorial/ch07/exercise-09/`.
- [ ] **T142-PROPOSE** [US3] Propose primary action (run `play4.` (CSSG: All four accept child introduction) + `play5.` (CSSG: Bob rejects); trace records both branches per FR-007 (b) friend-mediated + Q4a) + 0–1 inspection action. Lock + verify.
- [ ] T143 [US3] REPL session; capture trace.
- [ ] T144 [US3] Write `ex-09-repl-trace.md` + `ex-09-tutorial.md`.
- [ ] T145 [US3] Status block flip + diff + approve.

**Checkpoint**: ex-09 approved. ex-10 unblocked.

---

## Phase 15: Cluster B — User Story 3 — ex-10 parent-mediated child intro variants plays 6–7 (P1)

**Predecessor gate**: ex-09 approved.

- [ ] T150 [US3] Pre-flight gate check.
- [ ] T151 [US3] Create `olamni/tutorial/ch07/exercise-10/`.
- [ ] **T152-PROPOSE** [US3] Propose primary action (run `play6.` + `play7.` — additional parent-mediated child intro variants per FR-007 (c)+(d) + Q4a; cover both approve and reject by each party) + 0–1 inspection action. Lock + verify.
- [ ] T153 [US3] REPL session; capture trace.
- [ ] T154 [US3] Write `ex-10-repl-trace.md` + `ex-10-tutorial.md`.
- [ ] T155 [US3] Status block flip + diff + approve.

**Checkpoint**: ex-10 approved. ex-11 unblocked.

---

## Phase 16: Cluster B — User Story 3 — ex-11 cross-module-call inspection (P1)

**Predecessor gate**: ex-10 approved.

- [ ] T160 [US3] Pre-flight gate check.
- [ ] T161 [US3] Create `olamni/tutorial/ch07/exercise-11/`.
- [ ] **T162-PROPOSE** [US3] Propose primary action (cross-module-call inspection: observe `boot.glp` calling `agent # agent(...)`, `mediator # ui_mediator(...)`, `actors # alice4(...)` resolved through `imported procedure` declarations without source access per Formal 7.2 + §7.4 + spec US3 acceptance scenario 5) + 1–2 inspection actions. Lock + verify.
- [ ] T163 [US3] REPL session; capture trace.
- [ ] T164 [US3] Write `ex-11-repl-trace.md` + `ex-11-tutorial.md`.
- [ ] T165 [US3] Status block flip + diff + approve.

**Checkpoint**: ex-11 approved. ex-12 unblocked.

---

## Phase 17: Cluster B — User Story 4 — ex-12 CSSG plays in Flutter (P2)

**Predecessor gate**: ex-11 approved + Phase 5 T032 complete (cluster B Flutter pairing builds).

- [ ] T170 [US4] Pre-flight gate check.
- [ ] T171 [US4] Create `olamni/tutorial/ch07/exercise-12/`.
- [ ] **T172-MANUAL-TEST** [US4] Per FR-017 + R-011 + `contracts/flutter-trace-format.md`: manually run cluster B Flutter pairing build + launch + observe the locked 5-play subset per Q4a (play1 + play2 + play3 + play4 + play5) running with the expected on-screen behaviour (multi-actor UI panels: parent + child split per `_agentInfos`). HALT per FR-013 + FR-017 on failure. Capture `ex-12-flutter-trace.md` from manually-tested run.
- [ ] T173 [US4] Write `ex-12-tutorial.md` per `contracts/flutter-trace-format.md`. Back-references ex-06's clean-session block (no re-explanation per spec US4); cluster B-specific build/launch commands (cite cluster B Flutter pairing). Postscript references §7.7 use cases + the cluster B Flutter pairing source file.
- [ ] T174 [US4] Status block flip + diff + approve.

**Checkpoint**: ex-12 approved. Chapter complete.

---

## Phase 18: Chapter completion

- [ ] T180 [US7] Edit `olamni/tutorial/tutorial.md` — flip ch07 row from `pending review (YYYY-MM-DD)` to `implemented YYYY-MM-DD`. Footnote remains.
- [ ] T181 Run baseline tests one more time: `bash test/run_all_tests.sh` → 495/495 pass (Section R 10 cases + 485 pre-ch07 baseline).
- [ ] T182 Verify `ch07_tutorial.md` status block: all 12 exercise lines + cluster-A line `approved YYYY-MM-DD`. Auxiliary check: `grep -cE "^- exercise-(0[1-9]|1[0-2]): approved" ch07_tutorial.md` returns 12; `grep -cE "^- cluster-A: approved" ch07_tutorial.md` returns 1.
- [ ] T183 Final commit: `implement(ch07): chapter complete — 12 exercises (Module System) across 2 clusters; cluster A simple-multimodule + cluster B byte-exact CSSG; Section R 10 new tests passing 495/495; 2 Flutter pairings + 11 cluster project files + 12 exercise dirs`.
- [ ] T184 Provide merge instructions to user per CLAUDE.md §14 (mandatory format with absolute paths; current branch `008-tutorial-ch07`).

**Final checkpoint**: ch07 chapter complete; all 12 exercises approved + cluster boundary approved; top-level index updated; ready for merge to main.

---

## Parallel execution opportunities

- **T010 + T011 + T012** can run in parallel (different cluster project subdirs).
- **T030 + T031** can run in parallel (different Flutter pairing files); both depend on T010+T011+T012 complete (Flutter pairings reference cluster project subdirs as `_projectDir`).
- **T046 + T048** can run in parallel (signpost + top-level index — different files; both touch ch07 navigation).
- **T013 (cluster A boot.glp derivation)** depends on T011 only (cluster A subdir exists with the 4 byte-exact files); does NOT depend on cluster B work.
- Within each ex-NN exercise: T-PROPOSE → REPL session → trace → tutorial → status block flip are strictly sequential.
- Phases 6–11 (cluster A exercises ex-01..ex-06) are strictly sequential per pairwise gates.
- Phases 12–17 (cluster B exercises ex-07..ex-12) are strictly sequential per pairwise gates AND collectively gated by cluster-A boundary gate (T106).

## Dependencies

- Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → ... → Phase 11 → Phase 12 → ... → Phase 17 → Phase 18.
- Phase 4 (Section R) depends on Phase 3 (cluster project files exist + load cleanly).
- Phase 5 (Flutter pairings) depends on Phase 3 (cluster project subdirs exist for `_projectDir` retargeting).
- Phase 6 onwards (per-exercise tasks) depend on Phase 4 + Phase 5 (so the test mirror catches drift + Flutter pairings exist for ex-06 / ex-12).
- Each Phase k+1 (k ∈ {6..16}) is gated by the prior phase's exercise approval (per `contracts/status-block-format.md` grep contract).
- Phase 12 (start of cluster B) is additionally gated by the cluster-boundary gate (T106).
- Phase 18 (T182, T183) gated by T174 (ex-12 approval).

## Per-task estimated effort

- Phase 1 (T001..T006d): ~30 min.
- Phase 2 (T007, T008): ~15 min (per /speckit-analyze auto-mode).
- Phase 3 (T010..T015): ~1 h (file copying + header blocks + cluster A boot.glp pruning + REPL load verification).
- Phase 4 (T020, T021): ~1 h (Bash test section authoring + verification).
- Phase 5 (T030..T032): ~1 h (Dart cloning + Flutter build).
- Phase 6 (ex-01): ~2–3 h (signpost + top-level index work bundled).
- Phases 7–10 (ex-02..ex-05): ~1–2 h each (~5 h total).
- Phase 11 (ex-06 Flutter): ~3–4 h (manual Flutter testing is the long pole).
- Phases 12–16 (ex-07..ex-11): ~1–2 h each (~6 h total).
- Phase 17 (ex-12 Flutter): ~2–3 h.
- Phase 18 (chapter completion): ~1 h.

**Total estimated effort**: ~25–35 hours (5–7 days at 5 h/day with auto-mode-friendly approval gates).
