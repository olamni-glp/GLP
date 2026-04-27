"""Integration test: PDF code-block parse failure aborts the chapter (T016, FR-003a).

This test deliberately stages a chapter whose PDF (when extracted) yields
a syntactically broken GLP code block. The tool MUST round-trip the block
through the GLP REPL parser, observe the failure, and abort the chapter.

Skips when dart / pdfplumber / reportlab is unavailable.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

reportlab = pytest.importorskip("reportlab")
pdfplumber = pytest.importorskip("pdfplumber")


def _build_broken_pdf(target: Path) -> None:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

    c = canvas.Canvas(str(target), pagesize=LETTER)
    width, height = LETTER
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, height - 1 * inch, "§99.9 Broken Section")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1 * inch, height - 1.5 * inch, "Program 99.9")
    c.setFont("Courier", 11)
    # Deliberately broken GLP — incomplete clause head, missing period
    c.drawString(1 * inch, height - 2 * inch, "p(X) :- ?* not glp")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, 0.5 * inch, "1")
    c.showPage()
    c.save()


def test_pdf_parse_failure_aborts_chapter(tmp_path):
    if shutil.which("dart") is None:
        pytest.skip("dart not on PATH")
    if not (tmp_path / "..").exists():
        pytest.skip("tmp_path missing parent")

    repo = tmp_path
    tutorial = repo / "olamni" / "tutorial" / "ch99"
    tutorial.mkdir(parents=True)
    (repo / "olamni" / "tutorial" / "charter.md").write_text(
        "# charter\n", encoding="utf-8"
    )
    (tutorial / "ch99_plan.md").write_text(
        "# Ch 99\n\n**Mode**: block-focused\n\n## Files\n"
        "- ch99/ch-99-ex-01.glp: §99.9 broken example. → broken_demo. [s1]\n",
        encoding="utf-8",
    )
    (tutorial / "ch99-sources.md").write_text(
        "1. broken pdf\n", encoding="utf-8"
    )
    (tutorial / "ch99_tutorial.md").write_text("# ch99 tutorial\n", encoding="utf-8")

    _build_broken_pdf(repo / "GLP_ART.pdf")

    env = dict(os.environ)
    env["TUTORIAL_SPECIFY_ROOT"] = str(repo)
    pkg_src = Path(__file__).resolve().parents[2] / "src"
    env["PYTHONPATH"] = str(pkg_src) + os.pathsep + env.get("PYTHONPATH", "")

    proc = subprocess.run(
        [sys.executable, "-m", "tutorial_specify", "ch99"],
        capture_output=True,
        text=True,
        env=env,
        timeout=180,
    )
    assert proc.returncode == 2, proc.stderr or proc.stdout
    blob = proc.stdout + proc.stderr
    assert "REPL parse-check failed" in blob or "parse" in blob.lower()
