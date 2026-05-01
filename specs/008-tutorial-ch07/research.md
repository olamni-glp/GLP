# Research — ch07 (Module System)

**Phase 0 output**. All NEEDS CLARIFICATION items from Technical Context resolved here. Cites spec.md (FR-NNN, SC-NNN, Q1–Q5), CLAUDE.md, and predecessor research (`specs/007-tutorial-ch06/research.md` R-001..R-009).

ch07 is the first chapter that fundamentally departs from the chs 1–6 pattern: per charter §2.2 it introduces the **multimodule project subdirectory** as the primary tutorial artefact AND pairs each project with a Flutter `main_olamni_ch07_<cluster>.dart` runtime. ch07 is also the first chapter whose tutorial code IS testable mechanically (per spec FR-014 + the "explicit override of CLAUDE.md §11 tutorial-chapter exception" clause in spec Assumptions).

## R-001 — Per-`.glp` `%%` paraphrase comment volume

**Decision**: Cluster A has 5 `.glp` files with byte-exact content from `programs/cssg_modules/` (with one file — `boot.glp` — pruned to plays 1–3 + fplay 1–3); cluster B has 5 `.glp` files byte-exact from `programs/cssg_modules/` (including all 7 plays + 7 fplays). Per-clause `%%` paraphrase comments are **inherited unchanged from the source `programs/cssg_modules/`** which already carries them; ch07 does NOT re-paraphrase. New `%%` synthesis-or-derivation header blocks are added per the glp-file-format contract (one header per `.glp` per cluster).

**Counts** (verified):
- Cluster A: `self.glp` 155 lines; `agent.glp` 219 lines; `ui/mediator.glp` 178 lines; `ui/actors.glp` 479 lines (all four byte-exact); `boot.glp` ~286 lines (plays 1–3 + fplay 1–3 + the local utilities `tee/sink/send_to_user_tagged/merge` + `network3/3` switch — pruned from the 814-line canonical).
- Cluster B: all six (`self.glp` + `agent.glp` + `ui/mediator.glp` + `ui/actors.glp` + `boot.glp` + `mad_boot.glp`) byte-exact at 155 + 219 + 178 + 479 + 814 + 136 = 1,981 lines.

**Rationale**: charter §1.5's "one paraphrase comment per clause" mandate is satisfied by `programs/cssg_modules/`'s existing `%%` comments (per inspection of `boot.glp` lines 1–11 + 56–80, the canonical files already follow this convention). ch07's tutorial copies inherit these comments verbatim and add only the synthesis-or-derivation header block at the top of each file. Per FR-002 + FR-003, the byte-exact mandate on cluster B is strict (the per-file diff test of FR-014 catches drift); cluster A's pruning of `boot.glp` is the only sanctioned modification.

**Alternatives considered**: re-paraphrasing every `%%` comment for ch07's framing (rejected — would defeat the byte-exact + diff-detectable mandate); adding new per-clause `%%` comments to the cluster A `boot.glp` pruned form (rejected — pruning removes whole plays, not individual clauses; each remaining clause keeps its original `%%` from canonical).

## R-002 — Cluster A's project shape — reconciliation of Q1 + Q5 spec inconsistency

**Spec inconsistency identified**: Spec Q1 says "drop the `ui/` subdir entirely". Q5 then says "all 3 plays (play1/play2/play3) … keeps the THREE 3-agent friend-mediated plays". But plays 1–3 in canonical `programs/cssg_modules/boot.glp` USE `actors # alice1`, `mediator # ui_mediator`, etc. (per file inspection lines 174–204) — i.e., they REQUIRE the `ui/` subdir to load. Q1's "drop ui/" cannot coexist with Q5's "keep plays 1–3" without rewriting plays 1–3.

**Decision**: Reconcile by amending Q1 (recorded as Q-amendment **Q1a** in spec Clarifications during /speckit-implement T006a-equivalent — proposed here as Phase 0 research): cluster A KEEPS `ui/{mediator.glp, actors.glp}` byte-exact (NOT pruned — pruning would invalidate byte-exact and break plays 1–3); the only modification is `boot.glp` pruning to plays 1–3 + fplay 1–3 + supporting utilities (`tee`, `sink`, `send_to_user_tagged`, `merge`, `network3/3`). The `network2/2` switch + `network3/3`'s 3-arg-msg friend-to-friend clauses + plays 4–7 + fplay 4–7 + the actors 4–7 cross-references in `boot.glp`'s `imported procedure` block are pruned. The `ui/actors.glp` file itself is kept byte-exact (479 lines) even though only `alice1`/`bob1`/`charlie1`/`alice2`/`bob2`/`charlie2`/`alice3`/`bob3`/`charlie3` are reachable from cluster A's pruned boot — pruning unused actors would (a) violate byte-exact mandate and (b) re-introduce the maintenance burden of selectively pruning a 479-line file.

There is **no `ui/self.glp`** in `programs/cssg_modules/` (file system inspection confirms `ui/` contains only `actors.glp` + `mediator.glp`). Spec FR-003's listing `ui/{self.glp, mediator.glp, actors.glp}` is incorrect — the spec confuses the book §7.2 abstract project-tree EXAMPLE (where `ui/self.glp` is illustrated, p 56) with the canonical `programs/cssg_modules/` IMPL (which does not have one). Recorded as Q-amendment **Q-FR003a** during /speckit-analyze remediation: FR-003's file listing is corrected to `{self.glp, agent.glp, ui/{mediator.glp, actors.glp}, boot.glp, mad_boot.glp}` matching the canonical. The book's §7.2 illustrative tree remains as-is (it is the book's example, not a normative claim about `programs/cssg_modules/`).

`mad_boot.glp` (136 lines) is in `programs/cssg_modules/` and is loaded by `glp_multiagent/lib/main_cssg_mad_modules.dart` as `_bootFileName = 'mad_boot.glp'`. Cluster B's byte-exact copy MUST include it; cluster A's project does NOT need it (cluster A's Flutter pairing per FR-015 retargets `_projectDir` only — `_bootFileName` may stay `mad_boot.glp` for API parity OR may be retargeted to a cluster-A-specific `mad_boot.glp` IFF the Flutter app needs to drive cluster A through madGLP isolates; locked at /speckit-implement T006c per project owner).

**Rationale**: pruning byte-exact source while keeping it "byte-exact" is a contradiction. The cleanest reconciliation keeps `ui/` present and prunes only `boot.glp` (whose pruning is non-byte-exact by definition — the spec already accepts this by saying cluster A is "derived from" rather than "byte-exact from"). The `boot.glp` pruning IS the only divergence from canonical for cluster A.

**Alternatives considered**:
1. **Drop `ui/` entirely AND rewrite plays 1–3 inline** — rejected: significant rewrite, breaks Q1's "minimises scaffolding work" rationale, and pedagogically misleading because `agent # agent(...)` cross-module call SITES would have to be replaced with bare `agent(...)` calls, defeating the §7.3 cross-module-call demonstration.
2. **Drop `ui/` entirely AND inline `actors.glp` content into a single-file cluster A project** — rejected: defeats the multimodule pedagogy that is ch07's whole point.
3. **Keep `ui/` AND prune actors.glp to alice1/bob1/charlie1 only (1 actor per role)** — rejected: cluster A's 3 plays use 3 actor variants (alice1/2/3 + bob1/2/3 + charlie1/2/3), so pruning actors invalidates plays 2 and 3.
4. **Keep `ui/` AND prune actors.glp to alice1-3/bob1-3/charlie1-3 (drop alice4-7/bob4-7/carol4-7/dave4-7)** — partial alternative: would save ~270 lines of dead-code actors. Rejected because: (a) byte-exact diff detection of `ui/actors.glp` against canonical is part of the F-section repair safety net; (b) the 270 lines of unused 4-agent actors are visible to the learner who explores `ui/actors.glp` and provides natural cross-reference to cluster B's CSSG plays (a pedagogical bridge rather than dead code).

**Decision** (per the chosen alternative 0): cluster A's `ui/` is byte-exact unchanged from canonical. Only `boot.glp` is the modification surface. Cluster A's `mad_boot.glp` is included byte-exact IFF Flutter pairing decision at T006c says so; default is exclude (the cluster A Flutter exercise ex-06 uses non-mad-boot REPL semantics).

## R-003 — Top-level `tutorial.md` update strategy

**Decision**: Incremental update per FR-011: ch07's row flips from `planned` to `pending review (YYYY-MM-DD)` when the FIRST cluster A exercise lands; `implemented YYYY-MM-DD` when ALL 12 cluster A + cluster B exercises are approved. The "How to use this tutorial" section's mention of "use-case-driven from chapter 7 onward" gains a footnote pointing at ch07 as the concrete transition example (charter §2.2 cited).

**Rationale**: Inherits ch01–ch06 incremental-update pattern. The footnote NEW content is the transition-chapter explanation per FR-011 second sentence.

**Alternatives considered**: batch-update at chapter completion only (rejected — loses visibility into in-flight state across the 12 exercises, which spans 6 weeks of expected dev time vs ch06's 1 day).

## R-004 — Per-exercise inspection-goal selection

**Decision**: **Deferred to /speckit-implement T-PROPOSE-equivalent** with project-owner approval recorded in this `research.md` at that point. Each cluster A REPL exercise (ex-01..ex-05) and each cluster B REPL exercise (ex-07..ex-11) has a primary-demo-style trace anchor (a project load + a play run OR an inspection sequence) plus 0–3 exploratory inspection goals at the implementer's discretion (the cluster A "load + observe %% Loaded × 4 modules + run play1" trace structure differs from chs 1–6's "1 primary + 3 inspection" pattern because the load itself IS the demonstration of §7.x mechanics). The per-exercise goal set is locked empirically against the actual REPL on this Windows host before any tutorial.md is written for that exercise.

For cluster A:
- ex-01 — primary: load `simple-multimodule/` via project-loading mode; observe per-module `✓ Loaded:` lines + entry-point alias generation (`play1 :- boot:play1.`). 0–2 inspection goals optional (e.g., `:listing` if the REPL supports it; cross-reference to entry-point aliases).
- ex-02 — primary: inspection of `agent.glp`'s exported `agent/4` + private `merge/3` decls; demonstration that `boot.glp` reaches `agent#agent/4` (exported) but not `agent#merge/3` (private). 1–2 inspection goals on call resolution.
- ex-03 — primary: ancestor-scoping inspection — types defined in `simple-multimodule/self.glp` resolving from `agent.glp` and `boot.glp` without imports. 1–2 inspection goals exhibiting concrete type uses.
- ex-04 — primary: procedure-renaming inspection per §7.5 — observe `boot:play1`, `agent:agent` namespace + entry-point alias `play1 :- boot:play1.` resolving a top-level call. 1 inspection goal exhibiting cross-module call resolution.
- ex-05 — primary: end-to-end run of `play1.` (cluster A's play 1 — both accept). Trace records play completion + cross-references which §7.x mechanics from ex-01..ex-04 were exercised.

For cluster B:
- ex-07 — primary: load `cssg-modules/` via project-loading mode; observe per-module load summary (40 types in `self.glp`, 13 private procs in `agent.glp`, etc., per FR-007 + spec US3 acceptance scenario 1). 0–2 optional inspection goals.
- ex-08 — primary: cold-call befriending — run `play1.`, `play2.`, `play3.` in sequence; trace records each play's outcome + channel state.
- ex-09 — primary: friend-mediated introduction — run the locked play subset covering accept + reject branches (per FR-007 default: plays 4–5 OR a subset finalized at T006c per Q4 use-case mapping).
- ex-10 — primary: parent-mediated child introduction — run the locked play subset covering both approve and reject by each party (per FR-007 default: plays 6–7).
- ex-11 — primary: cross-module-call inspection — observe `boot.glp` calling `agent # agent(...)`, `mediator # ui_mediator(...)`, `actors # alice4(...)` resolved through `imported procedure` declarations without source access (per Formal 7.2 + §7.4).

**Rationale**: Inherits ch01–ch06 deferral pattern (ch01 R-004, ch02 ex-02/ex-03 shape selection, ch03 R-007, ch04 R-007, ch05 Q2, ch06 R-004). The project owner reviews each exercise's goal set before commit; halt-and-amend per FR-013 for any binding mismatch or missing-mechanic coverage.

**Alternatives considered**: locking goals at the spec layer (rejected — past Q-retraction precedent; the empirical-verification window at /speckit-implement is the cheaper validation point for ch07's larger 12-exercise scope).

## R-005 — Cross-platform Dart verification

**Decision**: Dart 3.10.1 at `C:\Users\gavri\dart-sdk\bin\dart.exe`. Verified at session start (CLAUDE.md §2 environment detection). Re-verified at /speckit-implement T001 against the constitution requirement (Dart `^3.9.4`).

**Rationale**: Inherited from ch01–ch06; no change for ch07.

**NEW for ch07 — Flutter SDK requirement**: Per FR-005 + FR-015, ex-06 + ex-12 require Flutter. Per Constitution §Technology Stack, the Flutter dependency is at `glp_multiagent/` (Dart `^3.0.0` + Flutter). The implementing session MUST verify Flutter is installed and operational on the implementing host BEFORE attempting ex-06; if Flutter is absent, halt per FR-013 and report. The Flutter SDK version requirement is whatever `glp_multiagent/pubspec.yaml` declares (NOT independently locked at the ch07 spec layer to avoid version-drift from main). Verified at /speckit-implement T001b (NEW pre-flight step inherited as a sub-step of T001).

## R-006 — Type-checker live-pipeline pre-flight verification (inherited from ch05 R-006)

**Decision**: Before any cluster A exercise work begins at /speckit-implement, the implementer MUST verify the live type-checker stage of the REPL pipeline is operational by running the same two-step regression that ch05 R-006 + ch06 R-006 established:
1. **Positive case**: load any ch05/ch06 byte-exact `.glp` (e.g., `olamni/tutorial/ch06/exercise-02/ch-06-ex-02-typed-quicksort.glp`) — MUST report `✓ Loaded:` with no errors.
2. **Negative case**: load any ch05 negative-exercise failing-form `.glp` (e.g., `olamni/tutorial/ch05/exercise-06/ch-05-ex-06-type-error-failing.glp`) — MUST report the documented type-error message and refuse the load.

If the type-checker is broken (positive case fails OR negative case loads cleanly), ch07 work HALTS per FR-013 and the implementer reports the regression. Do NOT proceed against a broken type-checker.

**NEW for ch07 — project-loader pre-flight**: Cluster A and cluster B both rely on the REPL's project-loading mode (load a directory, not a single file; the loader walks `self.glp` ancestors). Per CLAUDE.md §12 the project-loader is operational and exercised by `programs/cssg_modules/` already (`test/run_all_tests.sh` Section F). Pre-flight verification is the **Section F pass** at the baseline test run (T004 — see quickstart Pre-flight). If Section F regresses, ch07 work halts; the project loader is the cluster A + cluster B load mechanism.

**Rationale**: ch07 inherits ch05/ch06's type-system content + the project loader from `programs/cssg_modules/`. No new pre-flight gates beyond the type-checker + Section F pass.

**Alternatives considered**: skipping the pre-flight (rejected — same rationale as ch05 R-006 / ch06 R-006).

## R-007 — Test-mirror Section letter — Section R (NOT Section S)

**Spec drift identified**: Spec FR-014 says "new dedicated **Section S** (next available letter after the current Q AOT smoke / R stale-binary; per ch06 ship state through Section R)". Inspection of `test/run_all_tests.sh` confirms the highest existing section is **Section Q** (AOT REPL exe regression smoke, line 1807); there is no Section R in the file. The "R stale-binary" claim in the spec inherits from a workflow-memory note about an unmerged branch (`claude/fix-misleading-build-line` → would have added stale-binary checks as Section R) that did NOT land in this state. As of HEAD `be473849` (ch06 ship), Section R does not exist.

**Decision**: ch07's test-mirror section is **Section R** (next available letter after Q). Recorded as Q-amendment **Q-FR014a** during /speckit-analyze remediation: FR-014's section letter is corrected from "Section S" to "Section R". The cluster A `simple-multimodule/` load + play test + cluster B byte-equivalence diff test both live under Section R.

**Rationale**: The spec's "Section S" naming was based on an inaccurate assumption about the current state of `run_all_tests.sh`. Empirical verification at HEAD `be473849` shows Section R is the next free letter.

**Alternatives considered**: keeping "Section S" and adding a placeholder Section R (rejected — would manufacture an empty section purely to satisfy the spec); adding the stale-binary checks under a NEW Section R as part of ch07 work (rejected — out of scope for ch07; the stale-binary fix is a separate workstream that has not been agreed for ch07).

## R-008 — Cross-chapter relationship contract — multimodule-project-derivation (NEW for ch07)

**Decision**: ch07's cross-chapter relationship is **multimodule-project-derivation**: cluster A is a **derived** project (byte-exact files except `boot.glp` is pruned to plays 1–3); cluster B is a **byte-exact** project copy. Both clusters' tutorial-side projects bind to canonical `programs/cssg_modules/` as the source of truth.

This contract is distinct from:
- **ch04's cross-chapter inversion** (same code, two homes — producer/consumer in ch03 and ch04).
- **ch05's typed↔untyped relationship** (same procedure name, different signature — typed `merge/3` vs untyped `merge/3`).
- **ch02's cross-chapter forward import** (chapter pulls byte-exact code from later chapter).
- **ch06's synthesis-from-earlier-chapters** (each ex's clauses are byte-exact from earlier chapter, declarations are introduced fresh).

The multimodule-project-derivation contract for ch07 documents:
1. **Each `.glp` header block** (per FR-004 + glp-file-format contract): MUST cite the canonical source (`programs/cssg_modules/<file>`) AND the §7.x mechanic the file demonstrates (for cluster A) OR the §7.7 use case it covers (for cluster B). For cluster A's `boot.glp`, the header MUST explicitly state "pruned from canonical to plays 1–3 + fplay 1–3 only; full canonical version at `programs/cssg_modules/boot.glp` runs all 7 plays". For all other cluster A files + all cluster B files, the header MUST state "byte-exact from `programs/cssg_modules/<file>`".
2. **Each chapter signpost `ch07_tutorial.md`** (per FR-010): MUST contain plain prose explaining the two-cluster derivation approach (cluster A simple → cluster B full validation), the cluster A pruning, the byte-exactness mandate for cluster B, and the test-mirror's role in catching drift.
3. **Top-level `tutorial.md` row footnote** (per FR-011 + FR-014): MUST state "ch07 is the transition chapter to use-case-driven multimodule projects per charter §2.2; cluster B's `cssg-modules/` is byte-exact-equivalent to `programs/cssg_modules/` enforced by Section R of `test/run_all_tests.sh`".
4. **Test-mirror Section R header comment** (per FR-014): MUST cross-reference the spec's FR-014 + the Q-amendment Q-FR014a.

**Rationale**: ch07 is the first chapter where the tutorial code is project-derived rather than per-clause-byte-exact. The derivation approach is novel and needs an explicit contract distinct from the existing cross-chapter relationship types. The four-site documentation (header + signpost + top-level footnote + test-section header) ensures a learner encountering the ch07 project-derivation from any entry point understands the source-of-truth relationship.

**Alternatives considered**: documenting only in the chapter signpost (rejected — a learner who jumps straight into a `.glp` from a search would miss the context); documenting only in `.glp` headers (rejected — a learner browsing the top-level index would miss why ch07's row has a footnote).

## R-009 — Filename conventions (locked per workflow memory + per charter §2.2)

**Decision**:
- Chapter signpost: `ch07_tutorial.md` (underscore between `ch07` and `tutorial`, per workflow memory file-naming dialect).
- Per-exercise tutorial: `ex-NN-tutorial.md` (hyphens, per dialect; NN ∈ 01..12).
- Per-exercise REPL trace: `ex-NN-repl-trace.md` (hyphens) for cluster A REPL exercises (ex-01..ex-05) + cluster B REPL exercises (ex-07..ex-11).
- Per-exercise Flutter trace: `ex-NN-flutter-trace.md` (hyphens) for the two Flutter exercises (ex-06 cluster A + ex-12 cluster B). Per FR-009: each exercise produces ONE trace file; trace type matches the exercise type (REPL or Flutter).
- Cluster A project subdir: `olamni/tutorial/ch07/simple-multimodule/` — locked per FR-002. Files inside: `self.glp`, `agent.glp`, `boot.glp` (pruned), `ui/mediator.glp`, `ui/actors.glp` (per R-002 reconciliation).
- Cluster B project subdir: `olamni/tutorial/ch07/cssg-modules/` — locked per FR-003. Files inside: `self.glp`, `agent.glp`, `boot.glp`, `mad_boot.glp`, `ui/mediator.glp`, `ui/actors.glp` (byte-exact from canonical).
- Flutter pairings: `glp_multiagent/lib/main_olamni_ch07_simple_multimodule.dart` (cluster A) + `glp_multiagent/lib/main_olamni_ch07_cssg.dart` (cluster B). Per FR-015 + FR-020 cloned from `main_cssg_mad_modules.dart` template with `_projectDir` retargeted.
- Exercise dirs do NOT contain their own copies of cluster project files (per FR-009). Each cluster project is shared across all 6 exercises in its cluster.

**Rationale**: Inherits ch01–ch06 conventions for tutorial filenames. NEW for ch07: the cluster-project subdir (which lives under `olamni/tutorial/ch07/` directly, not under any `exercise-NN/`) and the Flutter pairing files (which live under `glp_multiagent/lib/`, not under `olamni/tutorial/ch07/`). Both are normative per FR-002 + FR-003 + FR-015 + FR-020.

**Alternatives considered**: putting cluster project files under each exercise dir (rejected — duplicates the project tree 6 times per cluster + violates FR-009 + masks drift detection); putting Flutter pairings under `olamni/tutorial/ch07/` (rejected — they MUST live with the other Flutter mains under `glp_multiagent/lib/` so the Flutter app's build process picks them up).

## R-010 — Cluster A boot.glp pruning content (NEW for ch07)

**Decision**: Cluster A's `boot.glp` is the canonical `programs/cssg_modules/boot.glp` (814 lines) with the following sections REMOVED:
- The 16 4-agent `imported procedure actors#alice4..dave7` declarations (lines 35–50 in canonical).
- The 6 friend-to-friend (3-arg-msg) `network3/3` clauses (canonical lines 120–148).
- The `network2/2` switch entirely (canonical lines 152–168 — cluster A's plays 1–3 use only `network3/3`).
- The 4 plays + 4 fplays for play4..play7 (canonical lines 282–500 + 604–814).

What REMAINS in cluster A's pruned `boot.glp`:
- Module preamble + imported decls for `agent#agent` + `mediator#ui_mediator` + the 9 3-agent actor decls (alice1/bob1/charlie1/alice2/bob2/charlie2/alice3/bob3/charlie3) — canonical lines 1–32.
- The 6 cold-call (2-arg-msg) `network3/3` clauses + the base case `network3(ch([],[]),...)` (canonical lines 87–116 + 150).
- Local utilities `tee/2`, `sink/1`, `send_to_user_tagged/3`, `merge/3` (canonical lines 56–80).
- `play1`, `play2`, `play3` (canonical lines 174–276).
- `fplay1`, `fplay2`, `fplay3` (canonical lines 508–602).

Estimated cluster A `boot.glp` line count: ~286 lines (down from 814).

**Header block** for cluster A's `boot.glp` (per glp-file-format contract):
```
%% ch07 cluster A boot.glp — DERIVED from programs/cssg_modules/boot.glp
%% Pruned to plays 1–3 + fplay 1–3 (the three 3-agent friend-mediated plays).
%% Canonical source has 7 plays + 7 fplays + network2/2 + 4-agent actors.
%% This pruning preserves runnability of plays 1–3 with the byte-exact ui/{mediator.glp, actors.glp}.
%% Per /speckit-clarify Q5 + Q-amendment Q1a (recorded in spec.md Clarifications during /speckit-implement).
```

**Rationale**: The pruning surface is well-defined and reviewable. Each removed section is a contiguous block of canonical lines, so the diff against canonical is a clean "removed lines X–Y, X–Y, …" report — easy for the byte-equivalence test to be formulated as "cluster A boot.glp is the canonical with line ranges X–Y removed" (or, more pragmatically, the byte-equivalence test for cluster A is NOT enforced; only cluster B's full byte-equivalence is enforced per FR-014).

**Alternatives considered**: keeping the full canonical `boot.glp` for cluster A and tagging plays 4–7 as "out of scope for cluster A" via comments only (rejected — defeats Q1+Q5's "minimised scaffolding"); pruning more aggressively (e.g., dropping fplay1-3 too) (rejected — fplay1-3 are needed for cluster A's Flutter exercise ex-06 per FR-015 + Q5).

## R-011 — Flutter pairing source files content (NEW for ch07)

**Decision**: Both Flutter pairing files (`main_olamni_ch07_simple_multimodule.dart` for cluster A + `main_olamni_ch07_cssg.dart` for cluster B) are clones of `glp_multiagent/lib/main_cssg_mad_modules.dart` with the following modifications:
1. The `_projectDir` constant retargets:
   - Cluster A: `_projectDir = '../olamni/tutorial/ch07/simple-multimodule'`.
   - Cluster B: `_projectDir = '../olamni/tutorial/ch07/cssg-modules'`.
2. The `_bootFileName` constant:
   - Cluster A: `_bootFileName = 'boot.glp'` (uses non-mad-boot semantics by default; cluster A's boot is the pruned canonical, NOT mad_boot — see R-002). IF the project owner decides at T006c that cluster A also needs a `mad_boot.glp` for madGLP-style multi-isolate boot, cluster A's project subdir gets a mad_boot.glp file copied from canonical with appropriate `play1`→`fplay1` retargeting.
   - Cluster B: `_bootFileName = 'mad_boot.glp'` (byte-exact from canonical).
3. The `_agentInfos` panel configuration:
   - Cluster A: 3-agent panel layout (Alice / Bob / Charlie — simple-multimodule's 3-agent friend-mediated plays).
   - Cluster B: 4-agent panel layout (Alice / Carol / Bob / Dave — canonical CSSG's parent-child split, byte-exact from `main_cssg_mad_modules.dart`).
4. The `_cssgSpawnConfigs(int playNum)` helper:
   - Cluster A: spawns 3 isolates per play (alice/bob/charlie with their fplay-specific configs).
   - Cluster B: byte-exact from canonical.
5. **Header comment block** (per FR-020): MUST cite `main_cssg_mad_modules.dart` as the template + the cluster's tutorial path + the date of cloning + the spec FR cross-reference.

**Rationale**: Per FR-015 + FR-020 + charter §2.2. The cloning approach minimizes Flutter-side maintenance burden (changes to the canonical `main_cssg_mad_modules.dart` propagate manually to ch07's clones).

**Alternatives considered**: parameterizing `main_cssg_mad_modules.dart` to accept `_projectDir` + `_agentInfos` + `_cssgSpawnConfigs` as constructor args (rejected — out of scope for ch07; would require a refactor of the canonical Flutter main; the cloning approach is the documented charter §2.2 pattern); having both clusters share one Flutter pairing with a runtime selector (rejected — defeats the per-cluster-Flutter-pairing isolation guarantee).

## R-012 — Per Q4 cluster B Flutter (ex-12) play subset locked at /speckit-plan

**Decision** (per spec Q4 deferral to /speckit-plan T006-equivalent — locked HERE):
ex-12's play subset covers each of the four §7.7 use cases:
- (a) Cold-call befriending (3-agent): **play1** (`fplay1` — the both-accept variant per `boot.glp` line 171's heading).
- (b) Friend-mediated introduction with accept: **play4** (`fplay4` — CSSG: All four accept child introduction per line 280's heading; this is closest to friend-mediated accept since plays 4-7 are all CSSG variants).
- (b') Friend-mediated introduction with reject: **play5** (`fplay5` — CSSG: Bob rejects per line 339's heading).
- (c) Parent-mediated child introduction with accept: **play4** (overlaps (b) — see below).
- (c') Parent-mediated child introduction with reject: **play6** OR **play7** (per `boot.glp` line 393–395 "PLAYS 6-7 follow the same pattern with play6/play7 actors" + the `_cssgSpawnConfigs` `child_init/3` parent-approval-gate flow).

**Spec inconsistency identified — Q4's "5 plays" claim**: Q4 specified "typically 5 plays out of the 7" — but inspection of `boot.glp` shows plays 1–3 are 3-agent friend-mediated (cold-call) and plays 4–7 are 4-agent CSSG (parent-mediated child introduction). The book §7.7's three use cases (cold-call / friend-mediated / parent-mediated child) do NOT have a 1:1 mapping to plays 1–7. Specifically:
- Q4's "(a) cold-call ×1" = play1 (3-agent).
- Q4's "(b) friend-mediated accept + reject" — but plays 4–7 are CSSG (parent-mediated child intro), not friend-mediated. Friend-mediated is §7.3's example, not §7.7's. **Q4 conflated friend-mediated and parent-mediated**. Per Q4 textual claim "the boot.glp comments label plays 1–3 as 3-agent friend-mediated and plays 4–7 as 4-agent CSSG child-introduction; cold-call vs friend-mediated discrimination needs PDF re-read at plan time", this is the PDF re-read at /speckit-plan.
- The actual `boot.glp` headings: plays 1–3 are "Both accept introduction" / "Alice accepts, Charlie rejects" / "Both reject introduction" — these are the **cold-call + friend-mediated** scenarios that book §7.3's `agent/4` clause handles (the `connect`/`intro` two-step protocol). Plays 4–7 are "CSSG: All four accept" / "Bob rejects" / "play6, play7" — these are the **parent-mediated child introduction** scenario specific to §7.7.

**Reconciliation** (recorded as Q-amendment **Q4a** during /speckit-analyze remediation):
- (a) Cold-call befriending — both accept: **play1** (fplay1).
- (b) Cold-call befriending — accept + reject: **play2** (fplay2).
- (c) Cold-call befriending — both reject: **play3** (fplay3).
- (d) Parent-mediated child introduction — both accept: **play4** (fplay4).
- (e) Parent-mediated child introduction — Bob rejects: **play5** (fplay5).

Total: **5 plays** out of the 7 in cssg_modules/boot.glp (skipping play6 + play7 which are variants of play5's reject branch). This matches Q4's "typically 5 plays" target.

**Rationale**: The §7.7 narrative's three use cases conflate cold-call and friend-mediated as one "introduction protocol" (the `agent/4` clause handles both — the difference is whether `connect(Target)` originates from the user directly or from a friend's intro). The 5-play subset gives the learner all 3 outcome branches of cold-call (accept/asymmetric/reject) + the parent-mediated CSSG accept + reject. Plays 6–7 are demonstrated variants of play5's reject mechanism, not new use cases — out of scope for ex-12.

**Alternatives considered**: covering all 7 plays (rejected per Q4 reasoning); covering only 3 plays (rejected — would skip the CSSG parent-mediated demonstration that is §7.7's central distinguishing scenario).

## Appendix A — pre-implement verification checklist

Run BEFORE T001 of /speckit-implement:
- [ ] `git status` — branch is `008-tutorial-ch07`, working tree clean except for spec/plan/research/data-model/contracts/quickstart/tasks artefacts.
- [ ] `dart --version` — reports `^3.9.4` or later (currently 3.10.1).
- [ ] **NEW for ch07**: `flutter --version` — reports a working Flutter SDK. If absent, halt per FR-013 and report.
- [ ] REPL build: `dart compile exe glp_runtime/bin/glp_repl.dart --define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')" -o glp_runtime/glp_repl.exe` — succeeds with no warnings.
- [ ] REPL banner verified: `Built from: <commit>` matches `Repo HEAD: <commit>` (no STALE BINARY warning).
- [ ] R-006 type-checker pre-flight (positive + negative cases) — both pass per the documented procedure.
- [ ] **NEW for ch07**: project-loader pre-flight via Section F pass — verified by baseline test run (next step).
- [ ] Baseline test run: `DART="/c/Users/gavri/dart-sdk/bin/dart" bash test/run_all_tests.sh` — passes at the ch06 ship state baseline (485/485 expected per workflow memory + ch06 ship commit `be473849`; record any drift).
- [ ] R-002 spec inconsistency Q-amendment **Q1a** (cluster A keeps `ui/{mediator.glp, actors.glp}` byte-exact + only `boot.glp` is pruned): recorded in spec.md Clarifications session.
- [ ] R-002 + R-007 spec correction Q-amendment **Q-FR003a** (FR-003 file listing corrected to match canonical) + **Q-FR014a** (FR-014 section letter R, not S): recorded in spec.md Clarifications session.
- [ ] R-012 Q-amendment **Q4a** (5 plays for ex-12: 1+2+3 cold-call + 4+5 CSSG): recorded in spec.md Clarifications session.
