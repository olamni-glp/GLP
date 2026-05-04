# Contract — Trace file format (ch07)

**Path**: `olamni/tutorial/ch07/exercise-NN/ex-NN-repl-trace.md` (one per REPL exercise: NN ∈ {01..05, 07..11}, 10 total).

**Inherited from ch01–ch06** with two ch07-specific additions:
1. The "primary action" structure differs from chs 1–6 — for cluster A's REPL exercises, the load IS the primary trace anchor (project-loading mode emits per-module load lines + entry-point alias generation per §7.5); for cluster B's REPL exercises, a play sequence IS the primary trace anchor (each play runs to completion or `→ suspended`).
2. Negative exercises do NOT exist for ch07 (all REPL exercises are positive; no §7.x mechanic triggers a load-time failure).

## Structure (REPL traces)

Each `ex-NN-repl-trace.md` MUST contain at minimum:

1. **Phase A — Build / load**: REPL banner + project-load command (cluster A: load `simple-multimodule/` directory; cluster B: load `cssg-modules/` directory), ending in either:
   - per-module `✓ Loaded:` lines for each `.glp` in the project + a project-completion summary, OR
   - the equivalent project-loading-mode log lines per the REPL's actual output for project loads.
2. **Phase B — Primary action**: the locked primary demo for this exercise.
   - For cluster A ex-01 (project-load demo): no goal beyond the load; Phase A and Phase B may merge.
   - For cluster A ex-02..ex-04 (mechanic inspection): the locked inspection goal sequence.
   - For cluster A ex-05 (end-to-end): `play1.` (locked).
   - For cluster B ex-07 (project-load demo): like cluster A ex-01 but with cluster B's larger project.
   - For cluster B ex-08..ex-10 (play sequences): the locked play subset, run in sequence (e.g., `play1. play2. play3.` for ex-08).
   - For cluster B ex-11 (cross-module-call inspection): the locked inspection goal sequence.
3. **Phase C..E — Inspection actions** (0–3 phases): inspection goals beyond the primary, locked at /speckit-implement per R-004.

Each phase consists of:
- 1–3 sentence learner-targeted preface (outside the code block).
- ONE fenced ` ```glp ` code block containing the verbatim REPL session for this phase.
- 1–2 brief annotation lines (outside the code block).

After the last phase:
- 1–3 sentence learner-targeted postscript referencing the §7.x mechanic (cluster A) or §7.7 use case (cluster B), the cluster's source canonical (`programs/cssg_modules/<file>`), and (for ex-05 + ex-08..ex-11) which prior exercises' mechanics were exercised in this trace.

## Phase count per exercise

Phase count varies by exercise. Inherited from ch02's "phase count varies" precedent. Locked at /speckit-implement T-equivalent per exercise. Expected:

| Exercise | Cluster | Phase count | Notes |
|---|---|---|---|
| ex-01 | A | 1–2 | Project load demo; Phase A may include `:listing` if used. |
| ex-02 | A | 2–4 | Decl-kind inspection; up to 3 inspection goals per R-004. |
| ex-03 | A | 2–4 | Ancestor-scoping inspection. |
| ex-04 | A | 2–4 | Procedure-renaming inspection. |
| ex-05 | A | 2 | Project load + `play1.` end-to-end. |
| ex-07 | B | 1–2 | Project load demo for cluster B. |
| ex-08 | B | 4 | Project load + `play1. play2. play3.` (3 cold-call plays). |
| ex-09 | B | 3 | Project load + `play4. play5.` (CSSG accept + reject per Q4a). |
| ex-10 | B | 3 | Project load + `play6. play7.` (parent-mediated child intro variants per Q4a). |
| ex-11 | B | 2–4 | Project load + cross-module-call inspection goals. |

## Byte-equality contract (FR-012)

The fenced code block contents MUST be byte-equal to the actual REPL session output, modulo:
- REPL banner lines (`Built from`, `Built at`, `Repo HEAD`, `Working directory`, `Loaded root self.glp from`) — these vary by build/host and are excluded from byte-equality.
- Build wallclock lines (timestamps embedded by the REPL banner) — excluded.
- Project-load mode timestamp/duration lines (if present) — excluded; the per-module `✓ Loaded:` lines themselves are byte-equal.

**Per-run-variation**: ch07 source code does NOT use `now/1` or `'_output'/1` directly in cluster A (cluster A's `boot.glp` keeps `send_to_user_tagged` which calls `'_output'/1`, but cluster A's REPL exercises ex-01..ex-05 do NOT run `fplay1` etc.; they run `play1` which uses `sink/1` instead). Cluster B's REPL exercises also default to non-fplay variants (per locked play assignments). If any wallclock-derived element appears in a phase output, the trace's annotation MUST mark it "varies per run; the SHAPE matters, not the specific number" per the ch02 FR-014 precedent.

**Variable numbering** (ch06 ex-04 precedent): GLP variable numbers (e.g., `X12`, `X14`) ARE deterministic per fresh REPL invocation in the byte-exact sense. The trace records the literal variable numbers from the implementer's REPL run; if a re-run produces different numbers, that signals a REPL implementation change (halt per FR-013).

## Annotation rules

- Annotation lines outside code blocks describe what the learner is observing. They do NOT modify the verbatim text.
- The cluster's source canonical reference is in the postscript (e.g., "the `agent.glp` you saw load is byte-exact from `programs/cssg_modules/agent.glp`; per §7.3 it declares `agent/4` exported and `merge/3` private").
- For cluster A traces, the annotation MAY reference the canonical's existing per-clause `%%` paraphrase comments (the tutorial copy inherits them unchanged).

## Reproducibility contract

The implementer MUST be able to re-run the REPL session that produced the trace and observe byte-identical output (per the byte-equality contract above). The reproducibility check is part of /speckit-implement T-equivalent verification.

## Inherited from ch01–ch06

This contract inherits from `specs/007-tutorial-ch06/contracts/trace-file-format.md`. ch07 introduces project-load primary actions + play-sequence primary actions; the underlying byte-equality + annotation rules are unchanged.

## Out of scope for ch07 REPL traces

- Negative exercises (no §7.x mechanic triggers a load-time failure).
- Two-`.glp`-file pattern within an exercise dir (ch07 exercises do NOT have `.glp` files; the cluster project subdir is shared).
- Per-run-variation relaxation (no wallclock-derived output expected — see Per-run-variation note above).

## See also

- `flutter-trace-format.md` — separate contract for the two Flutter exercises (ex-06 + ex-12).
- `status-block-format.md` — gate-grep contract for cluster-internal pairwise gates + the cluster-boundary gate.
