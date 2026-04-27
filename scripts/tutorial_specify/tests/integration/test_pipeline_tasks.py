"""US2 / T035: generated spec acceptance criteria require REPL load test.

Validates that every generated spec carries an FR or success criterion
demanding a REPL load+goal verification, which `/speckit-tasks` will turn
into a Phase 1 baseline-test task per Constitution Principle V.
"""

from __future__ import annotations

import pytest

from tests.integration.test_pipeline_clarify import _generate_spec_for_test  # type: ignore


def test_generated_spec_demands_repl_test(tmp_path):
    spec_path = _generate_spec_for_test(tmp_path)
    body = spec_path.read_text(encoding="utf-8")

    # The spec MUST require REPL load+goal verification per FR-010 of the tool.
    assert "REPL" in body
    assert "succeeds" in body or "→ succeeds" in body
    # Constitution Principle V (Test-First) reference
    assert "Constitution Principle" in body or "Principle V" in body or "Tutorial Charter" in body
