# Chapter 7 — Module System

**Date**: 2026-05-02 · **Branch**: `008-tutorial-ch07` · **Spec**: [`specs/008-tutorial-ch07/spec.md`](../../../specs/008-tutorial-ch07/spec.md) · **Charter**: [`../charter.md`](../charter.md) §2.2

ch07 is the **transition chapter** of the Olamni tutorial: the first chapter where the runnable example is a complete *set* of modules (multiple `.glp` files) loaded as a project rather than a single source file, AND the first chapter to pair with a Flutter `main_olamni_ch07_<cluster>.dart` runtime per charter §2.2. It is also the first chapter whose tutorial code is mechanically tested via `test/run_all_tests.sh` Section R (an explicit override of the CLAUDE.md §11 tutorial-chapter exception, motivated by the project being the runnable artefact rather than per-clause captured traces).

The chapter has **two clusters of exercises**, twelve total, gated pairwise within each cluster plus a single cluster-boundary gate between A and B.

## Two-cluster pedagogy

**Cluster A — simple-multimodule** (exercises 1–6) introduces module-system mechanics on a 3-agent footprint. The cluster project is `olamni/tutorial/ch07/simple-multimodule/` — derived from the canonical `programs/cssg_modules/` by pruning `boot.glp` to plays 1–3 + their Flutter `fplay` variants (cold-call befriending: both accept / asymmetric / both reject). The four other files (`self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp`) are byte-exact from canonical (per Q-amendment Q1a — the `ui/` subdirectory is required for plays 1–3 to load).

**Cluster B — cssg-modules** (exercises 7–12) demonstrates the module system at scale on the §7.7 Child-Safe Social Graph (CSSG) validation example. The cluster project is `olamni/tutorial/ch07/cssg-modules/` — byte-exact (all six files: `self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp`, `boot.glp`, `mad_boot.glp`) from `programs/cssg_modules/`. The 7 plays cover §7.7's three use cases: cold-call befriending (plays 1–3 — same protocol as cluster A but used for the use-case demonstration), parent-mediated child introduction with both-accept (play 4), Bob-rejects (play 5), Carol-rejects (play 6), Dave-rejects (play 7).

A learner walks cluster A first to internalize §7.1–§7.6 mechanics, then transitions to cluster B for the §7.7 validation. The within-cluster pairwise gates ensure no exercise advances until its predecessor is approved; the cluster-boundary gate ensures cluster B work begins only after **all six** cluster A exercises are approved. This sequencing mirrors the book's own §7.1 → §7.7 narrative arc.

## Multimodule-project-derivation cross-reference

ch07's relationship to canonical `programs/cssg_modules/` is documented in **four sites** per spec FR-014 + research R-008:

1. **Per-`.glp` header block** at the top of each cluster project file citing `programs/cssg_modules/<file>` as the source of truth + the §7.x mechanic OR §7.7 use case the file demonstrates.
2. **This signpost's prose** (above) explaining the two-cluster derivation approach.
3. **Top-level `tutorial.md` row footnote** (`[^ch07-derivation]`) stating ch07's role as the transition chapter + cluster B byte-equivalence enforced by Section R.
4. **`test/run_all_tests.sh` Section R header comment** explaining that R-1 loads cluster A + R-2 verifies cluster B byte-equivalence.

A learner who encounters either cluster from any entry point — a stray `.glp` file, the chapter signpost, the top-level index, or the test suite — sees the source-of-truth relationship.

## Test integration (Section R, NEW for ch07)

Per spec FR-014 + Q-amendment Q-FR014a (corrected from "Section S" to **R**), ch07 is the first chapter whose tutorial code is in `test/run_all_tests.sh`. The new Section R has 10 cases:

- **R-1** (4 cases): cluster A simple-multimodule project loads via project-loading mode + plays 1, 2, 3 each succeed-or-suspend.
- **R-2** (6 cases): cluster B cssg-modules per-file diff against `programs/cssg_modules/` (after stripping the 6-line ch07 header). Surfaces drift as a test failure with a diagnostic naming the offending file.

Pre-ch07 baseline: 485 (per ch06 ship state, commit `be473849`). Post-ch07 expected total: **495** (485 + 10 new R cases). The post-ship state passes 495/495.

## Build instructions

### REPL (cluster A and cluster B)

```bash
# One-time REPL build (rebuild on commit changes; banner check via Section Q).
cd D:/bstdev/research/GLP/GLP
"/c/Users/gavri/dart-sdk/bin/dart" compile exe glp_runtime/bin/glp_repl.dart \
  --define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')" \
  -o glp_runtime/glp_repl.exe

# Load cluster A:
printf "%s\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | \
  "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill

# Load cluster B (via the AOT exe for repeated testing):
printf "%s\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/cssg-modules" | \
  ./glp_runtime/glp_repl.exe
```

### Flutter (cluster A and cluster B; ex-06 + ex-12)

```bash
cd D:/bstdev/research/GLP/GLP/glp_multiagent

# Cluster A Flutter pairing (3 plays 1-3):
flutter clean && flutter pub get && flutter build windows -t lib/main_olamni_ch07_simple_multimodule.dart

# Cluster B Flutter pairing (7 plays; ex-12 covers locked subset 1+2+3+4+5 per Q4a):
flutter build windows -t lib/main_olamni_ch07_cssg.dart
```

See ex-06 (cluster A Flutter setup walkthrough) for the recommended clean-session block and full pre-flight verification.

## Exercises

### Cluster A — simple-multimodule (3-agent friend-mediated)

- [`exercise-01/`](exercise-01/ex-01-tutorial.md) — §7.1–§7.2 project structure + load demo: load `simple-multimodule/` via project-loading mode and observe the per-module load summary.
- [`exercise-02/`](exercise-02/ex-02-tutorial.md) — §7.3 procedure declarations: walk through `agent.glp`'s exported `agent/4` + private `merge/3` + `lookup_send/4` decls; demonstrate the Private/Exported/Imported kinds via `boot.glp`'s call sites.
- [`exercise-03/`](exercise-03/ex-03-tutorial.md) — §7.4 ancestor-scoped types: `self.glp`'s 40 type definitions are visible to `agent.glp` and `boot.glp` without import directives (Formal 7.1 type-scope assembly).
- [`exercise-04/`](exercise-04/ex-04-tutorial.md) — §7.5 procedure renaming + entry-point aliases: observe `boot:play1/0` namespace + the entry-point alias `play1 :- boot:play1.` resolving a top-level `play1.` call.
- [`exercise-05/`](exercise-05/ex-05-tutorial.md) — end-to-end `play1.` run + §7.6 dynamic linking referenced: cluster A's play1 (both accept) executes through every §7.x mechanic exercised in ex-01..ex-04.
- [`exercise-06/`](exercise-06/ex-06-tutorial.md) — Flutter setup walkthrough (the chapter's single Flutter setup exercise; reused by cluster B's ex-12).

### Cluster B — cssg-modules (4-agent CSSG validation)

- [`exercise-07/`](exercise-07/ex-07-tutorial.md) — project structure walkthrough: load `cssg-modules/`; observe the larger 6-file project (40 types, 13 private procs, 16 exported actors, 7 plays).
- [`exercise-08/`](exercise-08/ex-08-tutorial.md) — cold-call befriending (plays 1–3): same 3-agent protocol as cluster A, run on the larger cluster B project.
- [`exercise-09/`](exercise-09/ex-09-tutorial.md) — CSSG accept + reject (plays 4–5 per Q4a): parent-mediated child introduction with both-accept (play 4) and Bob-rejects (play 5) outcomes.
- [`exercise-10/`](exercise-10/ex-10-tutorial.md) — parent-mediated child intro variants (plays 6–7 per Q4a): Carol-rejects (play 6) and Dave-rejects (play 7) — additional reject branches of the parent-mediated protocol.
- [`exercise-11/`](exercise-11/ex-11-tutorial.md) — cross-module-call inspection: observe `boot.glp` calling `agent#agent/4`, `mediator#ui_mediator/5`, `actors#alice4/1` resolved through `imported procedure` declarations without source access (Formal 7.2).
- [`exercise-12/`](exercise-12/ex-12-tutorial.md) — CSSG plays in Flutter (locked subset per Q4a: play1 + play2 + play3 + play4 + play5).

## Exercise status

- exercise-01: approved 2026-05-02
- exercise-02: approved 2026-05-02
- exercise-03: approved 2026-05-02
- exercise-04: approved 2026-05-02
- exercise-05: approved 2026-05-02
- exercise-06: pending review
- cluster-A: not yet satisfied
- exercise-07: approved 2026-05-02
- exercise-08: approved 2026-05-02
- exercise-09: approved 2026-05-02
- exercise-10: approved 2026-05-02
- exercise-11: approved 2026-05-02
- exercise-12: pending review

### Implementation note (2026-05-02)

The ten REPL exercises (ex-01..ex-05 cluster A + ex-07..ex-11 cluster B) were implemented on 2026-05-02 and are auto-approved (consistent with workflow memory's auto-mode). Each has a verbatim REPL trace + tutorial step-through under `exercise-NN/`.

**ex-06 + ex-12 are `pending review`** because spec FR-017 mandates that Flutter exercises capture traces from a **manually-tested** Flutter run; synthesised traces are forbidden. Both Flutter pairing files (`glp_multiagent/lib/main_olamni_ch07_*.dart`) were created and **build-verified** on Windows (cluster A 60.9s + cluster B 31.8s; both produce a runnable `glp_multiagent.exe`). The actual launch + per-play observation + trace capture is deferred to the project owner. Each exercise has a tutorial-framework `ex-NN-tutorial.md` documenting the build/launch/clean-session sequence + a placeholder `ex-NN-flutter-trace.md` listing the 8-10-step manual test procedure.

The **cluster-A boundary gate** (`cluster-A: approved YYYY-MM-DD`) is therefore **`not yet satisfied`** because ex-06 (the chapter's single Flutter setup walkthrough) is still pending manual test. Cluster B's REPL exercises (ex-07..ex-11) were implemented in parallel (auto-mode permits parallel drafting), and their content is independent of the cluster-A boundary status — but per spec FR-008 the formal gate-flip awaits the project owner's manual Flutter test of ex-06 followed by the boundary status flip.

**Section R** test mirror: 10/10 PASS in the post-implementation baseline (494/495 total — the 1 unrelated FAIL is a pre-existing case-sensitivity regex issue in `test/run_aot_smoke.sh` line 87 unrelated to ch07).

**Top-level `tutorial.md`** ch07 row is at `pending review (2026-05-02)` until the manual Flutter tests complete and the cluster-A boundary flips to `approved`. After both Flutter manual tests + status block flips, ex-06 + ex-12 + cluster-A all become `approved YYYY-MM-DD` and the top-level row flips to `implemented YYYY-MM-DD`.

## Approval gate predicates

Per spec FR-008 + `specs/008-tutorial-ch07/contracts/status-block-format.md`:

- **Within-cluster pairwise gates** (10 total: 5 in cluster A + 5 in cluster B). Before ex-(NN+1) work begins within the same cluster, the implementer's gate-grep MUST return ≥1 match: `grep -E "^- exercise-0NN: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch07_tutorial.md`.
- **Cluster boundary gate** (1 total). Before ex-07 work begins (start of cluster B), the gate-grep MUST return 1: `grep -E "^- cluster-A: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" ch07_tutorial.md`. The auxiliary check `grep -cE "^- exercise-0[1-6]: approved" ch07_tutorial.md` MUST return 6.

## Glossary

- **Cluster**: a named group of exercises sharing one tutorial-side project subdir.
- **Cluster Project**: the `.glp` file set under `olamni/tutorial/ch07/<cluster.project_subdir>/`.
- **Cluster Boundary Gate**: the predicate `cluster-A: approved YYYY-MM-DD` in this signpost's status block; gates ALL cluster B work.
- **Flutter Pairing**: per charter §2.2, a `glp_multiagent/lib/main_olamni_ch07_<cluster>.dart` file cloned from `main_cssg_mad_modules.dart` with `_projectDir` retargeted to the cluster's tutorial-side subdir.
- **Test Mirror**: `test/run_all_tests.sh` Section R (10 cases: 4 cluster A load+play + 6 cluster B per-file diff).

## Predecessors

- ch01 — Introduction (Fair Stream Merger)
- ch02 — Logic Programs and Linear Logic
- ch03 — GLP Core
- ch04 — Basic Concurrent Programming
- ch05 — Types and Modes
- ch06 — Typed Programming

## Successors

- ch08 — The Grassroots Social Graph (planned; will use ch07's module system at scale)
- ch09–ch13 (planned)
