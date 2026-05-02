# ex-06 — Flutter trace (cluster A simple-multimodule)

**Status**: TODO — pending manual Flutter test by project owner per spec FR-017.

The flutter-trace-format contract requires this file be byte-equal to a captured Flutter session from a manually-verified run. Per FR-017 + the contract:

> The implementer MUST manually test the Flutter app + capture the trace BEFORE writing the tutorial.md. NO synthesised traces. If the Flutter app fails to launch or behave as expected, halt per FR-013 and report.

The cluster A Flutter pairing (`glp_multiagent/lib/main_olamni_ch07_simple_multimodule.dart`) was created and verified to BUILD by the implementing session. The actual run + trace capture is deferred to the project owner.

## Manual test procedure (to be executed by project owner)

1. Verify Flutter: `/c/Users/gavri/flutter/bin/flutter.bat --version`.
2. Build: `cd D:/bstdev/research/GLP/GLP/glp_multiagent && /c/Users/gavri/flutter/bin/flutter.bat build windows -t lib/main_olamni_ch07_simple_multimodule.dart`.
3. Launch: `./build/windows/x64/runner/Release/glp_multiagent.exe`.
4. Click Play 1 button. Observe the 3 agent panels (Alice / Bob / Charlie) reflecting the both-accept introduction protocol.
5. Click Play 2 button. Observe Alice gets `rejected(charlie)`.
6. Click Play 3 button. Observe the both-reject branch.
7. Capture the per-agent panel content + the platform log file (Windows: `%TEMP%\glp_multiagent_trace.log`; macOS: `/private/tmp/glp_multiagent_trace.log`; Linux: `/tmp/glp_multiagent_trace.log`).
8. Replace this file's content with the structured trace per `specs/008-tutorial-ch07/contracts/flutter-trace-format.md` (Phase A pre-flight + Phase B build + Phase C launch + Phase D per-play observations + Phase E recommended clean-session block).

## See also

- `ex-06-tutorial.md` — the learner-facing step-through with build/launch/clean-session instructions.
- `specs/008-tutorial-ch07/contracts/flutter-trace-format.md` — the trace contract.
