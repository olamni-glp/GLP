# tutorial-specify

Python `^3.13` tool that generates speckit-compliant `spec.md` files for each
chapter of the olamni tutorial, sourcing all code-bearing content from
`GLP_ART.pdf` (never from model memory or training).

## Authoritative spec

`specs/001-tutorial-specify-tool/` (in this repo) holds:
- `spec.md` — feature specification
- `plan.md` — implementation plan (Constitution v1.2.0 compliant)
- `research.md` — design decisions
- `data-model.md` — entities + lifecycle
- `contracts/` — CLI contract, output-format contract, checkpoint JSON Schema
- `quickstart.md` — invocation guide and diagnostics
- `tasks.md` — task list (this implementation)

Read those before editing the code.

## Install

```bash
cd scripts/tutorial_specify
python -m pip install -e .[dev]
```

## Usage

Either via the Claude Code skill:

```
/tutorial-specify ch04
/tutorial-specify ch12 --resume
/tutorial-specify all
```

…or directly:

```bash
python -m tutorial_specify ch04
```

See `specs/001-tutorial-specify-tool/quickstart.md` for the diagnostics matrix.

## Run tests

```bash
cd scripts/tutorial_specify
pytest                              # unit + integration
```

Tests that require `dart` (REPL parse-check tests, full end-to-end integration
tests) skip gracefully when dart is not on PATH.

## Build the synthetic test PDF

```bash
cd scripts/tutorial_specify/tests/fixtures
python build_mock_pdf.py
```

This produces `glp_art_mock.pdf` — a synthetic 4-page PDF with TeX-typeset
GLP-shaped code blocks, used by the test suite. Per `/speckit-analyze` Q6/A,
this avoids any copyright exposure from the real `GLP_ART.pdf`.

## Constitution

`.specify/memory/constitution.md` v1.2.0. Principle I (Spec-First),
Principle V (Test-First), and Principle VI (Tutorial Charter Compliance)
govern this code.
