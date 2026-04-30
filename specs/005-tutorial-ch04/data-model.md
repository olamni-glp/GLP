# Phase 1 Data Model — Olamni Tutorial Chapter 4

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-30

This file enumerates the entities introduced (or extended) by this feature, their attributes, relationships, validation rules, and state transitions. It is documentation of pure-Markdown / pure-`.glp` artefacts; there is no database, no API surface, no in-memory runtime model. The "entities" here are file artefacts with structural contracts.

---

## Entity: Exercise (chapter-4 variant)

A subdirectory under `olamni/tutorial/ch04/` named `exercise-NN/` for `NN ∈ 01..10` (per Clarifications Q1 lock).

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `dir_name` | string | filesystem | `exercise-NN` for `NN ∈ 01..10` |
| `glp_file` | Path | filesystem | The single `.glp` source per R-008 (no compose-pair needed for any ch04 exercise) |
| `tutorial_md` | Path | filesystem | `ex-NN-tutorial.md` learner step-through |
| `trace_md` | Path | filesystem | `ex-NN-repl-trace.md` verbatim REPL session |
| `status` | enum | `ch04_tutorial.md` status block | `not yet implemented` / `pending exercise-N approval` (in pre-§4.1-group-approval state, used for ex-03+ before §4.1 group lands; for ex-07+ before §4.2; for ex-09+ before §4.3) / `pending review` / `approved YYYY-MM-DD` |
| `sub_section_group` | enum | derived from spec Q1 | `§4.1` (ex-01, ex-02) / `§4.2` (ex-03, ex-04, ex-05, ex-06) / `§4.3` (ex-07, ex-08) / `§4.4` (ex-09, ex-10) |
| `programs_grouped` | list[Program] | derived from spec Q1 | The PDF Programs covered by this exercise (per Q1 locked list) |

**Programs-per-exercise locked distribution** (per Q1):

| # | Sub-section | Filename | Programs |
|---|---|---|---|
| ex-01 | §4.1 | `ch-04-ex-01-constants-and-gates.glp` | 4.1.1 `p(a)` + 4.1.2 `q(b)/q(a)` + 4.1.3 logic gates `and/3` `or/3` `not/2` `xor/3` |
| ex-02 | §4.1 | `ch-04-ex-02-compound-circuits.glp` | 4.1.4 `nand/3` + 4.1.5 `half_adder/4` + 4.1.6 `full_adder/5` |
| ex-03 | §4.2 | `ch-04-ex-03-producer-consumer-reverse.glp` | 4.2.1 `producer/2` + 4.2.2 `consumer/3` + 4.2.3 naive `reverse/2` + 4.2.4 acc `reverse/2` + `reverse_acc/3` |
| ex-04 | §4.2 | `ch-04-ex-04-merge-variants.glp` | 4.2.5 simple `merge/3` + 4.2.6 `dmerge/3` + `dmerger/3` + 4.2.7 `merge_tree/2` + `merge_layer/2` |
| ex-05 | §4.2 | `ch-04-ex-05-stream-operators.glp` | 4.2.8 `distribute/3` + 4.2.9 `distribute_indexed/3` + 4.2.10 `observer/3` + 4.2.11 `adder/4` ripple-carry |
| ex-06 | §4.2 | `ch-04-ex-06-buffered-and-monitors.glp` | 4.2.12 `bb/0` + 4.2.13 `bb_test/0` + 4.2.14 `counter/1` + `counter_loop/2` + 4.2.15 `accumulator/1` + clients |
| ex-07 | §4.3 | `ch-04-ex-07-recursive-numerics.glp` | 4.3.1 Peano + 4.3.2 integer arith + 4.3.3 `factorial/2` + 4.3.4 tail factorial + 4.3.5 `fib/2` + 4.3.6 `fib_linear/2` |
| ex-08 | §4.3 | `ch-04-ex-08-recursive-list-tree.glp` | 4.3.7 `flatten/2` + 4.3.8 `tree_sum/2` + 4.3.9 `insertion_sort/2` + 4.3.10 `mergesort/2` + 4.3.11 `distribute_ng/3` + 4.3.12 `substitute/4` |
| ex-09 | §4.4 | `ch-04-ex-09-metaprogramming-foundations.glp` | 4.4.1 `reduce/2` programs-as-data + 4.4.2 trust-mode `run/2` |
| ex-10 | §4.4 | `ch-04-ex-10-advanced-meta-interpreters.glp` | 4.4.3 fail-safe `run/4` + 4.4.4 control `run/5` + `suspended_run/4` + 4.4.5 tracing `run/3` + indexed `reduce/3` + `replay/3` |

**Validation rules**:

- `dir_name` MUST exist on disk only when status is `pending …`, `pending review`, or `approved …`. Status `not yet implemented` requires the dir to NOT exist.
- `glp_file` count MUST equal 1 for all 10 exercises (no compose-pair needed per R-008).
- `tutorial_md` and `trace_md` MUST both exist when status is `approved`.
- Each `.glp` file MUST conform to `contracts/glp-file-format.md` (multi-Program version of ch01/ch02/ch03 contract).
- Each `trace_md` MUST conform to `contracts/trace-file-format.md`.
- `programs_grouped` MUST match the Q1 lock exactly; deviation requires Clarifications amendment per FR-013.

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

For ex-01: predecessor is the chapter signpost itself; transitions directly from `not yet implemented` → `pending review` (after ex-01 + ex-02 both written) → `approved YYYY-MM-DD` (when §4.1 group approved). For ex-03+: predecessor is the prior group fully approved + within-group order honoured.

---

## Entity: Sub-section group (chapter-4 NEW)

A logical grouping of exercises by book sub-section. Four groups govern this chapter:

| Group | Exercises | Approval gate to enter | Approval gate to exit |
|---|---|---|---|
| §4.1 | ex-01, ex-02 | Chapter signpost exists | All §4.1 exercises approved → unblocks §4.2 |
| §4.2 | ex-03, ex-04, ex-05, ex-06 | §4.1 fully approved | All §4.2 exercises approved → unblocks §4.3 |
| §4.3 | ex-07, ex-08 | §4.2 fully approved | All §4.3 exercises approved → unblocks §4.4 |
| §4.4 | ex-09, ex-10 | §4.3 fully approved | All §4.4 exercises approved → chapter complete |

**Validation rules**:

- The group's exit gate is satisfied iff ALL exercises in the group have status `approved YYYY-MM-DD` in the per-exercise status block.
- The group's entry gate is checked at the start of each in-group exercise (per FR-008 grep contract: `grep -E "^- exercise-(NN|MM|...): approved" ch04_tutorial.md` returns count equal to the predecessor group's exercise count).
- Within-group exercises are implemented sequentially in order; concurrent in-group implementation is NOT allowed (single implementer assumption).

---

## Entity: Chapter Tutorial (chapter-4 variant)

The `olamni/tutorial/ch04/` directory.

**Attributes**:

| Field | Type | Source | Description |
|---|---|---|---|
| `path` | Path | filesystem | `olamni/tutorial/ch04/` |
| `signpost` | Path | filesystem | `ch04_tutorial.md` (note **underscore**) |
| `sources_index` | Path | filesystem | `ch04-sources.md` (existing, committed in `592d89e3`) |
| `input_prompt` | Path | filesystem | `ch04-specification-input-prompt.md` (already created on this branch) |
| `deprecated_spec_copy` | Path | filesystem | `spec-rev-eng-input/ch04-DEPRECATED-spec.md` (existing) |
| `exercises` | list[Exercise] | filesystem | 10 subdirs |
| `cross_chapter_inversion_note` | string | `ch04_tutorial.md` body | plain-prose explanation of `producer/2` + `consumer/3` reclaim |
| `group_structure_note` | string | `ch04_tutorial.md` body | plain-prose outline of the 4 sub-section groups + 3 boundary gates |

**Validation rules**:
- `signpost` filename uses underscore (`ch04_tutorial.md`).
- `signpost` MUST contain the cross-chapter inversion note.
- `signpost` MUST contain the group-structure note.
- `signpost` MUST contain the per-exercise 10-line status block per Q3 + `contracts/status-block-format.md`.
- `input_prompt` MUST already exist before `/speckit-specify` runs (it does as of branch creation).
- `deprecated_spec_copy` MUST NOT be edited.

---

## Entity: Top-level Tutorial Index (extended)

The `olamni/tutorial/tutorial.md` file.

**Attributes**: as defined in ch01/ch02/ch03 data-model.md. For ch04:

- A row for chapter 4 already exists from prior implementations (added as `planned`).
- This implementation flips the ch04 row from `planned` to `pending review (YYYY-MM-DD)` after the §4.1 group approves.
- Once all 10 exercises (4 groups) approve, the row flips to `implemented YYYY-MM-DD`.
- Chapters 5–13 stay marked `planned`.

---

## Entity: Approval Gate (chapter-4 instance)

Three procedural gates govern this chapter's progression. NEW pattern for ch04 — group-boundary, not pairwise.

| Gate | Predecessor group | Block on | Format |
|---|---|---|---|
| §4.1→§4.2 gate | §4.1 (ex-01 + ex-02) | status block shows BOTH `exercise-01: approved YYYY-MM-DD` AND `exercise-02: approved YYYY-MM-DD` | greppable: `grep -cE "^- exercise-(01\|02): approved" ch04_tutorial.md` returns 2 |
| §4.2→§4.3 gate | §4.2 (ex-03..ex-06) | status block shows ALL 4 §4.2 exercises approved | greppable: `grep -cE "^- exercise-(03\|04\|05\|06): approved" ch04_tutorial.md` returns 4 |
| §4.3→§4.4 gate | §4.3 (ex-07 + ex-08) | status block shows BOTH §4.3 exercises approved | greppable: `grep -cE "^- exercise-(07\|08): approved" ch04_tutorial.md` returns 2 |

The group-internal "gates" are NOT formal gates — within-group exercises proceed sequentially without pause for approval (FR-009).

---

## Entity: Cross-chapter Inversion (NEW for ch04)

The `producer/2` + `consumer/3` clauses are imported INTO ch03 ex-01 from ch04 §4.2.1 + §4.2.2 (forward import documented in ch03 spec FR-002 + Clarifications Q1). Chapter 4 reclaims them as their NATIVE home in ex-03.

**Attributes**:

| Field | Value |
|---|---|
| `imported_from_chapter` | 4 |
| `imported_into_chapter` | 3 (ch03 ex-01) |
| `reclaimed_in_chapter` | 4 (ch04 ex-03) |
| `source_section` | §4.2.1 + §4.2.2 ("Producers and Consumers") |
| `source_pages` | book p 31 (PDF p 43) |
| `procedures` | `producer/2` (2 clauses: base + recursive) + `consumer/3` (2 clauses: base + recursive) |
| `byte_exact_identity_contract` | per spec FR-002 + SC-007: ch03's `ch-03-ex-01-producer-consumer.glp` clause text MUST be byte-identical to ch04's `ch-04-ex-03-producer-consumer-reverse.glp` clause text (modulo header + `%%` annotations) |

**Validation rules**:

- ex-03's `.glp` MUST contain `producer/2` + `consumer/3` clauses byte-identical to ch03's import.
- ex-03's header comment block MUST contain the canonical inversion-acknowledgment block from R-007.
- Verification at /speckit-implement: `diff` between the two files modulo header + `%%` returns zero clause-text differences.

---

## Relationships

```
TopLevelTutorialIndex (tutorial.md)
    └── references ──▶ ChapterTutorial (ch04/)
                            ├── contains ──▶ ApprovalGate × 3 (group-boundary; FR-008 + FR-009)
                            ├── contains ──▶ Sub-section Group × 4 (§4.1, §4.2, §4.3, §4.4)
                            ├── contains ──▶ Exercise × 10 (ex-01 through ex-10)
                            │       │
                            │       └── each contains ──▶ Programs (locked per Q1; ~38 total)
                            │
                            └── contains ──▶ CrossChapterInversion (producer/consumer reclaim from ch03 forward import)
```

---

## Summary

Six entities. Three new for ch04 (Sub-section group, Cross-chapter Inversion as a relationship-entity, group-boundary Approval Gate); three carried over from ch01/ch02/ch03 (Exercise variant, Chapter Tutorial variant, Top-level Index). All entities have file-system or spec-document representations; no database or API surface introduced.
