# Quickstart — ch07 (Module System) implementer's guide

**Phase 1 output**. Sequential implementation order with halt-and-report rules. Cites spec.md FR-NNN, plan.md, research.md R-NNN, and contracts/.

ch07 is structurally larger than chs 1–6 (12 exercises across 2 clusters, 2 Flutter pairings, 1 new test section). Plan ~5–10× the implement-time of ch06 (ch06 was 1 day; ch07 is 5–10 days end-to-end with Flutter manual testing as the long pole).

## Pre-flight (run BEFORE T001)

Per research.md Appendix A, verify:

1. **Branch + tree state**: `git status` — branch is `008-tutorial-ch07`; working tree contains spec/plan/research/data-model/contracts/quickstart/tasks artefacts plus the existing `ch07-sources.md` + `spec-rev-eng-input/` + `QUARANTINE-DO-NOT-USE/`. No stray cluster project files or trace files yet.
2. **Dart**: `dart --version` reports `^3.9.4` or later (3.10.1 on this Windows host).
3. **Flutter** (NEW for ch07): `flutter --version` reports a working Flutter SDK. If absent, halt per FR-013 and report.
4. **REPL build**: rebuild with `--define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')"` per workflow memory; verify banner `Built from: <commit>` matches `Repo HEAD: <commit>`.
5. **R-006 type-checker pre-flight**: load a known-good ch06 typed `.glp` (positive) AND a known-bad ch05 negative-form `.glp` (negative); confirm positive loads cleanly + negative is rejected. **HALT per FR-013 if either case fails.**
6. **Baseline test run**: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — passes at the ch06 ship state baseline (485/485 expected per ch06 commit `be473849`). Section F (CSSG Modules) MUST pass — this is the project-loader pre-flight per R-006.
7. **Canonical state verification**: `programs/cssg_modules/` exists with the 6 expected files (`self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp`, `boot.glp`, `mad_boot.glp`). Per `ls programs/cssg_modules/ programs/cssg_modules/ui/` confirm.
8. **Spec amendments recorded**: spec.md Clarifications session 2026-05-01 carries Q-amendments **Q1a** (cluster A keeps `ui/`), **Q-FR003a** (FR-003 file listing corrected — no `ui/self.glp`, includes `mad_boot.glp`), **Q-FR014a** (Section letter R not S), **Q4a** (cluster B Flutter ex-12 play subset = 1+2+3+4+5). If these are not in spec.md, the /speckit-analyze remediation step is the place to add them.

## Implementation order — cluster A first, cluster B second, both clusters' exercises pairwise-gated

### Phase 1 — Setup (Shared infrastructure for both clusters)

1. **T001** — verify Dart SDK + Flutter SDK + REPL build + REPL banner.
2. **T002** — verify baseline 485/485 + Section F pass.
3. **T003** — verify `programs/cssg_modules/` canonical state.
4. **T004** — record spec amendments (Q1a, Q-FR003a, Q-FR014a, Q4a) into spec.md Clarifications session 2026-05-01 (per /speckit-analyze remediation; auto-mode-approved).
5. **T005** — confirm subordinate decisions per /speckit-implement T008 inheritance: R-002 cluster A shape; R-008 documentation sites; R-009 filenames; R-010 boot.glp pruning content; R-011 Flutter pairing content; R-012 ex-12 play subset.

### Phase 2 — Cluster project files (Foundational for both clusters)

6. **T010** — Create `olamni/tutorial/ch07/simple-multimodule/` + `olamni/tutorial/ch07/cssg-modules/` directories (and `simple-multimodule/ui/` + `cssg-modules/ui/` subdirs).
7. **T011** — Copy canonical `programs/cssg_modules/{self.glp, agent.glp, ui/mediator.glp, ui/actors.glp}` to BOTH cluster project subdirs (4 files × 2 clusters = 8 files; cluster A keeps these byte-exact). Add the ch07 header block at the top of each file per `contracts/glp-file-format.md`.
8. **T012** — Copy canonical `programs/cssg_modules/{boot.glp, mad_boot.glp}` to `cssg-modules/` (2 files; cluster B keeps these byte-exact). Add the ch07 header block.
9. **T013** — DERIVE cluster A's `boot.glp` from canonical per R-010 (remove sections per the listed line ranges; retain the documented sections). Add the ch07 header block per `glp-file-format.md` for derived files.
10. **T014** — Verify cluster A's project loads via REPL: `printf "$(pwd)/olamni/tutorial/ch07/simple-multimodule\n:quit\n" | dart run glp_runtime/.dart_tool/repl.dill` → all 5 modules `✓ Loaded:`. **HALT per FR-013 if any module fails to load.**
11. **T015** — Verify cluster B's project loads via REPL: same pattern with `cssg-modules/`. All 6 modules `✓ Loaded:`. **HALT per FR-013 if any module fails to load.**

### Phase 3 — Test mirror (Section R)

12. **T020** — Append Section R to `test/run_all_tests.sh` per `contracts/test-mirror-format.md`. 4 cases in R-1 (cluster A load + 3 plays) + 6 cases in R-2 (cluster B per-file diff). Total 10 cases.
13. **T021** — Run baseline + Section R: `DART=... bash test/run_all_tests.sh` → expect 495/495 (485 + 10 new). **HALT per FR-013 if any new case fails OR any pre-existing case regresses.**

### Phase 4 — Flutter pairings (Both clusters, but only ex-06 / ex-12 use them downstream)

14. **T030** — Create `glp_multiagent/lib/main_olamni_ch07_simple_multimodule.dart` per R-011 (clone of `main_cssg_mad_modules.dart` with `_projectDir = '../olamni/tutorial/ch07/simple-multimodule'` + `_bootFileName = 'boot.glp'` per R-011 + `_agentInfos` 3-agent panel layout + 3-agent `_cssgSpawnConfigs` + the FR-020 header block).
15. **T031** — Create `glp_multiagent/lib/main_olamni_ch07_cssg.dart` per R-011 (clone with `_projectDir = '../olamni/tutorial/ch07/cssg-modules'` + `_bootFileName = 'mad_boot.glp'` + 4-agent panel layout byte-exact from canonical + the FR-020 header block).
16. **T032** — Verify both Flutter pairings build: `cd glp_multiagent && flutter clean && flutter pub get && flutter build <platform>` (per CLAUDE.md §18). **HALT per FR-017 if either build fails.** (Manual launch happens at ex-06 / ex-12 per phase below.)

### Phase 5 — Cluster A REPL exercises (ex-01..ex-05; pairwise-gated)

For each exercise:
1. **Re-check predecessor gate** (ex-NN+1 requires ex-NN approved): `grep -E "^- exercise-0{NN}: approved" ch07_tutorial.md` returns ≥1.
2. **Create `olamni/tutorial/ch07/exercise-NN/`**.
3. **T-PROPOSE** — propose primary action + 0–3 inspection actions per R-004; show to project owner; await approval; record locked actions + bindings in research.md (or in the per-exercise tutorial.md if research.md gets unwieldy at that point).
4. **REPL verification** — load cluster A's project + run the locked actions; capture trace verbatim. Bindings/observations MUST match locked values.
5. **Write `ex-NN-tutorial.md` + `ex-NN-repl-trace.md`** per `contracts/trace-file-format.md`.
6. **Update `ch07_tutorial.md` status block**: `exercise-NN: files written` initially; `pending review` when complete.
7. **Project owner reviews + approves**: status block flips to `exercise-NN: approved YYYY-MM-DD`. R-008 4 documentation sites verified.
8. **Gate satisfied**: ex-(NN+1) work may begin.

### Phase 6 — Cluster A Flutter exercise (ex-06; gated by ex-05)

1. **Re-check predecessor gate** (ex-06 requires ex-05 approved).
2. **Create `olamni/tutorial/ch07/exercise-06/`**.
3. **Manual Flutter test** — per FR-017 + R-011 + flutter-trace-format contract: `flutter clean && flutter pub get && flutter build <platform>`; launch the cluster A Flutter pairing; verify each of plays 1, 2, 3 runs with the expected on-screen behaviour + log file output. **HALT per FR-013 + FR-017 if any play fails to launch or behave correctly.** Capture the trace as `ex-06-flutter-trace.md` from this manually-tested run; do NOT synthesise.
4. **Write `ex-06-tutorial.md`** per `contracts/flutter-trace-format.md` — including the recommended clean-session block per FR-005 (b).
5. **Update `ch07_tutorial.md` status block**: `exercise-06: files written` → `pending review` → `approved YYYY-MM-DD`.
6. **Cluster boundary gate satisfied**: write `cluster-A: approved YYYY-MM-DD` line into the status block (auxiliary check: 6 cluster-A exercise lines all approved). Cluster B work may now begin.

### Phase 7 — Cluster B REPL exercises (ex-07..ex-11; pairwise-gated; cluster-boundary gate satisfied)

For each exercise: same shape as Phase 5 but with cluster B project + cluster B's locked actions per R-004 + R-012.

ex-07: project structure walkthrough (load + per-module summary).
ex-08: cold-call befriending — `play1.`, `play2.`, `play3.`.
ex-09: friend-mediated — locked play subset per Q4a (plays 4–5).
ex-10: parent-mediated child intro additional — locked subset per Q4a (plays 6–7).
ex-11: cross-module-call inspection.

### Phase 8 — Cluster B Flutter exercise (ex-12; gated by ex-11)

1. **Re-check predecessor gate**.
2. **Create `olamni/tutorial/ch07/exercise-12/`**.
3. **Manual Flutter test** — per FR-017 + R-011 + flutter-trace-format contract: build the cluster B Flutter pairing; launch; verify the locked 5-play subset per Q4a (play1 + play2 + play3 + play4 + play5) runs with the expected on-screen behaviour. ex-12 references ex-06's recommended clean-session block (no re-explanation). **HALT per FR-013 + FR-017 on failure.** Capture trace.
4. **Write `ex-12-tutorial.md`** per `contracts/flutter-trace-format.md` — including a back-reference to ex-06's setup + the cluster B-specific build/launch commands.
5. **Status block**: `exercise-12: files written` → `pending review` → `approved YYYY-MM-DD`.

### Phase 9 — Chapter completion

1. **T120** — Edit `olamni/tutorial/tutorial.md`: flip ch07 row from `pending review (YYYY-MM-DD)` to `implemented YYYY-MM-DD` + add the R-008 third-site footnote + the R-003 + R-008 "How to use this tutorial" section footnote.
2. **T121** — Run baseline tests one more time: `DART=... bash test/run_all_tests.sh` → 495/495 pass (485 pre-ch07 baseline + 10 new Section R cases).
3. **T122** — Verify `ch07_tutorial.md` status block: all 12 exercise lines + the cluster-A line all `approved YYYY-MM-DD`. Auxiliary check: `grep -cE "^- exercise-(0[1-9]|1[0-2]): approved" ch07_tutorial.md` returns 12; `grep -cE "^- cluster-A: approved" ch07_tutorial.md` returns 1.
4. **T123** — Final commit: `implement(ch07): chapter complete — 12 exercises (Module System) across 2 clusters; cluster A simple-multimodule + cluster B byte-exact CSSG; Section R 10 new tests passing 495/495`.
5. **T124** — Provide merge instructions to user per CLAUDE.md §14 (mandatory format).

## On failure

Per FR-013 and Constitution Principle II:
- Cluster project file fails to load via project-loading mode → STOP. Re-verify byte-exactness against canonical (cluster B) or pruning correctness (cluster A `boot.glp`). If transcription is correct, the project loader has regressed; halt + report.
- Section R test case fails → STOP. Investigate which case (R-1 load/play OR R-2 diff). For R-2 diff: the canonical may have changed since this branch's checkout; re-sync. For R-1: the cluster A project derivation may be incorrect; verify the pruning per R-010.
- Flutter build fails → STOP. Verify Flutter SDK + `glp_multiagent/pubspec.yaml` deps. If the `main_olamni_ch07_*.dart` file has a syntax error, fix + re-build.
- Flutter app launches but the play behaviour diverges from the expected (cluster A: 3 plays' accept/asymmetric/reject branches; cluster B: 5 plays per Q4a) → STOP per FR-017. Do NOT write a synthesised trace; the manual-test-first discipline is non-negotiable.
- R-006 type-checker pre-flight fails → STOP. Do NOT proceed against a broken type-checker.
- Spec amendment Q1a / Q-FR003a / Q-FR014a / Q4a not yet recorded in spec.md Clarifications → record at /speckit-analyze remediation BEFORE /speckit-implement T001.

## Status block evolution

Throughout implementation, `ch07_tutorial.md` carries the 13-line block per `contracts/status-block-format.md`. Per FR-008:
- Within cluster A: ex-(NN+1) work begins only after ex-NN is `approved`.
- Cluster boundary: ex-07 work begins only after `cluster-A: approved YYYY-MM-DD` is in the status block (which itself requires all 6 cluster-A exercise lines `approved`).
- Within cluster B: ex-(NN+1) work begins only after ex-NN is `approved` (same pairwise pattern).

## Top-level index update

Per FR-011 + R-003 + R-008: when ex-01 lands, flip ch07 row in `olamni/tutorial/tutorial.md` from `planned` to `pending review (YYYY-MM-DD)` + add the multimodule-project-derivation footnote (R-008 third site) + the "How to use" section footnote (R-003 + R-008). When ex-12 is approved, flip to `implemented YYYY-MM-DD` (footnotes remain).

## Numbered step list (high level — ~75 steps total; authoritative tracker is `tasks.md`)

This conceptual numbering is for the learner's mental model of the implementation flow. **The authoritative implementation tracker is `tasks.md` (T001–T~150)**; the conceptual numbering below is parallel-but-not-identical to the T-task numbering and SHOULD NOT be used for status tracking.

1–8: Phase 1 setup (verifying environment + Flutter + R-006 + canonical state + spec amendments).
9–16: Phase 2 cluster project files (8 byte-exact files + cluster A boot.glp pruning + load verification).
17–18: Phase 3 test mirror Section R.
19–21: Phase 4 Flutter pairings.
22–35: Phase 5 cluster A REPL exercises (ex-01..ex-05; ~3 steps per exercise — propose, write, review/approve).
36–39: Phase 6 cluster A Flutter exercise (ex-06; manual test → write → status flip → cluster boundary).
40–53: Phase 7 cluster B REPL exercises (ex-07..ex-11; same shape as Phase 5).
54–57: Phase 8 cluster B Flutter exercise (ex-12).
58–62: Phase 9 chapter completion (top-level index + final tests + commit + merge instructions).
