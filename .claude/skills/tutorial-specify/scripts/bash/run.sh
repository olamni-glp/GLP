#!/usr/bin/env bash
# /tutorial-specify slash-command bash runner.
# See .claude/skills/tutorial-specify/SKILL.md.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export TUTORIAL_SPECIFY_ROOT="${TUTORIAL_SPECIFY_ROOT:-$REPO_ROOT}"

PY="${TUTORIAL_SPECIFY_PYTHON:-python}"

# Make sure the package is on the path. Editable install is the supported
# install method (`pip install -e scripts/tutorial_specify`); if that hasn't
# been done, fall back to direct PYTHONPATH for ergonomic first-run.
if ! "$PY" -c "import tutorial_specify" >/dev/null 2>&1; then
  export PYTHONPATH="${REPO_ROOT}/scripts/tutorial_specify/src:${PYTHONPATH:-}"
fi

exec "$PY" -m tutorial_specify "$@"
