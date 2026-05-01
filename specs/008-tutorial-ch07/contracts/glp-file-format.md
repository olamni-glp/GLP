# Contract — `.glp` file format (ch07)

**Path**: `olamni/tutorial/ch07/<cluster.project_subdir>/<file>.glp` (cluster project files; shared across all 6 exercises in the cluster).

**Inherited from ch06's contract** with two ch07-specific shifts:
1. ch07 exercises do NOT have their own `.glp` files (per FR-009 + R-009). Each cluster's project subdir holds the shared cluster project files; per-exercise dirs hold only `ex-NN-tutorial.md` + `ex-NN-{repl,flutter}-trace.md`.
2. ch07's `.glp` files are NOT byte-exact transcriptions of PDF source clauses — they are byte-exact copies (or, for cluster A's `boot.glp`, a pruned derivation) of `programs/cssg_modules/<file>`. The byte-exact reference target is the canonical project, not the book's PDF. This is the multimodule-project-derivation contract per R-008.

## File structure

Each cluster project's `.glp` files retain the canonical `programs/cssg_modules/<file>`'s structure unchanged, with ONE addition: a header comment block at the top of each file documenting the multimodule-project-derivation cross-reference per R-008 + FR-014's first documentation site.

For cluster A:
- `self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp` (4 files): byte-exact + new header block.
- `boot.glp` (1 file): pruned per R-010 + new header block documenting the pruning.

For cluster B:
- `self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp`, `boot.glp`, `mad_boot.glp` (6 files): byte-exact + new header block.

## Header block contract (NEW for ch07 per R-008 + FR-014 first site)

Every `.glp` file in either cluster project MUST have a header comment block of the form:

For byte-exact files (all of cluster A's except `boot.glp`; all of cluster B's):

```
%% ch07 cluster <X> — <relative path within project>
%% BYTE-EXACT copy of programs/cssg_modules/<relative path within project>.
%% Source canonical: programs/cssg_modules/ (the §7.7 validation example from book p 61).
%% Demonstrates: <§7.x mechanic OR §7.7 use case this file participates in>.
%% Section R of test/run_all_tests.sh enforces byte-equivalence to canonical (cluster B);
%%   cluster A's byte-exact files inherit the same enforcement transitively.
```

Concrete example for cluster A `agent.glp`:

```
%% ch07 cluster A — agent.glp
%% BYTE-EXACT copy of programs/cssg_modules/agent.glp.
%% Source canonical: programs/cssg_modules/ (the §7.7 validation example from book p 61).
%% Demonstrates: §7.3's exported procedure agent/4 + private merge/3 + lookup_send/4.
%% Section R of test/run_all_tests.sh enforces byte-equivalence to canonical (cluster B);
%%   cluster A's byte-exact files inherit the same enforcement transitively.
```

Concrete example for cluster B `boot.glp`:

```
%% ch07 cluster B — boot.glp
%% BYTE-EXACT copy of programs/cssg_modules/boot.glp.
%% Source canonical: programs/cssg_modules/ (the §7.7 validation example from book p 61).
%% Demonstrates: all 7 §7.7 plays + the network2/2 + network3/3 switches + the local utilities.
%% Section R of test/run_all_tests.sh enforces byte-equivalence to canonical (per-file diff).
```

For cluster A's pruned `boot.glp` (the only DERIVED file in either cluster):

```
%% ch07 cluster A — boot.glp (DERIVED)
%% Pruned from programs/cssg_modules/boot.glp.
%% Removed: 4-agent actor imported decls (alice4..dave7); friend-to-friend network3/3 clauses;
%%   network2/2 entirely; plays 4–7; fplays 4–7.
%% Retained: 3-agent actor imported decls (alice1..charlie3); cold-call network3/3 clauses
%%   + base case; local utilities (tee/sink/send_to_user_tagged/merge); plays 1–3; fplays 1–3.
%% Per /speckit-clarify Q1 + Q5 + Q-amendment Q1a (recorded in spec.md Clarifications).
%% Cluster A's byte-exact files (self.glp, agent.glp, ui/mediator.glp, ui/actors.glp) are
%%   inherited unchanged from canonical; only this boot.glp is the derivation surface.
```

## Per-clause `%%` paraphrase comments (charter §1.5)

The cluster project files INHERIT canonical's existing per-clause `%%` paraphrase comments unchanged. ch07 does NOT add or modify per-clause comments (rationale per R-001).

For cluster A's pruned `boot.glp`: the retained sections retain their canonical per-clause `%%` comments unchanged; the removed sections take their per-clause `%%` comments with them.

## Byte-exact mandate scope

Per FR-002 + FR-003 + R-002 reconciliation:
- ✓ All cluster B files: byte-exact copies of canonical (the per-file diff in Section R enforces this).
- ✓ All cluster A files EXCEPT `boot.glp`: byte-exact copies of canonical.
- ✗ Cluster A's `boot.glp`: pruned per R-010 (the only DERIVATION). Section R does NOT enforce byte-equivalence on cluster A's `boot.glp` — instead, it loads the cluster A project + runs `play1.`/`play2.`/`play3.` to verify the pruned `boot.glp` is loadable + runnable.
- ✓ Header blocks added at the top of each file: NOT byte-exact (they are NEW for ch07). Section R's per-file diff for cluster B EXCLUDES the header block bytes (the test compares only the canonical-source byte range, NOT the header).

## File-count contract (FR-009)

Each exercise dir under `olamni/tutorial/ch07/exercise-NN/` contains exactly TWO files:
- `ex-NN-tutorial.md` (always).
- `ex-NN-repl-trace.md` (REPL kind: ex-01..ex-05, ex-07..ex-11) OR `ex-NN-flutter-trace.md` (Flutter kind: ex-06, ex-12).

The cluster project subdir under `olamni/tutorial/ch07/<cluster.project_subdir>/` contains the cluster's `.glp` files (5 for cluster A; 6 for cluster B). NO `.glp` files in any `exercise-NN/` dir.

## SRSW + type-check verification (FR-018)

Each cluster project's `.glp` files MUST pass:
1. SRSW analyser at REPL load (inherited automatic verification — fails the load if violated).
2. Live type-checker at REPL load (per ch05 R-006 inheritance + ch06 R-006 + ch07 R-006).
3. Project-loading-mode compilation + execution of the locked plays (cluster A: play1..play3; cluster B: play1..play7 + fplay1..fplay7 callable).

Mismatch at any step is halt-and-amend per FR-013. The byte-exact source files are LOCKED — only header blocks are amendable for ch07 work; canonical-content amendments require a separate spec-amendment + a corresponding canonical update at `programs/cssg_modules/`.

## Inherited from ch01–ch06

This contract inherits from `specs/007-tutorial-ch06/contracts/glp-file-format.md` with the multimodule-project-derivation header block as the ch07-specific addition per R-008. Differences from ch06's contract:
- ch06 had per-exercise `.glp` files; ch07 has per-cluster shared `.glp` files (5 or 6 per cluster).
- ch06's `.glp` files were byte-exact transcriptions of PDF clauses; ch07's `.glp` files are byte-exact copies (or, for cluster A's boot, derivations) of canonical project files.
- ch06's header block cited an earlier-chapter PDF source; ch07's header block cites `programs/cssg_modules/<file>`.
- ch06 had a Q2-deferred declaration-shape locking; ch07 has NO new declarations to lock (canonical's existing declarations are inherited byte-exact).
