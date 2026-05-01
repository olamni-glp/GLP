# Data Model — ch07 (Module System)

**Phase 1 output**. Documents the entities, attributes, relationships, and state transitions for the ch07 tutorial. Cites spec.md FRs, plan.md, research.md (R-001..R-012).

ch07 is the first chapter to introduce **Cluster** and **Cluster Project** entities; both **Approval Gate (within cluster)** and **Cluster Boundary Gate** entities; the **Flutter Pairing** entity (NEW per charter §2.2 + FR-015); the **Test Mirror** entity (NEW per FR-014 — first chapter whose tutorial code is in `test/run_all_tests.sh`).

## Entities

### Cluster

A named group of exercises sharing one tutorial-side project subdir. ch07 has exactly TWO clusters.

**Attributes**:
- `name`: enum `{cluster-A, cluster-B}`.
- `project_subdir`: string — `olamni/tutorial/ch07/simple-multimodule/` for cluster-A; `olamni/tutorial/ch07/cssg-modules/` for cluster-B.
- `derivation_kind`: enum `{derived, byte-exact}` — cluster-A is `derived`; cluster-B is `byte-exact`.
- `source_canonical`: string — `programs/cssg_modules/` for both clusters.
- `exercises`: list of 6 Exercise references (cluster-A: ex-01..ex-06; cluster-B: ex-07..ex-12).
- `flutter_pairing`: Flutter Pairing reference (1:1).
- `state`: enum `{not yet started, in flight, all approved}`.

**Relationships**:
- Each Cluster has exactly one Cluster Project (1:1).
- Each Cluster has exactly six Exercises (1:6).
- Each Cluster has exactly one Flutter Pairing (1:1).
- Cluster A → Cluster B is gated by the Cluster Boundary Gate (1:1).

**State transitions**:
```
not yet started
        ↓ (first exercise files written)
in flight
        ↓ (all 6 exercises approved)
all approved
```

### Exercise

A self-contained tutorial unit identified by `exercise-NN` (NN ∈ 01..12).

**Attributes**:
- `id`: integer (01..12).
- `cluster`: Cluster reference (ex-01..ex-06 → cluster-A; ex-07..ex-12 → cluster-B).
- `kind`: enum `{REPL, Flutter}` — ex-01..ex-05 + ex-07..ex-11 = REPL (10 total); ex-06 + ex-12 = Flutter (2 total).
- `section_or_use_case`: string — for cluster A, a §7.x mechanic (`§7.1–§7.6` + §7.5 procedure-renaming for ex-01..ex-05; ex-06 = "Flutter setup walkthrough"); for cluster B, a §7.7 use case (ex-07 = project structure; ex-08 = cold-call befriending plays 1–3; ex-09 = friend-mediated introduction plays 4–5 [per Q4a reconciliation in research R-012, "friend-mediated" is the cold-call accept/reject sub-scenarios in plays 1–3, but per Q4a the play assignment for ex-09 is locked to PLAYS 4–5 covering CSSG accept + Bob-rejects respectively]; ex-10 = parent-mediated child introduction plays 6–7; ex-11 = cross-module-call inspection; ex-12 = CSSG Flutter walkthrough).
- `tutorial_file`: filename `ex-NN-tutorial.md`.
- `trace_file`: filename `ex-NN-repl-trace.md` (REPL kind) OR `ex-NN-flutter-trace.md` (Flutter kind).
- `primary_demo_action`: string — for REPL: load command + primary goal sequence; for Flutter: build command + launch sequence.
- `inspection_actions`: list of 0–3 strings (per R-004 deferred selection); cluster A's 5 REPL exercises typically have the load itself as the primary action with 0–2 inspection actions; cluster B's 5 REPL exercises typically have a play sequence as the primary action with 1–2 inspection actions.
- `locked_bindings_or_observations`: dict `{action: expected_observation}`; empirically verified at /speckit-implement.
- `state`: enum `{not yet implemented, files written, pending review, approved}`.
- `approved_date`: ISO date string `YYYY-MM-DD` (only when state = `approved`).

**Relationships**:
- Each Exercise belongs to exactly ONE Cluster (12:2).
- Each Exercise has ONE Approval Gate to ex-(N+1) within its cluster (4 gates per cluster, 8 gates total: ex-01→ex-02, ex-02→ex-03, ex-03→ex-04, ex-04→ex-05, ex-05→ex-06; ex-07→ex-08, ex-08→ex-09, ex-09→ex-10, ex-10→ex-11, ex-11→ex-12 — actually 5+5 = 10 within-cluster gates).
- Cluster A's ex-06 → Cluster B's ex-07 transition is gated by the Cluster Boundary Gate (1 boundary gate).

**State transitions**:
```
not yet implemented
        ↓ (implementer writes tutorial.md + trace + any required Flutter Pairing changes)
files written
        ↓ (project owner reviews; updates status block)
pending review
        ↓ (project owner approves; status block flips)
approved YYYY-MM-DD
```

### Cluster Project

The `.glp` file set under `olamni/tutorial/ch07/<cluster.project_subdir>/`. Cluster A's project is **derived** from `programs/cssg_modules/` (per FR-002 + R-002 reconciliation); cluster B's project is **byte-exact** copy (per FR-003 + R-002 ui/self.glp correction).

**Attributes**:
- `cluster`: Cluster reference (1:1).
- `path`: string (the cluster's `project_subdir`).
- `files`: list of Cluster Project File records.
- `byte_exact_against_canonical`: bool — `false` for cluster A (derived; only `boot.glp` differs from canonical); `true` for cluster B (all files byte-exact).
- `state`: enum `{not yet present, present, present-and-loadable}`.

**Per-Cluster file lists**:
- Cluster A: `self.glp` (byte-exact, 155 lines), `agent.glp` (byte-exact, 219 lines), `ui/mediator.glp` (byte-exact, 178 lines), `ui/actors.glp` (byte-exact, 479 lines), `boot.glp` (DERIVED — pruned to ~286 lines per R-010). 5 files total.
- Cluster B: `self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp`, `boot.glp`, `mad_boot.glp` (all 6 files byte-exact at 155 + 219 + 178 + 479 + 814 + 136 = 1,981 lines). 6 files total.

**Relationships**:
- Each Cluster Project belongs to exactly ONE Cluster (1:1).
- Cluster A's Cluster Project is verified loadable via REPL project-loading mode at /speckit-implement T-equivalent before cluster A's exercise content depends on it.
- Cluster B's Cluster Project is verified byte-exact-equivalent to `programs/cssg_modules/` via Section R per-file diff test (FR-014).

**State transitions**:
```
not yet present
   ↓ (files copied/derived from canonical)
present
   ↓ (REPL project-loading mode succeeds + Section R test passes)
present-and-loadable
```

### Cluster Project File

A single `.glp` file inside a Cluster Project.

**Attributes**:
- `cluster_project`: Cluster Project reference.
- `relative_path`: string (e.g., `self.glp`, `agent.glp`, `ui/mediator.glp`, `boot.glp`).
- `byte_exact_against_canonical`: bool.
- `canonical_source_path`: string — `programs/cssg_modules/<relative_path>`.
- `header_block_required`: bool — `true` for cluster A's pruned `boot.glp` (per R-010); `false` for all other files (they retain canonical's existing `%%` comments).
- `line_count`: integer.

**Relationships**:
- Each Cluster Project File belongs to exactly ONE Cluster Project (n:1 within cluster).

### Approval Gate (within cluster)

A predicate `exercise-NN: approved YYYY-MM-DD` in `ch07_tutorial.md`'s status block; gates ex-(NN+1) work within the same cluster.

**Attributes**:
- `cluster`: Cluster reference.
- `from_exercise`: integer (NN).
- `to_exercise`: integer (NN+1).
- `predicate`: regex `^- exercise-{NN}: approved [0-9]{4}-[0-9]{2}-[0-9]{2}$` matching the status-block line.
- `state`: enum `{not yet satisfied, satisfied}`.

**Cardinality**: 5 within-cluster gates per cluster × 2 clusters = 10 within-cluster gates (cluster A: ex-01→02, ex-02→03, ex-03→04, ex-04→05, ex-05→06; cluster B: ex-07→08, ex-08→09, ex-09→10, ex-10→11, ex-11→12).

**Relationships**:
- Each Gate is satisfied by exactly ONE Exercise being approved.
- The implementer's gate-grep at the start of each ex-(N+1) work checks `grep -E "^- exercise-0{NN}: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch07/ch07_tutorial.md` returns ≥1 match.

### Cluster Boundary Gate

A predicate `cluster-A: approved YYYY-MM-DD` in `ch07_tutorial.md`'s status block; gates ALL cluster B work.

**Attributes**:
- `from_cluster`: cluster-A.
- `to_cluster`: cluster-B.
- `predicate`: regex `^- cluster-A: approved [0-9]{4}-[0-9]{2}-[0-9]{2}$` matching the status-block line.
- `state`: enum `{not yet satisfied, satisfied}`.
- `precondition`: ALL 6 cluster-A exercises (ex-01..ex-06) are `approved` AND signpost status block carries the `cluster-A: approved` line.

**Cardinality**: 1 boundary gate (cluster-A → cluster-B).

**Relationships**:
- The Cluster Boundary Gate is satisfied by all 6 cluster A exercises being approved AND the implementing session writing the `cluster-A: approved YYYY-MM-DD` line into `ch07_tutorial.md`'s status block.
- The implementer's gate-grep at the start of cluster B work (specifically T-equivalent for ex-07) checks `grep -E "^- cluster-A: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch07/ch07_tutorial.md` returns 1.

### Cross-chapter Relationship (multimodule-project-derivation)

Per R-008, the documented link between a ch07 Cluster Project and its source `programs/cssg_modules/`; recorded in four sites per FR-014 + R-008.

**Attributes**:
- `cluster_project`: Cluster Project reference.
- `derivation_kind`: enum `{derived, byte-exact}`.
- `source_canonical_path`: string (`programs/cssg_modules/`).
- `documentation_sites`: list of 4 — `{glp_header_per_file, signpost_prose, top_level_footnote, test_section_header_comment}`.

**State transitions** (per documentation site):
```
not yet documented
        ↓ (writer adds the cross-reference)
documented
```

**Cardinality**: 2 relationships (one per Cluster); each relationship MUST have all 4 documentation sites populated for the Cluster to advance to `all approved` state.

### Flutter Pairing

Per charter §2.2 + FR-015 + FR-020, a Dart file under `glp_multiagent/lib/main_olamni_ch07_<cluster>.dart` cloned from the canonical `main_cssg_mad_modules.dart` template.

**Attributes**:
- `cluster`: Cluster reference (1:1).
- `path`: string (`glp_multiagent/lib/main_olamni_ch07_simple_multimodule.dart` for cluster A; `glp_multiagent/lib/main_olamni_ch07_cssg.dart` for cluster B).
- `template_source`: string (`glp_multiagent/lib/main_cssg_mad_modules.dart`).
- `project_dir`: string (cluster's tutorial-side project subdir, retargeted in `_projectDir` constant).
- `boot_file_name`: string (`boot.glp` for cluster A; `mad_boot.glp` for cluster B per R-011).
- `agent_infos_count`: integer (3 for cluster A; 4 for cluster B).
- `header_block_required`: bool — `true` (per FR-020).
- `state`: enum `{not yet present, present, present-and-buildable, present-and-launched}`.

**Relationships**:
- Each Flutter Pairing belongs to exactly ONE Cluster (1:1).
- Each Flutter Pairing is verified buildable via `flutter build <platform>` at /speckit-implement T-equivalent for the cluster's Flutter exercise (ex-06 for cluster A; ex-12 for cluster B).
- Each Flutter Pairing is verified launchable + producing the expected per-platform log file at the same step.

**State transitions**:
```
not yet present
   ↓ (implementer writes the .dart file)
present
   ↓ (flutter build succeeds)
present-and-buildable
   ↓ (flutter run launches + log file appears)
present-and-launched
```

### Chapter Tutorial (signpost)

The chapter-level signpost `olamni/tutorial/ch07/ch07_tutorial.md`.

**Attributes**:
- `path`: `olamni/tutorial/ch07/ch07_tutorial.md`.
- `intro_section`: prose explaining ch07's role as the transition chapter (charter §2.2 cited).
- `build_instructions_repl`: REPL build commands (inherited from ch01–ch06 boilerplate).
- `build_instructions_flutter`: Flutter build commands (NEW for ch07; cite FR-005 + ex-06).
- `cluster_pedagogy_paragraph`: plain-prose paragraph explaining cluster A → cluster B order (per FR-010 second sentence).
- `test_integration_paragraph`: plain-prose paragraph explaining Section R + byte-equivalence test (per FR-010 third sentence).
- `exercise_links`: list of 12 entries, one per exercise, with one-line summaries (cluster-tagged: cluster-A entries first, cluster-B entries second).
- `multimodule_derivation_explanation`: plain prose per R-008 + FR-010 (the second documentation site for Cross-chapter Relationship).
- `status_block`: structured 13-line block per `contracts/status-block-format.md` (12 exercise lines + 1 cluster-boundary line).

**State transitions**: rewritten incrementally as exercises advance; final state when all 12 exercises + cluster-boundary are approved.

### Top-level Index

The chapter-by-chapter entry point `olamni/tutorial/tutorial.md`.

**Attributes**:
- `path`: `olamni/tutorial/tutorial.md`.
- `ch07_row`: structured row with status (`planned`, `pending review (YYYY-MM-DD)`, `implemented YYYY-MM-DD`).
- `ch07_footnote`: per FR-011 + R-008 third site — multimodule-project-derivation explanation footnote.
- `how_to_use_section`: gains a footnote on the "use-case-driven from chapter 7 onward" sentence (per FR-011 second sentence + R-003 + R-008).

**State transitions** (ch07 row):
```
planned
   ↓ (any cluster-A exercise lands)
pending review (YYYY-MM-DD)
   ↓ (all 12 exercises approved)
implemented YYYY-MM-DD
```

### Test Mirror

The `test/run_all_tests.sh` Section R section that exercises ch07's cluster projects (per FR-014 + Q-FR014a corrected section letter R per R-007).

**Attributes**:
- `script_path`: `test/run_all_tests.sh`.
- `section_letter`: `R`.
- `case_count`: integer (locked at /speckit-plan T009-equivalent — see locked enumeration below).
- `pre_ch07_baseline`: integer (485 per ch06 ship).
- `post_ch07_total_expected`: integer (`pre_ch07_baseline + case_count`).
- `state`: enum `{not yet present, present-passing, present-failing}`.

**Locked case enumeration** (per Q-amendment Q-FR014a + R-007):
1. `cluster-A: simple-multimodule project loads via project-loading mode` — load the directory `olamni/tutorial/ch07/simple-multimodule/`; assert `✓ Loaded:` for each module + entry-point alias generation log lines.
2. `cluster-A: play1 runs to completion` — after load, run `play1.`; assert the play's expected outcome (per FR-016 + R-010).
3. `cluster-A: play2 runs to completion` — after load, run `play2.`; assert the asymmetric-accept outcome.
4. `cluster-A: play3 runs to completion` — after load, run `play3.`; assert the both-reject outcome.
5. `cluster-B: per-file diff equivalence` — for each file in `olamni/tutorial/ch07/cssg-modules/`, assert `diff` against `programs/cssg_modules/` returns 0 (no differences). 6 files diffed (self.glp, agent.glp, ui/mediator.glp, ui/actors.glp, boot.glp, mad_boot.glp). 6 sub-cases, each surfacing drift with a diagnostic naming the offending file.

Total Section R cases: **4 + 6 = 10 new test cases**. Pre-ch07 baseline 485 + 10 = post-ch07 total **495**.

**Relationships**:
- The Test Mirror references both Cluster Projects (cluster A's load + 3 plays; cluster B's diff equivalence).
- Section R is independent of the existing Section F (CSSG Modules) which exercises `programs/cssg_modules/` end-to-end.

**State transitions**:
```
not yet present
   ↓ (implementer adds the section to test/run_all_tests.sh)
present-passing | present-failing (depends on cluster project state)
```

## Validation Rules

- **VR-1** (FR-001): exactly 12 Exercises exist (NN ∈ 01..12); 6 in cluster A, 6 in cluster B; ex-06 + ex-12 are Flutter, the other 10 are REPL.
- **VR-2** (FR-002 per R-002 reconciliation Q1a): cluster A's Cluster Project files are byte-exact to canonical EXCEPT `boot.glp` which is the canonical with line ranges per R-010 removed.
- **VR-3** (FR-003 per R-002 reconciliation Q-FR003a): cluster B's Cluster Project files are byte-exact to canonical (all 6 files); Section R per-file diff test enforces this.
- **VR-4** (FR-004 + glp-file-format contract): each Cluster A `.glp` MUST have a header block citing `programs/cssg_modules/<file>` + the §7.x mechanic; each Cluster B `.glp` MUST have a header block citing `programs/cssg_modules/<file>` + the §7.7 use case + the byte-exact mandate.
- **VR-5** (FR-005 + flutter-trace-format contract): each Flutter exercise's tutorial.md contains copy-pastable terminal commands (per platform); the corresponding Flutter Pairing is built + launched manually before the trace is captured.
- **VR-6** (FR-006): cluster A's 5 REPL exercises (ex-01..ex-05) collectively exercise §7.1–§7.6 mechanics + §7.5 procedure-renaming + entry-point-aliases.
- **VR-7** (FR-007): cluster B's 5 REPL exercises (ex-07..ex-11) collectively exercise the four §7.7 use cases per R-012 + Q4a reconciliation: cold-call (ex-08 plays 1–3) + CSSG accept (ex-09 play 4) + CSSG Bob-rejects (ex-09 play 5) + parent-mediated child intro additional variants (ex-10 plays 6–7) + cross-module-call inspection (ex-11).
- **VR-8** (FR-008): pairwise gate predicate satisfied for every (NN, NN+1) WITHIN each cluster before ex-(NN+1) work begins; cluster boundary gate satisfied (all 6 cluster A + `cluster-A: approved` line) before any cluster B work begins.
- **VR-9** (FR-014 + Q-FR014a): Test Mirror Section R passes pre- AND post-ch07 (485/485 baseline; 495/495 post-implementation). Per-file diff test for cluster B catches drift.
- **VR-10** (FR-015 + FR-020 + R-011): each Cluster's Flutter Pairing exists, builds, launches, and produces the expected per-platform log file; header block cites template + `_projectDir` retargeting + spec FR cross-reference.
- **VR-11** (FR-017): Flutter exercise tutorials are NOT written until the implementer manually tests + captures the trace from a working Flutter app launch (no synthesised traces).
- **VR-12** (FR-018 — input prompt artifact): `olamni/tutorial/ch07/ch07-specification-input-prompt.md` MUST exist by /speckit-implement T-equivalent (per spec FR-018; auto-resolved at /speckit-clarify session 2026-05-01 since it has not been authored yet — TODO: author at /speckit-implement T002b OR before, per project owner direction).
- **VR-13** (FR-019): per-session `git add` discipline — never `git add -A`; cluster B byte-exact copy is the only modification surface for `cssg_modules/` paths (canonical at `programs/cssg_modules/` is NOT modified by this branch).

## Inheritance from ch01–ch06

The following entity definitions are inherited unchanged:
- Exercise's `state` enum (from ch02 contract; extended in ch05 to include `pending review`).
- Approval Gate predicate regex (from ch01).
- Chapter Tutorial structure (from ch01) with NEW additions: `build_instructions_flutter`, `cluster_pedagogy_paragraph`, `test_integration_paragraph`, `multimodule_derivation_explanation`.
- Top-level Index structure (from ch01; updated incrementally per ch01–ch06 pattern) with NEW additions: `how_to_use_section` footnote.

The following are NEW for ch07:
- **Cluster** entity (NEW — first chapter to have multiple per-chapter clusters).
- **Cluster Project** entity (NEW — first chapter where the runnable artefact is a project subdir, not a single `.glp`).
- **Cluster Project File** entity (NEW).
- **Cluster Boundary Gate** entity (NEW — distinct from within-cluster pairwise Approval Gates).
- **Flutter Pairing** entity (NEW — first chapter to have per-cluster Flutter mains per charter §2.2).
- **Test Mirror** entity (NEW — first chapter whose tutorial code is in `test/run_all_tests.sh` per FR-014 + override of CLAUDE.md §11).
- **Cross-chapter Relationship** of type `multimodule-project-derivation` (NEW — distinct from ch04 inversion / ch05 typed↔untyped / ch02 forward-import / ch06 synthesis-from-earlier-chapters).
- Top-level Index `how_to_use_section` footnote (NEW — first chapter to require a structural addition to the top-level navigation prose; ch06 added a row footnote, ch07 adds a section-level footnote).
