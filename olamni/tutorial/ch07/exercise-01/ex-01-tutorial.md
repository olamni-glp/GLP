# Exercise 01 — Cluster A project structure + load demo (§7.1–§7.2)

Welcome to chapter 7, exercise 1.  This is the first ch07 exercise and the
first tutorial exercise to work with a MULTIMODULE PROJECT rather than a
single `.glp` file.  Cluster A — the "simple-multimodule" project — is a
3-agent friend-mediated subset of the §7.7 validation example.  Here in
ex-01 you point the REPL at the project directory and watch it load.

## What you'll learn

- **§7.1 design principles** — module hierarchy mirrors the filesystem
  (one directory per submodule, one `.glp` per leaf module); types in
  `self.glp` are visible to ALL modules under that directory via
  ancestor-scoping; each module is type-checked self-contained against
  its imports, never against the body of other modules; structural type
  compatibility lets two modules share a type by name as long as the
  shapes agree.
- **§7.2 project-loading mode** — point the REPL at a directory (instead
  of a single `.glp`) and the REPL walks the tree, loading each `.glp`
  module in ancestor-scoped order, assembling the type vocabulary per
  §7.4, and resolving cross-module imports per §7.3.
- **What `✓ Loaded project:` means** — SRSW + partial evaluation +
  type-check + compile passed for ALL files in the project, AND the
  project-completion checks (cross-module import resolution, type
  vocabulary assembly, no orphan exports) all passed.  One line replaces
  the five per-file `✓ Loaded:` lines that single-file mode would emit.
- **The cluster A shape** — five `.glp` files across two directories
  (root + `ui/`), one canonical source (`programs/cssg_modules/`), one
  derivation (`boot.glp` pruned to the 3-agent subset per spec Q1+Q5+Q1a).

## Cluster A project structure

```
olamni/tutorial/ch07/simple-multimodule/
├── self.glp           — shared type vocabulary (FriendChannel, Response, …)
├── agent.glp          — exported agent/4 + private merge/3 + lookup_send/4
├── boot.glp           — DERIVED: 3-agent network/play/fplay orchestration
└── ui/
    ├── mediator.glp   — exported ui_mediator/5 + 3 private helpers
    └── actors.glp     — 16 exported actors (alice1..dave7); cluster A reaches
                         9 of them via boot.glp's pruned imports
```

Each file's role at a glance:

- `self.glp` — root type vocabulary for the cluster (book §7.4 ancestor-
  scoping source).  Defines `FriendChannel`, `FriendStream`, `FriendMsg`,
  `FriendContent`, `Response`, etc.  Visible to every other file in the
  project.
- `agent.glp` — the social agent module (book §7.3 exported/private
  example).  Exports `agent/4`; the helpers `merge/3` and `lookup_send/4`
  are private to this module.  No cross-module imports — fully self-
  contained at module level.
- `boot.glp` — the play orchestrator (the ONLY derived file in cluster A).
  Imports `agent#agent/4`, `mediator#ui_mediator/5`, and the 3-agent actor
  procedures (`alice1..charlie3`).  Wires them together via `network/3`
  cold-call clauses; defines the `play1`, `play2`, `play3` entry points
  and their `fplay1..fplay3` multi-isolate variants.
- `ui/mediator.glp` — UI mediator between agent and user actors (book §7.3
  example with 1 export + 3 privates).  Exports `ui_mediator/5`.  The `ui/`
  directory means this module is addressed as `mediator#ui_mediator/5` from
  outside (with `ui/` interpreted as the parent submodule).
- `ui/actors.glp` — actor scripts for CSSG plays.  Exports 16 actors total
  (alice1-7, bob1-7, charlie1-3, carol4-7, dave4-7); cluster A reaches the
  9 used by play1+play2+play3 via boot.glp's pruned imports.

## Run the load demo

Run this command from the GLP repo root:

```bash
cd D:/bstdev/research/GLP/GLP && printf "%s\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill 2>&1
```

Expected last two non-`Goodbye` lines:

```
GLP> ✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/simple-multimodule
GLP> Goodbye!
```

The single `✓ Loaded project:` line is the project-loading-mode success
signal.  No per-file `✓ Loaded:` lines appear — project mode collapses
success into one line covering all five files.  Cross-check: trace's
**Phase A**.

## Reference: the trace

See [`ex-01-repl-trace.md`](ex-01-repl-trace.md) for the verbatim REPL
session captured by the implementer.  The trace is byte-exact modulo the
REPL banner block (`Build`, `Compiled`, `Working directory`, `Loaded root
self.glp from`) and the `Goodbye!` line — these vary per build/host and
are EXEMPT from byte-equality per `contracts/trace-file-format.md`.

## Multimodule-project-derivation note

Cluster A is the first instance of the new ch07 cross-chapter relationship
type **multimodule-project-derivation** (R-008): four of cluster A's five
files are BYTE-EXACT copies of `programs/cssg_modules/`, and the fifth
(`boot.glp`) is the ONLY derivation surface — pruned per spec Clarifications
Q1 + Q5 + Q-amendment Q1a.  Specifically:

- `self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp` are
  byte-exact from `programs/cssg_modules/<file>` and inherit the existing
  canonical's per-clause `%%` paraphrase comments unchanged.
- `boot.glp` is pruned: the 4-agent actor imports (`alice4..dave7`),
  friend-to-friend `network3/3` clauses, `network2/2` entirely, and plays
  4–7 + fplays 4–7 are removed.  Retained: 3-agent imports
  (`alice1..charlie3`), the cold-call `network3/3` clauses + base case,
  local utilities (`tee/sink/send_to_user_tagged/merge`), plays 1–3, and
  fplays 1–3.

This derivation note applies to ALL cluster A exercises (ex-01..ex-06).
The full audit (line-by-line diff vs canonical) lives in `boot.glp`'s
header comment block.

## Next

Exercise 02 zooms in on §7.3 procedure declarations — exported, private,
and imported — and inspects them directly in `agent.glp` and
`boot.glp`.  See [`../exercise-02/ex-02-tutorial.md`](../exercise-02/ex-02-tutorial.md).
