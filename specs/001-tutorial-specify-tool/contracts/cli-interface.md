# Contract: CLI Interface

**Date**: 2026-04-27
**Spec**: [../spec.md](../spec.md)

This contract defines the externally observable command-line interface of `/tutorial-specify` and the underlying Python tool. It is the source of truth for argument parsing, exit codes, and side effects.

## Slash command

```
/tutorial-specify <chapter> [--resume | --restart]
```

## Underlying CLI

```
python -m tutorial_specify <chapter> [--resume | --restart]
```

The slash-command bash and PowerShell wrapper scripts dispatch to the underlying CLI with identical argument forwarding.

## Positional argument

| Name | Required | Type | Constraints |
|------|----------|------|-------------|
| `chapter` | yes | string | One of `ch01`, `ch02`, …, `ch13`, or the literal `all` |

## Optional flags

| Flag | Description | Mutually exclusive with |
|------|-------------|--------------------------|
| `--resume` | Resume from the latest valid checkpoint at `specs/<NNN>-tutorial-chNN/.checkpoint.json`. Aborts if input content-hashes do not match the recorded hashes. | `--restart` |
| `--restart` | Delete any existing checkpoint and run from scratch. Requires interactive confirmation (`y/N`) on stderr unless `TUTORIAL_SPECIFY_FORCE=1` is set. | `--resume` |

If neither flag is given and a checkpoint already exists for the chapter, the tool prints a clear error explaining the choice between `--resume` and `--restart` and exits 2 — never silently picking one.

## Side effects

The tool MAY write only under:

- `specs/<NNN>-tutorial-chNN/spec.md`
- `specs/<NNN>-tutorial-chNN/.checkpoint.json`
- `specs/<NNN>-tutorial-chNN/.lock`
- `specs/<NNN>-tutorial-chNN/.checkpoint.json.tmp` (transient, removed by atomic rename)

The tool MUST NOT write to or modify:

- `olamni/tutorial/**` (charter, chapter plans, sources, tutorials)
- `GLP_ART.pdf`
- `.specify/**`
- Any other repository file

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success — the spec for the chapter (or every chapter, under `all`) was generated cleanly |
| 1 | Internal error (unexpected exception, dependency missing, PDF library failure) |
| 2 | Input deficiency — chapter plan invalid (FR-007a / FR-007b), PDF extraction failed REPL parse-check (FR-003a), checkpoint state invalid for `--resume`, or concurrency lock held |
| 3 | User-cancelled `--restart` confirmation |

When invoked with `all`, the exit code is `0` only if **every** chapter exited 0; if any chapter exits 2 or 3, the overall exit code is 2 and the per-chapter summary on stdout indicates which chapters succeeded vs. were skipped.

## Standard streams

- **stdout**: Per-step progress lines (one line per completed checkpoint step) and a final summary block. Machine-parseable when `--json` is later added; for v1, human-readable.
- **stderr**: Errors, warnings, and the `--restart` confirmation prompt. Errors include the chapter id and a precise pointer to the offending file or block.
- **No prompts on stdout**: per FR-007b "tool MUST NOT prompt user interactively" — the only interactive prompt anywhere is the `--restart` confirmation, on stderr.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `TUTORIAL_SPECIFY_ROOT` | repo root via `git rev-parse --show-toplevel` | Override repo root for tests |
| `TUTORIAL_SPECIFY_PDF` | `<root>/GLP_ART.pdf` | Override PDF path for tests |
| `TUTORIAL_SPECIFY_FORCE` | unset | When `=1`, skip `--restart` confirmation prompt |
| `TUTORIAL_SPECIFY_REPL_TIMEOUT_S` | `30` | Per-block REPL parse timeout in seconds |

## Sample invocations

```bash
# Generate ch04 spec from scratch
/tutorial-specify ch04

# Resume after compaction killed a prior run
/tutorial-specify ch12 --resume

# Wipe and regenerate ch06 (interactive confirmation on stderr)
/tutorial-specify ch06 --restart

# Generate every chapter sequentially
/tutorial-specify all
```

## Idempotence guarantee

Two successive invocations on the same chapter with no input changes (no edits to charter, chapter plan, sources, tutorial, or `GLP_ART.pdf`) MUST produce a `spec.md` byte-identical to the previous run (FR-022, SC-004). If you observe any byte difference, that is a bug.
