---
description: "Generate buildkit-compliant specs for olamni/tutorial chapters by extracting from GLP_ART.pdf and following the tutorial charter"
---

# Tutorial-Specify Skill

Wraps the `tutorial-specify` Python CLI as a Claude Code slash command. The
authoritative contract is in
[`specs/001-tutorial-specify-tool/contracts/cli-interface.md`](../../../specs/001-tutorial-specify-tool/contracts/cli-interface.md).

## Usage

```
/tutorial-specify <chapter> [--resume | --restart]
```

- `<chapter>`: one of `ch01`, `ch02`, …, `ch13`, or `all`
- `--resume`: resume from the latest checkpoint at
  `specs/<NNN>-tutorial-chNN/.checkpoint.json` (FR-018)
- `--restart`: wipe the checkpoint and rerun from scratch (interactive
  confirmation on stderr unless `TUTORIAL_SPECIFY_FORCE=1`)

## What it does

For each chapter:

1. Reads `olamni/tutorial/charter.md` and the per-chapter `chNN_plan.md`,
   `chNN-sources.md`, `chNN_tutorial.md` (`ch01-04_plan.md` for chs 1–4).
2. Reads the chapter's `**Mode**:` declaration (`cohesive-synthesis`,
   `block-focused`, or `multi-actor-distillation`); aborts if missing
   (FR-007a) or inconsistent with the file list (FR-007b).
3. Extracts code-bearing content directly from `GLP_ART.pdf` at the
   project root (FR-002) — never from model memory or training.
4. Round-trips every extracted code block through the GLP REPL
   parser; aborts the chapter on parse failure (FR-003a).
5. Composes a buildkit-compliant `spec.md` under
   `specs/<NNN>-tutorial-chNN/spec.md`, with citations in the canonical
   `book pp X–Y §A.B[, Program N.N]` format (FR-003).
6. Writes a checkpoint to `.checkpoint.json` after every meaningful step
   so the run is resumable across context compaction (FR-016, FR-020).

## Execution

The skill dispatches to bash on POSIX or PowerShell on Windows:

- Bash: `.claude/skills/tutorial-specify/scripts/bash/run.sh "$@"`
- PowerShell: `.claude/skills/tutorial-specify/scripts/powershell/run.ps1 @args`

Both wrappers invoke `python -m tutorial_specify ...` with passthrough
arguments after setting `TUTORIAL_SPECIFY_ROOT` to the repo root.

## Exit codes

| Code | Meaning |
|------|---------|
| 0    | Success |
| 1    | Internal error |
| 2    | Input deficiency / PDF missing / lock contention |
| 3    | User cancelled `--restart` |

## Constitution

`.specify/memory/constitution.md` v1.2.0 — Principle V (Test-First, REPL gate)
and Principle VI (Tutorial Charter Compliance) govern every generated spec.
