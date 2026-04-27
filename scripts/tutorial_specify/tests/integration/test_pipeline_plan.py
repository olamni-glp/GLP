"""US2 / T034: generated spec is shaped for /speckit-plan consumption.

Validates that the spec contains the metadata `/speckit-plan` extracts
(tutorial mode, references to charter and chapter plan paths) and that
its assumptions explicitly mention the chapter sub-plan paths required
for plan template Option C.
"""

from __future__ import annotations

from pathlib import Path

import pytest

# Reuse the spec-generation helper
from tests.integration.test_pipeline_clarify import _generate_spec_for_test  # type: ignore


def test_generated_spec_is_plan_ready(tmp_path):
    spec_path = _generate_spec_for_test(tmp_path)
    body = spec_path.read_text(encoding="utf-8")

    # Plan template Option C selectors
    assert "olamni/tutorial/charter.md" in body
    assert "ch99_plan.md" in body or "ch99-plan.md" in body
    # Tutorial Mode header is what /speckit-plan keys on for project-shape selection
    assert "Tutorial Mode" in body
