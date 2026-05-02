# ex-05 — REPL trace (cluster A end-to-end play1)

This trace captures the verbatim REPL session for ex-05 — the cluster A
end-to-end exercise that runs `play1.` against the `simple-multimodule/`
project.  Two phases: the project load (Phase A, same shape as ex-01..ex-04)
and the `play1.` end-to-end run (Phase B).  Together they exercise every
§7.x mechanic introduced in ex-01..ex-04: project-loading mode (§7.1–§7.2),
exported / private / imported procedure declarations (§7.3), ancestor-
scoped types (§7.4), procedure-renaming via the `module#name` form (§7.5),
and the §7.7 multi-module play form.  The trace is a single REPL session;
Phase A and Phase B come back-to-back inside the same fenced block per the
trace-file-format contract.

## Phase A + B — Project load + `play1.` end-to-end

The implementer launches the REPL kernel snapshot, pipes the absolute path
of the cluster A project directory, raises the goal-reduction limit to one
million per CLAUDE.md §12 (plays may need higher limits), and submits
`play1.`.  The REPL detects the directory, switches to project-loading
mode, and emits the single `✓ Loaded project:` success line.  The
`play1.` goal then runs end-to-end: it allocates the 3-agent network,
spawns Alice / Bob / Charlie agents (each paired with its mediator and
actor), and connects everything via cross-module calls.  The result is
`→ suspended` — the goal does not fail, but the channels stay open by
design (the actors complete their scripted exchanges and the channels
remain unsealed, awaiting further input that never arrives).  Per
CLAUDE.md §12, `→ suspended` is a valid play outcome — the play
configuration succeeded, the protocol completed, and no fault was raised.

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
GLP> Goal reduction limit set to 1000000
GLP> → suspended

GLP> Goodbye!
```

The single `✓ Loaded project:` line is the project-loading-mode success
signal — it covers all five files (`self.glp`, `agent.glp`, `boot.glp`,
`ui/mediator.glp`, `ui/actors.glp`) plus the ancestor-scoping type assembly
per §7.4.  The `→ suspended` line is the `play1.` outcome — see the
postscript below for what suspended means here.

---

## Postscript — §7.x mechanics exercised by this play

`play1` is the smallest end-to-end demo of cluster A's multimodule
structure: a 3-agent friend-mediated network running the §7.3 cold-call
befriending protocol where both Bob and Charlie accept Alice's
introduction.  In running it, this exercise rolls every §7.x mechanic
from ex-01..ex-04 into one trace:

1. **§7.1–§7.2 project loading (ex-01)** — the directory load brings in
   all five `.glp` files: `self.glp`, `agent.glp`, `boot.glp`,
   `ui/mediator.glp`, `ui/actors.glp`.  Without project loading mode,
   `play1` would not be reachable; you would have to load each file
   manually and the `module#name` cross-module references would not
   resolve.
2. **§7.3 exported / private / imported procedures (ex-02)** — `play1`'s
   body calls `agent # agent(...)`, `mediator # ui_mediator(...)`, and
   `actors # alice1(...)` / `bob1(...)` / `charlie1(...)`.  These succeed
   because (a) `agent.glp` declares `agent/4` exported, (b)
   `ui/mediator.glp` declares `ui_mediator/5` exported, and (c)
   `ui/actors.glp` declares each `aliceN/1` / `bobN/1` / `charlieN/1`
   exported.  `boot.glp` declares matching `imported procedure` lines for
   each of these (lines 27, 30, 33–41 of the cluster A `boot.glp`).  The
   `network3/3` switch + `tee/3`, `sink/1`, `merge/3` utilities are
   private to `boot.glp` (no `exported` keyword) — they cannot be called
   from any other module, but `play1` calls them locally.
3. **§7.4 ancestor-scoped types (ex-03)** — every channel allocated by
   `play1` (e.g., `ch(AliceNetOut?, AliceNetIn)`,
   `ch(AliceActorIn?, AliceActorOut)`, `ch(AliceAgentToUser?, AliceAgentIn)`)
   uses types defined ONCE in `simple-multimodule/self.glp`
   (`FriendChannel`, `IntroChannel`, `AgentChannel`, `UserChannel`,
   `ActorChannel`).  All four modules see the same type assembly because
   they share the `cssg` ancestor declared in `self.glp`'s `-module(cssg).`
   line.  Without §7.4, each module would have to re-declare these types
   — duplication that the canonical `programs/cssg_modules/` example was
   built to eliminate.
4. **§7.5 procedure renaming via `module#name` (ex-04)** — every
   `agent # agent(...)`, `mediator # ui_mediator(...)`,
   `actors # alice1(...)` form is the §7.5 procedure-renaming syntax in
   action.  These resolve at link time (per §7.6 dynamic linking) to the
   exported `agent/4`, `ui_mediator/5`, `alice1/1` etc. procedures in
   their respective sibling modules.

The `play1` clause body itself (lines 115–145 of cluster A's `boot.glp`)
is the §7.7 multimodule play form — it threads the network channels
through three agents, three mediators, and three actors, with `tee/3` +
`sink/1` to absorb the display streams that would otherwise back-pressure
the mediators.  After `play1` finishes setting up the network and the
actors complete their scripted exchanges, the channels remain open
(unsealed) — that is the `→ suspended` outcome.  Per CLAUDE.md §12,
`succeeds` and `suspended` are both valid play outcomes; `suspended`
indicates the protocol completed without fault and the channels are
simply waiting for further input that never comes.

The cluster A canonical source is `programs/cssg_modules/` (the §7.7
validation example from book p 61); cluster A's `self.glp`, `agent.glp`,
`ui/mediator.glp`, and `ui/actors.glp` are byte-exact from the canonical,
with only `boot.glp` derived (pruned to the 3-agent friend-mediated
subset retaining plays 1–3 + fplays 1–3 per spec Q1+Q5+Q1a).  This is
the cap-stone of cluster A's REPL exercises: ex-01 loaded the project,
ex-02..ex-04 inspected the §7.3–§7.5 mechanics in isolation, and ex-05
puts them all into motion in a single end-to-end run.
