"""Per-mode spec composers.

Each module implements one of the three tutorial modes declared in
spec.md FR-007:
- cohesive_synthesis: weave multiple book code blocks into one tutorial file
- block_focused: one tutorial file per book Program
- multi_actor_distillation: project-shaped multi-actor play

The `compose(...)` function in each module returns the body markdown for a
generated `spec.md` per `contracts/spec-output-format.md`.
"""

from __future__ import annotations

from tutorial_specify.modes.block_focused import compose as compose_block_focused
from tutorial_specify.modes.cohesive_synthesis import compose as compose_cohesive_synthesis
from tutorial_specify.modes.multi_actor_distillation import compose as compose_multi_actor_distillation

MODE_REGISTRY = {
    "cohesive-synthesis": compose_cohesive_synthesis,
    "block-focused": compose_block_focused,
    "multi-actor-distillation": compose_multi_actor_distillation,
}

VALID_MODES = frozenset(MODE_REGISTRY)
