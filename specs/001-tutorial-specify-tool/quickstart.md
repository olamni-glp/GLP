# Quickstart: Tutorial-Specify Tool

**Audience**: Tutorial authors generating per-chapter speckit specs for the Olamni tutorial.

## Prerequisites

- Repository checked out at the standard path.
- Python `^3.13` available on PATH.
- Dart `^3.9.4` available on PATH (the GLP REPL is invoked for code-block parse-checks).
- `GLP_ART.pdf` present at the repo root.
- `olamni/tutorial/charter.md` present and current.
- The chapter you want to process has a `chNN_plan.md` (or you are processing chs 1–4 via `ch01-04_plan.md`) with a valid `**Mode**:` header.

## First-time setup

```bash
# from repo root
cd scripts/tutorial_specify
python -m pip install -e .
cd -
```

Optional sanity check:

```bash
python -m tutorial_specify --version
```

## Generate one chapter's spec

```bash
/tutorial-specify ch04
```

Or, equivalently, the underlying CLI:

```bash
python -m tutorial_specify ch04
```

What happens:

1. The tool acquires a file lock on `specs/<NNN>-tutorial-ch04/.lock`.
2. It reads `olamni/tutorial/charter.md`, `olamni/tutorial/ch01-04_plan.md`, `olamni/tutorial/ch01-04-sources.md`, and `olamni/tutorial/ch04/ch04_tutorial.md`.
3. It reads `GLP_ART.pdf` and builds the book-page→PDF-page map (cached in the checkpoint).
4. For each book section the chapter plan references, it extracts the relevant code blocks.
5. Each extracted block is round-tripped through the GLP REPL parser; failures abort the chapter with a precise error.
6. The mode composer (`cohesive-synthesis`, `block-focused`, or `multi-actor-distillation` — read from the plan) builds the spec body.
7. `specs/<NNN>-tutorial-ch04/spec.md` is written atomically.
8. Checkpoint is marked `terminated_with: success`; the lock is released.

## Generate every chapter

```bash
/tutorial-specify all
```

Chapters run sequentially (ch01 → ch13). A chapter that hits a plan-deficiency error is skipped with an entry in the final summary; the next chapter still runs.

## Recover from context compaction

If your Claude Code session compacts mid-run and the `/tutorial-specify` invocation never finishes:

```bash
/tutorial-specify ch12 --resume
```

The tool reads the latest valid checkpoint, verifies that input content-hashes are unchanged, and continues from the recorded `current_step`. Output is byte-identical to an uninterrupted run (FR-020 / SC-005). If any input has changed since the checkpoint was written, the tool aborts and instructs you to use `--restart` instead.

## Restart from scratch

```bash
/tutorial-specify ch04 --restart
```

You will be prompted on stderr to confirm; type `y` to proceed. To skip the prompt in CI / scripted runs:

```bash
TUTORIAL_SPECIFY_FORCE=1 /tutorial-specify ch04 --restart
```

## Run the next speckit phase

Once `spec.md` is generated, proceed with the standard speckit flow:

```bash
/speckit-clarify          # optional; resolves any [NEEDS CLARIFICATION] markers
/speckit-plan             # generates plan.md, research.md, data-model.md, contracts/, quickstart.md
/speckit-tasks            # generates tasks.md
/speckit-implement        # executes tasks.md
```

## Common diagnostics

| Symptom | Cause | Fix |
|---------|-------|-----|
| `error: chapter plan missing **Mode**: header` | Chapter plan does not declare its tutorial mode (FR-007a) | Add `**Mode**: <cohesive-synthesis \| block-focused \| multi-actor-distillation>` to `chNN_plan.md` |
| `error: multi-actor-distillation declared but use-case 'X' has no boot.glp` | Plan-vs-mode inconsistency (FR-007b) | Add `boot.glp` to the use case's file list, or change the declared Mode |
| `error: REPL parse failed for block ch04-pp38-block-03` | PDF extraction garbled a code block (FR-003a) | Inspect `.checkpoint.json` for the block's text and stderr; fix the PDF source if a typesetting bug, or open an extraction bug if a `pdfplumber` issue |
| `error: input content-hash changed since checkpoint; use --restart` | Charter, plan, sources, tutorial, or PDF was edited mid-flight (FR-019) | Run `--restart` |
| `error: another invocation is processing this chapter` | File lock held by a parallel run (FR-021) | Wait for the other run to finish, or remove a stale `.lock` if no process is alive |

## Where output lives

```
specs/
└── 001-tutorial-specify-tool/         # the tool's own spec (this very feature)
└── 0NN-tutorial-chNN/                 # one directory per processed chapter
    ├── spec.md                        # the generated speckit spec
    ├── .checkpoint.json               # state file; safe to delete to force restart
    └── .lock                          # transient run lock
```

The chapter directory's `<NNN>` prefix is sequential and stable per chapter (e.g., `ch04` always lands at `0NN-tutorial-ch04` for some fixed `NNN`).
