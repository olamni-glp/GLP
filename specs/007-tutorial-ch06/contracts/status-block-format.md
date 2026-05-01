# Contract — Status block format (ch06)

**Path**: appears as a section in `olamni/tutorial/ch06/ch06_tutorial.md`.

**Inherited from ch01–ch03 pairwise pattern** (NOT ch04/ch05's group-boundary pattern). Per spec FR-008 + plan §Approval gates: ch06 has 5 exercises with pairwise gates, so the status block carries one line per exercise (5 lines).

## Block structure

```markdown
## Exercise status

- exercise-01: <status> [<date or empty>]
- exercise-02: <status> [<date or empty>]
- exercise-03: <status> [<date or empty>]
- exercise-04: <status> [<date or empty>]
- exercise-05: <status> [<date or empty>]
```

`<status>` ∈ `{not yet implemented, files written, pending review, approved YYYY-MM-DD}`.

## Status semantics

| Status | Meaning |
|---|---|
| `not yet implemented` | Exercise dir does not exist OR `.glp` file is absent. |
| `files written` | All three artefacts (`ch-06-ex-NN-<short>.glp`, `ex-NN-tutorial.md`, `ex-NN-repl-trace.md`) exist; implementer has not yet flagged for review. |
| `pending review` | Implementer flags for project-owner review; corresponds to T-equivalent task completion in /speckit-implement. |
| `approved YYYY-MM-DD` | Project owner has approved; the date is the approval date. Required to satisfy the gate to ex-(NN+1). |

## Gate-grep contract

Per spec FR-008, ex-(NN+1) work begins only after ex-NN is `approved`. The implementer's gate check at the start of each ex-(NN+1) work:

```bash
grep -E "^- exercise-0{NN}: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch06/ch06_tutorial.md
```

MUST return ≥1 match. If 0 matches, ex-(NN+1) work HALTS per FR-013.

For ch06 specifically, the four gates correspond to:
- Before ex-02: `grep -E "^- exercise-01: approved [0-9]{4}-[0-9]{2}-[0-9]{2}"` returns 1.
- Before ex-03: `grep -E "^- exercise-02: approved [0-9]{4}-[0-9]{2}-[0-9]{2}"` returns 1.
- Before ex-04: `grep -E "^- exercise-03: approved [0-9]{4}-[0-9]{2}-[0-9]{2}"` returns 1.
- Before ex-05: `grep -E "^- exercise-04: approved [0-9]{4}-[0-9]{2}-[0-9]{2}"` returns 1.

## Date format

Dates MUST be ISO 8601 `YYYY-MM-DD`. The approval date is the date the project owner approves, NOT the date the implementer wrote the files.

## Inheritance from ch01–ch03

This contract inherits from `specs/004-tutorial-ch03/contracts/status-block-format.md` (the canonical pairwise-gate format). ch04/ch05's group-boundary format is NOT inherited because ch06 is small enough (5 exercises) that pairwise gates inherit cleanly without overhead.

## Why pairwise (not group)

ch04 and ch05 used group-boundary gates because their exercise counts (10 and 7 respectively) made pairwise approval tedious. ch06 has 5 exercises — pairwise gates inherit from ch01–ch03 with no friction, and each exercise's synthesis-from-different-earlier-chapter source means each gate is a meaningful independent decision (rather than a cluster decision over related Programs from one sub-section).
