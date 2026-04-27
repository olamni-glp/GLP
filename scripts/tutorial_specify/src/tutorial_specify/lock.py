"""Per-spec-dir file lock (FR-021).

Wraps `filelock.FileLock` to provide a context manager that raises a typed
`ConcurrentInvocationError` on contention, with a helpful message pointing
to the offending lock file.
"""

from __future__ import annotations

from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

from filelock import FileLock, Timeout

from tutorial_specify.errors import ConcurrentInvocationError


@contextmanager
def acquire_spec_dir_lock(spec_dir: Path, timeout: float = 0.0) -> Iterator[None]:
    """Acquire the lock at `<spec_dir>/.lock`.

    Args:
        spec_dir: directory under `specs/` for the chapter being processed.
        timeout: seconds to wait; 0.0 = fail immediately (default).

    Raises:
        ConcurrentInvocationError: if the lock is already held.
    """
    spec_dir.mkdir(parents=True, exist_ok=True)
    lock_path = spec_dir / ".lock"
    lock = FileLock(str(lock_path), timeout=timeout)
    try:
        lock.acquire()
    except Timeout as exc:
        raise ConcurrentInvocationError(
            f"another invocation is processing this chapter "
            f"(lock held at {lock_path}); wait for it to finish or remove the "
            f"stale lock file if no process is alive"
        ) from exc
    try:
        yield
    finally:
        lock.release()
