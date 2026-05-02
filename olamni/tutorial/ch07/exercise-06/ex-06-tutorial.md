# Exercise 06 — Cluster A Flutter setup walkthrough

This is the Olamni tutorial's first Flutter onboarding exercise. It is the chapter-7 entry point for every learner who will run a GLP project under the Flutter app, and it sets the precedent that subsequent Flutter exercises (chs 7-13) inherit. Its single purpose is to get you from "Flutter SDK installed" to "cluster A's three plays running on screen with per-agent panels".

## What you'll learn

- How to verify the Flutter SDK is installed and reachable from the GLP repo's shell environment.
- The role of the `glp_multiagent/` Flutter project: an isolate-host that spawns one Dart isolate per agent, loads a GLP project into each, drives it with a tagged-output protocol, and renders per-agent panels.
- How a "Flutter pairing" (the `lib/main_olamni_ch07_simple_multimodule.dart` entry point) maps to a cluster project under `olamni/tutorial/ch07/`. Each Flutter pairing pins one project directory + one boot-file name + the agent panel layout.
- The recommended clean-session sequence — `pkill` + `flutter clean` + `flutter pub get` + rebuild — for when stale build cache or pubspec drift causes weird launch failures.
- The expected on-screen behavior for cluster A's three plays (play 1 both-accept, play 2 Charlie-rejects, play 3 both-reject).

## Prerequisites

- **Flutter SDK installed**, reachable on the implementing host. On the Windows research clone this is `C:\Users\gavri\flutter\bin\flutter.bat` (under MSYS / Git-Bash: `/c/Users/gavri/flutter/bin/flutter.bat`). On macOS/Linux the binary is `flutter` on `PATH`.
- **Cluster A Flutter pairing exists** at `glp_multiagent/lib/main_olamni_ch07_simple_multimodule.dart` (478 lines, cloned from `main_cssg_mad_modules.dart` and retargeted to cluster A's pruned project per research R-011). This was created at task T030.
- **Cluster A project loadable** — the directory `olamni/tutorial/ch07/simple-multimodule/` (containing `self.glp`, `agent.glp`, `boot.glp`, `ui/mediator.glp`, `ui/actors.glp`) must pass project-load. This was verified at task T014.

## Pre-flight: verify Flutter

Before doing anything else, confirm Flutter is reachable. Open a Git-Bash / MSYS shell at the GLP repo root and run:

```bash
/c/Users/gavri/flutter/bin/flutter.bat --version
```

Expected output starts with a line like `Flutter 3.x.x ...` plus channel/branch + Dart SDK version. The Flutter SDK is **required** for this exercise (ex-06) and the chapter's other Flutter exercise (ex-12), as well as every Flutter exercise in chapters 8 through 13. If the command fails (binary not found, SDK missing), **halt**: the chapter contract (FR-013) requires the implementer to stop and report a missing-toolchain pre-flight failure rather than papering over it.

On macOS/Linux the equivalent commands are:

```bash
flutter --version
```

(assuming `flutter` is on `PATH` per the standard Flutter install).

## Build cluster A Flutter pairing

The Flutter app is built per platform with the cluster A entry-point file passed via `-t`. From the GLP root in Git-Bash:

```bash
cd D:/bstdev/research/GLP/GLP/glp_multiagent
/c/Users/gavri/flutter/bin/flutter.bat build windows -t lib/main_olamni_ch07_simple_multimodule.dart
```

For other platforms substitute the `build` target:

- macOS: `flutter build macos -t lib/main_olamni_ch07_simple_multimodule.dart`
- Linux: `flutter build linux -t lib/main_olamni_ch07_simple_multimodule.dart`

Expected output (Windows) ends with lines roughly of the form:

```text
Building Windows application...
Built build/windows/x64/runner/Release/glp_multiagent.exe
```

(The intermediate `Compiling X% ...` progress lines vary per run and are not part of the trace's byte-equality contract — only the success line + the resulting binary path are.)

If the build fails with a "stale cache" / pubspec-drift symptom, jump to the next section.

## Recommended clean session

Per FR-005 (b) of the chapter spec and CLAUDE.md §18's Flutter-rebuild guidance, when a build fails for cache-related reasons run this clean+rebuild block. Copy-paste the entire block at once:

```bash
cd D:/bstdev/research/GLP/GLP/glp_multiagent
taskkill /F /IM glp_multiagent.exe 2>NUL
/c/Users/gavri/flutter/bin/flutter.bat clean
/c/Users/gavri/flutter/bin/flutter.bat pub get
/c/Users/gavri/flutter/bin/flutter.bat build windows -t lib/main_olamni_ch07_simple_multimodule.dart
```

On macOS/Linux the equivalent block uses `pkill` instead of `taskkill`:

```bash
cd <GLP-root>/glp_multiagent
pkill -f "glp_multiagent" 2>/dev/null
flutter clean
flutter pub get
flutter build macos -t lib/main_olamni_ch07_simple_multimodule.dart
```

The four steps are: kill any running app instance (so the executable isn't locked); clear the Flutter build cache; re-resolve the package dependencies (the Flutter app uses `glp_runtime` via a path dependency, so a fresh `pub get` ensures the latest local runtime is wired in); rebuild the binary.

## Launch cluster A Flutter pairing

After a successful build, launch the binary directly:

```bash
./build/windows/x64/runner/Release/glp_multiagent.exe
```

(macOS: `open build/macos/Build/Products/Release/glp_multiagent.app`; Linux: `./build/linux/x64/release/bundle/glp_multiagent`.)

For development iteration you may prefer hot-restart mode:

```bash
/c/Users/gavri/flutter/bin/flutter.bat run -t lib/main_olamni_ch07_simple_multimodule.dart
```

Either way, a window opens with the title `ch07 cluster A — simple-multimodule (3-agent friend-mediated plays 1-3)`. The window contains three buttons (Play 1, Play 2, Play 3) above three agent panels (Alice, Bob, Charlie).

## Run the 3 plays

Cluster A's project has three Flutter plays — `fplay1`, `fplay2`, `fplay3` — defined in `boot.glp`. Each is the tagged-output variant of its corresponding REPL play (`play1`, `play2`, `play3` from ex-05); the only difference is `send_to_user_tagged` in place of `sink`, which routes the per-agent display streams via `_output/1` to the Dart panels as `tagged(Id, cmd(...))` / `tagged(Id, notify(...))` terms.

Clicking a Play button spawns three Dart isolates — one per agent — each loading the cluster A project and running the corresponding `fplayN/0` goal. Tagged output is parsed by the regex
`^tagged\((\w+), (cmd|notify)\((.+)\)\)$` (defined in the pairing source) and routed to the matching panel.

Per the actor scripts in `olamni/tutorial/ch07/simple-multimodule/ui/actors.glp` (verified live):

- **Play 1 — both accept** (alice1 / bob1 / charlie1). Alice's panel shows `connect(bob)` then `send(bob, hello)`; Alice receives `connected(bob)` then a `befriend_intro(bob, charlie, ReqId)` notification, sends `accept_intro(charlie, ReqId)`, then `connected(charlie)` and `send(charlie, 'Hi Charlie')`, ending on `received(charlie, 'Hi Alice')`. Bob's panel shows the `befriend(alice, ReqId)` arrival, the `decision(yes, alice, ReqId)`, then receiving Alice's hello, `connect(charlie)`, `connected(charlie)`, receiving Charlie's hello, and finally `introduce(alice, charlie)`. Charlie's panel shows `befriend(bob, ReqId)`, `decision(yes, bob, ReqId)` + `send(bob, hello)`, then the `befriend_intro(bob, alice, ReqId)`, `accept_intro(alice, ReqId)`, and `send(alice, 'Hi Alice')`.
- **Play 2 — Alice accepts, Charlie rejects** (alice2 / bob2 / charlie2). Same as Play 1 through Bob's `introduce(alice, charlie)`. Then Charlie's panel shows `reject_intro(alice, ReqId)` instead of accept; Alice's panel ends on a `rejected(charlie)` notification rather than the greeting exchange.
- **Play 3 — both reject** (alice3 / bob3 / charlie3). Bob still accepts the initial befriend, but Alice's actor's `alice3_wait_intro` clause emits `reject_intro(charlie, ReqId)` immediately on receiving the intro notification. Charlie's actor (`charlie3`) also has a reject branch in its own intro-handler. The net effect: no `connected(charlie)` on Alice's panel, no greeting exchange.

Click each Play button in turn and observe the panels updating. The output for each play matches the corresponding `fplayN` REPL trace from ex-05's REPL play sequence, modulo the tagged-output wrapping.

## Trace capture

**PENDING MANUAL TEST.** Per spec FR-017:

> The implementer MUST manually test the Flutter app + capture the trace BEFORE writing the tutorial.md. NO synthesised traces. If the Flutter app fails to launch or behave as expected, halt per FR-013 and report.

This tutorial framework was written by the implementing session AFTER verifying the Flutter pairing source compiles cleanly (the file exists; Dart syntax is valid; constants resolve to the cluster A project). The actual end-to-end run + trace capture is a manual step deferred to the project owner.

`[TODO: capture ex-06-flutter-trace.md via manual run by project owner]` — see the placeholder at `ex-06-flutter-trace.md` in this same directory.

## Manual test checklist

Steps for the project owner to complete the trace artefact:

1. Run `/c/Users/gavri/flutter/bin/flutter.bat --version` and capture the output (Phase A of the trace).
2. Run the build command from the "Build cluster A Flutter pairing" section and capture the build's success line + binary path (Phase B).
3. Launch the binary and confirm the window opens with the expected title; capture the launch command + the immediate platform-log-file creation observation (Phase C).
4. Click **Play 1** and observe Alice / Bob / Charlie panels reflecting the both-accept introduction protocol (per the actor-script summary above). Capture the panel content + the relevant lines from the platform log file (Phase D, sub-section play 1).
5. Click **Play 2** and observe Alice's panel ending on `rejected(charlie)`. Capture the panels + log lines (Phase D, sub-section play 2).
6. Click **Play 3** and observe the both-reject branch (no greeting exchange between Alice and Charlie). Capture the panels + log lines (Phase D, sub-section play 3).
7. Capture screenshots of each panel state if useful for documentation, plus the platform log file's contents:
   - Windows: `%TEMP%\glp_multiagent_trace.log`
   - macOS: `/private/tmp/glp_multiagent_trace.log`
   - Linux: `/tmp/glp_multiagent_trace.log`
8. Run the recommended clean-session block from the "Recommended clean session" section, rebuild, relaunch, and re-run play 1. Verify the resulting log matches the captured trace's expected sequence (Phase E, ex-06's reproducibility verification).
9. Replace the `ex-06-flutter-trace.md` placeholder content with the structured trace per `specs/008-tutorial-ch07/contracts/flutter-trace-format.md` — Phase A pre-flight + Phase B build + Phase C launch + Phase D per-play observations + Phase E recommended clean-session block.

## Cluster A Flutter pairing source

The Flutter pairing entry-point file is `glp_multiagent/lib/main_olamni_ch07_simple_multimodule.dart`. Its header block declares the chapter / cluster / clarification linkage:

```dart
/// ch07 cluster A Flutter pairing — simple-multimodule project.
///
/// Cloned from glp_multiagent/lib/main_cssg_mad_modules.dart (charter §2.2 pattern).
/// Retargets _projectDir to olamni/tutorial/ch07/simple-multimodule/ (cluster A's
/// pruned version of programs/cssg_modules/, kept to plays 1-3 + fplays 1-3).
///
/// Cluster A's project demonstrates §7.1-§7.6 module-system mechanics on a
/// 3-agent footprint (Alice / Bob / Charlie); cluster B's pairing
/// (main_olamni_ch07_cssg.dart) covers §7.7's full 4-agent CSSG validation.
///
/// Per /speckit-clarify Q1 + Q5 + Q-amendment Q1a + research R-011.
/// Spec: specs/008-tutorial-ch07/spec.md FR-015 + FR-020.
```

The constants that pin this pairing to cluster A's project + boot file are:

```dart
/// Project directory for static linking (repo-relative from glp_multiagent/).
const _projectDir = '../olamni/tutorial/ch07/simple-multimodule';

/// madGLP boot source — loaded on top of the linked project.
const _bootFileName = 'boot.glp';
```

The agent panel layout — three agents in alphabetical order, indigo / teal / red header colors — is declared via `_agentInfos`:

```dart
/// Panel order: Alice, Bob, Charlie — 3-agent friend-mediated layout.
const _agentInfos = [
  _AgentInfo('Alice', 'Agent', Color(0xFF3949AB), Color(0xFFE8EAF6)),
  _AgentInfo('Bob',   'Agent', Color(0xFF00897B), Color(0xFFE0F2F1)),
  _AgentInfo('Charlie', 'Agent', Color(0xFFD32F2F), Color(0xFFFFEBEE)),
];
```

The spawn-config helper that wires play 1 / 2 / 3 buttons to `fplay1/0` / `fplay2/0` / `fplay3/0` goals is:

```dart
/// Build spawn configs for a given play number.
List<_SpawnConfig> _cssgSpawnConfigs(int playNum) => [
  _SpawnConfig('main', 'fplay$playNum/0', []),
];
```

To extend the pairing with additional plays (e.g., a research branch experimenting with 4-agent variants on cluster A's pruned base), edit `_agentInfos` and `_cssgSpawnConfigs`, ensure the corresponding `fplayN/0` goal is defined in `boot.glp`, and rebuild.

## Multimodule-project-derivation note

The cluster A project is a **derivation** of the canonical `programs/cssg_modules/` project per the `multimodule-project-derivation` cross-chapter relationship contract (research R-008). Four of cluster A's five files (`self.glp`, `agent.glp`, `ui/mediator.glp`, `ui/actors.glp`) are byte-exact copies of the canonical sources and inherit byte-equivalence enforcement transitively via Section R of `test/run_all_tests.sh`. Only `boot.glp` is the derivation surface — pruned to remove the 4-agent CSSG actor imports, the network2/2 + the friend-to-friend network3/3 clauses, and plays 4-7 + fplays 4-7. All five files carry the multimodule-project-derivation header block declaring this relationship explicitly. Cluster B's project (used by ex-07 and ex-12) is the byte-exact full canonical, exercising the §7.7 4-agent CSSG validation example.

## Next

- **ex-07** — cluster B project introduction (REPL load demo of the byte-exact full canonical `programs/cssg_modules/` project, mirrored under `olamni/tutorial/ch07/cssg-modules/`).
- **ex-12** — cluster B Flutter pairing (the chapter's second Flutter exercise, covering the 5-play locked subset per Q4a, with the Parent / Child split panel layout per FR-009 + spec US4 acceptance scenario 2).
