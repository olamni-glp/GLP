# Phase 1 Data Model — Olamni Tutorial Chapter 3

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-30

This file enumerates the entities introduced (or extended) by this feature, their attributes, relationships, validation rules, and state transitions. It is documentation of pure-Markdown / pure-`.glp` artefacts; there is no database, no API surface, no in-memory runtime model. The "entities" here are file artefacts with structural contracts.

---

## Entity: Exercise (chapter-3 variant)

A subdirectory under `olamni/tutorial/ch03/` named `exercise-NN/` for `NN ∈ {01, 02, 03}`.

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `dir_name` | string | filesystem | `exercise-01`, `exercise-02`, or `exercise-03` |
| `glp_files` | list[Path] | filesystem | The `.glp` source(s) — see "GLP file count" below |
| `tutorial_md` | Path | filesystem | `ex-NN-tutorial.md` learner step-through |
| `trace_md` | Path | filesystem | `ex-NN-repl-trace.md` verbatim REPL session |
| `status` | enum | `ch03_tutorial.md` status block | `not yet implemented` / `pending exercise-N approval` / `pending review` / `approved YYYY-MM-DD` |
| `guard_species_introduces` | list[string] | spec | what new guard species this exercise teaches the learner (cumulative) |
| `composition_shape` | enum | `research.md` R-009 | `composed` (exercises Program 3.1 `merge/3`) or `stand_alone` (no `merge/3` reference) |

**GLP file count by exercise**:

| Exercise | `.glp` files | Filenames |
|---|---|---|
| 01 | **2** (Program 3.1 + cross-chapter producer/consumer pair) | `ch-03-ex-01-glp-fair-stream-merger.glp`, `ch-03-ex-01-producer-consumer.glp` |
| 02 | **1** | `ch-03-ex-02-defined-guards.glp` |
| 03 | **1** | `ch-03-ex-03-guard-negation.glp` |

This asymmetry (ex-01 has two files, ex-02 / ex-03 each have one) is deliberate and inherits from ch02's pattern: ex-01's pedagogy is the multi-procedure composed pipeline, so both source files must exist; ex-02 / ex-03 each demonstrate a single new guard species in a focused stand-alone file.

**§3.2 guard species introduction by exercise** (cumulative across the chapter; per spec curriculum claim and FR-009 / FR-010):

| Exercise | Guard species introduced | Specific guards used |
|---|---|---|
| 01 | built-in guards | `>` (in `producer/2` recursive clause), `ground` (in `consumer/3` recursive clause) |
| 02 | + defined guards | `channel/1` (used at guard position in `process/2` clause 1); `otherwise` (already built-in but pedagogically highlighted as the dispatch fallback) |
| 03 | + guard negation | `=?=` (positive in `lookup/3` clause 1); `~(=?=)` (negated in `lookup/3` clause 2) |

**Composition shape by exercise** (per R-009):

| Exercise | Shape | Procedures in `.glp` |
|---|---|---|
| 01 | composed | `merge/3` (3 clauses, in glp-fair-stream-merger file) + `producer/2` (2 clauses) + `consumer/3` (2 clauses) (in producer-consumer file) |
| 02 | stand_alone | `channel/1` (1 unit clause) + `process/2` (2 clauses) + `handle/1` stub (1 unit clause); NO `merge/3` duplication |
| 03 | stand_alone | `lookup/3` (2 clauses); NO `merge/3` or `channel/1` / `process/2` duplication |

**Validation rules**:

- `dir_name` MUST exist on disk only when status is `pending …`, `pending review`, or `approved …`. Status `not yet implemented` requires the dir to NOT exist (per spec SC-008).
- `glp_files` count MUST match the table above; deviation halts implementation per FR-013.
- `tutorial_md` and `trace_md` MUST both exist when status is `approved`; absence is a halt-and-report bug.
- Each `.glp` file MUST conform to the contract in `contracts/glp-file-format.md`.
- `trace_md` MUST conform to the contract in `contracts/trace-file-format.md`. ALL THREE traces inherit strict byte-equality (per FR-014; chapter 3 has no wallclock-derived output, so no per-run-variation relaxation applies).
- `composition_shape` MUST match R-009's locked decisions (`composed` for ex-01, `stand_alone` for ex-02, `stand_alone` for ex-03). Deviation requires a Clarifications amendment per FR-013.

**State transitions**:

```
[ not yet implemented ]
        │
        │ (gate: predecessor approved + REPL-tested; spec-locked variation shape)
        ▼
[ pending exercise-N approval ]
        │
        │ (per ch02 contract — stage between writing and project-owner review)
        ▼
[ pending review ]
        │
        │ (project owner reviews trace + tutorial)
        ▼
[ approved YYYY-MM-DD ]
```

ex-01's predecessor gate is empty (it has no predecessor; its gate is the chapter signpost existing). ex-02's predecessor gate requires ex-01 approved. ex-03's predecessor gate requires ex-02 approved.

---

## Entity: Chapter Tutorial (chapter-3 variant)

The `olamni/tutorial/ch03/` directory.

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `path` | Path | filesystem | `olamni/tutorial/ch03/` |
| `signpost` | Path | filesystem | `ch03_tutorial.md` (note **underscore**, not hyphen) |
| `sources_index` | Path | filesystem | `ch03-sources.md` (existing, committed in 592d89e3) |
| `input_prompt` | Path | filesystem | `ch03-specification-input-prompt.md` (already created) |
| `deprecated_spec_copy` | Path | filesystem | `spec-rev-eng-input/ch03-DEPRECATED-spec.md` (existing) |
| `exercises` | list[Exercise] | filesystem | three subdirs (only ex-01 initially populated) |
| `cross_chapter_import_note` | string | `ch03_tutorial.md` body | plain-prose explanation of the ch4 §4.2.1 + §4.2.2 producer + consumer import |
| `guard_curriculum_note` | string | `ch03_tutorial.md` body | plain-prose outline of the §3.2 guard curriculum (built-in → defined → negation across the three exercises) |

**Validation rules**:

- `signpost` filename uses underscore (`ch03_tutorial.md`), NOT hyphen — per workflow memory's file-naming dialect.
- `signpost` MUST contain the cross-chapter import note (per spec FR-005).
- `signpost` MUST contain the §3.2 guard curriculum outline (per spec FR-005's "outline the three-step §3.2 guard curriculum").
- `signpost` MUST contain the date-stamped status block per `contracts/status-block-format.md`.
- `input_prompt` MUST already exist before `/speckit-specify` runs (it's the input). At branch creation it does exist.
- `deprecated_spec_copy` MUST NOT be edited; it is reverse-engineering input only.

---

## Entity: Top-level Tutorial Index (extended)

The `olamni/tutorial/tutorial.md` file.

**Attributes**: as defined in ch01 / ch02 `data-model.md`. For ch03:

- A row for chapter 3 already exists from ch01's implementation (added as `planned`).
- This implementation FLIPS the ch03 row from `planned` to `pending review (YYYY-MM-DD)` after ex-01 lands, then to `implemented YYYY-MM-DD` after all three exercises are approved.
- Chapters 4–13 rows remain unchanged.

**Validation rules**:

- The chapter-3 row MUST link to `ch03/ch03_tutorial.md` (not to `ch03/ch03-sources.md` as it does in the planned state).
- Status string format: `implemented YYYY-MM-DD` (after all three exercises approved) or `pending review (YYYY-MM-DD)` (during ex-NN landing) or `planned` (before this chapter starts).

---

## Entity: Approval Gate (chapter-3 instance)

Two procedural gates govern exercise progression. Each is an Approval Gate per ch01's data-model.md, instantiated for chapter 3 as follows. (All three variation-shape gates are CLOSED in this spec via Clarifications Q1+Q2+Q3 and are listed below for completeness.)

| Gate | Status | Predecessor / Lock | Block on | Format |
|---|---|---|---|---|
| ex-02 predecessor-approval gate | ACTIVE | exercise-01 | status block in `ch03_tutorial.md` shows `exercise-01: approved YYYY-MM-DD` AND ex-01 trace covers all "thoroughly REPL-tested" criteria | greppable status line |
| ex-03 predecessor-approval gate | ACTIVE | exercise-02 | status block shows `exercise-02: approved YYYY-MM-DD` AND ex-02 trace covers same criteria | greppable status line |
| ch4-exemplar variation-shape gate | CLOSED | spec.md Clarifications Q1 | n/a — locked to §4.2.1 + §4.2.2 producer/consumer | spec.md content |
| §3.2 defined-guard variation-shape gate | CLOSED | spec.md Clarifications Q2 | n/a — locked to `channel/1` + `process/2` | spec.md content |
| §3.2 negation-using variation-shape gate | CLOSED | spec.md Clarifications Q3 | n/a — locked to `lookup/3` complete | spec.md content |

The CLOSED variation-shape gates are SATISFIED by the spec's Clarifications session having locked the shapes; no separate approval action is required during /speckit-plan or /speckit-implement. Per spec FR-013, if any locked shape is found incompatible at REPL load, halt-and-amend via a new Clarifications entry — NEVER silently substitute.

Subordinate decompositions (per R-008 + R-009) are NOT approval gates — they are research.md decision-log entries requiring project-owner approval but not blocking parallel work:
- R-008 `handle/1` resolution: local stub (recommended, requires approval at /speckit-implement)
- R-009 ex-02 composition: stand-alone (recommended, requires approval at /speckit-implement)
- R-009 ex-03 composition: stand-alone (recommended, requires approval at /speckit-implement)

---

## Entity: §3.2 Guard Species (referenced; not modified)

A category of guard mechanism introduced by book §3.2. Chapter 3's curriculum uses three species across the three exercises. Pre-existing in the GLP language and runtime (no language additions per Constitution Language Design Authority).

| Species | Mechanism | Examples used in ch03 | Used in |
|---|---|---|---|
| Built-in guards | runtime-implemented guard predicates declared in `programs/self.glp` and the runtime's guard-evaluator | `>` (numeric comparison), `ground` (term-groundedness test), `=?=` (positive equality test), `otherwise` (catch-all fallback) | ex-01 (`>`, `ground`); ex-02 (`otherwise` in `process/2` clause 2); ex-03 (`=?=` positive in clause 1) |
| Defined guards | unit clauses or short procedures the compiler unfolds at guard sites | `channel/1` unit clause matching `ch(_, _)` term shape | ex-02 (`channel(X?)` at `process/2` clause 1's guard site) |
| Guard negation | the `~(...)` form, restricted to negatable built-in guards (per book §3.2 SRSW Rules table on p 24) | `~(=?=)` negation of equality | ex-03 (`~(Key? =?= K?)` at `lookup/3` clause 2's guard site) |

**Validation rules** (per spec FR-009 / FR-010 / FR-015):

- ex-01's `.glp` files MUST use ONLY built-in guards. Specifically: `>` and `ground` from the inherited ch4 procedures; no defined guards, no negation.
- ex-02's `.glp` MUST use the `channel/1` defined guard at a guard position in at least one clause.
- ex-03's `.glp` MUST use the `~(=?=)` negation form at a guard position in at least one clause.
- Defined guards CANNOT be negated (per §3.2 SRSW Rules table on book p 24); ex-03 MUST NOT use `~(channel(...))` or any other defined guard inside `~(...)`. Only built-in negatable guards are permitted inside the negation form.

---

## Entity: Cross-chapter Import (chapter-3 variant)

A code block from a later chapter used inside an earlier chapter's tutorial. Chapter 3 has exactly one cross-chapter import: the `producer/2` + `consumer/3` pair from book p 31 (chapter 4 §4.2.1 + §4.2.2 "Producers and Consumers").

**Attributes**:

| Field | Value |
|---|---|
| `source_chapter` | 4 |
| `source_section` | §4.2.1 + §4.2.2 ("Producers and Consumers") |
| `source_pages` | book p 31 (PDF p 43) |
| `imported_definitions` | `producer/2` (2 clauses: base + recursive) + `consumer/3` (2 clauses: base + recursive) |
| `imported_into_files` | `ch-03-ex-01-producer-consumer.glp` (only — ex-02 + ex-03 are STAND-ALONE per R-009 and do NOT duplicate the imported procedures) |
| `provenance_note_format` | per `research.md` R-007 |
| `inherited_body_kernels` | `:=` (used inside `producer/2` recursive clause for `N1 := N? - 1` decrement; used inside `consumer/3` recursive clause for `Sum1 := Sum? + X?` accumulation) — permitted ONLY inside this byte-exact import per FR-015 amendment |

**Validation rules**:

- The four clauses imported (2 producer + 2 consumer) MUST be byte-identical to PDF p 43 (per spec SC-007).
- The provenance note (per R-007) MUST appear in the importing file's header comment block.
- NO other cross-chapter imports are permitted in ch03 (per spec FR-015 / SC-013).
- The `:=` body kernel inside the imported procedures is permitted by the FR-015 amendment AS LONG AS the surrounding clause text is byte-identical to PDF p 43; modifying the imported clauses to remove `:=` would break byte-exactness AND would re-trigger the FR-015 prohibition.

---

## Relationships

```
TopLevelTutorialIndex (tutorial.md)
    └── references ──▶ ChapterTutorial (ch03/)
                            ├── contains ──▶ Exercise (ex-01, composed)
                            │       ├── contains ──▶ GLP file (Program 3.1 fair merger)
                            │       │                       │
                            │       │                       └── byte-exact-from ──▶ book p 15 §3.1
                            │       └── contains ──▶ GLP file (producer/2 + consumer/3)
                            │                              │
                            │                              ├── byte-exact-from ──▶ CrossChapterImport (ch4 §4.2.1+§4.2.2)
                            │                              └── inherits ──▶ §3.2 GuardSpecies (built-in: `>`, `ground`)
                            │                              └── inherits ──▶ BodyKernel (`:=` via FR-015 amendment)
                            ├── contains ──▶ Exercise (ex-02, stand_alone, gated)
                            │       └── contains ──▶ GLP file (channel/1 + process/2 + handle/1 stub)
                            │                              │
                            │                              ├── byte-exact-from ──▶ book p 22 §3.2 (channel/1 + process/2)
                            │                              ├── locally-defines ──▶ handle/1 stub (per R-008)
                            │                              └── introduces ──▶ §3.2 GuardSpecies (defined: `channel/1`)
                            ├── contains ──▶ Exercise (ex-03, stand_alone, gated)
                            │       └── contains ──▶ GLP file (lookup/3 complete)
                            │                              │
                            │                              ├── byte-exact-from ──▶ book p 22 §3.2 (lookup/3 both clauses)
                            │                              └── introduces ──▶ §3.2 GuardSpecies (negation: `~(=?=)`)
                            └── contains ──▶ ApprovalGate × 2 active (ex-02, ex-03 predecessor-approval)
                                       + 3 closed (ch4-exemplar, defined-guard, negation variation-shape; closed via spec Clarifications Q1+Q2+Q3)
```

The closed variation-shape gates are NOT tied to any specific Exercise progression-action; they are spec-level constraints satisfied by the Clarifications session.

---

## Summary

Six entities. Two existing (`Top-level Tutorial Index`, `§3.2 Guard Species`) — referenced and lightly extended; the §3.2 Guard Species entity replaces ch02's "Body Kernel" entity since ch3's curriculum axis is guards, not body kernels. Four new or chapter-specific (`Exercise (ch03 variant)`, `Chapter Tutorial (ch03 variant)`, `Approval Gate (ch03 instance)`, `Cross-chapter Import (ch03 variant)`). All entities have file-system or spec-document representations; no database or API surface introduced.
