# Chapter 13 — Bonus: AI Engineers Collaborating, with Python Actors

**Status:** plan agreed; implementation to follow once chapters 1–12 are in place.

This bonus chapter is **not from the book**. It demonstrates two things together:

1. **A small AI-engineer collaboration network**, applying the parent-children CSSN protocol to a fresh setting: 3 AI engineers (humans) each with 3 named AI agents collaborating on shared work. Engineers play the **parent** role; AI agents play the **child** role. Pairs of engineers first establish parent-parent connections; each engineer then independently authorizes specific agents — individually or in named groups — to connect to a colleague's agents, scoped by a declared purpose / context.
2. **Actors encoded in Python instead of Dart/Flutter**, bringing the example to life as a multi-actor demonstration in which each engineer is a small Python program driving its parent-agent over a runtime-to-Python bridge, rather than a Flutter UI panel.

## Use case: `ai-engineers-collab`

Three engineers — `alice`, `bob`, `carol` — each with three named AI agents — Alice's `a1`/`a2`/`a3`, Bob's `b1`/`b2`/`b3`, Carol's `c1`/`c2`/`c3`. Twelve GLP processes total (three parents + nine children), routed through the network switch.

Story:
1. Alice and Bob, two engineer colleagues, decide to connect (engineer-to-engineer pair-connect, parent-parent friendship in CSSN terms).
2. Once connected, Alice authorizes her agent `a1` to talk to Bob's `b1` for purpose `code-review`. Bob independently authorizes the reverse direction with the same purpose.
3. `a1` and `b1` then exchange messages within that purpose's scope.
4. Optionally: Alice authorizes a *group* of her agents (e.g., `{a1, a2}`) to talk to Bob's group `{b1, b2}` for purpose `pair-programming`, exercising the group-formation primitives from book ch 8.

## Design notes

### GLP side

A single project subdirectory `ch13/ai-engineers-collab/` following the same template as ch 8–12: `self.glp`, `agent.glp`, `network.glp`, `actors.glp`, `boot.glp`. The agent code reuses parent-children CSSN modules (`programs/cssn_modules/`) and the play-child-safe approval idiom (`programs/typed_book/social_networks/play_child_safe.glp`), with vocabulary adapted (parent → engineer, child → ai_agent) and an extra purpose/context constant on every authorization message. `actors.glp` holds deterministic GLP-side scripts so the play runs headless in the REPL without Python.

### Python actor bridge

One Python process per engineer — `engineer_alice.py`, `engineer_bob.py`, `engineer_carol.py` — each connecting to its engineer-parent's user-channel via a simple text protocol: line-delimited JSON over a stdin/stdout pipe, spawned by a host Dart runner derived from `main_cssg_mad_modules.dart`. The host wires each engineer's tagged-output stream to its paired Python process and each Python process's stdout back into its engineer's user-input stream, using the same `mad_router.dart` + `isolate_protocol.dart` model already in use for Flutter UI panels. The nine ai_agent processes use GLP-side scripts in `actors.glp` for v1; richer per-agent Python actors are an extension.

## How to run

```bash
# REPL: headless, GLP-side actors only
cd glp_runtime/bin
dart run glp_repl.dart
load ../../olamni/tutorial/ch13/ai-engineers-collab
play_ai_engineers_collab.

# Flutter + Python: full multi-process demo
cd glp_multiagent
flutter run -d windows -t lib/main_olamni_ch13_ai_engineers_collab.dart
# (host spawns 12 Dart isolates + 3 Python subprocesses; observe agent panels)
```

## Pattern source in the repo

`programs/cssn_modules/` (parent-children CSSN agent code), `programs/typed_book/social_networks/play_child_safe.glp` (parent-approval play), `programs/typed_book/social_networks/group_formation.glp` + `group_messaging.glp` (for group-scoped authorizations), `glp_multiagent/lib/main_cssn_village.dart` and `main_cssg_mad_modules.dart` (Dart-side multi-isolate templates).
