# Contract — Flutter trace file format (ch07, NEW)

**Path**: `olamni/tutorial/ch07/exercise-NN/ex-NN-flutter-trace.md` (one per Flutter exercise: NN ∈ {06, 12}, 2 total).

**NEW for ch07**. ch01–ch06 are REPL-only per charter §1; ch07 is the first chapter introducing Flutter pairings per charter §2.2.

## Structure

Each `ex-NN-flutter-trace.md` MUST contain at minimum:

1. **Phase A — Pre-flight verification**: `flutter --version` output (or its Windows equivalent); `flutter doctor` summary if relevant; verification that `glp_multiagent/` builds.
2. **Phase B — Build**: `flutter build <platform>` invocation + the build's success log (modulo wallclock).
3. **Phase C — Launch**: the launch command + the immediate window-open / log-file-creation observations.
4. **Phase D — Per-play observation**: for each play in the locked play subset, a sub-section showing:
   - The play-trigger action (button click / launch goal / etc.).
   - The expected on-screen UI states (per agent panel).
   - The platform log file's relevant lines (`/private/tmp/glp_multiagent_trace.log` on macOS or platform-equivalent).
5. **Phase E — Recommended clean session block** (ex-06 only — per FR-005 (b)): the `pkill` + `flutter clean` + `flutter pub get` + `flutter build` block + verification that the rebuild produces a fresh log matching the captured trace's expected sequence.

For ex-06 (cluster A — Flutter setup walkthrough): Phase D covers all three plays (play1 / play2 / play3 per Q5).

For ex-12 (cluster B — CSSG plays in Flutter): Phase D covers the locked 5-play subset per Q4a (play1 cold-call / play2 cold-call asymmetric / play3 cold-call reject / play4 CSSG accept / play5 CSSG Bob-rejects). Per FR-009 + spec US4 acceptance scenario 2 the panels show Parent / Child split.

Each phase consists of:
- 1–3 sentence learner-targeted preface (outside the code block).
- ONE OR MORE fenced code blocks (` ```bash ` for terminal commands; ` ```text ` for log file extracts; ` ```glp ` if any GLP-form output is shown).
- 1–2 brief annotation lines (outside the code blocks).

After Phase E (or Phase D for ex-12):
- 1–3 sentence learner-targeted postscript referencing the §7.x mechanic / §7.7 use case demonstrated, the cluster project the Flutter app loads, and the Flutter Pairing source file (`main_olamni_ch07_<cluster>.dart`).

## Byte-equality contract (FR-012)

The fenced code block contents MUST be byte-equal to the actual session, modulo:
- Build wallclock lines + Flutter build progress percentages (`Compiling X% ...`) — excluded; the success/failure line + the resulting binary path ARE byte-equal.
- Terminal banner / shell-prompt lines — excluded; the command + the command's output ARE byte-equal.
- Platform-specific paths in the log file (e.g., `/private/tmp/...` on macOS vs the platform-equivalent on other OSes) — annotated as varies-by-platform; the log line CONTENT after the path prefix is byte-equal.
- Per-run-varying log timestamps + isolate IDs + GLP variable numbers — annotated as "varies per run; the SHAPE matters" per the ch02 FR-014 precedent.

## Manual-test-first requirement (FR-017)

Per spec FR-017, the implementer MUST manually test the Flutter app + capture the trace BEFORE writing the tutorial.md. NO synthesised traces. If the Flutter app fails to launch or behave as expected, halt per FR-013 and report.

## Platform notes

The trace MUST be captured on the implementing host's primary platform. Per CLAUDE.md §2 the Windows host's primary platform is Windows 11. The captured trace SHOULD record:
- The platform under which it was generated (e.g., "Captured on Windows 11 with Flutter <version>; macOS / Linux paths annotated where they differ").
- The platform-specific log file path (Windows: `%TEMP%\glp_multiagent_trace.log` or platform-equivalent; macOS: `/private/tmp/glp_multiagent_trace.log`; Linux: `/tmp/glp_multiagent_trace.log`).

If multiple platforms are tested, the trace MAY include platform-comparison sub-sections (NOT required for ch07; the implementing host's single-platform trace suffices).

## Reproducibility contract

The implementer MUST be able to re-run the Flutter app on the same host and observe the same on-screen + log behaviour modulo the per-run-varying elements documented above. The reproducibility check is part of /speckit-implement T-equivalent verification.

## Recommended clean session block (FR-005 (b))

Required only in ex-06 (cluster A — the chapter's Flutter setup walkthrough). The block MUST contain (per CLAUDE.md §18 Flutter rebuild section + the chapter's own pre-flight verification):

```bash
pkill -f "glp_multiagent" 2>/dev/null   # kill running app
flutter clean                            # clear cached builds
flutter pub get                          # re-resolve dependencies
flutter build <platform>                 # rebuild
```

Plus the launch command + verification step. The block MUST be presented in copy-pastable form (no inline comments inside the block; comments above/below if needed).

## See also

- `trace-file-format.md` — REPL trace contract for the 10 REPL exercises.
- `status-block-format.md` — gate-grep contract.
- `glp-file-format.md` — header-block requirements for cluster project files.
