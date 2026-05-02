# Exercise 02 — Cluster A §7.3 procedure declarations

Welcome to chapter 7, exercise 2. This exercise inspects the **three
kinds of procedure declarations** that §7.3 introduces: **private**
(plain `procedure`), **exported** (`exported procedure`), and **imported**
(`imported procedure`). Cluster A's `agent.glp` is the §7.3 worked
example — it declares one EXPORTED procedure (`agent/4`) and several
PRIVATE helpers (`merge/3`, `lookup_send/4`, …); cluster A's `boot.glp`
is the consumer side that declares an IMPORTED reference and uses it.

## What you'll learn

- The three procedure-declaration kinds defined in §7.3 — what each
  keyword means for visibility and cross-module-call permission.
- Why `merge/3` is **private** to `agent.glp` — it is an internal
  helper for `agent/4`'s state-machine clauses; encapsulating it
  prevents external modules from depending on what is essentially an
  implementation detail.
- Why `agent/4` is **exported** — it is the public API of the agent
  module; `boot.glp` and any future consumer wires its three streams
  (`UserIn`, `NetIn`, `Outs`) into `network3/3` and `ui_mediator/5`.
- How **imported procedure** declarations enable **separate
  type-checking** — the type checker reads `boot.glp`'s
  `imported procedure agent#agent/4` decl locally, **without ever
  opening `agent.glp`'s source**; per Formal 7.2 the project loader
  later reconciles the imported declaration against `agent.glp`'s
  exported declaration when both modules are in the same project.

## The three procedure-declaration kinds (book §7.3, p 56)

| Kind | Syntax | Scope | Use case |
|---|---|---|---|
| Private | `procedure name(Type1?, Type2, ...).` | Clause bodies in this module only. | Internal helpers — list manipulation, message routing, anything other modules should not depend on. |
| Exported | `exported procedure name(Type1?, Type2, ...).` | Clause bodies in this module + any sibling module that declares an `imported procedure module#name(...)`. | Public API — the module's stable, intended-for-external-use entry points. |
| Imported | `imported procedure module#name(Type1?, Type2, ...).` | Clause bodies in this consumer module may call `module # name(...)`. | Cross-module dependency — declares "I will call `module#name/N` and here is the type signature I expect"; the project loader checks this matches the source module's `exported` declaration at load time. |

The fundamental property §7.3 establishes is that **type-checking is
separate per module**: when the checker processes `boot.glp`, it
reads `boot.glp`'s `imported procedure agent#agent/4` declaration to
type-check uses of `agent # agent(...)` — **without** reading
`agent.glp`'s source. The type checker only needs the imported
declaration to do its job. The actual reconciliation (does
`agent.glp` actually export `agent/4` with this exact signature?)
happens at **project load time** per Formal 7.2 (cross-module
well-typing).

## Cluster A's `agent.glp` declarations

`agent.glp` declares one exported procedure plus several private
helpers. The relevant lines (byte-exact from
`programs/cssg_modules/agent.glp`):

```prolog
%% Line 20 — PRIVATE merge: stream-merging helper for handle_response
procedure merge(Stream(X)?, Stream(X)?, Stream(X)).
merge([X|Xs], Ys, [X?|Zs?]) :- merge(Ys?, Xs?, Zs).
merge(Xs, [Y|Ys], [Y?|Zs?]) :- merge(Xs?, Ys?, Zs).
merge([], Ys, Ys?).
merge(Xs, [], Xs?).

%% Line 30 — PRIVATE lookup_send: routing helper for output-key lookups
procedure lookup_send(OutputKey?, OutputMsg?, OutputsList?, OutputsList).
lookup_send(Key, Msg, Outs, Outs1?) :-
    ground(Key?) |
    lookup_send_step(Key?, Msg?, Outs?, Outs1).

%% Line 113 — EXPORTED agent: the public API
exported procedure agent(Constant?, UserInStream?, NetInStream?, OutputsList?).
```

`merge/3` and `lookup_send/4` are PRIVATE — they have no `exported`
keyword. They are used internally by `agent/4`'s state-machine
clauses (e.g. `merge` is called inside the `handle_response` clause at
line 104; `lookup_send` is called from many `agent/4` clauses for
output-stream routing). External modules cannot import them.

`agent/4` is EXPORTED — the `exported procedure` keyword opens this
procedure to consumers. The signature `(Constant?, UserInStream?,
NetInStream?, OutputsList?)` is the public contract.

## Cluster A's `boot.glp` imports

`boot.glp` declares its consumer-side dependency on `agent#agent/4`
(byte-exact from cluster A's pruned `boot.glp`, around line 27):

```prolog
%% From agent.glp (sibling)
imported procedure agent#agent(Constant?, UserInStream?, NetInStream?, OutputsList?).
```

The signature exactly matches `agent.glp`'s exported declaration. The
type checker uses ONLY this imported declaration when verifying the
six places where `boot.glp`'s `play1`/`play2`/`play3` (and
`fplay1`/`fplay2`/`fplay3`) call `agent # agent(...)`. No access to
`agent.glp`'s source is required for type-checking `boot.glp`.

## Run the cross-module call (exported, succeeds)

```bash
cd D:/bstdev/research/GLP/GLP && printf "%s\n:limit 1000000\nplay1.\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill 2>&1
```

Expected: `✓ Loaded project: ...simple-multimodule` followed by
`→ suspended` for `play1`. The `→ suspended` is the normal terminal
state for these multi-process plays (the agent loops never close
their input streams). Cross-check: trace **Phase A + Phase B**.

This succeeds because `agent#agent/4` is the EXPORTED entry point of
the agent module and `boot.glp`'s `imported procedure` declaration
matches its signature.

## Try the private call (probes the PRIVATE boundary)

```bash
cd D:/bstdev/research/GLP/GLP && printf "%s\n:limit 1000000\nagent # merge([1,2], [3,4], X).\n:quit\n" "$(pwd -W)/olamni/tutorial/ch07/simple-multimodule" | "/c/Users/gavri/dart-sdk/bin/dart" run glp_runtime/.dart_tool/repl.dill 2>&1
```

Expected (and CAPTURED VERBATIM in trace **Phase C**):
`→ failed` followed by `Error: [syntax] Expected "." at end of clause at
Line 1, Column 7`.

**Read the trace's Phase C annotation carefully**: this is a syntax
error from the REPL goal parser, NOT a privacy-violation error. The
REPL's interactive goal prompt does not support `module#proc(...)`
syntax — it rejects the `#` character on parsing. The same error
appears for `agent#agent(...)` at the goal prompt; the rejection is
universal across `module#proc` goals, regardless of whether the
target is private or exported.

So where IS the privacy boundary enforced? **At clause-body
cross-module-call resolution time during project load** (Formal 7.2):
if `boot.glp` had `imported procedure agent#merge/3.` plus a clause
body calling `agent # merge(...)`, the project loader would reject
the load because `agent.glp` declares `merge/3` PRIVATE (no
`exported` keyword). The successful `play1` proves the EXPORTED
side; the absence of any working REPL goal that reaches `agent#merge/3`
proves the syntactic gate is set; the conceptual mismatch detection at
project load is what enforces privacy.

## Multimodule-project-derivation note

Cluster A's `agent.glp` is **byte-exact** from
`programs/cssg_modules/agent.glp` per spec amendment Q1a — including
the `merge/3`/`lookup_send/4` private decls and the
`exported procedure agent/4` at line 113. Cluster A's `boot.glp` is
the ONLY DERIVED cluster-A file (per R-010 pruning content); the
`imported procedure agent#agent/4` declaration is retained from
canonical because it is needed for the 3-agent plays kept in cluster
A. Section R of `test/run_all_tests.sh` enforces byte-equivalence to
canonical for cluster B's files and (transitively) for cluster A's
four byte-exact files.

## Next

Exercise 3 is §7.4 — ancestor-scoping of types. It inspects how
`self.glp`'s type definitions (`Stream`, `Constant`, etc.) are visible
to every module in the cluster A project without any per-module type
import or re-declaration. Cross-check the module-system invariants
exercised here against the type-system invariants exercised next:
together they realise the §7.x module abstraction.
