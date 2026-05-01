# Data Model — ch06 (Typed Programming)

**Phase 1 output**. Documents the entities, attributes, relationships, and state transitions for the ch06 tutorial. Cites spec.md FRs and plan.md.

## Entities

### Exercise

A self-contained tutorial unit identified by `exercise-NN` (NN ∈ 01..05).

**Attributes**:
- `id`: integer (01..05).
- `section_heading`: string (§6.1, §6.2, §6.3, §6.4, §6.5).
- `short_name`: string (`difference-lists`, `typed-quicksort`, `equators-emergency-brake`, `bidirectional-communication`, `buffered-communication`). Locked per R-009.
- `source_chapter`: integer (3, 4, or 5).
- `source_section`: string (e.g., `§4.3.7`, `§5.6`, `§4.4.4`, `§3.2`, `§4.2.12+§4.2.13`).
- `source_page_range`: string (e.g., `pp 38–39`, `p 51`, `p 42`, `p 23`, `pp 34–35`).
- `glp_file`: filename `ch-06-ex-NN-<short-name>.glp` (single file per exercise).
- `tutorial_file`: filename `ex-NN-tutorial.md`.
- `trace_file`: filename `ex-NN-repl-trace.md`.
- `primary_demo_goal`: string (locked at /speckit-implement T006-equivalent).
- `inspection_goals`: list of 3 strings (locked at /speckit-implement T006-equivalent).
- `locked_bindings`: dict `{goal: binding}` (4 entries: 1 primary + 3 inspection); empirically verified at /speckit-implement.
- `state`: enum `{not yet implemented, files written, pending review, approved}`.
- `approved_date`: ISO date string `YYYY-MM-DD` (only when state = `approved`).

**Relationships**:
- Each Exercise has exactly ONE Source Program (1:1).
- Each Exercise has exactly ONE Cross-chapter Relationship (1:1).
- Each Exercise has exactly ONE Approval Gate to ex-(N+1), except ex-05 (4 gates total for 5 exercises).

**State transitions**:
```
not yet implemented
        ↓ (implementer writes .glp + tutorial.md + trace.md)
files written
        ↓ (project owner reviews; updates status block)
pending review
        ↓ (project owner approves; status block flips)
approved YYYY-MM-DD
```

### Source Program

The earlier-chapter byte-exact PDF block from which an Exercise's clauses are transcribed.

**Attributes**:
- `chapter`: integer (3, 4, or 5).
- `section`: string (e.g., `§4.3.7`).
- `page_range`: string (e.g., `pp 38–39`).
- `program_identifier`: string from `chXX-sources.md` index (e.g., `4.3.7 flatten/2 + flatten_acc/3`, `Program 5.6`, `4.4.4 control run/5`, `§3.2 inline channel ops`, `4.2.12 bb/0` + `4.2.13 bb_test/0`).
- `clause_count`: integer (~5 for flatten, ~6 for quicksort, ~7 for control MI, ~6 for channel ops, ~4 for bb).
- `byte_exact_text`: the literal PDF text (transcribed at /speckit-implement T-equivalent against PDF).

**Relationships**:
- Each Source Program belongs to exactly ONE Exercise (1:1).
- Each Source Program has its byte-exact text re-verified during /speckit-implement (per FR-003 + ch01–ch05 lesson — `chXX-sources.md` files have drifted by single characters).

### Approval Gate

A predicate `exercise-NN: approved YYYY-MM-DD` in `ch06_tutorial.md`'s status block; gates ex-(NN+1) work.

**Attributes**:
- `from_exercise`: integer (NN).
- `to_exercise`: integer (NN+1).
- `predicate`: regex `^- exercise-{NN}: approved [0-9]{4}-[0-9]{2}-[0-9]{2}$` matching the status-block line.
- `state`: enum `{not yet satisfied, satisfied}`.

**Cardinality**: 4 gates total (ex-01→ex-02, ex-02→ex-03, ex-03→ex-04, ex-04→ex-05).

**Relationships**:
- Each Gate is satisfied by exactly ONE Exercise being approved.
- The implementer's gate-grep at the start of each ex-(N+1) work checks `grep -E "^- exercise-0{NN}: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch06/ch06_tutorial.md` returns ≥1 match.

### Cross-chapter Relationship (synthesis-from-earlier-chapters)

Per R-008, the documented link between a ch06 Exercise and its earlier-chapter Source Program; recorded in three sites per FR-014.

**Attributes**:
- `ch06_exercise_id`: integer (01..05).
- `source_chapter`: integer (3, 4, 5).
- `source_section`: string.
- `source_page_range`: string.
- `source_program_identifier`: string.
- `documentation_sites`: list of 3 — `{glp_header, signpost_prose, top_level_footnote}`.

**State transitions** (per documentation site):
```
not yet documented
        ↓ (writer adds the cross-reference)
documented
```

**Cardinality**: 5 relationships (one per Exercise); each relationship MUST have all 3 documentation sites populated for the Exercise to advance to `approved` state.

### Chapter Tutorial

The chapter-level signpost `olamni/tutorial/ch06/ch06_tutorial.md`.

**Attributes**:
- `path`: `olamni/tutorial/ch06/ch06_tutorial.md`.
- `intro_section`: prose explaining the chapter's stub-source-and-synthesis nature.
- `build_instructions`: REPL build commands (inherited from ch01–ch05 boilerplate).
- `exercise_links`: list of 5 entries, one per exercise, with one-line summaries.
- `synthesis_explanation`: plain prose (per FR-010 + R-008).
- `status_block`: structured 5-line block per `contracts/status-block-format.md`.

**State transitions**: rewritten incrementally as exercises advance; final state when all 5 are approved.

### Top-level Index

The chapter-by-chapter entry point `olamni/tutorial/tutorial.md`.

**Attributes**:
- `path`: `olamni/tutorial/tutorial.md`.
- `ch06_row`: structured row with status (`planned`, `pending review (YYYY-MM-DD)`, `implemented YYYY-MM-DD`).
- `ch06_footnote`: per FR-014 third site — synthesis-explanation footnote.

**State transitions** (ch06 row):
```
planned
   ↓ (any ex-NN lands)
pending review (YYYY-MM-DD)
   ↓ (all 5 approved)
implemented YYYY-MM-DD
```

## Validation Rules

- **VR-1** (FR-001): exactly 5 Exercises exist (NN ∈ 01..05).
- **VR-2** (FR-002 + FR-003): each Exercise's `glp_file` clause body is byte-equal to its Source Program's `byte_exact_text`. Type/procedure declarations introduced fresh at §6.x are NOT byte-exact (per Q2 deferral).
- **VR-3** (FR-004): each Exercise's `glp_file` MUST have a header comment block citing both `source_chapter`/`source_section`/`source_page_range`/`source_program_identifier` AND `section_heading`, with explicit "synthesised from <source>" prose.
- **VR-4** (FR-005): each clause in each `glp_file` MUST have a `%%` paraphrase comment.
- **VR-5** (FR-006): each Exercise's 4-goal session (1 primary + 3 inspection) MUST collectively exercise every clause of every Program in the exercise.
- **VR-6** (FR-007): each goal's binding is empirically verified at /speckit-implement; mismatch is halt-and-report per FR-013.
- **VR-7** (FR-008): pairwise gate predicate satisfied for every (NN, NN+1) before ex-(NN+1) work begins.
- **VR-8** (FR-014): all 3 cross-chapter documentation sites populated before Exercise advances to `approved`.
- **VR-9** (FR-015): ch06 PDF page (book p 53) byte-exactly re-read at /speckit-implement T001-equivalent; halt per FR-013 if stub state has changed.
- **VR-10** (FR-018 + SC-006): each `glp_file` passes the live type-checker after declarations are added; halt per FR-013 if rejected.

## Inheritance from ch01–ch05

The following entity definitions are inherited unchanged:
- Exercise's `state` enum (from ch02 contract; extended in ch05 to include `pending review`).
- Approval Gate predicate regex (from ch01).
- Chapter Tutorial structure (from ch01).
- Top-level Index structure (from ch01; updated incrementally per ch01–ch05 pattern).

The following are NEW for ch06 (per R-008):
- Cross-chapter Relationship of type `synthesis-from-earlier-chapters` (distinct from ch04 inversion / ch05 typed↔untyped / ch02 forward-import).
- Top-level Index `ch06_footnote` (FR-014 third site — first chapter to require a row footnote).
