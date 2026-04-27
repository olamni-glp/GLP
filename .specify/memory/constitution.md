<!--
SYNC IMPACT REPORT — v1.1.0 → v1.2.0
- §Development Workflow > Multi-Claude collaboration: amended to accept two
  branch patterns side by side. Ad-hoc session branches `claude/<name>-<session-id>`
  remain; speckit feature branches `<NNN>-<short-name>` are now also accepted for
  spec-driven features flowing through the speckit pipeline. Resolves the friction
  observed during /speckit-analyze of the Tutorial-Specify Tool feature
  (`001-tutorial-specify-tool`).
- Templates ⚠ pending alignment review (no changes required this revision):
  - .specify/templates/{plan,spec,tasks,checklist}-template.md
- Deferred TODOs: none.

SYNC IMPACT REPORT — v1.0.0 → v1.1.0
- New principle: VI. Tutorial Charter Compliance — tutorial code and supporting
  artifacts MUST be constructed per olamni/tutorial/charter.md.
- New section: Technology Stack — names GLP, Dart, Flutter, Python 3.13+, Bash/PowerShell.
- New paragraph in Development Workflow: REPL as the unified GLP tool (no
  separate type checker / compiler tools).
- Wording tightened across I–V to RFC 2119 (MUST / MUST NOT / SHOULD); no semantic changes.
- NON-NEGOTIABLE markers consolidated to I (Spec-First) and III (SRSW); removed
  from II (No Workarounds) and V (Test-First) per spec-kit guidance reserving the
  marker for the 1–2 principles defended under deadline pressure.
- Templates ⚠ pending alignment review (not yet edited):
  - .specify/templates/plan-template.md (Constitution Check section)
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
  - .specify/templates/agent-file-template.md
  - .specify/templates/checklist-template.md
- Deferred TODOs: none.
-->

# GLP Constitution

The Grassroots Logic Programming (GLP) project is a typed concurrent
logic-programming language with a Dart-based runtime, a Flutter multi-actor UI
orchestrator, and a corpus of ~917 `.glp` programs spanning runtime tests, book
examples, multiagent plays, and tutorial projects. This constitution defines
the non-negotiable principles, language-design authority, authorised
technology stack, and development workflow that govern all contributions.

## Core Principles

### I. Spec-First Development (NON-NEGOTIABLE)

Every code change MUST trace to a specification. The hierarchy is paper → spec
→ tests → implementation; no implementation proceeds without a corresponding
spec section. If a spec is missing, unclear, or contradictory, the spec MUST
be fixed first. Existing code MUST NOT be treated as authoritative when the
spec is silent — the spec defines correctness; code is an implementation that
may or may not be correct.

### II. No Workarounds; Bugs Reported, Not Bypassed

When a bug or unexpected behaviour is discovered, work STOPS and the bug is
reported precisely (expected vs. actual, repro steps). Workarounds,
route-arounds, catch-and-ignore, expected-to-fail markings, and structural
compensation for known defects MUST NOT be introduced. Fixes MUST be complete
and comprehensive: every error in scope is fixed, never prioritised away.

### III. SRSW Discipline (NON-NEGOTIABLE)

Single-Reader Single-Writer is a language invariant of GLP. SRSW analysis MUST
run before type checking on every load. The only sanctioned exceptions are
the anonymous writer (`_`, `_Name`), constant-typed variables, and
ground-guard relaxations as defined by the spec. A `skipSRSW` option MUST NOT
exist.

### IV. FCP Reference Architecture

The runtime follows the Flat Concurrent Prolog heap and emulator design.
Deviations — bidirectional variable pairs, tag-based dispatch, dereferencing
with path compression, suspension on readers — MUST be raised for explicit
discussion and approval before implementation. Reinventing heap mechanisms
when FCP already provides a solution is forbidden.

### V. Test-First Discipline

A baseline test run MUST be recorded before any change. The unified REPL
suite (`bash test/run_all_tests.sh`), the Dart unit tests
(`dart test` in `glp_runtime/`), and — for changes affecting the multi-actor
UI — `flutter build` in `glp_multiagent/`, MUST pass before a task is declared
done. Every bug fix MUST add a regression test; every new feature MUST add
coverage for its main use cases. Tests MUST NOT be deleted or marked
expected-to-fail to silence a defect.

### VI. Tutorial Charter Compliance

Tutorial code and supporting artifacts — per-chapter `.glp` files, actors,
plays, and Flutter tutorial entry points (`glp_multiagent/lib/main_olamni_*`)
— MUST be constructed in accordance with `olamni/tutorial/charter.md` and its
per-chapter sub-plans (`chNN/chNN_plan.md`, `chNN/chNN-sources.md`,
`chNN/chNN_tutorial.md`). The charter is the single source of truth for
tutorial scope, file layout, naming, and source-material attribution.
Tutorial work that diverges from the charter MUST NOT be merged; if the
charter is wrong, the charter is amended first, then the work proceeds.

## Language Design Authority

The GLP language definition — its primitive types, guards, system predicates,
body kernels, directives, and type-system features — MUST NOT be revised,
extended, or added to without explicit approval from the project lead. The
required sequence is: propose with rationale, wait for approval, then
implement. Reverse-engineering language behaviour from test output, or
guessing from procedure names, MUST NOT substitute for reading the spec.

## Technology Stack

Authorised technologies and their roles:

- **GLP** (`.glp` source) — the project's own typed concurrent
  logic-programming language; ~917 files across `programs/`, `glp_runtime/`,
  `AofGLP/`, and `olamni/tutorial/`. Authoritative for language semantics;
  runs in the GLP REPL (`dart run bin/glp_repl.dart`).
- **Dart `^3.9.4`** (`glp_runtime/`) — implementation language for the GLP
  runtime, REPL, type checker, partial evaluator, bytecode VM, and the
  multiagent isolate infrastructure. No Flutter dependency.
- **Dart `^3.0.0` + Flutter** (`glp_multiagent/`) — UI orchestrator for
  complex tutorials and exemplar code where multi-actor GLP code MUST be
  orchestrated. Per-tutorial entry points live at
  `glp_multiagent/lib/main_*.dart` and reference `glp_runtime` as a path
  dependency.
- **Python `^3.13`** — tooling only (build helpers, future Python actor
  bridges per `olamni/tutorial/ch13/`). New Python tooling MUST target Python
  3.13 or later.
- **Bash + PowerShell** — test scripts (`test/run_*.sh`) and
  `.specify/extensions/git/scripts/{bash,powershell}/` helpers; both shells
  MUST be supported in parity since the project runs on Windows, macOS, and
  Linux.

New third-party dependencies (Dart packages, Python libs, Flutter plugins)
MUST be added only via a spec section and the corresponding `pubspec.yaml`,
`requirements.txt`, or equivalent declaration — never ad-hoc.

## Development Workflow

**Discussion mode is the default.** No code changes, test runs, or git
operations occur while a discussion is open. The user's "stop" is absolute
and overrides hooks, in-flight cleanups, and skill flows. Implementation mode
begins only on the user's explicit signal ("discussion over", "go ahead",
"let's implement").

**The REPL is the unified GLP tool.** Loading a `.glp` file in the REPL runs
SRSW analysis → partial evaluation → type checking → compilation → execution
in one pipeline. Standalone tools (separate type checker, separate compiler)
MUST NOT be reintroduced.

**GLP code modification protocol.** `.glp` files written by the user MUST NOT
be modified without prior discussion and explicit approval. Before running or
tracing GLP code in the REPL, the file to be loaded and the goal to be
executed MUST be shown.

**Multi-Claude collaboration.** `main` is the source of truth. Two branch
patterns are accepted:

- **Ad-hoc session branches** — `claude/<name>-<session-id>`. Used for
  exploratory work and discussion-driven changes outside the speckit pipeline.
- **Speckit feature branches** — `<NNN>-<short-name>` (sequential numeric or
  timestamp prefix per `.specify/extensions/git/git-config.yml`). Used for
  spec-driven features flowing through Constitution → spec → clarify → plan →
  tasks → implement. Validated by `.specify/scripts/powershell/check-prerequisites.ps1`.

In either case, the session MAY pull from any branch, MUST push only to its
own branch, and MUST NOT merge to `main`. Only the user merges to `main`.
Commits stage only files the session worked on — `git add -A` and `git add .`
MUST NOT be used because they capture other sessions' work.

**Spec-Kit pipeline.** Constitution → spec → clarify → plan → tasks →
implement, each gated by the corresponding `/speckit.*` command. Hooks
defined in `.specify/extensions.yml` execute deterministically; sessions
MUST NOT bypass a mandatory pre-hook.

## Governance

This constitution supersedes ad-hoc practices. Amendments require explicit
approval from the project lead and a Sync Impact Report (prepended as an
HTML comment to this file) recording the version change, modified
principles, added or removed sections, and dependent templates needing
realignment.

**Versioning policy.** Semantic versioning applies to this document:
- **MAJOR** — backward-incompatible governance changes; principle removal or
  redefinition that invalidates prior compliance.
- **MINOR** — new principle or section added; materially expanded guidance.
- **PATCH** — clarifications, wording fixes, non-semantic refinements.

**Compliance review.** Every PR or merge MUST verify constitutional
compliance against the Constitution Check in `plan-template.md`. Apparent
conflicts between this constitution and another document (`CLAUDE.md`,
`DISCIPLINE.md`, per-team specs, `olamni/tutorial/charter.md`) are resolved
by the constitution; the other document is then updated by amendment to
converge.

**Version**: 1.2.0 | **Ratified**: 2026-04-27 | **Last Amended**: 2026-04-27
