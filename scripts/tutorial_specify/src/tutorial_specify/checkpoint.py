"""Checkpoint persistence (FR-016, FR-017, FR-019, FR-022).

Atomic write-then-rename JSON checkpoint at `<spec_dir>/.checkpoint.json`.
Validates against `contracts/checkpoint-schema.json` on read.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

from tutorial_specify.errors import CheckpointMismatchError, CheckpointSchemaError

CHECKPOINT_SCHEMA_VERSION = "1.0.0"


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    """SHA-256 hex digest of a file's contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_inputs(paths: Iterable[Path]) -> dict[str, str]:
    """Return a sorted map of {relative path string: sha256} for the given files.

    Raises FileNotFoundError if any input is missing.
    """
    out: dict[str, str] = {}
    for p in paths:
        out[str(p).replace("\\", "/")] = sha256_file(p)
    return dict(sorted(out.items()))


@dataclass
class ExtractedBlock:
    block_id: str
    book_pages: str
    text: str
    parse_status: str = "pending"  # pending | passed | failed
    program_id: str | None = None
    pdf_pages: list[int] = field(default_factory=list)


@dataclass
class ReplResult:
    block_id: str
    passed: bool
    repl_stdout: str = ""
    repl_stderr: str = ""


@dataclass
class Checkpoint:
    chapter_id: str
    schema_version: str = CHECKPOINT_SCHEMA_VERSION
    started_at: str = field(default_factory=_now_utc_iso)
    last_updated_at: str = field(default_factory=_now_utc_iso)
    inputs: dict[str, str] = field(default_factory=dict)
    book_page_to_pdf_page: dict[int, int] = field(default_factory=dict)
    tutorial_mode: str | None = None
    extracted_blocks: list[ExtractedBlock] = field(default_factory=list)
    repl_results: list[ReplResult] = field(default_factory=list)
    completed_steps: list[str] = field(default_factory=list)
    pending_steps: list[str] = field(default_factory=list)
    current_step: str | None = None
    terminated_with: str | None = None
    abort_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "schema_version": self.schema_version,
            "chapter_id": self.chapter_id,
            "started_at": self.started_at,
            "last_updated_at": self.last_updated_at,
            "inputs": dict(sorted(self.inputs.items())),
            "tutorial_mode": self.tutorial_mode,
            "completed_steps": list(self.completed_steps),
            "pending_steps": list(self.pending_steps),
            "current_step": self.current_step,
            "terminated_with": self.terminated_with,
            "abort_reason": self.abort_reason,
        }
        if self.book_page_to_pdf_page:
            # JSON object keys are strings; sort by integer
            d["book_page_to_pdf_page"] = {
                str(k): v for k, v in sorted(self.book_page_to_pdf_page.items())
            }
        if self.extracted_blocks:
            d["extracted_blocks"] = [asdict(b) for b in self.extracted_blocks]
        if self.repl_results:
            d["repl_results"] = [asdict(r) for r in self.repl_results]
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Checkpoint":
        cp = cls(chapter_id=d["chapter_id"])
        cp.schema_version = d.get("schema_version", CHECKPOINT_SCHEMA_VERSION)
        cp.started_at = d["started_at"]
        cp.last_updated_at = d["last_updated_at"]
        cp.inputs = dict(d.get("inputs", {}))
        cp.book_page_to_pdf_page = {
            int(k): int(v) for k, v in d.get("book_page_to_pdf_page", {}).items()
        }
        cp.tutorial_mode = d.get("tutorial_mode")
        cp.extracted_blocks = [
            ExtractedBlock(**b) for b in d.get("extracted_blocks", [])
        ]
        cp.repl_results = [ReplResult(**r) for r in d.get("repl_results", [])]
        cp.completed_steps = list(d.get("completed_steps", []))
        cp.pending_steps = list(d.get("pending_steps", []))
        cp.current_step = d.get("current_step")
        cp.terminated_with = d.get("terminated_with")
        cp.abort_reason = d.get("abort_reason")
        return cp


def checkpoint_path(spec_dir: Path) -> Path:
    return spec_dir / ".checkpoint.json"


def write_checkpoint(spec_dir: Path, checkpoint: Checkpoint) -> None:
    """Atomically write the checkpoint to disk (FR-017)."""
    checkpoint.last_updated_at = _now_utc_iso()
    target = checkpoint_path(spec_dir)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        checkpoint.to_dict(), indent=2, sort_keys=True, ensure_ascii=False
    )
    fd, tmp_path = tempfile.mkstemp(
        prefix=".checkpoint.", suffix=".tmp", dir=str(target.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, target)
    except Exception:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise


def read_checkpoint(spec_dir: Path) -> Checkpoint | None:
    target = checkpoint_path(spec_dir)
    if not target.exists():
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CheckpointSchemaError(
            f"checkpoint at {target} is not valid JSON ({exc}); "
            f"use --restart to wipe and start over"
        ) from exc
    return Checkpoint.from_dict(data)


def verify_inputs_unchanged(checkpoint: Checkpoint, current_inputs: dict[str, str]) -> None:
    """Raise CheckpointMismatchError if any recorded input hash differs from current.

    Implements FR-019.
    """
    if checkpoint.inputs != current_inputs:
        diffs: list[str] = []
        for path in sorted(set(checkpoint.inputs) | set(current_inputs)):
            old = checkpoint.inputs.get(path)
            new = current_inputs.get(path)
            if old != new:
                diffs.append(f"  - {path}: {old} -> {new}")
        raise CheckpointMismatchError(
            "input content-hashes differ from checkpoint; use --restart "
            "to wipe and rerun. Differences:\n" + "\n".join(diffs)
        )
