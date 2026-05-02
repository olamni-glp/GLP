# ch07 ex-03 — Cluster A §7.4 ancestor-scoped types — REPL trace

This trace captures the verbatim REPL session for ex-03.  Two phases:
A loads cluster A (`simple-multimodule/`) — the load itself proves §7.4
ancestor scoping at type-check time, because every module's clauses use
types that exist nowhere except in the cluster's `self.glp`.  B runs
`play1.` so the same types are exercised at run time as `agent.glp` /
`mediator.glp` / `actors.glp` / `boot.glp` exchange messages along the
typed channels.

## Phase A — Build / load

The implementer rebuilds the REPL exe from the current commit and asks
the project loader to load the cluster A directory.  A clean
`✓ Loaded project: ...` line means SRSW + partial evaluation +
type-checking + compilation **all succeeded across all five modules
(self, agent, boot, ui/mediator, ui/actors)**.  The type checker had to
resolve every reference to `FriendContent`, `AgentChannel`, `OutputsList`,
`UserCmdStream`, `ActorChannel`, etc., in files that **declare none of
those types themselves**.  The only place those types are defined is
`simple-multimodule/self.glp`; the type checker found them by walking
the ancestor `self.glp` chain per Formal 7.1.

```glp
GLP> ✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/simple-multimodule
```

The single `✓ Loaded project:` line is the project-loader's success
signal.  Per project-loading mode it summarises the load of the whole
directory; the type-checker's per-module work happens inside this load
silently because every module passed.

## Phase B — Primary action: run `play1.`

`play1.` exercises the cluster's types at run time: `agent.glp` reads
`OutputsList` / `UserInStream` / `NetInStream` from its parameters and
pattern-matches on `OutputContent` constructors (`befriend/2`,
`connected/1`, `received/2`, `text/1`, …); `ui/mediator.glp` matches
`AgentToUserMsg` / `MediatorToAgentMsg` and emits `UserNotify`;
`ui/actors.glp`'s `alice1/1` / `bob1/1` / `charlie1/1` consume
`UserNotifyStream` and produce `UserCmdStream`.  None of these files
declares any of those types themselves — they are all inherited from
`simple-multimodule/self.glp` via §7.4.

```glp
GLP> ✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/simple-multimodule
GLP> Goal reduction limit set to 1000000
GLP> → suspended
```

`→ suspended` is the expected outcome for play1 once all three actors
finish their scripted exchanges and the network's cold-call streams
empty out — readers on the closed-but-not-yet-consumed tails simply
suspend, which is the normal end-state for these CSSG plays (compare
the bonds plays' suspension semantics in `CLAUDE.md` §12).  What
matters for ex-03 is that **the run reached suspension** rather than
type-failing at compile time or pattern-failing at run time, which it
could not have done if the ancestor-scoped types from
`simple-multimodule/self.glp` were not visible to all four sibling
modules.

---

The five-module project you just loaded is the §7.7 validation example
from book p 61 (its canonical home is `programs/cssg_modules/`,
distributed here as `olamni/tutorial/ch07/simple-multimodule/` — four
files byte-exact from canonical, only `boot.glp` pruned per Q1a).  The
40 protocol types in `simple-multimodule/self.glp` are visible to
every other module in the cluster **without any import directive** —
this is the §7.4 ancestor-scoping rule (Formal 7.1, Type Scope
Assembly, book pp 57–58): each module's type environment is the
**union** of all `self.glp` files from the project root down to that
module's own directory.  Because cluster A has no `ui/self.glp` (per
Q-FR003a in the spec), the type environment for `ui/mediator.glp` and
`ui/actors.glp` is exactly the same as for top-level `agent.glp` and
`boot.glp`: root `programs/self.glp` ∪ `simple-multimodule/self.glp`.
