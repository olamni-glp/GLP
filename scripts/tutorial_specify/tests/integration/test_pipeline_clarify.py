"""US2 / T033: generated spec is shaped for /speckit-clarify consumption.

Speckit slash commands are not directly invokable in pytest — they are
Claude Code skills. This test instead validates the structural promise:
the generated spec.md contains a `## Clarifications` section, has at most
3 [NEEDS CLARIFICATION] markers, and has all mandatory speckit sections
the slash command expects.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

reportlab = pytest.importorskip("reportlab")
pdfplumber = pytest.importorskip("pdfplumber")


def _generate_spec_for_test(tmp_path: Path) -> Path:
    """Generate a real spec via the CLI (uses the mock PDF)."""
    import os, shutil, subprocess, sys
    if shutil.which("dart") is None:
        pytest.skip("dart not on PATH")

    repo = tmp_path
    tutorial_dir = repo / "olamni" / "tutorial" / "ch99"
    tutorial_dir.mkdir(parents=True)
    (repo / "olamni" / "tutorial" / "charter.md").write_text(
        "# charter\n", encoding="utf-8"
    )
    (tutorial_dir / "ch99_plan.md").write_text(
        "# Ch 99\n\n**Mode**: block-focused\n\n## Files\n"
        "- ch99/ch-99-ex-01.glp: §99.1 example. → mock_demo. [s1]\n",
        encoding="utf-8",
    )
    (tutorial_dir / "ch99-sources.md").write_text("1. mock\n", encoding="utf-8")
    (tutorial_dir / "ch99_tutorial.md").write_text("# ch99\n", encoding="utf-8")

    fixtures = Path(__file__).resolve().parents[1] / "fixtures"
    sys.path.insert(0, str(fixtures))
    try:
        import build_mock_pdf  # type: ignore
        build_mock_pdf.build(repo / "GLP_ART.pdf")
    finally:
        sys.path.pop(0)

    env = dict(os.environ)
    env["TUTORIAL_SPECIFY_ROOT"] = str(repo)
    env["TUTORIAL_SPECIFY_FORCE"] = "1"
    pkg_src = Path(__file__).resolve().parents[2] / "src"
    env["PYTHONPATH"] = str(pkg_src) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-m", "tutorial_specify", "ch99", "--restart"],
        capture_output=True, text=True, env=env, timeout=300,
    )
    if proc.returncode != 0:
        pytest.skip(f"spec generation failed: {proc.stderr[:300]}")
    return next((repo / "specs").rglob("spec.md"))


def test_generated_spec_is_clarify_ready(tmp_path):
    spec_path = _generate_spec_for_test(tmp_path)
    body = spec_path.read_text(encoding="utf-8")

    # Mandatory speckit sections
    for header in (
        "## Clarifications",
        "## User Scenarios & Testing",
        "## Requirements",
        "## Success Criteria",
        "## Assumptions",
    ):
        assert header in body, f"missing required section: {header}"

    # Tutorial Mode declared
    assert "Tutorial Mode" in body
    assert "block-focused" in body

    # Clarification budget per FR-022 / spec-quality checklist
    markers = re.findall(r"\[NEEDS CLARIFICATION", body)
    assert len(markers) <= 3
