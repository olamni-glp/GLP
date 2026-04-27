# Ch 13 Plan (bonus, Python actors)

## Shared
- Scenario: 3 AI engineers, each with 3 named AI agents, collaborating on shared work. Engineers play the **parent** role from the parent-children CSSN protocol (`programs/cssn_modules/` + `programs/typed_book/social_networks/play_child_safe.glp`); AI agents play the **child** role. Engineer pairs first establish parent-parent connections; each engineer then independently authorizes specific agents — individually or as named groups — to connect to a colleague's agents, scoped by purpose / context.
- Reuse parent-children CSSN code; adapt vocabulary (parent → engineer, child → ai_agent) and add a purpose/context tag to authorization messages.

## Files
- ch13/ai-engineers-collab/: GLP project (self/agent/network/actors/boot.glp). Three engineer (parent) agents — e.g., `alice`, `bob`, `carol` — and nine ai_agent (child) agents — Alice's `a1/a2/a3`, Bob's `b1/b2/b3`, Carol's `c1/c2/c3`. Authorization carries a purpose/context constant. actors.glp holds GLP-side fallback scripts so the play runs headless in the REPL without Python; boot wires the three engineer processes, the nine ai_agent processes, and the network switch.
- ch13/python/: one Python script per engineer — `engineer_alice.py`, `engineer_bob.py`, `engineer_carol.py` — each a small process that reads JSON lines from stdin and writes JSON lines to stdout, driving its parent role: pair-connect with another engineer, then authorize specific agents (or groups) to connect to a colleague's agents under a declared purpose / context.
- glp_multiagent/lib/main_olamni_ch13_ai_engineers_collab.dart: derived from `main_cssg_mad_modules.dart`; spawns one Dart isolate per engineer and per ai_agent (12 isolates total) plus three Python subprocesses (one per engineer) wired to its engineer-parent's user-channel via `mad_router.dart` / `isolate_protocol.dart`; line-delimited JSON over stdin/stdout.

## Test
- REPL: load project; run `play_ai_engineers_collab.` with GLP-side actors → succeeds (or suspended for plays with open channels).
- Bridge: launch Flutter host; observe Python ↔ GLP message flow across the three engineer panels and the nine ai_agent panels — pair-connect, then a sample authorization granting `alice/a1` to talk to `bob/b1` for purpose `code-review`.
