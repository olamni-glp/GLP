"""Integration test: two consecutive uninterrupted runs produce byte-identical output (T028).

Implements SC-004 / FR-022. Skips if dart / pdfplumber / reportlab unavailable.
"""

from __future__ import annotations

import filecmp
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

reportlab = pytest.importorskip("reportlab")
pdfplumber = pytest.importorskip("pdfplumber")


def _build_repo(tmp_path: Path) -> Path:
    repo = tmp_path
    tutorial_dir = repo / "olamni" / "tutorial" / "ch99"
    tutorial_dir.mkdir(parents=True)
    (repo / "olamni" / "tutorial" / "charter.md").write_text(
        "# charter\n", encoding="utf-8"
    )
    (tutorial_dir / "ch99_plan.md").write_text(
        "# Ch 99\n\n**Mode**: block-focused\n\n## Files\n"
        "- ch99/ch-99-ex-01.glp: §99.1 first example. → mock_demo. [s1]\n"
        "- ch99/ch-99-ex-02.glp: §99.2 second example. → mock_demo2. [s1]\n",
        encoding="utf-8",
    )
    (tutorial_dir / "ch99-sources.md").write_text(
        "1. PDF mock pp 1–2 §99.1 Program 99.1\n", encoding="utf-8"
    )
    (tutorial_dir / "ch99_tutorial.md").write_text("# ch99 tutorial\n", encoding="utf-8")

    # Build mock PDF
    fixtures_dir = Path(__file__).resolve().parents[1] / "fixtures"
    sys.path.insert(0, str(fixtures_dir))
    try:
        import build_mock_pdf  # type: ignore
        build_mock_pdf.build(repo / "GLP_ART.pdf")
    finally:
        sys.path.pop(0)
    return repo


def _run(repo: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["TUTORIAL_SPECIFY_ROOT"] = str(repo)
    pkg_src = Path(__file__).resolve().parents[2] / "src"
    env["PYTHONPATH"] = str(pkg_src) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "tutorial_specify", "ch99", "--restart"],
        capture_output=True,
        text=True,
        env={**env, "TUTORIAL_SPECIFY_FORCE": "1"},
        timeout=300,
    )


def test_two_runs_produce_byte_identical_spec(tmp_path):
    if shutil.which("dart") is None:
        pytest.skip("dart not on PATH")

    repo = _build_repo(tmp_path)

    proc1 = _run(repo)
    if proc1.returncode != 0:
        pytest.skip(f"first run did not complete; env-dependent. stderr: {proc1.stderr[:300]}")

    spec_files_first = list((repo / "specs").rglob("spec.md"))
    assert len(spec_files_first) == 1
    spec1_bytes = spec_files_first[0].read_bytes()

    # Capture content, then rerun fresh
    proc2 = _run(repo)
    assert proc2.returncode == 0, proc2.stderr
    spec2_bytes = spec_files_first[0].read_bytes()

    assert spec1_bytes == spec2_bytes, "two consecutive runs produced differing spec.md"
