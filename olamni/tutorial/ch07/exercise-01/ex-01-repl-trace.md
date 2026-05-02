# ex-01 — REPL trace (cluster A project load demo)

This trace captures the verbatim REPL session for ex-01.  One phase: the
implementer points the REPL at the cluster A project directory
(`olamni/tutorial/ch07/simple-multimodule`), and the project-loading mode
walks it, loading each `.glp` module in ancestor-scoped order per §7.1–§7.2.
A clean load means SRSW + partial evaluation + type-check + compile passed
for ALL five files in the cluster — there are no per-module load errors and
no project-completion errors.

## Phase A — Project load

The implementer launches the REPL kernel snapshot and pipes the absolute
path of the cluster A project directory.  The REPL detects this is a
directory (not a single `.glp` file) and switches to project-loading mode
per §7.2.  The single `✓ Loaded project:` line is the project-loading-mode
success signal — it covers all five files (`self.glp`, `agent.glp`,
`boot.glp`, `ui/mediator.glp`, `ui/actors.glp`) plus the ancestor-scoping
type assembly per §7.4.

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

GLP> ✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/simple-multimodule
GLP> Goodbye!
```

The single `✓ Loaded project:` line replaces the per-file `✓ Loaded:` lines
that single-file mode would emit; project-loading mode collapses success
into one line covering the whole tree.  The REPL banner block (`Build`,
`Compiled`, `Working directory`, `Loaded root self.glp from`) and the
`Goodbye!` line are the standard REPL chrome — these vary per build/host
and are EXEMPT from byte-equality per `contracts/trace-file-format.md`
§Byte-equality.  The byte-exact element is the literal text
`✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/simple-multimodule`
(modulo path separator on the implementer's host).

---

This load demo is the §7.1–§7.2 mechanic in its simplest form — point the
REPL at a directory, get one success line back.  The cluster A canonical
source is `programs/cssg_modules/` (the §7.7 validation example from
book p 61); cluster A inherits its `self.glp`, `agent.glp`,
`ui/mediator.glp`, and `ui/actors.glp` BYTE-EXACT from the canonical, with
only `boot.glp` derived (pruned to the 3-agent friend-mediated subset per
spec Q1+Q5+Q1a).  The §7.3 exported/private/imported procedure mechanics,
§7.4 ancestor-scoping, §7.5 procedure-renaming, and §7.7 multi-module
plays are all latent here — they will be inspected directly in ex-02..ex-05.
