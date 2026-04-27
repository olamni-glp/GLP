"""Typed exceptions raised by tutorial_specify modules.

Per Constitution Principle II (No Workarounds): each error type points to a
specific failure mode and surfaces a precise diagnostic message.
"""

from __future__ import annotations


class TutorialSpecifyError(Exception):
    """Base class for all tool errors. Maps to CLI exit code 2."""

    exit_code: int = 2


class MissingModeError(TutorialSpecifyError):
    """Chapter plan lacks the mandatory `**Mode**:` header (FR-007a)."""


class PlanDeficiencyError(TutorialSpecifyError):
    """Chapter plan has a structural deficiency (FR-007b)."""


class ConcurrentInvocationError(TutorialSpecifyError):
    """Another invocation holds the spec-dir lock (FR-021)."""


class CheckpointMismatchError(TutorialSpecifyError):
    """`--resume` invoked but input content-hashes differ from checkpoint (FR-019)."""


class ReplParseError(TutorialSpecifyError):
    """Extracted code block failed REPL parse-check (FR-003a)."""

    def __init__(
        self,
        block_id: str,
        book_pages: str,
        repl_stderr: str,
        message: str | None = None,
    ) -> None:
        self.block_id = block_id
        self.book_pages = book_pages
        self.repl_stderr = repl_stderr
        super().__init__(
            message
            or (
                f"REPL parse-check failed for block {block_id} ({book_pages}); "
                f"stderr: {repl_stderr.strip()[:200]}"
            )
        )


class PdfMissingError(TutorialSpecifyError):
    """`GLP_ART.pdf` is missing or unreadable."""


class CheckpointSchemaError(TutorialSpecifyError):
    """Checkpoint JSON does not validate against checkpoint-schema.json."""


class UserCancelledError(TutorialSpecifyError):
    """User declined the `--restart` confirmation prompt."""

    exit_code = 3


class InternalError(TutorialSpecifyError):
    """Unexpected internal error. Maps to CLI exit code 1."""

    exit_code = 1
