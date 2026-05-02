# ex-04 — REPL trace (cluster A §7.5 procedure renaming + entry-point aliases)

This trace captures two REPL sessions exercising §7.5 of the book (p 58-60).
Stage 3 of project compilation rewrites every defined procedure name from
`<file>:<proc>/<arity>` into `<module>:<proc>/<arity>` using the
`-module(M).` directive at the top of each file, and stage 5 synthesises
entry-point aliases like `play1 :- boot:play1.` so a top-level `play1.`
goal at the REPL resolves to the renamed `boot:play1/0` clause.  Session 1
runs the unqualified `play1.`; session 2 attempts the fully-qualified
`boot # play1.` form to see how the REPL parser handles namespaced goals
at top level.

## Phase A — Project load

Both sessions load the same cluster A project via project-loading mode
(per §7.2).  Discovery + type checking + procedure renaming + call
resolution + entry-point aliasing all complete inside the single
`✓ Loaded project:` line — this is the success signal that all five
stages of §7.5 finished without error.

## Phase B — Session 1: top-level `play1.` (entry-point alias path)

The implementer runs `play1.` unqualified.  The REPL goal parser sees the
bare atom `play1`, looks it up against the loaded project's entry-point
alias table, finds `play1 :- boot:play1.`, and rewrites the goal to the
renamed `boot:play1/0` clause.  That clause is the same body the file
`boot.glp` declares at line 115; it spawns three actor/agent/mediator
triples and a `network3` switch, and because those streams have no
terminator the play reduces to `→ suspended` (normal — the play has no
finite end-of-input).

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

The byte-exact element is the trio of REPL response lines —
`✓ Loaded project: …` (project-load mode), `Goal reduction limit set to
1000000` (the `:limit 1000000` ack), and `→ suspended` (the alias-rewritten
`boot:play1/0` outcome).  `→ suspended` is the §7.5 success signal here:
the alias resolved, the renamed clause was found, the body started
reducing, and the network/actor streams suspended waiting for further
input (which never arrives — the play has no `end_of_play/0` injector).
The REPL banner block and `Goodbye!` line are exempt from byte-equality
per `contracts/trace-file-format.md` §Byte-equality.

## Phase C — Session 2: fully-qualified `boot # play1.` (namespaced goal)

The implementer attempts the namespaced form directly.  The REPL goal
parser does NOT accept `boot # play1.` as a top-level goal — it raises a
syntax error at column 6 (the position of the `#` separator).  The
top-level REPL grammar treats `#` as the cross-module call operator only
inside clause bodies, not as a top-level goal-prefix operator.  This
means: in the current REPL, the entry-point alias path (Phase B) is the
ONLY way to invoke a renamed procedure from the REPL; you cannot bypass
the alias and call `boot:play1` directly from the goal prompt.

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
GLP> → failed
Error: [syntax] Expected "." at end of clause at Line 1, Column 6

GLP> Goodbye!
```

The byte-exact elements are `✓ Loaded project: …`, `Goal reduction limit
set to 1000000`, the `→ failed` outcome line, and the syntax error
`Error: [syntax] Expected "." at end of clause at Line 1, Column 6`.
Column 6 is the `#` character (the goal text is `boot # play1.`; positions
1-4 are `boot`, position 5 is the space, position 6 is `#`).  The parser
expects a `.` (clause terminator) right after the head atom and rejects
`#` as not part of the top-level goal grammar.

The takeaway for §7.5: cross-module qualification syntax (`M # G`) is a
clause-body call site form (see `boot.glp` clauses calling
`agent # agent(...)`, `mediator # ui_mediator(...)`, `actors # alice1(...)`);
top-level REPL goals must use the entry-point alias (`play1.`) rather
than the namespaced form.

---

This trace exercises §7.5 stage 3 (procedure renaming — `boot.glp:play1/0`
→ `boot:play1/0`) and stage 5 (entry-point aliases — `play1 :-
boot:play1.`) of the project compilation pipeline.  Cluster A's source
canonical is `programs/cssg_modules/`; this exercise's `boot.glp` is the
ONLY derived file in cluster A (pruned per spec Q1+Q5+Q1a to the
3-agent/play1-3 subset), and it inherits its `agent.glp`, `self.glp`,
`ui/mediator.glp`, and `ui/actors.glp` BYTE-EXACT from the canonical.
ex-02 inspected the §7.3 exported/private/imported procedure decls; ex-03
inspected §7.4 ancestor-scoping; this ex-04 inspects the §7.5 renaming +
entry-point alias mechanic — the bridge between §7.3 (where the names
live in source) and §7.7 (where the renamed names appear in cross-module
call sites).  ex-05 will run the same `play1.` alias-rewritten goal end
to end as the cluster A integration check.
