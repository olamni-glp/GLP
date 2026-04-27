"""Unit tests for tutorial_specify.lock (T026, FR-021)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tutorial_specify.errors import ConcurrentInvocationError
from tutorial_specify.lock import acquire_spec_dir_lock


def test_lock_acquired_and_released(tmp_path):
    spec = tmp_path / "spec"
    with acquire_spec_dir_lock(spec):
        assert (spec / ".lock").exists()
    # After release, the file may still exist (filelock doesn't always remove
    # the file), but a new acquisition is allowed.
    with acquire_spec_dir_lock(spec):
        pass


def test_concurrent_acquisition_raises(tmp_path):
    spec = tmp_path / "spec"
    with acquire_spec_dir_lock(spec, timeout=0.0):
        with pytest.raises(ConcurrentInvocationError):
            with acquire_spec_dir_lock(spec, timeout=0.0):
                pass
