# Phase 1 Data Model — Olamni Tutorial Chapter 5

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-30

This file enumerates the entities introduced (or extended) by this feature, their attributes, relationships, validation rules, and state transitions. It is documentation of pure-Markdown / pure-`.glp` artefacts; there is no database, no API surface, no in-memory runtime model. The "entities" here are file artefacts with structural contracts.

---

## Entity: Exercise (chapter-5 variant)

A subdirectory under `olamni/tutorial/ch05/` named `exercise-NN/` for `NN ∈ 01..08` (per Clarifications Q1 lock = Option A).

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `dir_name` | string | filesystem | `exercise-NN` for `NN ∈ 01..08` |
| `glp_files` | list[Path] | filesystem | 1 `.glp` for ex-01..ex-06; 2 `.glp` for ex-07 + ex-08 (failing + corrected) per R-009 |
| `tutorial_md` | Path | filesystem | `ex-NN-tutorial.md` learner step-through |
| `trace_md` | Path | filesystem | `ex-NN-repl-trace.md` verbatim REPL session |
| `status` | enum | `ch05_tutorial.md` status block | `not yet implemented` / `pending exercise-N approval` / `pending review` / `approved YYYY-MM-DD` |
| `sub_section_group` | enum | derived from spec Q1 | `Foundations` (ex-01, ex-02, ex-03) / `Mode-checking-flow` (ex-04, ex-05) / `Flagship` (ex-06) / `Negatives` (ex-07, ex-08) |
| `exercise_kind` | enum | NEW for ch05 | `type-only` (ex-01, ex-02) / `procedure-decl-only` (ex-03) / `full-program` (ex-04, ex-05, ex-06) / `negative` (ex-07, ex-08) |
| `programs_grouped` | list[Program] | derived from spec Q1 | The PDF Programs covered by this exercise (per Q1 locked list) |
| `helpers` | list[Clause] | derived from R-012 + T006 approval | Helper unit-clauses or stub body — non-empty for `type-only` / `procedure-decl-only` kinds; empty for others |

**Programs-per-exercise locked distribution** (per Q1):

| # | Sub-section | Filename(s) | Kind | Programs |
|---|---|---|---|---|
| ex-01 | §5.1 | `ch-05-ex-01-type-definitions.glp` | type-only | `Bit ::= 0 ; 1.` + `Nat ::= 0 ; s(Nat).` + `NumList ::= [] ; [Number \| NumList].` + helpers |
| ex-02 | §5.2 | `ch-05-ex-02-built-in-types.glp` | type-only | `List ::= [] ; [Any \| List].` + helpers |
| ex-03 | §5.3 | `ch-05-ex-03-procedure-declaration.glp` | procedure-decl-only | `procedure merge(List?, List?, List).` + 1–2-clause stub body |
| ex-04 | §5.4 | `ch-05-ex-04-mode-checked-merge.glp` | full-program | `List` (inline; per Q4) + `procedure merge(List?, List?, List).` + 3 clauses (with Q5 `?`-additions to body `Ys` → `Ys?`) + `%%` mode-check walk-through |
| ex-05 | §5.5 | `ch-05-ex-05-counter-response-slot.glp` | full-program | `CounterMsg` (with embedded `show(Number?)` consume mode) + `CounterStream` + `procedure counter(CounterStream?, Number?).` (per Q4: arg 2 is `Number?`) + response-slot clause with guard `number(State?) | counter(S?, State?).` (per Q6) |
| ex-06 | §5.6 | `ch-05-ex-06-typed-quicksort.glp` | full-program | `NumList` (inline, duplicated from ex-04) + `procedure quicksort/2` + `procedure qsort/3` + `procedure partition/4` + 6 clauses |
| ex-07 | §5.7.1 | `ch-05-ex-07-type-error-failing.glp` + `ch-05-ex-07-type-error-corrected.glp` | negative | `foo/1` failing form (load MUST FAIL) + corrected form |
| ex-08 | §5.7.2 | `ch-05-ex-08-mode-error-failing.glp` + `ch-05-ex-08-mode-error-corrected.glp` | negative | `bar/2` failing form (load MUST FAIL) + corrected `bar(X, Y?) :- Y := X? + 1.` |

**Validation rules**:

- `dir_name` MUST exist on disk only when status is `pending …`, `pending review`, or `approved …`. Status `not yet implemented` requires the dir to NOT exist.
- `glp_files` count MUST equal 1 for ex-01..ex-06 and 2 for ex-07 + ex-08 per R-009.
- `tutorial_md` and `trace_md` MUST both exist when status is `approved`.
- Each `.glp` file MUST conform to `contracts/glp-file-format.md` (extended for ch05 with helper-clause discipline + negative-form discipline).
- Each `trace_md` MUST conform to `contracts/trace-file-format.md` (extended for ch05 with negative 2-phase trace structure).
- `programs_grouped` MUST match the Q1 lock exactly; deviation requires Clarifications amendment per FR-013.
- `helpers` are EMPTY for `full-program` and `negative` exercises; NON-EMPTY for `type-only` and `procedure-decl-only` exercises and approved at /speckit-implement T006-equivalent per R-012.
- For `negative` exercises: the failing-form `.glp` MUST FAIL TO LOAD with a captured type-error or mode-error message; the corrected-form `.glp` MUST load successfully with `✓ Loaded:`.

**State transitions**:

```
[ not yet implemented ]
        │
        │ (within-group sequential implementation; predecessor in same group complete OR first-in-group + group's predecessor-group approved)
        ▼
[ pending review ]
        │
        │ (project owner approves the GROUP; all exercises in the group flip together)
        ▼
[ approved YYYY-MM-DD ]
```

For ex-01: predecessor is the chapter signpost itself; transitions directly from `not yet implemented` → `pending review` (after ex-01 + ex-02 + ex-03 all written) → `approved YYYY-MM-DD` (when Foundations group approved). For ex-04+: predecessor is the prior group fully approved + within-group order honoured.

---

## Entity: Sub-section group (chapter-5 NEW grouping; inherits ch04 group-gate pattern)

A logical grouping of exercises by book sub-section. Four groups govern this chapter:

| Group | Exercises | Approval gate to enter | Approval gate to exit |
|---|---|---|---|
| Foundations | ex-01, ex-02, ex-03 | Chapter signpost exists + R-006 type-checker verification passes | All Foundations exercises approved → unblocks Mode-checking-flow |
| Mode-checking-flow | ex-04, ex-05 | Foundations fully approved | All Mode-checking-flow exercises approved → unblocks Flagship |
| Flagship | ex-06 (single) | Mode-checking-flow fully approved | ex-06 approved → unblocks Negatives |
| Negatives | ex-07, ex-08 | Flagship approved + R-006 re-verification (typically no-op) | All Negatives exercises approved → chapter complete |

**Validation rules**:

- The group's exit gate is satisfied iff ALL exercises in the group have status `approved YYYY-MM-DD` in the per-exercise status block.
- The group's entry gate is checked at the start of each in-group exercise (per FR-008 grep contract: `grep -cE "^- exercise-(NN|MM|...): approved" ch05_tutorial.md` returns count equal to the predecessor group's exercise count).
- Within-group exercises are implemented sequentially in order; concurrent in-group implementation is NOT allowed (single implementer assumption).
- The Flagship group has a single exercise (ex-06); its "exit gate" is trivially "ex-06 approved".
- Foundations gate has an additional pre-condition: R-006 type-checker verification MUST pass before any Foundations exercise begins. ch05 work cannot proceed against a broken type-checker.

---

## Entity: Chapter Tutorial (chapter-5 variant)

The `olamni/tutorial/ch05/` directory.

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `path` | Path | filesystem | `olamni/tutorial/ch05/` |
| `signpost` | Path | filesystem | `ch05_tutorial.md` (note **underscore**) |
| `sources_index` | Path | filesystem | `ch05-sources.md` (existing, committed in `592d89e3`) |
| `input_prompt` | Path | filesystem | `ch05-specification-input-prompt.md` (already created on this branch) |
| `deprecated_spec_copy` | Path | filesystem | `spec-rev-eng-input/ch05-DEPRECATED-spec.md` (existing) |
| `exercises` | list[Exercise] | filesystem | 8 subdirs |
| `cross_chapter_relationships_note` | string | `ch05_tutorial.md` body | plain-prose explanation of typed `merge/3` ↔ ch04 untyped `merge/3` AND typed `counter/2` ↔ ch04 untyped `counter/1` |
| `group_structure_note` | string | `ch05_tutorial.md` body | plain-prose outline of the 4 sub-section groups + 3 boundary gates |
| `negative_exercise_contract_note` | string | `ch05_tutorial.md` body | NEW for ch05 — explicit prose stating ex-07 + ex-08 are MEANT to fail to load with documented errors |

**Validation rules**:
- `signpost` filename uses underscore (`ch05_tutorial.md`).
- `signpost` MUST contain the cross-chapter relationships note.
- `signpost` MUST contain the group-structure note.
- `signpost` MUST contain the negative-exercise contract note (NEW for ch05).
- `signpost` MUST contain the per-exercise 8-line status block per Q3 + `contracts/status-block-format.md`.
- `input_prompt` MUST already exist before `/speckit-specify` runs (it does as of branch creation).
- `deprecated_spec_copy` MUST NOT be edited.

---

## Entity: Top-level Tutorial Index (extended)

The `olamni/tutorial/tutorial.md` file.

**Attributes**: as defined in ch01/ch02/ch03/ch04 data-model.md. For ch05:

- A row for chapter 5 already exists from prior implementations (added as `planned`).
- This implementation flips the ch05 row from `planned` to `pending review (YYYY-MM-DD)` after the Foundations group approves.
- Once all 8 exercises (4 groups) approve, the row flips to `implemented YYYY-MM-DD`.
- Chapters 6–13 stay marked `planned`.

---

## Entity: Approval Gate (chapter-5 instance)

Three procedural gates govern this chapter's progression. Inherits ch04 group-boundary pattern — NOT pairwise.

| Gate | Predecessor group | Block on | Format |
|---|---|---|---|
| Foundations→Mode-checking-flow gate | Foundations (ex-01 + ex-02 + ex-03) | status block shows ALL 3 Foundations exercises approved | greppable: `grep -cE "^- exercise-(01\|02\|03): approved" ch05_tutorial.md` returns 3 |
| Mode-checking-flow→Flagship gate | Mode-checking-flow (ex-04 + ex-05) | status block shows BOTH Mode-checking-flow exercises approved | greppable: `grep -cE "^- exercise-(04\|05): approved" ch05_tutorial.md` returns 2 |
| Flagship→Negatives gate | Flagship (ex-06) | status block shows ex-06 approved | greppable: `grep -cE "^- exercise-06: approved" ch05_tutorial.md` returns 1 |

The group-internal "gates" are NOT formal gates — within-group exercises proceed sequentially without pause for approval (FR-009).

Pre-Foundations precondition (NEW for ch05): R-006 type-checker verification MUST pass before any Foundations exercise begins. This is technically not a "gate" in the same sense (no status-block line), but is enforced procedurally as a pre-condition documented in T001-equivalent.

---

## Entity: Cross-chapter Relationship (NEW for ch05; distinct from ch04's Cross-chapter Inversion)

Two pedagogical relationships between ch05 typed procedures and ch04 untyped predecessors. NOT cross-chapter imports (no byte-exact code sharing).

| Field | ex-04 instance | ex-05 instance |
|---|---|---|
| `ch05_exercise` | ex-04 | ex-05 |
| `ch05_procedure` | typed `merge/3` (3 clauses, mode-declared with `List` per Q4 + Q5 `?`-additions) | typed `counter/2` (1 clause with guard + body, mode-declared with `Number?` per Q4 + full clause body per Q6) |
| `ch05_section` | §5.4, p 49 | §5.5, p 50 |
| `ch04_exercise_predecessor` | ex-04 (per ch04 spec) | ex-06 (per ch04 spec) |
| `ch04_procedure_predecessor` | un-typed `merge/3` (4 clauses, no mode declarations) | un-typed `counter/1` + `counter_loop/2` |
| `ch04_section` | §4.2.5, p 32 | §4.2.14 |
| `relationship_kind` | typed-vs-untyped same-name same-arity | typed-vs-untyped different-arity (1→2) |
| `header_cross_reference` | canonical block from R-008 (in ex-04 header) | canonical block from R-008 (in ex-05 header) |
| `signpost_prose` | included in `ch05_tutorial.md` cross-chapter relationships note | included in `ch05_tutorial.md` cross-chapter relationships note |
| `code_byte_exact_source` | §5.4 PDF (NOT ch04 ex-04's byte-exact code) | §5.5 PDF (NOT ch04 ex-06's byte-exact code) |

**Validation rules**:

- ex-04's header MUST contain the canonical R-008 cross-reference block citing ch04 ex-04 as the un-typed predecessor.
- ex-05's header MUST contain the analogous R-008 block citing ch04 ex-06 as the un-typed predecessor.
- ex-04's `.glp` clause text MUST be byte-exact from §5.4 PDF (verifiable via byte-exact verification per `contracts/glp-file-format.md` rule 7).
- ex-05's `.glp` clause text MUST be byte-exact from §5.5 PDF (similar verification).
- The cross-chapter relationships note in `ch05_tutorial.md` MUST mention both relationships and explicitly state that they are RELATIONSHIPS (cross-references), NOT code imports — distinguishing them from ch04's cross-chapter-inversion identity contract.

---

## Entity: Type-only / Procedure-decl-only Exercise (NEW for ch05)

A new exercise kind with no full procedure-with-body Program, only type definitions or procedure declarations + small helper unit-clauses or stub bodies.

| Field | Description |
|---|---|
| `applies_to` | ex-01 (`type-only`), ex-02 (`type-only`), ex-03 (`procedure-decl-only`) |
| `pdf_content` | Type definitions OR procedure declarations only — no clause body in the PDF source |
| `helper_clauses` | Small unit-clause / type-test predicate family (1–6 clauses per exercise) — proposed during /speckit-implement T006-equivalent per R-012 + Q2 |
| `primary_demo_goal` | The LOAD itself (file loads with type-check passing); NOT a runnable goal |
| `inspection_goals` | 3 goals exercising the helper unit-clauses or the stub body |
| `helper_discipline` | per R-012: helpers SRSW + type-check valid; on-theme; small (≤6 clauses); `%%` per clause; no PDF-Program shadowing; tutorial-distinguished from PDF Programs |

**Validation rules**:

- The exercise's `.glp` MUST contain the byte-exact PDF type definitions or procedure declaration AND the helper layer.
- The helper layer's procedure names MUST NOT collide with PDF-Program procedure names from any §5.x section.
- The "primary demo goal" for these exercises is documented in the trace as the load step itself (Phase 1: load-success); this is distinct from positive `full-program` exercises whose primary demo goal is a runnable query.
- The trace structure is the same 5-phase positive structure (load + 3 inspection goals + closing), with the load phase carrying extra annotation about the type/mode shape being demonstrated.

---

## Entity: Negative Exercise (NEW for ch05)

An exercise whose primary outcome is a documented load-time error, not a successful binding.

| Field | Description |
|---|---|
| `applies_to` | ex-07 (§5.7.1 type error), ex-08 (§5.7.2 mode error) |
| `glp_file_count` | 2 per exercise — failing form + corrected form (R-009) |
| `failing_form_outcome` | Load MUST FAIL with a captured type-error or mode-error message |
| `corrected_form_outcome` | Load MUST succeed with `✓ Loaded:` (the fix demonstration) |
| `primary_demo_goal` | The failing-form load attempt itself + the captured error message |
| `inspection_goals` | None or minimal — the corrected-form load is the second phase; an optional 3rd phase exercises the corrected form via a runnable goal (per R-011) |
| `trace_phases` | 2 minimum (failing-load + corrected-load); 3 if optional success-confirmation goal included |
| `error_byte_equality` | per FR-014 + R-011: byte-equal modulo per-run-varying segments authorised at /speckit-implement T026/T037-equivalent |
| `signpost_disclosure` | per FR-005: `ch05_tutorial.md` explicitly states ex-07 + ex-08 are MEANT to fail to load |

**Validation rules**:

- The failing-form `.glp` MUST FAIL TO LOAD; the captured error message MUST match the type or mode error category specified by the §5.7.x sub-section.
- The corrected-form `.glp` MUST load successfully and (if the 3-phase trace structure is chosen) the success-confirmation goal MUST return its locked binding.
- Per-run-varying segments (memory addresses, tuple-ids) are handled per R-011: if observed, halt-and-amend; if absent, full byte-equality holds.
- Charter §1.5 paraphrase comments still apply to negative exercises — every clause (failing AND corrected) carries a `%%` paraphrase per FR-005 + SC-017.

---

## Relationships

```
TopLevelTutorialIndex (tutorial.md)
    └── references ──▶ ChapterTutorial (ch05/)
                            ├── contains ──▶ ApprovalGate × 3 (group-boundary; FR-008 + FR-009)
                            ├── contains ──▶ Sub-section Group × 4 (Foundations, Mode-checking-flow, Flagship, Negatives)
                            ├── contains ──▶ Exercise × 8 (ex-01 through ex-08)
                            │       │
                            │       ├── kind=type-only       ──▶ Type-only Exercise behaviour (ex-01, ex-02)
                            │       ├── kind=procedure-decl-only ──▶ Procedure-decl-only Exercise behaviour (ex-03)
                            │       ├── kind=full-program    ──▶ Full Program Exercise behaviour (ex-04, ex-05, ex-06)
                            │       └── kind=negative        ──▶ Negative Exercise behaviour (ex-07, ex-08)
                            │
                            └── contains ──▶ CrossChapterRelationship × 2 (ex-04↔ch04 ex-04 untyped merge; ex-05↔ch04 ex-06 untyped counter)
```

---

## Summary

Eight entities. Four are NEW for ch05 (Type-only/Procedure-decl-only Exercise kind, Negative Exercise kind, Cross-chapter Relationship as a relationship-entity distinct from ch04's Cross-chapter Inversion, plus a refined Approval Gate set with R-006 type-checker pre-condition). Four are extended from ch01–ch04 (Exercise variant with `exercise_kind` discriminator, Sub-section group with Foundations/Mode-checking-flow/Flagship/Negatives names, Chapter Tutorial variant with negative-exercise-contract-note, Top-level Index unchanged). All entities have file-system or spec-document representations; no database or API surface introduced.
