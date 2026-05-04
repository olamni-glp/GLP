# Contract — Status block format (ch07)

**Path**: appears as a section in `olamni/tutorial/ch07/ch07_tutorial.md`.

**Inherited from ch01–ch03 + ch06 pairwise pattern** (NOT ch04/ch05's group-boundary pattern), with ONE ch07-specific addition: a single **cluster-boundary** line between the cluster-A exercise lines and the cluster-B exercise lines.

Per spec FR-008 + plan §Approval gates: ch07 has 12 exercises in 2 clusters of 6, gated pairwise WITHIN each cluster + a single boundary gate BETWEEN clusters, so the status block carries 13 lines total (12 exercise lines + 1 cluster-boundary line).

## Block structure

```markdown
## Exercise status

- exercise-01: <status> [<date or empty>]
- exercise-02: <status> [<date or empty>]
- exercise-03: <status> [<date or empty>]
- exercise-04: <status> [<date or empty>]
- exercise-05: <status> [<date or empty>]
- exercise-06: <status> [<date or empty>]
- cluster-A: <status> [<date or empty>]
- exercise-07: <status> [<date or empty>]
- exercise-08: <status> [<date or empty>]
- exercise-09: <status> [<date or empty>]
- exercise-10: <status> [<date or empty>]
- exercise-11: <status> [<date or empty>]
- exercise-12: <status> [<date or empty>]
```

`<status>` for exercise-NN lines ∈ `{not yet implemented, files written, pending review, approved YYYY-MM-DD}`.
`<status>` for the cluster-A line ∈ `{not yet satisfied, approved YYYY-MM-DD}`.

## Status semantics

| Status | Meaning |
|---|---|
| `not yet implemented` | Exercise's tutorial.md / trace file is absent. Cluster project files MAY or MAY NOT be present. |
| `files written` | All required artefacts (`ex-NN-tutorial.md`, `ex-NN-{repl,flutter}-trace.md`) exist; implementer has not yet flagged for review. |
| `pending review` | Implementer flags for project-owner review; corresponds to T-equivalent task completion in /speckit-implement. |
| `approved YYYY-MM-DD` | Project owner has approved; the date is the approval date. |
| `not yet satisfied` (cluster-A line only) | One or more cluster-A exercises is not yet `approved`. |

## Gate-grep contract

### Within-cluster pairwise gates

Per spec FR-008, ex-(NN+1) work begins only after ex-NN is `approved` WITHIN the same cluster. The implementer's gate check at the start of each ex-(N+1) work:

```bash
grep -E "^- exercise-0{NN}: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch07/ch07_tutorial.md
```

MUST return ≥1 match. If 0 matches, ex-(NN+1) work HALTS per FR-013.

For ch07 specifically, the within-cluster gates correspond to:
- Within cluster A:
  - Before ex-02: `grep -E "^- exercise-01: approved"` returns 1.
  - Before ex-03: `grep -E "^- exercise-02: approved"` returns 1.
  - Before ex-04: `grep -E "^- exercise-03: approved"` returns 1.
  - Before ex-05: `grep -E "^- exercise-04: approved"` returns 1.
  - Before ex-06: `grep -E "^- exercise-05: approved"` returns 1.
- Within cluster B:
  - Before ex-08: `grep -E "^- exercise-07: approved"` returns 1.
  - Before ex-09: `grep -E "^- exercise-08: approved"` returns 1.
  - Before ex-10: `grep -E "^- exercise-09: approved"` returns 1.
  - Before ex-11: `grep -E "^- exercise-10: approved"` returns 1.
  - Before ex-12: `grep -E "^- exercise-11: approved"` returns 1.

Total within-cluster gates: **5 + 5 = 10**.

### Cluster boundary gate (NEW for ch07)

Per spec FR-008, ALL cluster B work (starting from ex-07) begins only after ALL 6 cluster A exercises are `approved` AND the implementing session writes the `cluster-A: approved YYYY-MM-DD` line into the status block. The implementer's gate check at the start of cluster B work (specifically at T-equivalent for ex-07):

```bash
grep -E "^- cluster-A: approved [0-9]{4}-[0-9]{2}-[0-9]{2}" olamni/tutorial/ch07/ch07_tutorial.md
```

MUST return 1. If 0 matches, ex-07 work HALTS per FR-013.

The implementer is responsible for:
1. Verifying all 6 cluster-A exercise lines are `approved YYYY-MM-DD` (auxiliary check: `grep -cE "^- exercise-0[1-6]: approved" ch07_tutorial.md` returns 6).
2. Editing the `cluster-A:` line to flip from `not yet satisfied` to `approved YYYY-MM-DD` (with the same date as ex-06's approval, OR a strictly later date if any cluster-A re-review happened after ex-06's initial approval).

### Per-cluster auxiliary checks

Per Q-amendment Q-FR008-aux (proposed during /speckit-analyze remediation; auto-resolved):
- `grep -cE "^- exercise-0[1-6]: approved" ch07_tutorial.md` returns 6 BEFORE writing the cluster-A line as `approved`.
- `grep -cE "^- exercise-(0[7-9]|1[0-2]): approved" ch07_tutorial.md` returns 6 BEFORE flipping the top-level `tutorial.md` ch07 row to `implemented YYYY-MM-DD`.

## Date format

Dates MUST be ISO 8601 `YYYY-MM-DD`. The approval date is the date the project owner approves, NOT the date the implementer wrote the files.

## Inheritance from ch01–ch03 + ch06

This contract inherits from `specs/007-tutorial-ch06/contracts/status-block-format.md` (the most recent pairwise format). ch04/ch05's group-boundary format is NOT inherited because ch07 has a distinct cluster-boundary gate (singular, between clusters) rather than ch04's group gates (multiple, between thematic groups within one chapter).

## Why pairwise within cluster (not group)

ch04 and ch05 used group-boundary gates because their exercise counts (10 and 7 respectively) made pairwise approval tedious AND their groups were tight thematic clusters. ch07 has 12 exercises split 6/6 across two clusters, each cluster of 6 spans heterogeneous mechanics (cluster A: §7.1–§7.6 + Flutter setup; cluster B: project structure + 4 use-case-specific play sequences + cross-module-call + Flutter), so within-cluster pairwise gates inherit from ch01–ch03 + ch06 with one cluster-boundary gate added on top. The cluster-boundary gate is conceptually equivalent to ch04's group gates but applied at a higher level (cluster, not group).

## Status block evolution example

At the start of /speckit-implement (all not-yet-implemented):
```
## Exercise status

- exercise-01: not yet implemented
- exercise-02: not yet implemented
- exercise-03: not yet implemented
- exercise-04: not yet implemented
- exercise-05: not yet implemented
- exercise-06: not yet implemented
- cluster-A: not yet satisfied
- exercise-07: not yet implemented
- exercise-08: not yet implemented
- exercise-09: not yet implemented
- exercise-10: not yet implemented
- exercise-11: not yet implemented
- exercise-12: not yet implemented
```

After cluster A complete:
```
- exercise-01: approved 2026-05-02
- exercise-02: approved 2026-05-02
- exercise-03: approved 2026-05-03
- exercise-04: approved 2026-05-03
- exercise-05: approved 2026-05-04
- exercise-06: approved 2026-05-05
- cluster-A: approved 2026-05-05
- exercise-07: not yet implemented
... (cluster B still pending)
```

After ch07 complete:
```
... (all 12 exercise lines + cluster-A line all approved with dates)
```
