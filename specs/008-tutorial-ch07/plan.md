# Implementation Plan: Olamni Tutorial — Chapter 7 (Module System)

**Branch**: `008-tutorial-ch07` | **Date**: 2026-05-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/008-tutorial-ch07/spec.md` with **5 resolved Clarifications** (Q1: cluster A derived from `programs/cssg_modules/` reduced to 3-agent friend-mediated plays; Q2: 6+6=12 total exercises; Q3: new dedicated Section S [→ corrected to **Section R** per R-007 + Q-FR014a]; Q4: ex-12 covers one play per §7.7 use case [→ refined to 5 plays per Q4a]; Q5: cluster A keeps all 3 plays play1/play2/play3) **PLUS 4 Q-amendments to be recorded during /speckit-analyze remediation** (Q1a: cluster A keeps `ui/{mediator.glp, actors.glp}` byte-exact + only `boot.glp` is pruned; Q-FR003a: FR-003 file listing corrected — no `ui/self.glp`, includes `mad_boot.glp`; Q-FR014a: Section letter R not S; Q4a: ex-12 play subset = play1+play2+play3+play4+play5).

## Summary

Build the chapter-7 tutorial under `olamni/tutorial/ch07/`: **twelve** runnable exercises across **two clusters** with paired Flutter+play+boot Dart entry points per charter §2.2. Cluster A (simple multimodule, 3-agent introduction protocol) demonstrates §7.1–§7.6 module-system mechanics. Cluster B (CSSG, 4-agent parent-mediated child introduction) is the byte-exact §7.7 validation example. ch07 is the **transition chapter** to use-case-driven multimodule projects (charter §2.2) and is the **first chapter** whose tutorial code is in `test/run_all_tests.sh` (FR-014's explicit override of CLAUDE.md §11).

**Cluster project map** (locked per spec FR-002 + FR-003 + Q1+Q5 + R-002 reconciliation Q1a + Q-FR003a):
- Cluster A — `olamni/tutorial/ch07/simple-multimodule/`: byte-exact `{self.glp, agent.glp, ui/mediator.glp, ui/actors.glp}` + DERIVED `boot.glp` (pruned to plays 1–3 + fplay 1–3 + supporting utilities per R-010). 5 files. Sourced from `programs/cssg_modules/`.
- Cluster B — `olamni/tutorial/ch07/cssg-modules/`: byte-exact `{self.glp, agent.glp, ui/mediator.glp, ui/actors.glp, boot.glp, mad_boot.glp}`. 6 files. Sourced byte-exact from `programs/cssg_modules/`. **Note**: spec FR-003's listing `ui/{self.glp, mediator.glp, actors.glp}` is corrected per Q-FR003a — there is no `ui/self.glp` in canonical; `mad_boot.glp` IS in canonical and IS included in cluster B.

**Exercise map** (12 total, 6 per cluster):
- Cluster A REPL drills (5): ex-01 §7.1–§7.2 project structure / load demo; ex-02 §7.3 procedure declarations (private vs exported vs imported); ex-03 §7.4 ancestor-scoped types (Formal 7.1 + 7.2); ex-04 §7.5 procedure-renaming + entry-point aliases; ex-05 §7.6 dynamic linking — referenced; end-to-end `play1.` run.
- Cluster A Flutter setup walkthrough (1): ex-06 — single-source Flutter setup for chs 7–13; uses cluster A Flutter pairing (`main_olamni_ch07_simple_multimodule.dart`); 3 plays (play1/play2/play3 per Q5).
- Cluster B REPL drills (5): ex-07 project structure walkthrough; ex-08 cold-call befriending (plays 1–3); ex-09 friend-mediated/CSSG accept+reject (plays 4–5 per Q4a); ex-10 parent-mediated child intro additional variants (plays 6–7); ex-11 cross-module-call inspection.
- Cluster B Flutter exercise (1): ex-12 — CSSG plays in Flutter; uses cluster B Flutter pairing (`main_olamni_ch07_cssg.dart`); 5 plays per Q4a (play1+play2+play3+play4+play5).

**Approval gates**: pairwise within each cluster (5+5=10 within-cluster gates) + 1 cluster-boundary gate. Total 11 gates. Status block in `ch07_tutorial.md` carries 13 lines (12 exercise + 1 cluster-A boundary).

**Cross-chapter relationships are multimodule-project-derivation** (NEW for ch07 per R-008): cluster A's project files are derived (one file pruned) and cluster B's project files are byte-exact copies of `programs/cssg_modules/`. Documented in 4 sites per R-008: `.glp` header block per file, signpost prose, top-level `tutorial.md` row footnote, Section R header comment.

**Type-checker is operational** (inherited from ch05 R-006 + ch06 R-006). Project loader is operational (inherited from `programs/cssg_modules/` running as Section F of `test/run_all_tests.sh`). Both pre-flight verifications run at /speckit-implement T001+T002.

**Test mirror is NEW** (per FR-014 + Q-FR014a corrected to **Section R**, not S as spec originally said): 4 cluster A load+play cases + 6 cluster B per-file diff cases = 10 new test cases. Pre-ch07 baseline 485 → post-ch07 expected 495.

**Flutter pairings are NEW for ch07** (per FR-015 + FR-020 + R-011): two `glp_multiagent/lib/main_olamni_ch07_*.dart` files cloned from `main_cssg_mad_modules.dart` with `_projectDir` retargeted to the cluster's tutorial-side project subdir + per-cluster `_agentInfos` panel + `_cssgSpawnConfigs` configurations + ch07 header block.

**Per Q4a**: cluster B Flutter ex-12's locked play subset is play1+play2+play3+play4+play5 (5 plays out of canonical's 7); rationale per R-012 (the 3 cold-call plays exercise the §7.3 introduction protocol's accept/asymmetric/reject branches; play4 + play5 exercise CSSG's parent-mediated accept + reject). Plays 6–7 are demonstrated variants of play5's reject mechanism — covered in cluster B's REPL ex-10, NOT in Flutter ex-12.

Technical approach: documentation + GLP-source feature + Flutter integration + Bash test integration. Volume: ~30–35 files for the entire chapter (12 exercise dirs × 2 files each = 24; 2 cluster project subdirs × 5–6 files each = 11; 2 Flutter pairing .dart files; 1 chapter signpost + 1 input prompt to be authored; this plan + spec + research + data-model + 5 contracts + quickstart + tasks + checklists = artifacts). Plus modifications: 1 Section R appended to `test/run_all_tests.sh`; top-level `tutorial.md` ch07 row + footnotes.

## Technical Context

**Language/Version**: Dart `^3.9.4` for `glp_runtime/` (this Windows host has 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`); Dart `^3.0.0` + Flutter for `glp_multiagent/` (the version is whatever `glp_multiagent/pubspec.yaml` declares); GLP (cluster A: 5 `.glp` files; cluster B: 6 `.glp` files; all sourced from canonical `programs/cssg_modules/`); Bash (Section R additions to `test/run_all_tests.sh`); Markdown.
**Primary Dependencies**: `glp_runtime/` in-tree path dependency (used by REPL); `glp_multiagent/` in-tree Flutter app (used by ex-06 + ex-12); `programs/cssg_modules/` is the canonical source for both cluster project subdirs. NO new third-party deps.
**Storage**: On-disk Markdown + 11 `.glp` files (5 cluster A + 6 cluster B; sharing exists across cluster A and cluster B for `self.glp`/`agent.glp`/`ui/mediator.glp`/`ui/actors.glp` — these 4 byte-exact files are duplicated in both clusters' subdirs because per FR-019 the byte-exact reference is per-cluster). 2 `.dart` files (Flutter pairings). No runtime storage.
**Testing**: Per Constitution Principle V, baseline `bash test/run_all_tests.sh` before/after implementation. Per FR-014 the ch07 tests ARE in `test/run_all_tests.sh` (Section R) — explicit override of CLAUDE.md §11. Captured REPL traces + Flutter traces ARE the regression artifacts for the tutorial materials beyond Section R.
**Target Platform**: Windows host for development (REPL + Flutter); learner-facing artefacts platform-agnostic for REPL (cluster A REPL exercises ex-01..ex-05 + cluster B REPL exercises ex-07..ex-11) but platform-noted for Flutter (ex-06 + ex-12; per-platform log file paths annotated in `flutter-trace-format.md`).
**Project Type**: Tutorial chapter under charter (Constitution Option C) **PLUS** multi-actor UI tutorial (Constitution Option B) — first chapter to combine both. Charter §2.2 cited per Constitution Principle VI.
**Performance Goals**:
- Each cluster's project loads via REPL project-loading mode in <10 s on this Windows host (per SC-002; relaxed from chs 1–6's 5 s due to cluster B's ~2,500-line size).
- Each play (ex-05 cluster A; ex-08..ex-10 cluster B) completes within default `:limit` (per CLAUDE.md §11+§12 + SC-005).
- Section R completes in <30 s additional time on the test runner (4 load+play cases + 6 diff cases).
- Flutter build completes in <2 min on a fresh `flutter clean` (per CLAUDE.md §18); subsequent incremental builds <30 s.
- Chapter implementation total time: ~5–10 days (cluster A: ~2–3 days; cluster B: ~2–3 days; Flutter manual testing: 1–2 days; tests + commit + merge: ~0.5 day).
**Constraints**:
- 12 locked exercise distributions per FR-001 + spec exercise map — no count-restructuring during /speckit-plan; spec Q-amendments via documented Q-amendment per ch02–ch06 precedent.
- Cluster A is DERIVED, cluster B is BYTE-EXACT — per R-002 + FR-002/FR-003. Section R per-file diff (R-2) enforces cluster B byte-exactness.
- Cluster A `boot.glp` pruning is the ONLY derivation surface — per R-010. All other cluster A files are byte-exact.
- Section R is added to `test/run_all_tests.sh` — per FR-014 + Q-FR014a. Section letter is R (not S as spec originally said).
- Flutter pairings clone the canonical `main_cssg_mad_modules.dart` template — per FR-015 + FR-020 + R-011. NO refactor of canonical to parameterise.
- Flutter manual-test-first discipline — per FR-017 + flutter-trace-format. Synthesised Flutter traces are forbidden.
- Strict trace byte-equality per FR-012 (REPL traces) + flutter-trace-format (Flutter traces with platform/wallclock/varies-per-run annotations).
- Pairwise approval gates within each cluster + 1 cluster-boundary gate per FR-008 + status-block-format. Cluster B ALL work blocked until cluster boundary gate satisfied.
- Type-checker live-pipeline + project-loader pre-flight verification per FR-018 + SC-006 BEFORE any cluster project work begins; ch07 work halts per FR-013 against a broken type-checker OR a regressed Section F.
- Per FR-019: `git add` only files this session modified; never `git add -A` or `git add .`. Pre-existing files under `programs/cssg_modules/` are NOT modified.
- Cluster B's tutorial copy at `olamni/tutorial/ch07/cssg-modules/` is the modification surface; the canonical copy at `programs/cssg_modules/` remains untouched.
- Each Flutter pairing file MUST have a header comment block per FR-020 citing template + retarget + spec FR cross-reference.
- Body kernels: `:=` may appear in cluster project files where canonical uses it; `now/1` and `'_output'/1` appear in canonical's `boot.glp` (in `send_to_user_tagged/3`) and `mad_boot.glp` — they are inherited byte-exact for both clusters and tutorial annotations note their presence.
- Plan-then-act per FR-013.
**Scale/Scope**:
- 12 exercises (10 within-cluster pairwise gates + 1 cluster-boundary gate = 11 gates).
- 11 cluster project files (5 cluster A + 6 cluster B).
- 2 Flutter pairing `.dart` files.
- 1 new test section (Section R, 10 cases).
- Total `.glp` LOC across both clusters: ~3,000 (cluster A pruned ~1,300 + cluster B byte-exact 1,981; the duplicated byte-exact files between clusters add ~1,030 to the cluster A side).
- Total Markdown LOC: ~2,000–3,000 (12 tutorials × ~100 lines each + 12 traces × ~50 lines each + chapter signpost + top-level index updates).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.2.0.*

- **I. Spec-First Development (NON-NEGOTIABLE)**: **PASS**. Spec produced via `/speckit-specify` then refined through 5 Clarifications (Q1 cluster A source; Q2 12-exercise count; Q3 new test section; Q4 ex-12 play subset; Q5 cluster A 3 plays). This plan cites all 5 + identifies 4 Q-amendments to be recorded during /speckit-analyze remediation (Q1a/Q-FR003a/Q-FR014a/Q4a). The 5-clarification count vs ch06's 2 reflects ch07's larger scope (2 clusters + 12 exercises + Flutter + tests).
- **II. No Workarounds**: **PASS**. Halt-and-report posture documented at every failure mode in quickstart §"On failure". The cluster A `boot.glp` pruning is NOT a workaround — it is the spec-authorised approach per FR-002 + Q1+Q5; per R-002 reconciliation the pruning is the minimal modification required to make cluster A pedagogically distinct from cluster B while preserving runnability.
- **III. SRSW Discipline (NON-NEGOTIABLE)**: **PASS**. All cluster project files inherit canonical's SRSW correctness — `programs/cssg_modules/` already passes `test/run_all_tests.sh` Section F + Section M (multi-isolate). Cluster A's `boot.glp` pruning removes whole-clause sections; the remaining clauses retain SRSW correctness by inheritance. Adding header blocks does not affect SRSW.
- **IV. FCP Reference Architecture**: **N/A**. No runtime/compiler/type-checker code changes for ch07. Documentation + GLP-source-copy + Flutter-clone + Bash-test-section feature only.
- **V. Test-First Discipline**: **PASS**. Baseline expected 485/485 per ch06 ship state (commit `be473849`). Section R is NEW for ch07 — added to `test/run_all_tests.sh` per FR-014. Post-ch07 expected 495/495 (485 + 10 new R cases). Captured REPL + Flutter traces ARE additional regression artifacts for the per-exercise tutorials. Type-checker pre-flight verification per FR-018 + SC-006 + project-loader pre-flight via Section F pass.
- **VI. Tutorial Charter Compliance**: **PASS**. Charter §1 (REPL pre-existing for cluster A REPL exercises + cluster B REPL exercises) + §1.5 (`%%` paraphrase comments — inherited from canonical) + §2.2 (use-case-driven multimodule projects from chs 7 onward; Flutter pairings) cited. Cluster project files (per R-009) live under `olamni/tutorial/ch07/<cluster.project_subdir>/`; Flutter pairings live under `glp_multiagent/lib/main_olamni_ch07_*.dart` per FR-015 + FR-020. Cross-chapter relationships (multimodule-project-derivation) documented per R-008 as a NEW contract specific to ch07; distinct from ch04 inversion / ch05 typed↔untyped / ch02 forward-import / ch06 synthesis-from-earlier-chapters.
- **Language Design Authority**: **N/A**. No new guards, system predicates, body kernels, directives, or type-system features introduced.
- **Technology Stack**: **PASS**. All artifacts within Constitution-authorised stack:
  - GLP `.glp` source — cluster project files.
  - Dart `^3.9.4` — `glp_runtime/` (REPL inherited).
  - Dart `^3.0.0` + Flutter — `glp_multiagent/` (Flutter pairings inherited template).
  - Bash — Section R appended to `test/run_all_tests.sh`.
  - Markdown — tutorials + traces + signpost.

**Result**: All applicable principles PASS or N/A. Plan proceeds to Phase 0.

### Post-Design Re-evaluation (post-Phase 1)

After completing Phase 0 + Phase 1: all 8 principles still PASS or N/A. R-001 through R-012 in research.md trace back to spec FRs and Clarifications Q1–Q5 + 4 Q-amendments. Phase 1 contracts (trace-file-format, flutter-trace-format NEW, status-block-format with cluster-boundary line, glp-file-format with multimodule-project-derivation header, test-mirror-format NEW) inherit from ch01–ch06's contracts where applicable with ch07-specific additions documented inline.

**Post-design verdict**: no new violations. Plan complete; proceeds to /speckit-tasks.

## Project Structure

### Documentation (this feature)

```text
specs/008-tutorial-ch07/
├── spec.md                            # /speckit-specify + /speckit-clarify (Q1..Q5) output (existing)
├── plan.md                            # this file (/speckit-plan output)
├── research.md                        # Phase 0 output (R-001..R-012)
├── data-model.md                      # Phase 1 output (entities + Cluster + Cluster Project + Approval Gates + Cluster Boundary Gate + Flutter Pairing + Test Mirror)
├── quickstart.md                      # Phase 1 output
├── contracts/                         # Phase 1 output (5 contracts)
│   ├── trace-file-format.md           # REPL traces (10 exercises)
│   ├── flutter-trace-format.md        # Flutter traces (2 exercises) — NEW for ch07
│   ├── status-block-format.md         # 13-line block (12 exercise + 1 cluster-A) with pairwise + cluster-boundary grep contracts
│   ├── glp-file-format.md             # cluster project files: byte-exact + cluster A boot.glp derivation; multimodule-project-derivation header per R-008
│   └── test-mirror-format.md          # Section R structure (R-1 cluster A load+play; R-2 cluster B per-file diff) — NEW for ch07
├── checklists/requirements.md         # /speckit-specify output (existing)
├── QUARANTINE-DO-NOT-USE/             # existing — untouched per spec Out-of-scope
└── tasks.md                           # Phase 2 (/speckit-tasks output)
```

### Source Code (repository root)

**Constitution Option C (Tutorial chapter under charter) + Option B (Multi-actor UI tutorial / Flutter)** — first chapter to use both.

```text
olamni/tutorial/charter.md             # cited per Principle VI (existing)
olamni/tutorial/tutorial.md            # incremental top-level signpost (UPDATE ch07 row + footnote + "How to use" section footnote)
olamni/tutorial/ch07/
├── ch07-sources.md                    # PDF code-block index (existing)
├── ch07-specification-input-prompt.md # rev-eng prompt — TO BE AUTHORED (per FR-018 + VR-12)
├── ch07_tutorial.md                   # chapter signpost with 13-line status block (NEW)
├── spec-rev-eng-input/ch07-DEPRECATED-spec.md  # rev-eng input copy (existing — untouched)
├── simple-multimodule/                # cluster A project subdir (NEW; shared across ex-01..ex-06)
│   ├── self.glp                       #   byte-exact copy of programs/cssg_modules/self.glp + ch07 header block
│   ├── agent.glp                      #   byte-exact copy + header block
│   ├── boot.glp                       #   DERIVED (pruned per R-010) + header block
│   └── ui/
│       ├── mediator.glp               #   byte-exact + header block
│       └── actors.glp                 #   byte-exact + header block
├── cssg-modules/                      # cluster B project subdir (NEW; shared across ex-07..ex-12)
│   ├── self.glp                       #   byte-exact + header block
│   ├── agent.glp                      #   byte-exact + header block
│   ├── boot.glp                       #   byte-exact + header block
│   ├── mad_boot.glp                   #   byte-exact + header block
│   └── ui/
│       ├── mediator.glp               #   byte-exact + header block
│       └── actors.glp                 #   byte-exact + header block
├── exercise-01/                       # cluster A REPL ex (§7.1–§7.2 project structure / load demo)
│   ├── ex-01-tutorial.md
│   └── ex-01-repl-trace.md
├── exercise-02/                       # cluster A REPL ex (§7.3 procedure declarations)
│   ├── ex-02-tutorial.md
│   └── ex-02-repl-trace.md
├── exercise-03/                       # cluster A REPL ex (§7.4 ancestor-scoped types)
│   ├── ex-03-tutorial.md
│   └── ex-03-repl-trace.md
├── exercise-04/                       # cluster A REPL ex (§7.5 procedure-renaming + entry-point aliases)
│   ├── ex-04-tutorial.md
│   └── ex-04-repl-trace.md
├── exercise-05/                       # cluster A REPL ex (end-to-end play1 + §7.6 dynamic linking ref)
│   ├── ex-05-tutorial.md
│   └── ex-05-repl-trace.md
├── exercise-06/                       # cluster A Flutter setup walkthrough (NEW for ch07)
│   ├── ex-06-tutorial.md              #   includes recommended clean-session block per FR-005 (b)
│   └── ex-06-flutter-trace.md         #   captured from manually-tested run per FR-017
├── exercise-07/                       # cluster B REPL ex (project structure walkthrough)
│   ├── ex-07-tutorial.md
│   └── ex-07-repl-trace.md
├── exercise-08/                       # cluster B REPL ex (cold-call befriending — plays 1–3)
│   ├── ex-08-tutorial.md
│   └── ex-08-repl-trace.md
├── exercise-09/                       # cluster B REPL ex (CSSG accept/reject — plays 4–5 per Q4a)
│   ├── ex-09-tutorial.md
│   └── ex-09-repl-trace.md
├── exercise-10/                       # cluster B REPL ex (parent-mediated child intro variants — plays 6–7)
│   ├── ex-10-tutorial.md
│   └── ex-10-repl-trace.md
├── exercise-11/                       # cluster B REPL ex (cross-module-call inspection)
│   ├── ex-11-tutorial.md
│   └── ex-11-repl-trace.md
└── exercise-12/                       # cluster B Flutter exercise (NEW for ch07)
    ├── ex-12-tutorial.md              #   back-references ex-06's setup; cluster B-specific build/launch
    └── ex-12-flutter-trace.md         #   captured from manually-tested run per FR-017

glp_multiagent/lib/
├── main_cssg_mad_modules.dart         # canonical Flutter template (existing — untouched)
├── main_olamni_ch07_simple_multimodule.dart   # cluster A Flutter pairing (NEW per R-011 + FR-015 + FR-020)
└── main_olamni_ch07_cssg.dart         # cluster B Flutter pairing (NEW)

test/run_all_tests.sh                  # Section R appended (NEW for ch07 per FR-014 + Q-FR014a)

programs/cssg_modules/                 # canonical source — UNTOUCHED per FR-019
```

**Structure Decision**: Constitution Option C (Tutorial chapter under charter) + Option B (Multi-actor UI tutorial / Flutter). Cites Constitution Principle VI, charter §1 (REPL pre-existing), §1.5 (`%%` paraphrase comments — inherited from canonical), §2.2 (use-case-driven multimodule projects + Flutter pairings from chs 7 onward). Cross-chapter relationships (multimodule-project-derivation) documented per spec FR-014 as 4 sites: per-file `.glp` header block + signpost prose + top-level footnote + Section R header comment.

## Complexity Tracking

> Empty — no Constitution violations to justify.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _none_    | _n/a_      | _n/a_                                |
