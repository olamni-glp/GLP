# Exercise 03 — Cluster A §7.4 ancestor-scoped types (Formal 7.1)

You have already loaded the cluster A project in ex-01 and watched §7.3
exported / private declarations resolve module-by-module in ex-02.  The
load also did something more silent and more powerful: it resolved
**every type reference** in `agent.glp`, `boot.glp`, `ui/mediator.glp`,
and `ui/actors.glp` — even though none of those files defines a single
type itself.  The 40 protocol types those four files use are all
defined exactly once, in `simple-multimodule/self.glp`, and become
visible to every module in the cluster via §7.4 **ancestor scoping**.

## What you'll learn

- The §7.4 **ancestor-scoping rule** for types: each module's type
  environment is the **union** of all `self.glp` files from the
  project root down to (and including) the module's own directory —
  never any other directory.
- Why this means **no import directive is needed** to use a type
  defined in any ancestor `self.glp` — the type checker walks the
  ancestor chain automatically per Formal 7.1.
- That cluster A has **two** levels in its scope chain (root +
  cluster-`self.glp`) but **not three** — there is no
  `ui/self.glp`, so `ui/mediator.glp` and `ui/actors.glp` see the
  same type environment as the top-level `agent.glp` and `boot.glp`.

## The self.glp scope chain (Formal 7.1)

For a `.glp` source file `<root>/.../<dir>/M.glp`, the type checker
assembles the type environment by walking from the project root down
to `<dir>` and **unioning** every `self.glp` it finds along the way.
This is **Formal 7.1, Type Scope Assembly**, book pp 57–58.

For cluster A, the chain has two members:

| Level | Path (in this Windows clone) | What it contributes |
|---|---|---|
| Root | `programs/self.glp` | Predefined types (`Constant`, `Stream(X)`, …) and the kernel prelude |
| Cluster | `olamni/tutorial/ch07/simple-multimodule/self.glp` | The 40 CSSG protocol types (`FriendContent`, `AgentChannel`, `OutputsList`, `ActorChannel`, …) |

There is **no** `ui/self.glp` (per spec amendment Q-FR003a in
`spec.md` Clarifications session 2026-05-01); the `ui/` subdirectory
contains only `mediator.glp` + `actors.glp`.  The scope chain for
`ui/mediator.glp` is therefore exactly the same as for the top-level
`agent.glp`: root + cluster.

This is why `ui/actors.glp` can write `exported procedure
alice1(ActorChannel?).` and the type checker resolves `ActorChannel`
to the definition on line 154 of `simple-multimodule/self.glp` —
**without** any `imported type` directive (GLP has no such directive
because Formal 7.1 makes one unnecessary).

## Sample types from `simple-multimodule/self.glp`

The cluster's `self.glp` is a 162-line catalogue of 40 protocol types.
A representative slice:

```prolog
%% Friend messages (after connection established)
FriendContent ::= response(Response)
                ; text(Constant)
                ; intro(Constant, IntroChannel)
                ; child_intro(Constant, IntroChannel).
FriendMsg     ::= msg(Constant, Constant, FriendContent).
```

```prolog
%% Precise channel between agent and mediator
AgentChannel ::= ch(AgentToUserStream, MediatorToAgentStream?).
```

```prolog
%% Output list — keys distinguish system channels, friends, and children
OutputKey   ::= '_user' ; '_net' ; friend(Constant) ; child(Constant).
OutputEntry ::= output(OutputKey, OutputStream?).
OutputsList ::= [] ; [OutputEntry | OutputsList].
```

```prolog
%% Actor's view of the user channel (reversed)
ActorChannel ::= ch(UserNotifyStream, UserCmdStream?).
```

These four type families (Friend\*, Agent\*, Output\*, Actor\*) cover
the cross-module wiring that `boot.glp`'s `play1/0` clause assembles
when it stitches the agent / mediator / actor / network into a running
play.  Every line of those types lives **only** in `self.glp` —
nowhere else.

## Where these types are used

The same 40 types are referenced in dozens of declarations across the
four other modules in the cluster.  A non-exhaustive map:

| Type | Defined at | Used by |
|---|---|---|
| `OutputsList` | `self.glp:120` | `agent.glp:30,35,57,60,92,99,113` (5 procedure decls + the exported `agent/4`); `boot.glp:27` (imported decl) |
| `UserInStream` | `self.glp:95` | `agent.glp:47,80,113`; `boot.glp:27` |
| `NetInStream` | `self.glp:86` | `agent.glp:92,99,113`; `boot.glp:27` |
| `AgentChannel` | `self.glp:74` | `boot.glp:30` (imported decl for `mediator#ui_mediator/5`); `ui/mediator.glp:33` |
| `ActorChannel` | `self.glp:154` | `boot.glp:33-41` (9 imported decls — `alice1/bob1/charlie1` × plays 1/2/3); `ui/actors.glp:20,55,87,116,…` (one per exported actor) |
| `UserNotifyStream` | `self.glp:150` | `ui/actors.glp:24,32,41,49,63,73,80,…` (every internal helper procedure of every actor) |
| `UserCmdStream` | `self.glp:149` | same usage shape as `UserNotifyStream` (paired return type) |
| `FriendContent` | `self.glp:22` | `self.glp:26,85` (downstream type definitions only — `FriendContent` itself does not appear in any procedure body, but its *constructors* — `text`, `intro`, `child_intro`, `response` — do, in `agent.glp` and `ui/mediator.glp`) |

The takeaway: every type travels across module boundaries **purely by
ancestor scoping**.  The type checker, when it loads `ui/actors.glp`,
sees `ActorChannel` as a live name in scope because Formal 7.1
unioned `simple-multimodule/self.glp` into the type environment when
it walked the ancestor chain.  No declaration in `actors.glp` had to
say "import ActorChannel from ../self.glp" — there is no such
directive in GLP, and there does not need to be.

## Run the load + play1 demo

### Step 1 — Open the REPL

```bash
./glp_runtime/glp_repl.exe
```

### Step 2 — Load cluster A (ancestor scoping happens at type-check time)

At the `GLP>` prompt, paste the absolute path to the cluster directory
(no trailing slash):

```
D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/simple-multimodule
```

Expected: `✓ Loaded project: …`.  This single line summarises a
five-module load — and it would have failed loudly the moment any
type reference in `agent.glp`, `boot.glp`, or either `ui/` module
could not be resolved.  Cross-check: trace's **Phase A**.

### Step 3 — Raise the goal-reduction limit and run play1

```
:limit 1000000
play1.
```

Expected: `→ suspended`.  Per the bonds-plays note in `CLAUDE.md` §12,
a suspended end-state is the normal terminal condition for these CSSG
plays once the actors finish their scripts and the network's cold-call
streams empty out.  The fact that the run reached suspension —
rather than type-failing or pattern-failing — confirms the types from
`simple-multimodule/self.glp` were live at run time exactly as they
were at compile time.  Cross-check: trace's **Phase B**.

### Step 4 — Cross-check against the trace

Open `ex-03-repl-trace.md` and confirm the two `GLP>` exchanges match
your session.

## What you've seen

1. **Ancestor scoping in action** — four modules (`agent.glp`,
   `boot.glp`, `ui/mediator.glp`, `ui/actors.glp`) compile and run
   while referencing 40 protocol types defined in **none** of them.
   The types live in `simple-multimodule/self.glp` and reach all four
   modules via the §7.4 / Formal 7.1 ancestor-scoping rule.
2. **Two-level scope chain** — cluster A has `programs/self.glp` ∪
   `simple-multimodule/self.glp` and stops there; the `ui/`
   subdirectory does not host its own `self.glp` (Q-FR003a).
3. **No type import directive** — GLP does not have one, because
   Formal 7.1 makes one unnecessary.

## Note on the multimodule-project-derivation relationship

The byte-exact files (`self.glp`, `agent.glp`, `ui/mediator.glp`,
`ui/actors.glp`) you saw load are inherited unchanged from
`programs/cssg_modules/` (the §7.7 validation example, book p 61);
only `boot.glp` is derived (pruned per Q1a to keep the 3-agent plays
1/2/3 and drop the 4-agent CSSG plays 4–7).  This
**multimodule-project-derivation** relationship is the cross-chapter
contract introduced fresh at ch07; it is distinct from the byte-exact
single-file inheritance used in chs 1–6.  See `data-model.md` and the
ch07 charter §2.2.

## Next

Exercise 4 is §7.5 procedure renaming (`agent#agent`,
`mediator#ui_mediator`, `actors#alice1`, …).  You have already seen
those forms in `boot.glp`'s `imported procedure` declarations and
again in its `play1` clause body; ex-04 inspects them in detail.
