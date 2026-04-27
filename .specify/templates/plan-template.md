# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Dart ^3.9.4 (glp_runtime), Dart ^3.0.0 + Flutter (glp_multiagent), GLP (.glp source), Python ^3.13 (tooling) — match Constitution §Technology Stack; NEEDS CLARIFICATION otherwise]
**Primary Dependencies**: [Dart packages from pubspec.yaml; Flutter plugins; Python libs — declare every new dep, none ad-hoc per Constitution §Technology Stack]
**Storage**: [if applicable, e.g., on-disk JSON, in-memory only, GLP heap, or N/A]
**Testing**: `bash test/run_all_tests.sh` (REPL suite) + `dart test` in `glp_runtime/` + `flutter build` in `glp_multiagent/` (when UI affected) — per Constitution Principle V
**Target Platform**: [e.g., Windows + macOS + Linux desktop (Flutter); CLI (Dart on Windows/macOS/Linux); GLP REPL (any platform with Dart 3.9.4+) — NEEDS CLARIFICATION otherwise]
**Project Type**: [e.g., GLP runtime extension, GLP language feature, multiagent UI tutorial, REPL command, type-system change, build/CI tooling — NEEDS CLARIFICATION otherwise]
**Performance Goals**: [domain-specific, e.g., REPL test suite under 5 min, type-check <1s for 1k-line file, multiagent isolate spawn <100ms — NEEDS CLARIFICATION otherwise]
**Constraints**: [domain-specific, e.g., bash + PowerShell parity, no Flutter dep in glp_runtime, SRSW cannot be skipped — NEEDS CLARIFICATION otherwise]
**Scale/Scope**: [domain-specific, e.g., 917+ .glp files in corpus, 50+ Dart unit tests, 22 REPL test sections — NEEDS CLARIFICATION otherwise]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design. Source: `.specify/memory/constitution.md` v1.1.0.*

Mark each row PASS / VIOLATION (justify in Complexity Tracking) / N/A:

- **I. Spec-First Development (NON-NEGOTIABLE)**: a corresponding spec section in `docs/` exists and is current; this plan cites it. If the spec is silent or unclear, the spec is amended FIRST.
- **II. No Workarounds**: this plan introduces no try/catch-and-ignore, no expected-to-fail markings, no structural compensation for known defects. Bugs encountered during implementation HALT work for explicit triage.
- **III. SRSW Discipline (NON-NEGOTIABLE)**: any new `.glp` code respects SRSW; no `skipSRSW` paths are introduced; relaxations use only the documented mechanisms (anonymous writers, constant types, ground guards).
- **IV. FCP Reference Architecture**: heap, dereferencing, suspension, and tag dispatch follow FCP; deviations are explicitly listed and approved.
- **V. Test-First Discipline**: the unified REPL suite + `dart test` + (if UI) `flutter build` baseline is recorded BEFORE work; new tests cover bug-fix regressions and main feature paths.
- **VI. Tutorial Charter Compliance**: if this plan touches `olamni/tutorial/`, `glp_multiagent/lib/main_olamni_*.dart`, or per-chapter `.glp` files, it cites the relevant `chNN_plan.md` and `chNN-sources.md` from `olamni/tutorial/charter.md`. Divergence from charter is amended into charter FIRST.
- **Language Design Authority**: no new guard, system predicate, body kernel, directive, or type-system feature is added without prior approval cited here.
- **Technology Stack**: every dependency in this plan is in the constitution-authorised stack (GLP / Dart 3.9.4+ / Dart 3.0+ + Flutter / Python 3.13+ / Bash + PowerShell) OR is added via a declared spec section.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths. The delivered plan must not include Option labels.

  These options reflect the GLP repository's actual layout per Constitution
  §Technology Stack. Pick the one(s) the change actually touches.
-->

```text
# [REMOVE IF UNUSED] Option A: GLP runtime / language change (Dart, no Flutter)
glp_runtime/
├── lib/
│   ├── analysis/        # type checker, SRSW analyser, partial evaluator
│   ├── compiler/        # GLP → bytecode
│   ├── bytecode/        # VM, runner, opcodes
│   ├── runtime/         # heap, scheduler, cells, terms
│   └── multiagent/      # isolate manager, boot loader, relay
├── bin/
│   └── glp_repl.dart    # the unified GLP tool (Constitution §Workflow)
└── test/                # 50+ Dart unit tests

programs/                # GLP corpus (typed_book, cssg, cssn, bonds, lib)
test/                    # bash REPL test scripts (run_all_tests.sh, etc.)

# [REMOVE IF UNUSED] Option B: Multi-actor UI tutorial (Flutter)
glp_multiagent/
├── lib/
│   ├── main.dart                          # router
│   ├── main_<scenario>.dart               # per-scenario entry point
│   ├── mad_router.dart
│   └── isolate_protocol.dart
└── pubspec.yaml         # Dart ^3.0.0 + Flutter; path-deps glp_runtime/

olamni/tutorial/<chNN>/  # per-chapter .glp source (when applicable)

# [REMOVE IF UNUSED] Option C: Tutorial chapter (under charter)
olamni/tutorial/charter.md            # MUST be cited per Principle VI
olamni/tutorial/chNN/
├── chNN_plan.md
├── chNN-sources.md
├── chNN_tutorial.md
└── <use-case>/{self,agent,network,actors,boot}.glp

# [REMOVE IF UNUSED] Option D: Tooling (Python ^3.13)
scripts/<tool>/                       # Python tooling per Constitution §Technology Stack
```

**Structure Decision**: [Document the selected option(s) and reference the real
directories captured above. Cite the constitution principles this layout
respects.]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
