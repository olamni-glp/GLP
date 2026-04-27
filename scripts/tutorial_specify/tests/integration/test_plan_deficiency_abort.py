"""Integration test: plan deficiencies abort cleanly with exit 2 (T015).

Tests FR-007a (missing **Mode**:) and FR-007b (multi-actor-distillation
without boot.glp).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _build_repo(tmp_path: Path, plan_fixture: Path, chapter_id: str) -> Path:
    """Materialise a synthetic repo root with charter + plan + sources + tutorial."""
    root = tmp_path
    tutorial_dir = root / "olamni" / "tutorial"
    tutorial_dir.mkdir(parents=True)
    (tutorial_dir / "charter.md").write_text("# charter (test)\n", encoding="utf-8")

    if chapter_id in {"ch01", "ch02", "ch03", "ch04"}:
        plan_target = tutorial_dir / "ch01-04_plan.md"
        sources_target = tutorial_dir / "ch01-04-sources.md"
    else:
        sub = tutorial_dir / chapter_id
        sub.mkdir()
        plan_target = sub / f"{chapter_id}_plan.md"
        sources_target = sub / f"{chapter_id}-sources.md"

    shutil.copy(plan_fixture, plan_target)
    sources_target.write_text("1. test source\n", encoding="utf-8")

    sub_dir = tutorial_dir / chapter_id
    sub_dir.mkdir(exist_ok=True)
    (sub_dir / f"{chapter_id}_tutorial.md").write_text(
        f"# {chapter_id} tutorial (test)\n", encoding="utf-8"
    )

    # Synthetic empty PDF (won't be reached if abort fires during plan parse).
    (root / "GLP_ART.pdf").write_bytes(b"%PDF-1.4\n%%EOF\n")
    return root


def _run_cli(repo_root: Path, chapter_id: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["TUTORIAL_SPECIFY_ROOT"] = str(repo_root)
    # Make package importable in the subprocess.
    pkg_src = Path(__file__).resolve().parents[2] / "src"
    env["PYTHONPATH"] = str(pkg_src) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "tutorial_specify", chapter_id],
        capture_output=True,
        text=True,
        env=env,
    )


def test_missing_mode_aborts_with_exit_2(tmp_path, fixtures_dir):
    repo = _build_repo(tmp_path, fixtures_dir / "ch_missing_mode.md", "ch04")
    proc = _run_cli(repo, "ch04")
    assert proc.returncode == 2, proc.stderr
    assert "Mode" in proc.stderr


def test_inconsistent_multi_actor_aborts_with_exit_2(tmp_path, fixtures_dir):
    repo = _build_repo(tmp_path, fixtures_dir / "ch_inconsistent.md", "ch12")
    proc = _run_cli(repo, "ch12")
    assert proc.returncode == 2, proc.stderr
    assert "boot.glp" in proc.stderr
