# ex-07 — REPL trace (cluster B project load demo)

This trace captures the verbatim REPL session for ex-07.  One phase: the
implementer points the REPL at the cluster B project directory
(`olamni/tutorial/ch07/cssg-modules`), and the project-loading mode walks
it, loading each `.glp` module in ancestor-scoped order per §7.1–§7.2.
A clean load means SRSW + partial evaluation + type-check + compile passed
for ALL six files in the cluster — there are no per-module load errors and
no project-completion errors.  Cluster B is larger than cluster A (six files
vs five, ~2017 lines vs ~720, 7 plays + 7 fplays vs 3+3) — but the load
output is identical in shape: a single `✓ Loaded project:` success line.

## Phase A — Project load

The implementer launches the REPL kernel snapshot and pipes the absolute
path of the cluster B project directory.  The REPL detects this is a
directory (not a single `.glp` file) and switches to project-loading mode
per §7.2.  The single `✓ Loaded project:` line is the project-loading-mode
success signal — it covers all six files (`self.glp`, `agent.glp`,
`boot.glp`, `mad_boot.glp`, `ui/mediator.glp`, `ui/actors.glp`) plus the
ancestor-scoping type assembly per §7.4 and the cross-module import
resolution per §7.3.

```glp
╔════════════════════════════════════════╗
║  GLP REPL - With Type Checking         ║
╚════════════════════════════════════════╝

Build: d9045902 spec+clarify+plan+tasks+analyze(ch07): spec.md (5 Clarifications Q1..Q5) + plan + research (R-001..R-012) + data-model + 5 contracts (trace + flutter-trace NEW + status-block + glp-file + test-mirror NEW) + quickstart + tasks (T001..T184; 18 phases; 11 gates) + analyze remediations applied (F1 Q-FR003a no ui/self.glp + add mad_boot.glp / F2 Q-FR014a Section R not S / F3 Q1a cluster A keeps ui/ byte-exact only boot.glp pruned / F4 Q4a ex-12 plays = 1+2+3+4+5 / F5 FR-016 7-logical-plays clarification / F6 T005b author input prompt) — first chapter with two-cluster structure + Flutter pairings + tests in run_all_tests.sh
Compiled: 2026-02-01 (GlpEngine refactor)
Working directory: D:\bstdev\research\GLP\GLP

Input: filename.glp to load, or goal to execute
Commands: :quit, :help, :trace, :debug, :limit, :activate, :boot

Loaded root self.glp from: D:\bstdev\research\GLP\GLP\programs\self.glp

GLP> ✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/cssg-modules
GLP> Goodbye!
```

The single `✓ Loaded project:` line replaces the per-file `✓ Loaded:` lines
that single-file mode would emit; project-loading mode collapses success
into one line covering the whole tree, even though the tree has six files
across two directories.  The REPL banner block (`Build`, `Compiled`,
`Working directory`, `Loaded root self.glp from`) and the `Goodbye!` line
are the standard REPL chrome — these vary per build/host and are EXEMPT
from byte-equality per `contracts/trace-file-format.md` §Byte-equality.
The byte-exact element is the literal text
`✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/cssg-modules`
(modulo path separator on the implementer's host).

---

This load demo is the §7.1–§7.2 mechanic exercising the full §7.7 CSSG
(Child-Safe Social Graph) validation example from book p 61 — the same
canonical that cluster A is derived from, but here it is loaded BYTE-EXACT
in its complete form: all 40 types in `self.glp`, all 7 plays + 7 fplays
covering the four §7.7 use cases (cold-call befriending, friend-mediated
introduction, parent-mediated child-intro accept, parent-mediated child-intro
reject), the 25 actor procedures spanning plays 1–7, and the multi-isolate
boot procedures `parent_init/4` + `child_init/3` that the Flutter pairing
in ex-06 + ex-12 will use.  The cluster B canonical source is
`programs/cssg_modules/`; cluster B inherits ALL six files BYTE-EXACT
(no derivation), enforced by Section R of `test/run_all_tests.sh` via
per-file diff.  The §7.3 exported/private/imported procedure mechanics
across cluster B will be inspected directly in ex-11 (cross-module-call
inspection); the §7.7 use cases will be exercised end-to-end in ex-08
(plays 1–3, cold-call befriending), ex-09 (plays 4+5, CSSG accept + reject),
and ex-10 (plays 6+7, parent-mediated child intro variants).
