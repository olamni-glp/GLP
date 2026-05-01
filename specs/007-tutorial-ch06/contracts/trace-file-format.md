# Contract — Trace file format (ch06)

**Path**: `olamni/tutorial/ch06/exercise-NN/ex-NN-repl-trace.md` (one per exercise).

**Inherited from ch01–ch05** with no ch06-specific deviations. ch06 has no negative exercises (unlike ch05 ex-06+ex-07) and no per-run-varying segments (unlike ch02 ex-03's `now/1` output), so the standard 5-phase positive trace contract applies to all 5 exercises.

## Structure

Each `ex-NN-repl-trace.md` MUST contain exactly 5 phases:

1. **Phase A — Build / load**: REPL banner + load command for the `.glp` file, ending in `✓ Loaded:` line.
2. **Phase B — Primary demo goal**: the locked primary goal, ending in the locked binding.
3. **Phase C — Inspection goal 1**: the first locked inspection goal + binding.
4. **Phase D — Inspection goal 2**: the second locked inspection goal + binding.
5. **Phase E — Inspection goal 3**: the third locked inspection goal + binding.

Each phase consists of:
- 1–3 sentence learner-targeted preface (outside the code block).
- ONE fenced ` ```glp ` code block containing the verbatim REPL session for this phase.
- 1–2 brief annotation lines (outside the code block).

After Phase E:
- 1–3 sentence learner-targeted postscript referencing the §6.x heading and the synthesis source.

## Byte-equality contract (FR-012)

The fenced code block contents MUST be byte-equal to the actual REPL session output, modulo:
- REPL banner lines (`Built from`, `Built at`, `Repo HEAD`, `Working directory`, `Loaded root self.glp from`) — these vary by build/host and are excluded from byte-equality.
- Build wallclock lines (timestamps embedded by the REPL banner) — excluded.

**No per-run-variation relaxation expected for ch06.** If any wallclock-derived element appears in a phase output (it should not — none of the 5 source Programs use `now/1` or `'_output'/1`), the trace's annotation MUST mark it "varies per run; the SHAPE matters, not the specific number" per the ch02 FR-014 precedent.

## Annotation rules

- Annotation lines outside code blocks describe what the learner is observing. They do NOT modify the verbatim text.
- The synthesis source is referenced in the postscript (e.g., "this `flatten/2` is byte-exact from ch04 §4.3.7, p 38; re-presented here under §6.1 with a typed `procedure` declaration introduced fresh per Q2").

## Reproducibility contract

The implementer MUST be able to re-run the REPL session that produced the trace and observe byte-identical output (per the byte-equality contract above). The reproducibility check is part of /speckit-implement T-equivalent verification.

## Inherited from ch01–ch05

This contract inherits from `specs/006-tutorial-ch05/contracts/trace-file-format.md` (the most recent 5-phase positive contract). ch06 introduces NO new trace-file rules.

## Out of scope for ch06

- Negative exercises (no §6.x heading triggers a load-time failure; all 5 exercises are positive).
- Per-run-variation relaxation (no wallclock-derived output expected).
- Two-`.glp`-file pattern (each ch06 exercise has exactly one `.glp` file).
