# Ch 97 Plan (test fixture — FR-007b abort: multi-actor-distillation without complete project)

**Mode**: multi-actor-distillation

## Shared
- Project per use case: self/agent/network/actors with the orchestration file.

## Use cases
- broken-play/: this use case lists self.glp agent.glp network.glp actors.glp but is missing the orchestration file the validator expects.

## Test
- REPL each: load project; play. → succeeds.
