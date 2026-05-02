# Exercise 04 — Cluster A §7.5 procedure renaming + entry-point aliases

## What you'll learn

- The five stages of project compilation that turn a directory of `.glp`
  files into a single linked program (book §7.5, p 58-60).
- How stage 3 (procedure renaming) rewrites every defined procedure name
  from `<file>:<proc>/<arity>` into `<module>:<proc>/<arity>` based on
  each file's `-module(M).` directive.
- How stage 5 (entry-point aliases) synthesises clauses like
  `play1 :- boot:play1.` so a top-level REPL goal `play1.` finds the
  renamed `boot:play1/0` procedure.
- Why the two paths — entry-point alias and namespaced call — coexist:
  one for the REPL goal prompt, one for in-clause cross-module calls.

## The five stages of project compilation (§7.5)

Loading a project directory triggers a five-stage pipeline (book §7.5,
p 58-60).  Each stage either succeeds for the whole project or raises an
error before the next stage starts:

1. **Discovery** — walk the project subdir, find every `.glp` file,
   record its `-module(M).` directive (defaulting to filename if the
   directive is absent).  Cluster A's discovery yields five files: the
   ancestor `self.glp` (module `cssg`), the sibling `agent.glp` (module
   `agent`), the sibling `boot.glp` (module `boot`), and the two `ui/`
   files `mediator.glp` (module `mediator`) and `actors.glp` (module
   `actors`).
2. **Type checking** — per-module first (each file's locally-defined
   types + procedures pass type-check using only what is visible
   ancestor-scoped + locally-declared), then cross-module via
   `imported procedure` decls (the type checker uses these decls
   verbatim, never reaching into the other module's source).
3. **Procedure renaming** — every defined procedure gets its name
   rewritten from the parser's tentative `<file>:<proc>/<arity>` form
   into the final `<module>:<proc>/<arity>` form.  See the table below.
4. **Call resolution** — every cross-module call site `M # goal` is
   bound to the renamed `M:goal/N` procedure declared via
   `imported procedure M#goal(...)` in the calling module.
5. **Entry-point aliases** — for each procedure named like a top-level
   demo entry point (in cluster A: `play1`, `play2`, `play3`, `fplay1`,
   `fplay2`, `fplay3`), the project compiler synthesises an alias clause
   `play1 :- boot:play1.` so a top-level REPL goal `play1.` resolves
   without the user having to type the namespace.

## Procedure renaming table (book p 59 §7.5)

Stage 3 transforms each defined procedure name as follows.  The "Original
(file)" column is the parser's tentative form before the `-module(M).`
directive is applied; the "Renamed (module)" column is the final form
that lives in the linked project's procedure table:

| Original (file)                  | -module    | Renamed (module)         |
|----------------------------------|------------|--------------------------|
| `agent.glp:agent/4`              | `agent`    | `agent:agent/4`          |
| `agent.glp:merge/3`              | `agent`    | `agent:merge/3`          |
| `agent.glp:lookup_send/4`        | `agent`    | `agent:lookup_send/4`    |
| `agent.glp:add_output/4`         | `agent`    | `agent:add_output/4`     |
| `agent.glp:close_outputs/1`      | `agent`    | `agent:close_outputs/1`  |
| `boot.glp:play1/0`               | `boot`     | `boot:play1/0`           |
| `boot.glp:play2/0`               | `boot`     | `boot:play2/0`           |
| `boot.glp:play3/0`               | `boot`     | `boot:play3/0`           |
| `boot.glp:fplay1/0`              | `boot`     | `boot:fplay1/0`          |
| `boot.glp:network3/3`            | `boot`     | `boot:network3/3`        |
| `boot.glp:tee/3`                 | `boot`     | `boot:tee/3`             |
| `boot.glp:sink/1`                | `boot`     | `boot:sink/1`            |
| `boot.glp:merge/3`               | `boot`     | `boot:merge/3`           |
| `ui/mediator.glp:ui_mediator/5`  | `mediator` | `mediator:ui_mediator/5` |
| `ui/mediator.glp:lookup_pending/4` | `mediator` | `mediator:lookup_pending/4` |
| `ui/actors.glp:alice1/1`         | `actors`   | `actors:alice1/1`        |
| `ui/actors.glp:bob1/1`           | `actors`   | `actors:bob1/1`          |
| `ui/actors.glp:charlie1/1`       | `actors`   | `actors:charlie1/1`      |

Note `agent:merge/3` (private to module `agent`) and `boot:merge/3`
(local to module `boot`) coexist without collision after renaming —
each module keeps its own `merge/3` because the namespaces are
disjoint.  This is the §7.5 mechanism that makes per-module locality
of names work.

## Entry-point aliases (§7.5 stage 5)

A top-level REPL goal like `play1.` is just an atom — it has no namespace
prefix, so the compiler must connect it to the renamed `boot:play1/0`
clause somewhere.  Stage 5 synthesises an alias clause for every
recognised entry-point procedure in cluster A:

```glp
%% Synthesised by the project compiler (not in source); §7.5 stage 5.
play1  :- boot:play1.
play2  :- boot:play2.
play3  :- boot:play3.
fplay1 :- boot:fplay1.
fplay2 :- boot:fplay2.
fplay3 :- boot:fplay3.
```

When the REPL receives `play1.` at the goal prompt, it finds the alias
`play1 :- boot:play1.`, rewrites the goal to `boot:play1`, and reduces
that against the renamed clause body.  This is why session 1 of the trace
runs `play1.` and gets `→ suspended` (the body started reducing) rather
than "predicate not found".

## Run the demo

Two REPL sessions — one for each path:

Session 1 — top-level alias (`play1.`):

```bash
cd D:/bstdev/research/GLP/GLP && printf "%s\n:limit 1000000\nplay1.\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill
```

Session 2 — fully-qualified namespaced goal (`boot # play1.`):

```bash
cd D:/bstdev/research/GLP/GLP && printf "%s\n:limit 1000000\nboot # play1.\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill
```

See `ex-04-repl-trace.md` for the verbatim output — session 1 succeeds
(`→ suspended`) via the alias; session 2 fails (`→ failed` + syntax error
at column 6) because the REPL's top-level goal grammar does not accept
the `M # G` namespaced form.  This is a design choice: the alias is the
ONLY supported way to invoke a renamed procedure from the goal prompt.

## Cross-module call resolution in `boot.glp`

§7.5 stage 4 connects each `M # goal` call site to the corresponding
renamed `M:goal/N` procedure declared via `imported procedure M#goal(...)`
in the calling module.  Concretely, `boot.glp` declares its imports and
then uses them inside `play1/0`'s body (Formal 7.2 in the book — module
boundary integrity via imported declarations):

```glp
%% From boot.glp lines 26-30:
%% From agent.glp (sibling)
imported procedure agent#agent(Constant?, UserInStream?, NetInStream?, OutputsList?).

%% From ui/mediator.glp
imported procedure mediator#ui_mediator(Constant?, AgentChannel?, UserChannel?, PendingList?, Constant?).
```

```glp
%% From boot.glp lines 33-35:
%% From ui/actors.glp — plays 1-3 (3 agents)
imported procedure actors#alice1(ActorChannel?).
imported procedure actors#bob1(ActorChannel?).
imported procedure actors#charlie1(ActorChannel?).
```

```glp
%% From boot.glp lines 115-125 — the alice block of play1/0:
play1 :-
    network3(ch(AliceNetOut?, AliceNetIn),
             ch(BobNetOut?, BobNetIn),
             ch(CharlieNetOut?, CharlieNetIn)),

    actors # alice1(ch(AliceActorIn?, AliceActorOut)),
    tee(AliceActorOut?, AliceMedIn, AliceDispCmd),
    agent # agent(alice, AliceAgentIn?, AliceNetIn?,
          [output('_user', AliceAgentToUser), output('_net', AliceNetOut)]),
    mediator # ui_mediator(alice, ch(AliceAgentToUser?, AliceAgentIn),
                ch(AliceMedIn?, AliceMedOut), [], 1),
```

Three call sites in this fragment — `actors # alice1(...)`,
`agent # agent(alice, ...)`, and `mediator # ui_mediator(alice, ...)` —
each backed by an `imported procedure` decl above.  Stage 4 rewrites
them at link time to direct calls into `actors:alice1/1`, `agent:agent/4`,
and `mediator:ui_mediator/5` respectively.  Per Formal 7.2, the type
checker uses ONLY the local `imported procedure` decl when type-checking
`boot.glp`; it never reaches into `agent.glp`, `mediator.glp`, or
`actors.glp` to look up the actual implementation's signature.  That is
the module-boundary integrity property: each module is type-checked
against decls, not against other modules' source.

The local calls in this fragment — `network3(...)` and `tee(...)` —
have no `M #` prefix because they resolve to procedures defined in the
same module (`boot:network3/3` and `boot:tee/3`).  Stage 3 renames them
to `boot:network3/3` and `boot:tee/3`; stage 4 binds the call sites
within the same module without consulting any imported decl.

## Multimodule-project-derivation note

`boot.glp` is the ONE derived file in cluster A — it is pruned from
`programs/cssg_modules/boot.glp` to keep only plays 1-3 (the 3-agent
friend-mediated subset per spec Q1+Q5+Q1a).  The other four cluster A
files (`agent.glp`, `self.glp`, `ui/mediator.glp`, `ui/actors.glp`) are
byte-exact from the canonical and inherit Section R's byte-equality
enforcement transitively.  The §7.5 mechanic this exercise inspects is
unchanged across the canonical and the pruned tutorial copy: the same
five stages, the same renaming, the same alias synthesis — only the
specific procedures present (plays 1-3 versus 1-7) differ.

## Next

[`exercise-05/`](../exercise-05/ex-05-tutorial.md) — end-to-end `play1.`
run + §7.6 dynamic linking referenced.  ex-05 will run the same alias
path you saw in session 1 here, but as the cluster A integration test:
all four §7.x mechanics (§7.3 exported/private/imported decls from ex-02,
§7.4 ancestor-scoping from ex-03, §7.5 renaming + aliases from this
ex-04, and §7.7 multi-module call composition) firing together inside
one play body.
