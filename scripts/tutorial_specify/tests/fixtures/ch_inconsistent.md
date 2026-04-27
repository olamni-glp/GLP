# Ch 97 Plan (test fixture — FR-007b abort: multi-actor-distillation without boot.glp)

**Mode**: multi-actor-distillation

## Shared
- Project per use case: self/agent/network/actors/boot.glp.

## Use cases
- broken-play/: missing `boot.glp` from the file list — should trigger FR-007b abort.
  Files: self.glp, agent.glp, network.glp, actors.glp.

## Test
- REPL each: load project; play. → succeeds.
