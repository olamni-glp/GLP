# ch07 ex-02 — Cluster A §7.3 procedure declarations — REPL trace

This trace captures two verbatim REPL sessions for ex-02. Session 1 (Phase
A + Phase B) loads cluster A's `simple-multimodule/` project and runs
`play1`, exercising the cross-module path that resolves to `agent`'s
EXPORTED `agent/4`. Session 2 (Phase A repeat + Phase C) attempts a
direct REPL-goal-prompt call to `agent#merge/3` to probe the PRIVATE
procedure boundary; the actual REPL behaviour is documented and annotated
below — it differs from "predicate not found" in an instructive way.

## Phase A — Build / load (Session 1)

The project-loading mode emits a single `✓ Loaded project:` line for the
cluster A directory; the per-module `✓ Loaded:` lines are absorbed into
the project-load summary. Compare: the trace contract notes "the
equivalent project-loading-mode log lines per the REPL's actual output
for project loads" (`contracts/trace-file-format.md` Phase A bullet 1).

```glp
GLP> ✓ Loaded project: D:/bstdev/research/GLP/GLP/olamni/tutorial/ch07/simple-multimodule
GLP> Goal reduction limit set to 1000000
```

The 5-module cluster A project (`self.glp`, `agent.glp`, `ui/mediator.glp`,
`ui/actors.glp`, `boot.glp`) has loaded successfully — meaning SRSW + PE +
type checking + compilation all passed for every module, AND every
`imported procedure` declaration in `boot.glp` (including
`imported procedure agent#agent/4`) has been resolved against the
EXPORTED procedures of the named sibling modules. Per **Formal 7.2**
(book p 56, cross-module well-typing), this resolution is what licenses
`boot.glp` to call `agent # agent(alice, ...)` in `play1`.

## Phase B — Cross-module call to EXPORTED `agent#agent/4` via play1

`boot.glp`'s `play1` body wires three personal agents (alice, bob,
charlie) through `network3/3` and three `ui_mediator/5` instances; each
of the three agents is invoked as `agent # agent(Id, ...)`. This goal
exercises the EXPORTED + IMPORTED resolution mechanism end-to-end.

```glp
GLP> → suspended
```

**Annotation**: `→ suspended` is the expected outcome for `play1` — the
three agent loops, three mediator loops, and the `network3/3` switch all
remain reading their input streams indefinitely (each is a long-running
process), so the goal is never `→ succeeds` but never fails either.
This is the same "→ suspended" behaviour seen for ch04's bonds plays
(see CLAUDE.md §12 "Expected results"). What this proves: the call
`agent # agent(alice, AliceAgentIn?, AliceNetIn?, [...])` reached
`agent.glp`'s `exported procedure agent/4`, the type checker accepted
the imported declaration in `boot.glp`, the project loader resolved the
cross-module reference, and the bytecode compiled and dispatched to
`agent`'s clause set. The §7.3 EXPORTED-IMPORTED protocol is working.

## Phase C — Cross-module call to PRIVATE `agent#merge/3` (REPL goal prompt)

After loading cluster A (Phase A repeated; output identical to above), I
attempted `agent # merge([1,2], [3,4], X).` at the REPL goal prompt to
probe whether `agent`'s PRIVATE `merge/3` is callable from outside its
home module.

```glp
GLP> → failed
Error: [syntax] Expected "." at end of clause at Line 1, Column 7
```

**Annotation — actual behaviour, captured verbatim, NOT synthesised**:
the REPL's goal-prompt parser rejects the `module # proc(...)` syntax
with a syntax error at column 7 (the `#` character). Column 7 confirms
the parser had successfully consumed `agent ` (6 chars) and then choked
on the `#`. The same syntax error appears for `agent#merge(...)` at
column 6 (`#` immediately after `agent`) — i.e. the rejection is
syntactic, NOT a privacy/visibility check.

**What this means for the §7.3 mechanism**: the REPL's interactive goal
parser does NOT support cross-module call notation at the prompt level —
this is a property of the REPL goal parser, not of the privacy checker.
The PRIVATE/EXPORTED distinction is enforced **at clause-body
cross-module-call resolution time** when a `.glp` source file is loaded
as part of a project. Specifically:

- An `imported procedure agent#merge/3` declaration in `boot.glp`, plus
  a clause body call `agent # merge(...)`, would be **rejected** at
  project load time, because `agent.glp` declares
  `procedure merge/3` (no `exported` keyword) and Formal 7.2 requires
  the imported name to match an EXPORTED procedure of the source
  module.
- `agent.glp`'s OWN clause bodies call `merge/3` freely (e.g. line 104
  in the `handle_response` clause — `merge(In?, FIn?, In1)`) because
  within a module's home, all procedures (private + exported) are
  visible.
- `boot.glp` ALSO declares its own `procedure merge/3` (lines 67–71 of
  cluster A's `boot.glp`); this is a SEPARATE merge that is local to
  `boot.glp` and unrelated to `agent#merge/3`.

**Comparison call**: a direct `agent#agent(...)` at the REPL prompt
fails with the *same* syntax error at column 6 — confirming the parser
issue is universal across `module#proc` goals, not visibility-specific.
So the privacy boundary is not directly observable from the REPL goal
prompt; it is enforced inside the project loader during clause-body
cross-module-call resolution. The successful `play1` in Phase B (which
calls `agent#agent` from inside a `.glp` clause body) is the positive
proof that exported resolution works; the corresponding negative test
(introducing an imported declaration for `agent#merge/3` in a `.glp`
file and attempting to load) is out of scope for this exercise's REPL
trace and is described conceptually in `ex-02-tutorial.md`.

---

This trace's `agent.glp` is byte-exact from `programs/cssg_modules/agent.glp`
(per spec amendment Q1a); `boot.glp` is the only cluster-A file derived
from canonical (per R-010 pruning content). Per book §7.3 (book p 56),
`agent/4` is the only EXPORTED procedure (`exported procedure agent/4`
at line 113 of agent.glp); `merge/3` and `lookup_send/4` are private
(plain `procedure` keyword at lines 20 and 30). Per Formal 7.2, the
project loader's cross-module-call check rejects any clause-body call
to a non-exported procedure of a sibling module.
