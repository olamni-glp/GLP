"""Shared pytest fixtures and helpers."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def isolated_repo_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Provide a fresh tmp dir as the simulated repo root for tests."""
    monkeypatch.setenv("TUTORIAL_SPECIFY_ROOT", str(tmp_path))
    return tmp_path
