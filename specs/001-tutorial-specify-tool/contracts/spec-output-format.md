# Contract: Generated `spec.md` Output Format

**Date**: 2026-04-27
**Spec**: [../spec.md](../spec.md)

This contract defines the structural shape of every `spec.md` produced by `/tutorial-specify`. Downstream `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement` rely on these structures.

## Top-level sections (in order)

1. Optional `<!-- SYNC IMPACT REPORT … -->` HTML comment (FR-023) — present only when re-run with changed inputs.
2. `# Feature Specification: <Tutorial Chapter NN — <book chapter title>>` heading.
3. Header block:
   - `**Feature Branch**: \`<NNN>-tutorial-chNN\``
   - `**Created**: YYYY-MM-DD` (UTC, deterministic per run inputs)
   - `**Status**: Draft`
   - `**Input**: User description: …`
   - `**Constitution**: \`.specify/memory/constitution.md\` v<x.y.z> — Principle VI (Tutorial Charter Compliance) governs this spec.`
   - `**Tutorial Mode**: <cohesive-synthesis | block-focused | multi-actor-distillation>` (FR-007)
4. `## Clarifications` (empty placeholder; downstream `/speckit-clarify` populates).
5. `## User Scenarios & Testing` (mandatory) — at least one P1 user story per tutorial file or use case from the chapter plan, with acceptance scenarios that cite book pages.
6. `## Requirements > Functional Requirements` — every code-bearing requirement carries an inline citation in the canonical format.
7. `## Requirements > Key Entities` — only when the chapter introduces typed unions or new domain entities (e.g., chs 7–13 multi-actor plays).
8. `## Success Criteria > Measurable Outcomes` — at least one criterion is "tutorial code loaded into the GLP REPL succeeds (or suspends, where the chapter plan declares suspended is acceptable) on the demo goal" (FR-010).
9. `## Assumptions` — MUST cite `olamni/tutorial/charter.md`, `olamni/tutorial/chNN/chNN_plan.md` (or `ch01-04_plan.md`), `chNN-sources.md`, and `chNN_tutorial.md` (FR-011).

## Citation format (FR-003)

Every code-bearing FR MUST end with one of these forms:

| Form | Example |
|------|---------|
| Page range only | `(book pp 37–40 §4.3)` |
| Page range + program | `(book p 37 §4.3, Program 1.1)` |
| Section only (when book has no page-precise reference, e.g., ch 6 TOC) | `(§6.5; sourced from book §4.2 Buffered Communication, book p 34)` |

PDF page numbers MUST NOT appear anywhere in the output.

## Per-mode shape

### Mode A: cohesive-synthesis

- One single-file user story per chapter, e.g., "Reader of §X.Y can load `chXX-ex-NN-<topic>.glp` and run the demo goal."
- Functional Requirements grouped by book section with citations after each.
- File-level scope statement enumerates every Program woven in.

### Mode B: block-focused

- One user story per substantial book Program, e.g., "Reader of Program N.N can load `chXX-ex-NN-<short-name>.glp` and run the demo goal."
- One Functional Requirement per book Program, citing its book page.
- File-level scope statement names the single book Program covered.

### Mode C: multi-actor-distillation

- One user story per use case (e.g., `play_<scenario>`).
- Functional Requirements per use case grouped under headers naming the use case.
- Key Entities section lists the play's typed unions (e.g., `AgentMsg`, `Response`).
- Project shape MUST be `chNN/<use-case>/{self,agent,network,actors,boot}.glp`.
- If the chapter plan declares a Flutter entry point, an FR MUST require a `glp_multiagent/lib/main_olamni_chNN_<use-case>.dart` derived from the chapter plan's named template.

## Determinism rules

- Section order is fixed (above).
- Within a section, items appear in the order they appear in the chapter plan; ties broken by lexicographic file path.
- Timestamps in the header are UTC and derived from the latest input content-hash (not wall-clock); identical inputs → identical headers.
- Set/dict iteration is sorted before serialisation.

## Negative requirements (the spec MUST NOT contain)

- PDF page numbers.
- Any code block extracted from `GLP_ART.pdf` whose `ReplParseResult.passed` is `false`.
- Any reference to memory, training data, prior model knowledge, or summaries of the book.
- Implementation-language commitments beyond what the chapter plan declares (e.g., specific Dart library names).
- `[NEEDS CLARIFICATION]` markers exceeding 3 per FR-022 and the spec-quality checklist.
