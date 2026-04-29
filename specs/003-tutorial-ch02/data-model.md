# Phase 1 Data Model — Olamni Tutorial Chapter 2

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-28

This file enumerates the entities introduced (or extended) by this feature, their attributes, relationships, validation rules, and state transitions. It is documentation of pure-Markdown / pure-`.glp` artefacts; there is no database, no API surface, no in-memory runtime model. The "entities" here are file artefacts with structural contracts.

---

## Entity: Exercise (chapter-2 variant)

A subdirectory under `olamni/tutorial/ch02/` named `exercise-NN/` for `NN ∈ {01, 02, 03}`.

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `dir_name` | string | filesystem | `exercise-01`, `exercise-02`, or `exercise-03` |
| `glp_files` | list[Path] | filesystem | The `.glp` source(s) — see "GLP file count" below |
| `tutorial_md` | Path | filesystem | `ex-NN-tutorial.md` learner step-through |
| `trace_md` | Path | filesystem | `ex-NN-repl-trace.md` verbatim REPL session |
| `status` | enum | `ch02_tutorial.md` status block | `not yet implemented` / `pending exercise-N approval` / `approved YYYY-MM-DD` |
| `body_kernel_introduces` | list[string] | spec | what new kernels this exercise teaches the learner |

**GLP file count by exercise**:

| Exercise | `.glp` files | Filenames |
|---|---|---|
| 01 | **2** (LP-only + GLP) | `ch-02-ex-01-classical-append-LP-only.glp`, `ch-02-ex-01-glp-append.glp` |
| 02 | **1** | `ch-02-ex-02-append-and-sum.glp` |
| 03 | **1** | `ch-02-ex-03-timed-append.glp` |

This asymmetry (ex-01 has two files, ex-02 / ex-03 each have one) is deliberate: ex-01's pedagogy IS the contrast pair, so both files must exist; ex-02 / ex-03 each demonstrate a single new kernel layered on top of GLP append.

**Body kernel introduction by exercise**:

| Exercise | Kernels introduced (cumulative) |
|---|---|
| 01 | (none — pure list operations) |
| 02 | `:=` arithmetic via `+` body kernel (`_add`); accumulator-free recursion |
| 03 | `now/1` (`_now`); `'_output'/1` (`_output`); reuses `:=` from ex-02 |

**Validation rules**:

- `dir_name` MUST exist on disk only when status is `pending …` or `approved …`. Status `not yet implemented` requires the dir to NOT exist (per spec SC-008).
- `glp_files` count MUST match the table above; deviation halts implementation.
- `tutorial_md` and `trace_md` MUST both exist when status is `approved`; absence is a halt-and-report bug.
- Each `.glp` file MUST conform to the contract in `contracts/glp-file-format.md`.
- `trace_md` MUST conform to the contract in `contracts/trace-file-format.md`. ex-03's `trace_md` carries an extra annotation per FR-014.

**State transitions**:

```
[ not yet implemented ]
        │
        │ (gate: predecessor approved + REPL-tested + variation-shape locked in spec)
        ▼
[ pending exercise-N approval ]
        │
        │ (project owner approves the trace + tutorial)
        ▼
[ approved YYYY-MM-DD ]
```

ex-01's predecessor gate is empty (it has no predecessor; its gate is the chapter signpost existing). ex-02's predecessor gate requires ex-01 approved. ex-03's predecessor gate requires ex-02 approved.

---

## Entity: Chapter Tutorial (chapter-2 variant)

The `olamni/tutorial/ch02/` directory.

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `path` | Path | filesystem | `olamni/tutorial/ch02/` |
| `signpost` | Path | filesystem | `ch02_tutorial.md` (note **underscore**, not hyphen) |
| `sources_index` | Path | filesystem | `ch02-sources.md` (existing, committed in 592d89e3) |
| `input_prompt` | Path | filesystem | `ch02-specification-input-prompt.md` (already created) |
| `deprecated_spec_copy` | Path | filesystem | `spec-rev-eng-input/ch02-DEPRECATED-spec.md` (existing, committed in 146f430c) |
| `exercises` | list[Exercise] | filesystem | three subdirs (only ex-01 initially populated) |
| `cross_chapter_import_note` | string | `ch02_tutorial.md` body | plain-prose explanation of the ch 4 §4.2 GLP `append/3` import |

**Validation rules**:

- `signpost` filename uses underscore (`ch02_tutorial.md`), NOT hyphen — per workflow memory's file-naming dialect.
- `signpost` MUST contain the cross-chapter import note (per spec FR-005).
- `signpost` MUST contain the date-stamped status block per `contracts/status-block-format.md`.
- `input_prompt` MUST already exist before `/speckit-specify` runs (it's the input).
- `deprecated_spec_copy` MUST NOT be edited; it is reverse-engineering input only.

---

## Entity: Top-level Tutorial Index (extended)

The `olamni/tutorial/tutorial.md` file.

**Attributes**: as defined in ch01's `data-model.md`. For ch02:

- A row for chapter 2 already exists from ch01's implementation (added as `planned`).
- This implementation FLIPS the ch02 row from `planned` to `pending review (YYYY-MM-DD)` after ex-01 lands, then to `implemented YYYY-MM-DD` after all three exercises are approved.
- Chapters 3–13 rows remain unchanged.

**Validation rules**:

- The chapter-2 row MUST link to `ch02/ch02_tutorial.md` (not to `ch02/ch02-sources.md` as it does in the planned state).
- Status string format: `implemented YYYY-MM-DD` (after all three exercises approved) or `pending review (YYYY-MM-DD)` (during ex-NN landing) or `planned` (before this chapter starts).

---

## Entity: Approval Gate (chapter-2 instance)

Three procedural gates governing exercise progression. Each is an Approval Gate per ch01's data-model.md, instantiated for chapter 2 as follows:

| Gate | Predecessor | Block on | Format |
|---|---|---|---|
| ex-02 gate | exercise-01 | status block in `ch02_tutorial.md` shows `exercise-01: approved YYYY-MM-DD` AND ex-01 trace covers all "thoroughly REPL-tested" criteria | greppable status line |
| ex-03 gate | exercise-02 | status block shows `exercise-02: approved YYYY-MM-DD` AND ex-02 trace covers same criteria | greppable status line |
| variation-shape gate (ex-02) | spec.md Clarifications Q3 | shape `append_and_sum/4` is locked in spec.md per Clarifications | spec.md content |
| variation-shape gate (ex-03) | spec.md Clarifications Q3 | shape `timed_append/3` is locked in spec.md per Clarifications | spec.md content |

The variation-shape gates are SATISFIED by the spec's Clarifications session having locked the shapes; no separate approval action is required during /speckit-plan or /speckit-implement.

---

## Entity: Body Kernel (referenced; not modified)

A runtime-implemented predicate in `glp_runtime/lib/runtime/body_kernels.dart`. ch02 USES three categories:

| Category | Kernels (Dart name) | GLP-level access | Used in |
|---|---|---|---|
| Arithmetic | `_add` | `:=` via `Result := X + Y` syntax in `programs/self.glp` | ex-02, ex-03 |
| System time | `_now` | `now/1` declared in `programs/self.glp` | ex-03 |
| Ground I/O | `_output` | `'_output'/1` declared in `programs/self.glp` | ex-03 |

**Validation rules** (per spec FR-009 / FR-010):

- Tutorial code MUST NOT call kernels directly. All access goes through the GLP-level procedures in `programs/self.glp`.
- The `programs/self.glp` prelude is loaded automatically by the REPL; no explicit `:- use_module(...)` or equivalent is needed.

---

## Entity: Cross-chapter Import (new for ch02)

A code block from a later chapter used inside an earlier chapter's tutorial. Chapter 2 has exactly one cross-chapter import: the GLP `append/3` definition from book pp 31–32 (chapter 4 §4.2 "List Reversal — Naive Reverse").

**Attributes**:

| Field | Value |
|---|---|
| `source_chapter` | 4 |
| `source_section` | §4.2 "List Reversal — Naive Reverse" |
| `source_pages` | book pp 31–32 (PDF pp 43–44) |
| `imported_definition` | `append/3` — base case + recursive case |
| `imported_into_files` | `ch-02-ex-01-glp-append.glp`, `ch-02-ex-02-append-and-sum.glp`, `ch-02-ex-03-timed-append.glp` (duplicated inline per Clarification Q2) |
| `provenance_note_format` | per `research.md` R-007 |

**Validation rules**:

- The two clauses imported MUST be byte-identical to PDF pp 31–32 (per spec SC-007).
- The provenance note (per R-007) MUST appear in each importing file's header comment block.
- NO other cross-chapter imports are permitted in ch 02 (per spec FR-015 / SC-015).

---

## Relationships

```
TopLevelTutorialIndex (tutorial.md)
    └── references ──▶ ChapterTutorial (ch02/)
                            ├── contains ──▶ Exercise (ex-01)
                            │       ├── contains ──▶ GLP file (LP-only, intentionally rejected)
                            │       └── contains ──▶ GLP file (GLP append, accepted)
                            │                              │
                            │                              └── byte-exact-from ──▶ CrossChapterImport (ch4 §4.2)
                            ├── contains ──▶ Exercise (ex-02, gated)
                            │       └── contains ──▶ GLP file (duplicated GLP append + sum/2 + append_and_sum/4)
                            │                              │
                            │                              ├── duplicates ──▶ CrossChapterImport (ch4 §4.2)
                            │                              └── uses ──▶ BodyKernel (`_add` via `:=`)
                            ├── contains ──▶ Exercise (ex-03, gated)
                            │       └── contains ──▶ GLP file (duplicated GLP append + timed_append/3)
                            │                              │
                            │                              ├── duplicates ──▶ CrossChapterImport (ch4 §4.2)
                            │                              └── uses ──▶ BodyKernel (`_now`, `_output`, `_add`/`_sub` via `:=`)
                            └── contains ──▶ ApprovalGate × 4 (ex-02, ex-03, two variation-shape gates)
```

The variation-shape gates are NOT tied to any specific Exercise; they are spec-level constraints satisfied by the Clarifications session.

---

## Summary

Six entities. Two existing (`Top-level Tutorial Index`, `Body Kernel`) — referenced and lightly extended. Four new or chapter-specific (`Exercise (ch02 variant)`, `Chapter Tutorial (ch02 variant)`, `Approval Gate (ch02 instance)`, `Cross-chapter Import`). All entities have file-system or spec-document representations; no database or API surface introduced.
