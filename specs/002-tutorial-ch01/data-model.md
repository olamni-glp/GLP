# Phase 1 Data Model — Olamni Tutorial Chapter 1

**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md) | **Research**: [research.md](./research.md)
**Date**: 2026-04-28

This is a documentation-and-source feature. The "data model" is the file/directory schema and the in-file structures the tutorial enforces. No runtime entities; no database schema.

## Entities

### Exercise

An `exercise-NN/` subdirectory under a chapter directory.

**Fields**:
- `dir_path: string` — e.g., `olamni/tutorial/ch01/exercise-01/`.
- `exercise_number: int` — 01, 02, or 03 per chapter (per spec FR-008).
- `glp_file: string` — exactly one `.glp` source file named `ch-XX-ex-NN-<short-name>.glp` (e.g., `ch-01-ex-01-fair-stream-merger.glp`).
- `tutorial_file: string` — exactly one `ex-NN-tutorial.md` step-through guide.
- `trace_file: string` — exactly one `ex-NN-repl-trace.md` verbatim REPL session.
- `status: enum {approved, pending <predecessor> approval, not yet implemented}` — recorded in the parent chapter signpost (NOT in the exercise dir itself).

**Validation rules** (from spec FR-001, FR-002, FR-003, FR-008):
- The `.glp` file MUST contain exactly the Program-1.1 clauses verbatim from PDF p 5 (excluding `%%` paraphrase comments).
- Variable names MUST match the per-exercise scheme:
  - exercise-01: `X, Xs, Y, Ys, Zs` (original).
  - exercise-02: `First, RestFirst, Second, RestSecond, Out`.
  - exercise-03: `A, As, B, Bs, Cs`.
- The `tutorial.md` file MUST follow the contract in `contracts/glp-file-format.md` and `contracts/trace-file-format.md`.
- The `trace.md` file MUST be a verbatim capture (per Clarification Q3) — no synthesis allowed.

**State transitions**:
```
not yet implemented  →  pending <predecessor> approval  →  approved
       │                          │                            │
       │                          │                            └─→ exercise can be referenced as predecessor
       │                          └─→ exercise files written; awaiting human review
       └─→ exercise files do NOT exist on disk
```

Transitions are signalled by editing the **parent chapter's `chXX_tutorial.md` status block**. Downstream sessions MUST grep the predecessor's status before starting any new exercise (per spec FR-007 / Clarification Q2).

---

### Chapter Tutorial

A chapter directory `olamni/tutorial/chXX/`.

**Fields**:
- `chapter_number: int` — 01..13.
- `chapter_path: string` — e.g., `olamni/tutorial/ch01/`.
- `sources_file: string` — `chXX-sources.md` (the PDF code-block index; already exists for all 13 chapters as of commit `592d89e3`).
- `prompt_file: string` — `chXX-specification-input-prompt.md` (rev-eng output, NO speckit ceremony per spec FR-006).
- `signpost_file: string` — `chXX_tutorial.md` (chapter signpost with status block).
- `rev_eng_input_dir: string` — `spec-rev-eng-input/` containing `chXX-DEPRECATED-spec.md` (already exists; rev-eng input only; quarantined from active use).
- `exercises: list[Exercise]` — ordered list of exercise subdirs (1–3 per chapter for chs 1–6 per charter §1).

**Validation rules** (from spec FR-004, FR-005, FR-006):
- `signpost_file` MUST contain a status block listing every exercise with date-stamped status.
- `prompt_file` MUST be plain prose; NO Feature Branch / Status / FR-NNN / User Story / Given-When-Then forms.
- `signpost_file` MUST link to all exercises (implemented and planned-but-gated).

---

### TopLevelIndex

The single file `olamni/tutorial/tutorial.md`.

**Fields**:
- `chapters_table: list[ChapterRow]` where `ChapterRow = (chapter_number, title, link, status)`.
- `intro: string` — brief tutorial intro paragraph.
- `prerequisites: list[string]` — Dart SDK requirement, REPL-build instruction, etc.
- `usage_paragraph: string` — one-paragraph guidance referencing charter design principles.

**Validation rules** (from spec FR-005):
- File MUST exist after this spec's implementation (created or extended).
- Chapter 1 row MUST be marked "implemented" with the date `2026-04-28` and a link to `ch01/ch01_tutorial.md`.
- Chapters 2–13 rows MUST be marked "planned" with links to existing `chXX-sources.md` files (no broken links).
- File MUST be updated incrementally per chapter; full rewrite forbidden until all 13 chapters are done (per Clarification A2).

---

### ApprovalGate

A logical entity expressed as text in `chXX_tutorial.md`. Format per spec Clarification Q2:

```
- exercise-NN: <status> [<date>]
```

Where `<status>` ∈ {`approved`, `pending <predecessor> approval`, `not yet implemented`}.

**Validation rules**:
- For chapter 1: at end of this spec's implementation, the status block in `ch01_tutorial.md` MUST read:
  ```
  - exercise-01: approved 2026-04-28          # set after Udi approves the implementation
  - exercise-02: pending exercise-01 approval # OR pending exercise-02 implementation
  - exercise-03: not yet implemented
  ```
  (The `approved` line is set only when Udi explicitly approves; otherwise exercise-01 stays at `pending exercise-01 approval` until then.)
- Before the implementer writes ANY file under `exercise-NN/`, they MUST grep the predecessor's status line and refuse to proceed if it's not `approved`.
- The status block MUST be the single source of truth for approval state; no separate marker files (per Clarification Q2 alternatives rejection).

---

## Relationships

```
TopLevelIndex (olamni/tutorial/tutorial.md)
    ├── ChapterTutorial[01] (olamni/tutorial/ch01/)
    │       ├── sources_file (chXX-sources.md)
    │       ├── prompt_file (chXX-specification-input-prompt.md)
    │       ├── signpost_file (chXX_tutorial.md) ── owns ── ApprovalGate (status block)
    │       ├── rev_eng_input_dir/
    │       └── exercises[]
    │             └── Exercise[01] (exercise-01/)
    │                   ├── glp_file
    │                   ├── tutorial_file
    │                   └── trace_file
    ├── ChapterTutorial[02..13] (planned; not implemented this round)
    └── ...
```

## Lifecycle / Workflow

```
1. spec.md committed (proper-channel /speckit-specify + /speckit-clarify)            ✓ done
2. plan.md + research.md + data-model.md + contracts/ + quickstart.md committed       ◀── this command
3. /speckit-tasks → tasks.md                                                          ◀── next command
4. Implement exercise-01:
     a. dart --version (R-005 verification)
     b. Build REPL (`dart compile exe ...`)
     c. Re-read PDF p 5 byte-exactly (R-006)
     d. Propose 3 inspection goals → wait for Udi approval
     e. Write the .glp file
     f. Run REPL session, capture verbatim trace
     g. Write tutorial.md and repl-trace.md
     h. Write ch01_tutorial.md (signpost) with status `pending exercise-01 approval`
     i. Write/extend olamni/tutorial/tutorial.md (incremental, ch01 row only)
     j. Write ch01-specification-input-prompt.md (rev-eng output, no ceremony)
     k. Show diff to Udi → wait for approval → flip status to `approved 2026-04-28`
5. Once exercise-01 approved → propose exercise-02 details → /speckit-tasks for ex-02
6. Once exercise-02 approved → propose exercise-03 details → /speckit-tasks for ex-03
7. Bump CalVer release on main with merged work.
```

The lifecycle steps for chapter 2..13 follow the same shape; the `chXX-sources.md` files are already in place (from commit `592d89e3`) so each chapter's spec/clarify/plan/tasks/implement cycle can begin from the same anchor.
