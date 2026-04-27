"""Unit tests for tutorial_specify.checkpoint (T025, FR-016/017/019)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tutorial_specify.checkpoint import (
    Checkpoint,
    ExtractedBlock,
    checkpoint_path,
    hash_inputs,
    read_checkpoint,
    sha256_file,
    verify_inputs_unchanged,
    write_checkpoint,
)
from tutorial_specify.errors import CheckpointMismatchError, CheckpointSchemaError


def test_atomic_write_then_rename(tmp_path):
    cp = Checkpoint(chapter_id="ch04")
    cp.inputs = {"a": "0" * 64}
    write_checkpoint(tmp_path, cp)
    target = checkpoint_path(tmp_path)
    assert target.exists()

    # No temp file should be left behind
    leftover = list(tmp_path.glob(".checkpoint.*.tmp"))
    assert leftover == []


def test_round_trip(tmp_path):
    cp = Checkpoint(chapter_id="ch04")
    cp.inputs = {"plan.md": "f" * 64}
    cp.tutorial_mode = "block-focused"
    cp.completed_steps = ["parse_inputs"]
    cp.pending_steps = ["extract_pdf"]
    cp.extracted_blocks.append(
        ExtractedBlock(
            block_id="b1",
            book_pages="book p 37",
            text="p(a).",
            parse_status="passed",
            program_id="Program 1.1",
        )
    )
    write_checkpoint(tmp_path, cp)

    loaded = read_checkpoint(tmp_path)
    assert loaded is not None
    assert loaded.chapter_id == "ch04"
    assert loaded.tutorial_mode == "block-focused"
    assert loaded.completed_steps == ["parse_inputs"]
    assert len(loaded.extracted_blocks) == 1
    assert loaded.extracted_blocks[0].program_id == "Program 1.1"


def test_corrupted_checkpoint_raises(tmp_path):
    target = checkpoint_path(tmp_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(CheckpointSchemaError):
        read_checkpoint(tmp_path)


def test_missing_checkpoint_returns_none(tmp_path):
    assert read_checkpoint(tmp_path) is None


def test_mismatch_detection(tmp_path):
    cp = Checkpoint(chapter_id="ch04")
    cp.inputs = {"plan.md": "abc"}
    with pytest.raises(CheckpointMismatchError, match="differ from checkpoint"):
        verify_inputs_unchanged(cp, {"plan.md": "xyz"})


def test_hash_inputs_is_stable(tmp_path):
    f = tmp_path / "x.md"
    f.write_bytes(b"hello\n")
    h1 = hash_inputs([f])
    h2 = hash_inputs([f])
    assert h1 == h2
    # Sorting: keys are deterministic
    g = tmp_path / "y.md"
    g.write_bytes(b"world\n")
    out = hash_inputs([g, f])
    assert list(out.keys()) == sorted(out.keys())


def test_sha256_file_round_trip(tmp_path):
    f = tmp_path / "a.txt"
    f.write_bytes(b"hello")
    assert sha256_file(f) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
