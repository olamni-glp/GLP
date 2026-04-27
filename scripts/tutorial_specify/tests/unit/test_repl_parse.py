"""Unit tests for tutorial_specify.repl_parse (T012).

These tests run only when the GLP REPL is reachable (`dart run bin/glp_repl.dart`
from `glp_runtime/`). When dart is missing, the tests skip gracefully.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from tutorial_specify.repl_parse import parse_block


def _repo_root_from_env_or_git() -> Path | None:
    env = os.environ.get("TUTORIAL_SPECIFY_ROOT")
    if env:
        return Path(env).resolve()
    # Walk upward looking for glp_runtime/
    cur = Path(__file__).resolve()
    for parent in cur.parents:
        if (parent / "glp_runtime" / "bin" / "glp_repl.dart").exists():
            return parent
    return None


@pytest.fixture
def repo_root_for_repl() -> Path:
    root = _repo_root_from_env_or_git()
    if root is None or shutil.which("dart") is None:
        pytest.skip("GLP REPL or dart not available in this environment")
    return root


def test_parses_known_good_snippet(repo_root_for_repl):
    code = "p(a).\n"
    outcome = parse_block("test-good", code, repo_root_for_repl, timeout_s=60)
    assert outcome.passed, f"unexpected parse failure: {outcome.stderr}"


def test_rejects_mangled_snippet(repo_root_for_repl):
    # Deliberately broken: dangling clause head, no body, no period.
    code = "p(X) :- ?* this is not GLP\n"
    outcome = parse_block("test-bad", code, repo_root_for_repl, timeout_s=60)
    assert not outcome.passed
    assert outcome.stderr or "error" in outcome.stdout.lower()
