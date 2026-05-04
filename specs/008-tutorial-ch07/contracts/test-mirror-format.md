# Contract — Test mirror format (ch07, NEW)

**Path**: a new section appended to `test/run_all_tests.sh`.

**Section letter**: **R** (next available after Section Q AOT smoke per R-007 + Q-amendment Q-FR014a). The spec's original FR-014 wording said "Section S" — corrected to **R** because Section R does not currently exist (the workflow-memory note about a stale-binary Section R never landed).

**NEW for ch07**. ch01–ch06 are not in `test/run_all_tests.sh` per the CLAUDE.md §11 tutorial-chapter exception. ch07 is the first chapter to override that exception per spec FR-014 + Assumptions.

## Section R structure

Section R has two sub-blocks:

### R-1: Cluster A simple-multimodule load + play tests (4 cases)

Loads `olamni/tutorial/ch07/simple-multimodule/` via REPL project-loading mode + runs each of plays 1, 2, 3 + verifies the load itself succeeded.

```bash
echo "=== Section R: ch07 cluster projects ==="
echo ""

echo "--- R-1: cluster A simple-multimodule ---"

echo "  R-1.1 load simple-multimodule project ---"
output=$($DART run "$REPL" <<HEREDOC
$GLP_DIR/olamni/tutorial/ch07/simple-multimodule
:quit
HEREDOC
2>&1)
check "cluster A loads via project mode" "Loaded:" "$output"

for play in play1 play2 play3; do
  output=$($DART run "$REPL" <<HEREDOC
$GLP_DIR/olamni/tutorial/ch07/simple-multimodule
$play.
:quit
HEREDOC
  2>&1)
  check "cluster A $play runs" "→ succeeds\|→ suspended" "$output"
done
```

Total cases in R-1: **4** (1 project load + 3 play runs).

### R-2: Cluster B byte-equivalence diff tests (6 cases)

Verifies each file in `olamni/tutorial/ch07/cssg-modules/` is byte-equal to its canonical counterpart in `programs/cssg_modules/`. The diff EXCLUDES the new ch07 header block (the test compares only the canonical-source byte range).

```bash
echo "--- R-2: cluster B byte-equivalence to canonical ---"

CSSG_MODULES_FILES="self.glp agent.glp ui/mediator.glp ui/actors.glp boot.glp mad_boot.glp"

for f in $CSSG_MODULES_FILES; do
  CANONICAL="$GLP_DIR/programs/cssg_modules/$f"
  TUTORIAL="$GLP_DIR/olamni/tutorial/ch07/cssg-modules/$f"

  # Strip the leading ch07 header block (lines starting with "%% ch07" through the first non-comment-or-blank-or-non-ch07-comment line).
  # Per glp-file-format.md the header is N consecutive %% lines at the top; we strip exactly the lines starting with "%% ch07" or directly preceded by such.
  # Simplest heuristic: drop the first M lines where M = count of lines from start until the first line that does NOT start with "%%".

  HEADER_LINES=$(awk '/^%%/{c++; next} {print c; exit}' "$TUTORIAL")

  if diff <(tail -n +$((HEADER_LINES + 1)) "$TUTORIAL") "$CANONICAL" > /dev/null 2>&1; then
    check "byte-equivalent: $f" "ok" "ok"
  else
    DIFF_OUT=$(diff <(tail -n +$((HEADER_LINES + 1)) "$TUTORIAL") "$CANONICAL" | head -10)
    check "byte-equivalent: $f" "ok" "DRIFT: $DIFF_OUT"
  fi
done
```

Total cases in R-2: **6** (one per file in `cssg_modules/` plus its `ui/` subdir; per R-002 the actual file count is 6 not 7).

### Section R total: **10** test cases

Pre-ch07 baseline: **485** (per ch06 ship state commit `be473849`).
Post-ch07 expected total: **495** (485 + 10).

## Pre-condition checks

Before Section R runs, the script MUST have:
- `$DART` set (auto-detected via `which dart`).
- `$REPL` pointing to either `glp_runtime/glp_repl.exe` (AOT) or `glp_runtime/.dart_tool/repl.dill` (kernel).
- `$GLP_DIR` set to the GLP project root (absolute path).

These are inherited from earlier sections in the script; Section R does not need to re-establish them.

## Test framework conventions

Per the existing script's conventions:
- Each test uses the `check` helper: `check "<test name>" "<expected pattern>" "<actual output>"`.
- `check` is greppy — the expected pattern is matched against the actual output via `grep -E`.
- `check` increments either `$PASS` or `$FAIL`.
- Section-level pass/fail counts are derived from these increments.

Per CLAUDE.md §11 the test script's structure is:
- Headers introduce sections (`echo "=== Section X: ... ==="`).
- Sub-section breaks use `echo "--- ... ---"`.
- Each test has a 1-line description echo + the actual test invocation.

## What Section R does NOT cover

Per the principle of single-source-of-truth + non-duplication of test coverage:
- Section R does NOT re-test cluster B's `programs/cssg_modules/` end-to-end behaviour. That is Section F's job (existing). Cluster B's tutorial copy is byte-equivalent (R-2), so any behaviour mismatch would surface as a Section F failure on the canonical, not as a Section R failure on the tutorial copy.
- Section R does NOT test the Flutter pairings (`main_olamni_ch07_*.dart`). Flutter testing is manual per FR-017 + the flutter-trace-format contract.
- Section R does NOT verify the cluster A `boot.glp` pruning was correct in detail (e.g., it does NOT enumerate which specific lines are missing from canonical). It only verifies the pruned `boot.glp` is loadable + runnable for plays 1–3.

## Drift handling

If R-2 fails (a cluster B file has drifted from canonical):
1. The implementer halts per FR-013.
2. Identifies which copy is the source of truth: `programs/cssg_modules/<file>` is canonical (per FR-019).
3. Re-syncs the tutorial copy at `olamni/tutorial/ch07/cssg-modules/<file>` from canonical (preserving the ch07 header block).
4. Re-runs Section R.
5. If drift originated FROM the tutorial copy (e.g., an inadvertent edit), the canonical wins.
6. If drift originated FROM canonical (e.g., a recent commit to `programs/cssg_modules/`), the implementer halts and asks the project owner whether the canonical change should propagate to ch07's tutorial copy (likely yes, but the propagation is an explicit step, not silent).

## Inherited from ch01–ch06

This contract is **NEW for ch07** — no inheritance from ch01–ch06 (those chapters' tutorial files are NOT in `test/run_all_tests.sh` per CLAUDE.md §11). ch07 is the explicit first override of that exception per FR-014 + Assumptions.

The script-internal conventions (`check` helper, `$DART`, `$REPL`, `$GLP_DIR`, `echo` formatting) inherit from the existing script (last modified for Section Q AOT smoke).

## See also

- `trace-file-format.md` — contract for the 10 REPL exercises' traces.
- `flutter-trace-format.md` — contract for the 2 Flutter exercises' traces (ex-06, ex-12).
- `glp-file-format.md` — header-block contract for cluster project files (the headers Section R-2 strips before diffing).
- `status-block-format.md` — gate-grep contract for cluster-internal pairwise gates + the cluster-boundary gate.
