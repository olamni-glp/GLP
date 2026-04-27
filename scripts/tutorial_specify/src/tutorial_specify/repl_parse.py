"""GLP REPL parse-check (FR-003a, /research.md Decision 3).

Each extracted code block is written to a temp `.glp` file and loaded into
the REPL via subprocess. A clean parse means no error lines in stderr/stdout.
Any parse failure aborts the chapter with a precise diagnostic.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TIMEOUT_S = float(os.environ.get("TUTORIAL_SPECIFY_REPL_TIMEOUT_S", "30"))


@dataclass
class ReplParseOutcome:
    block_id: str
    passed: bool
    stdout: str
    stderr: str


def repl_command(repo_root: Path) -> list[str]:
    """Build the command to invoke the GLP REPL.

    Per Constitution §Workflow, the REPL is `dart run bin/glp_repl.dart` from
    `glp_runtime/`. We run from the repo root and let dart resolve.
    """
    return ["dart", "run", "bin/glp_repl.dart"]


def parse_block(block_id: str, code: str, repo_root: Path,
                 timeout_s: float | None = None) -> ReplParseOutcome:
    """Round-trip one code block through the REPL parser.

    Returns ReplParseOutcome with `passed` set per stdout/stderr inspection.
    Does NOT raise on parse failure — caller decides whether to abort.
    """
    timeout_s = timeout_s if timeout_s is not None else DEFAULT_TIMEOUT_S
    runtime_dir = repo_root / "glp_runtime"

    with tempfile.NamedTemporaryFile(
        prefix=f"ts_block_{block_id}_", suffix=".glp", delete=False, mode="w",
        encoding="utf-8",
    ) as tmp:
        tmp.write(code)
        tmp.write("\n")
        tmp_path = Path(tmp.name)

    repl_input = f"load {tmp_path.as_posix()}\n:quit\n"
    try:
        proc = subprocess.run(
            repl_command(repo_root),
            input=repl_input,
            cwd=str(runtime_dir) if runtime_dir.exists() else str(repo_root),
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except FileNotFoundError as exc:
        return ReplParseOutcome(
            block_id=block_id,
            passed=False,
            stdout="",
            stderr=f"dart not found on PATH: {exc}",
        )
    except subprocess.TimeoutExpired as exc:
        return ReplParseOutcome(
            block_id=block_id,
            passed=False,
            stdout=exc.stdout or "",
            stderr=(exc.stderr or "") + f"\n[timeout after {timeout_s}s]",
        )
    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass

    passed = _is_clean_load(proc.stdout, proc.stderr, proc.returncode)
    return ReplParseOutcome(
        block_id=block_id, passed=passed, stdout=proc.stdout, stderr=proc.stderr
    )


def _is_clean_load(stdout: str, stderr: str, returncode: int) -> bool:
    """Heuristic: REPL load succeeded if exit==0, no error/exception markers."""
    if returncode != 0:
        return False
    bad_markers = (
        "error",
        "Error",
        "ERROR",
        "Exception",
        "exception",
        "failed",
        "FAILED",
    )
    blob = stdout + "\n" + stderr
    return not any(m in blob for m in bad_markers)
