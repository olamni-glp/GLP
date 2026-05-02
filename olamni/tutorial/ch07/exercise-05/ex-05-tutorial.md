# Exercise 05 — Cluster A end-to-end play1 (cross-references ex-01..ex-04)

Welcome to chapter 7, exercise 5 — the cap-stone of cluster A.  Where
ex-01..ex-04 inspected each §7.x mechanic in isolation (project loading,
declaration kinds, ancestor-scoped types, procedure renaming), this
exercise puts them all in motion at once by running the smallest
end-to-end demo cluster A offers: `play1` from `simple-multimodule/boot.glp`.

## What you'll learn

Every §7.x mechanic introduced in ex-01..ex-04 is exercised when `play1`
runs.  The single goal `play1.` brings the multimodule project to life:
five `.glp` files are loaded as a unit; three agents, three mediators,
and three actors are spawned; cross-module procedure calls resolve via
the §7.5 `module#name` form; and the §7.4 ancestor-scoped types ensure
every channel typechecks consistently across module boundaries.  The
end-to-end run is the §7.7 multimodule play form (book p 61) —
the validation example of the chapter.

## play1 walkthrough

`play1`'s body in cluster A's `boot.glp` (lines 115–145) is a sequence of
twenty-one goals broken into one network allocation + three identical
agent-mediator-actor blocks.  Each line cross-references back to one or
more of ex-01..ex-04:

1. **Network allocation** —
   `network3(ch(AliceNetOut?, AliceNetIn), ch(BobNetOut?, BobNetIn), ch(CharlieNetOut?, CharlieNetIn))`
   allocates three network channels.  `network3/3` is a PRIVATE procedure
   in `boot.glp` (no `exported` keyword on its declaration; six recursive
   clauses + one base case).  Cross-reference: **ex-02 §7.3** —
   private procedures are visible only inside the module where they are
   defined.  `play1` is in `boot.glp`, so it can call `network3/3`
   directly.
2. **Alice's actor** —
   `actors # alice1(ch(AliceActorIn?, AliceActorOut))`.
   The `actors # alice1` form is §7.5 procedure renaming: it refers to
   the `alice1/1` procedure exported from sibling module `actors`.
   Cross-reference: **ex-04 §7.5** + **ex-02 §7.3** (the `imported
   procedure actors#alice1(ActorChannel?).` declaration on line 33 of
   `boot.glp` is the §7.3 import side of the §7.5 cross-module call).
3. **Alice's display tee** —
   `tee(AliceActorOut?, AliceMedIn, AliceDispCmd)`.
   `tee/3` is a PRIVATE procedure in `boot.glp` — it splits the actor's
   command stream into two copies, one going to the mediator and one
   captured for display.  Cross-reference: **ex-02 §7.3** (private,
   intra-module).
4. **Alice's agent** —
   `agent # agent(alice, AliceAgentIn?, AliceNetIn?, [output('_user', AliceAgentToUser), output('_net', AliceNetOut)])`.
   `agent # agent` is the §7.5 cross-module call to `agent/4` exported
   from the `agent` sibling module.  The `OutputsList` argument
   (`[output('_user', ...), output('_net', ...)]`) is typed by
   `OutputsList`/`OutputEntry`/`OutputKey` declared in `self.glp` —
   these types are visible to `boot.glp` because both modules share the
   `cssg` ancestor.  Cross-reference: **ex-04 §7.5** + **ex-03 §7.4**.
5. **Alice's mediator** —
   `mediator # ui_mediator(alice, ch(AliceAgentToUser?, AliceAgentIn), ch(AliceMedIn?, AliceMedOut), [], 1)`.
   `mediator # ui_mediator` is the §7.5 cross-module call to
   `ui_mediator/5` exported from `ui/mediator.glp`.  Note this resolves
   to a NESTED-directory module (`ui/`) — the project-loading mode
   (§7.1–§7.2, ex-01) walked the directory tree and registered
   `ui/mediator.glp` as module `mediator` (per the `-module(mediator).`
   directive inside that file).  Cross-reference: **ex-01 §7.1–§7.2** +
   **ex-04 §7.5**.
6. **Alice's mediator-display tee** —
   `tee(AliceMedOut?, AliceActorIn, AliceDispNotify)` — same shape as
   step 3 but for the mediator's notifications.
7. **Alice's display sinks** —
   `sink(AliceDispCmd?), sink(AliceDispNotify?)` absorb the display
   streams so they don't block the mediators.  `sink/1` is private to
   `boot.glp`.  Cross-reference: **ex-02 §7.3**.
8. **Bob's block (lines 129–136)** — repeats steps 2–7 with `bob1` /
   `bob` substituted for `alice1` / `alice`.  Same §7.3 + §7.4 + §7.5
   mechanics.
9. **Charlie's block (lines 138–145)** — repeats steps 2–7 with
   `charlie1` / `charlie` substituted.  Final clause body goal is
   `sink(CharlieDispNotify?)` — closes off `play1`'s body.

Throughout, the SRSW discipline (CLAUDE.md §16) holds: each variable
appears at most once as a reader and at most once as a writer per
clause.  This is why the network channels are allocated inverted
(`ch(AliceNetOut?, AliceNetIn)` — reader of out-stream, writer of
in-stream): the agent and the network see opposite views of the same
shared streams.

## Run the play

```bash
cd D:/bstdev/research/GLP/GLP && printf "%s\n:limit 1000000\nplay1.\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill 2>&1 | head -50
```

Cross-check: `ex-05-repl-trace.md` records the verbatim REPL session.

## Outcome

`play1.` returns `→ suspended`.  Per CLAUDE.md §12, both `→ succeeds`
and `→ suspended` are valid play outcomes:

- **`→ succeeds`** — the goal completes.  All channels are sealed
  (closed with `[]`), all spawned procedures have terminated, and there
  is no remaining work in the scheduler.
- **`→ suspended`** — the goal does not fail, and no fault is raised,
  but channels remain open by design.  This is normal for plays whose
  channels stay open after the actors finish their scripted exchanges
  — there is simply no further input arriving, and the agents +
  mediators are waiting for it.  The play's protocol logic completed
  successfully; the network simply stayed alive.

For `play1`, suspended is the expected outcome: Alice introduces Bob
and Charlie via the cold-call protocol, both Bob and Charlie accept,
the friendship channels are established, but no `text` messages or
disconnect signals are sent on those channels — so they remain open.
The §7.3 cold-call befriending protocol (book §7.3) is exercised
end-to-end in this play; suspended after a successful protocol run
is the same outcome shape that ch04 / ch05 / ch06 saw with their open
channels.

## §7.6 dynamic linking — referenced

§7.6 (book p 60) describes load-time verification + type-automata-as-
runtime-artifacts: when the project loader walks `simple-multimodule/`,
it does not just compile each `.glp` file in isolation — it also
verifies that every `imported procedure` declaration in `boot.glp`
matches an `exported procedure` declaration in the corresponding
sibling module, and that the type-automaton derived from each
module's types is consistent with the assembled ancestor-scoped types
in `self.glp`.  This is dynamic linking: the symbol table is built
incrementally as modules load, and cross-module references are
resolved before any goal can be run.

This exercise demonstrates the OUTCOME of dynamic linking — the
project loads (one `✓ Loaded project:` line), the play runs (no
unresolved-reference errors, no type mismatches across module
boundaries) — without diving into the linker internals.  The book's
§7.6 is descriptive (no executable demo); the cluster A project IS
the executable evidence that the linker did its job.

## Multimodule-project-derivation note

This is the first ch07 exercise that exercises the cluster as a
multimodule whole rather than inspecting individual mechanics.  Per
the `multimodule-project-derivation` cross-chapter relationship
contract (research R-008), cluster A's source canonical is
`programs/cssg_modules/` (the book §7.7 validation example, p 61);
cluster A's `self.glp`, `agent.glp`, `ui/mediator.glp`, and
`ui/actors.glp` are inherited byte-exact from the canonical, with
only `boot.glp` pruned to the 3-agent friend-mediated subset (retains
plays 1–3 + fplays 1–3; removes 4-agent CSSG plays 4–7).  Running
`play1` from cluster A's pruned `boot.glp` gives the same end-to-end
behaviour as running `play1` from the canonical — the pruning removed
plays, not protocol logic.

## Next

Exercise 6 is the Flutter setup walkthrough — the first ch07 exercise
that pairs with a Flutter trace per the FR-011 + FR-020 contract.  It
shows how to launch the cluster A project under the `glp_multiagent`
Flutter app to see the same `play1` behaviour with per-agent UI
windows.  See `ex-06-flutter-trace.md` (sibling artefact) and
`ex-06-tutorial.md`.
