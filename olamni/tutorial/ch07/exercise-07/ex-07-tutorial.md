# Exercise 07 — Cluster B project structure walkthrough (§7.7 CSSG)

Welcome to chapter 7, exercise 7.  This is the first cluster B exercise
and your first encounter with the FULL §7.7 CSSG (Child-Safe Social Graph)
validation example from book p 61.  Cluster A (ex-01..ex-06) showed you
multimodule projects in their simplest 3-agent friend-mediated form;
cluster B unfolds the same canonical at full scale — six files, ~2017
lines, 7 plays + 7 fplays covering all four §7.7 use cases, 4-agent
parent-mediated CSSG handshakes, and the multi-isolate `parent_init`/
`child_init` Flutter pairing.  Here in ex-07 you point the REPL at the
cluster B project directory and watch it load.  No goal — the load IS the
exercise.  This is the project-as-runnable-artefact pedagogy: a directory
of `.glp` files is itself a runnable program, not just a collection of
modules.

## What you'll learn

- **The four §7.7 CSSG use cases** that this project's plays cover:
  - **Cold-call befriending** (plays 1–3) — Alice writes `connect(bob)`;
    Bob's agent receives `befriend(alice, ...)`, decides yes/no; if yes,
    both agents add each other to their friend lists.
  - **Friend-mediated introduction** (plays 1–3) — Bob, already friends
    with both Alice and Charlie, writes `introduce(alice, charlie)`;
    Alice and Charlie each receive `befriend_intro(bob, ...)` and decide
    accept/reject; if both accept they exchange messages directly.
  - **Parent-mediated child-intro accept** (plays 4 + 6) — Alice (parent)
    writes `child_introduce(carol, bob, dave)`; Bob receives
    `child_befriend` and APPROVES via `approve_child_intro(...)`; Carol
    and Dave then meet via the established channel.
  - **Parent-mediated child-intro reject** (plays 5 + 7) — same setup as
    the accept case but Bob rejects via `reject_child_intro` — or Bob
    approves but the children themselves reject.
- **The project-as-runnable-artefact pedagogy** — point the REPL at the
  cluster B directory; project-loading mode walks the tree, loads
  `self.glp` first to assemble the type vocabulary, loads each module
  against its `imported procedure` declarations, resolves `agent#agent/4`,
  `mediator#ui_mediator/5`, and `actors#...` references, and emits one
  success line.  No build script, no makefile, no separate compile step
  — the directory IS the artefact.
- **Cluster B's byte-exact mandate** — unlike cluster A (where `boot.glp`
  is derived), cluster B's six files are ALL byte-exact copies of
  `programs/cssg_modules/`, including per-clause `%%` paraphrase comments
  inherited from the canonical.  Section R of `test/run_all_tests.sh`
  enforces this via per-file diff.

## Cluster B project tree

```
olamni/tutorial/ch07/cssg-modules/
├── self.glp        — 40 shared types (FriendChannel, Response, AgentChannel, …) — 161 lines
├── agent.glp       — 1 exported (agent/4) + 13 private helper procs — 225 lines
├── boot.glp        — 7 plays + 7 fplays + network2/network3 switches + utilities — 820 lines
├── mad_boot.glp    — multi-isolate boot: parent_init/4 + child_init/3 + ui_actor/3 — 142 lines
└── ui/
    ├── mediator.glp — 1 exported (ui_mediator/5) + 3 private helpers — 184 lines
    └── actors.glp   — 25 exported actors (alice1..dave7) for plays 1–7 — 485 lines
```

Total: 6 files, ~2017 lines.  The `ui/` subdirectory is addressed as the
`mediator` and `actors` modules from outside (the parent submodule prefix
`ui/` is dropped — the `-module(...)` directive in each file declares the
external name).

## Per-file structure

- **`self.glp`** — shared type vocabulary for the entire CSSG application.
  Declares 40 types covering the friend-channel handshake, the agent ↔
  mediator interface, network input types, agent output types, the user ↔
  mediator interface, and the mediator's pending list.  Byte-exact from
  `programs/cssg_modules/self.glp`.  Visible to every other file via
  ancestor-scoping — type-vocabulary backbone for ALL four §7.7 use cases.
- **`agent.glp`** — the social agent module.  Exports `agent/4` (main loop
  dispatching on incoming user/network messages); private helpers cover
  stream merging, output-list maintenance, keyed message dispatch,
  response injection, introduction handshake bookkeeping, and decision
  routing.  Byte-exact from `programs/cssg_modules/agent.glp`.  Dispatch
  clauses cover every §7.7 use case — `connect`, `introduce`,
  `child_introduce`, `accept_intro`/`reject_intro`,
  `accept_child_intro`/`reject_child_intro`, `approve_child_intro`.
- **`boot.glp`** — the play orchestrator.  Defines 7 numbered plays
  (`play1..play7`) + Flutter-tagged variants (`fplay1..fplay7`): plays
  1–3 cover cold-call + friend-mediated cases (3-agent alice/bob/charlie);
  plays 4–7 cover CSSG parent-mediated cases (4-agent
  alice/bob/carol/dave with carol/dave as children).  Defines `network3/3`
  cold-call + friend-to-friend clauses, `network2/2` for CSSG plays 4–7,
  and local utilities (`tee/3`, `sink/1`, `merge/3`,
  `send_to_user_tagged/3`).  Imports `agent#agent/4`,
  `mediator#ui_mediator/5`, and the 25 actor procedures.  Byte-exact from
  `programs/cssg_modules/boot.glp`.  Each play corresponds to one §7.7
  use case + outcome combination.
- **`mad_boot.glp`** — multi-isolate boot used by the Flutter pairing.
  Defines `parent_init/4` (parent agent boot for CSSG plays 4–7 — sends
  `parent_connect` cold call, then starts agent + mediator + actor + tee
  + send_to_user_tagged), `child_init/3` (child agent boot — intercepts
  `parent_connect` as first network message, binds the response channel,
  then starts its agent), and `ui_actor/3` (16-clause dispatch table
  mapping (agent_id, play_num) pairs to the actor procedure for plays
  4–7).  Byte-exact from `programs/cssg_modules/mad_boot.glp`.  Used by
  ex-12's Flutter pairing — these are the only plays the Flutter app
  runs because they exercise the multi-isolate parent/child structure.
- **`ui/mediator.glp`** — UI mediator between agent and user actors.
  Exports `ui_mediator/5` (17-clause main loop translating agent-to-user
  messages into user-facing notifications + a pending list, and translating
  user commands into agent inputs).  Private `lookup_pending/4` looks up
  pending request IDs and removes them on match.  Byte-exact from
  `programs/cssg_modules/ui/mediator.glp`.  Every notification and every
  user command in ALL four §7.7 use cases flows through this mediator.
- **`ui/actors.glp`** — actor scripts playing the role of users.  Exports
  25 actor entry points: alice1..charlie3 for plays 1–3 (3-agent), and
  alice4..dave7 for plays 4–7 (4-agent).  Each actor is a small state
  machine driving its `ActorChannel` based on received notifications —
  e.g. `alice1` writes `connect(bob)`, waits for `connected(bob)`, sends
  `hello`, waits for the `befriend_intro` with charlie, accepts, etc.
  Byte-exact from `programs/cssg_modules/ui/actors.glp`.  Actors 1–3
  drive cold-call + friend-mediated cases; actors 4–7 drive parent-mediated
  CSSG cases.

## Run the load demo

Run this command from the GLP repo root:

```bash
cd D:/bstdev/research/GLP/GLP && printf "%s\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/cssg-modules" | "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill 2>&1
```

Expected last two non-`Goodbye` lines:

```
GLP> ✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/cssg-modules
GLP> Goodbye!
```

The single `✓ Loaded project:` line is the project-loading-mode success
signal.  No per-file `✓ Loaded:` lines appear — project mode collapses
success into one line covering all SIX files (vs cluster A's five).
Cross-check: trace's **Phase A**.

## Reference: the trace

See [`ex-07-repl-trace.md`](ex-07-repl-trace.md) for the verbatim REPL
session captured by the implementer.  The trace is byte-exact modulo the
REPL banner block (`Build`, `Compiled`, `Working directory`, `Loaded root
self.glp from`) and the `Goodbye!` line — these vary per build/host and
are EXEMPT from byte-equality per `contracts/trace-file-format.md`.

## Multimodule-project-derivation note

Cluster B is the second instance of the new ch07 cross-chapter relationship
type **multimodule-project-derivation** (R-008), but unlike cluster A where
`boot.glp` is the derivation surface, cluster B has NO derivation surface —
all six files are byte-exact-equivalent to `programs/cssg_modules/<file>`.
Section R of `test/run_all_tests.sh` enforces this contract via per-file
diff: each ch07 file is compared against the canonical after stripping the
6-line ch07 header block (the `%% ch07 cluster B — <filename>` paraphrase
comments at the top of each file).  The diff target is zero non-header
differences.

Per FR-019, the canonical at `programs/cssg_modules/` is NOT modified by
this branch — cluster B is a strict downstream copy.  If a future change
to the canonical breaks Section R's diff, the resolution is to update the
ch07 cluster B copy (not the canonical) to restore byte-equivalence.

This derivation note applies to ALL cluster B exercises (ex-07..ex-12).
The full audit (line-by-line diff vs canonical) is encoded in Section R's
test cases.

## Next

Exercise 08 runs the cold-call befriending plays — `play1.`, `play2.`,
`play3.` — end-to-end on cluster B.  These are the same three plays
that cluster A's ex-05 ran on the pruned 3-agent project; here you see
them load and execute on the full 6-file CSSG canonical.  See
[`../exercise-08/ex-08-tutorial.md`](../exercise-08/ex-08-tutorial.md).
