# Contract — `ch04_tutorial.md` Status Block Format

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md)
**Date**: 2026-04-30

This contract defines the date-stamped per-exercise status block in `olamni/tutorial/ch04/ch04_tutorial.md` (the chapter signpost). Per Clarifications Q3, ch04 uses the **per-exercise 10-line format** inheriting ch01–ch03 unchanged. Group-boundary semantics are encoded in the gate-checking logic (FR-008), not the status-block format.

---

## Format

The status block MUST appear under a Markdown level-2 heading `## Exercise status` and MUST contain exactly TEN bullets, in order:

```markdown
## Exercise status

- exercise-01: <status> [<date>]
- exercise-02: <status> [<date>]
- exercise-03: <status> [<date>]
- exercise-04: <status> [<date>]
- exercise-05: <status> [<date>]
- exercise-06: <status> [<date>]
- exercise-07: <status> [<date>]
- exercise-08: <status> [<date>]
- exercise-09: <status> [<date>]
- exercise-10: <status> [<date>]
```

**`<status>` values** (single source of truth across all per-chapter signposts):

| Value | When used | Example |
|---|---|---|
| `not yet implemented` | exercise dir does NOT exist on disk; the predecessor group is also not yet implemented | `- exercise-04: not yet implemented` |
| `pending exercise-N approval` | predecessor exercise's status is not `approved` (within-group) OR predecessor group's last exercise is not `approved` (cross-group); current exercise dir does NOT exist | `- exercise-03: pending exercise-02 approval` |
| `pending review` | exercise dir EXISTS, files are written, but project-owner has not yet approved | `- exercise-01: pending review` |
| `approved YYYY-MM-DD` | project owner has explicitly approved (typically as part of a group approval) | `- exercise-01: approved 2026-04-30` |

**`<date>`** is in `YYYY-MM-DD` format. Empty for `not yet implemented` / `pending exercise-N approval` / `pending review`.

---

## Greppable contract

Downstream Claude sessions MUST be able to determine:

- An individual exercise's approval state via `grep -E "^- exercise-NN: (approved [0-9-]+|pending|not yet implemented)" olamni/tutorial/ch04/ch04_tutorial.md`
- A sub-section group's approval state via:
  - §4.1: `grep -cE "^- exercise-(01|02): approved" ...` returns 2
  - §4.2: `grep -cE "^- exercise-(03|04|05|06): approved" ...` returns 4
  - §4.3: `grep -cE "^- exercise-(07|08): approved" ...` returns 2
  - §4.4: `grep -cE "^- exercise-(09|10): approved" ...` returns 2

A session attempting to begin §4.2 work MUST refuse to proceed unless the §4.1 group grep returns 2. Same for §4.3 / §4.4.

---

## State transitions

```
[ not yet implemented ]
        │
        │ (within-group sequential implementation; predecessor in same group complete OR first-in-group + predecessor-group approved)
        ▼
[ pending review ]                (exercise files exist; awaiting project-owner approval)
        │
        │ (project owner approves the GROUP — all exercises in the group flip together)
        ▼
[ approved YYYY-MM-DD ]
```

Group approval flips all member exercises' lines together. For example, when §4.2 group is approved, ex-03 + ex-04 + ex-05 + ex-06 ALL flip from `pending review` to `approved YYYY-MM-DD` in one commit.

---

## Initial state of the chapter-4 status block

When `ch04_tutorial.md` is first written (during ex-01 implementation, before any approval), the status block reads:

```markdown
## Exercise status

- exercise-01: pending review
- exercise-02: pending exercise-01 approval
- exercise-03: pending exercise-02 approval
- exercise-04: pending exercise-03 approval
- exercise-05: pending exercise-04 approval
- exercise-06: pending exercise-05 approval
- exercise-07: pending exercise-06 approval
- exercise-08: pending exercise-07 approval
- exercise-09: pending exercise-08 approval
- exercise-10: pending exercise-09 approval
```

After ex-01 + ex-02 are written but §4.1 group is not yet approved:

```markdown
- exercise-01: pending review
- exercise-02: pending review
- exercise-03: pending exercise-02 approval
... (rest unchanged)
```

After §4.1 group approval (e.g., on 2026-05-01):

```markdown
- exercise-01: approved 2026-05-01
- exercise-02: approved 2026-05-01
- exercise-03: pending review
... (rest unchanged; ex-03 begins; ex-04 stays "pending exercise-03 approval" within-group meaning here is "predecessor exercise-03 needs to be written first")
```

Wait — clarification on within-group "pending" semantics: per FR-009, within a group exercises don't pairwise gate. So once §4.1 is approved, ex-03 starts writing → its status becomes `pending review` → then ex-04 starts writing → its status becomes `pending review` → etc. The `pending exercise-N approval` state is used ONLY for cross-group-predecessor pending (e.g., ex-07 stays `pending exercise-06 approval` until §4.2 group is fully approved, at which point ex-07 starts and flips to `pending review`). Within a group, the implementer writes exercises sequentially but they all flip to `pending review` as they're written, not blocked by a within-group predecessor's approval.

After all 10 exercises approved (chapter complete, e.g., 2026-05-04):

```markdown
- exercise-01: approved 2026-05-01
- exercise-02: approved 2026-05-01
- exercise-03: approved 2026-05-02
- exercise-04: approved 2026-05-02
- exercise-05: approved 2026-05-02
- exercise-06: approved 2026-05-02
- exercise-07: approved 2026-05-03
- exercise-08: approved 2026-05-03
- exercise-09: approved 2026-05-04
- exercise-10: approved 2026-05-04
```

This final state is the trigger for flipping the top-level `tutorial.md` chapter-4 row from `pending review (…)` to `implemented 2026-05-04`. Note: dates above are illustrative; actual implementation may compress to a single day if the implementer is autonomous.

---

## Validation rules

- Exactly TEN bullets in the block; no more, no fewer.
- Bullet order MUST match `exercise-01 / exercise-02 / … / exercise-10`.
- Each bullet MUST start with `- exercise-NN: ` (note the leading hyphen-space and the colon).
- `approved` status MUST carry a date; non-`approved` statuses MUST NOT carry one.
- Date MUST be in `YYYY-MM-DD` format.
- The block MUST appear under a level-2 heading `## Exercise status`.
- Group-boundary approval flips MUST be atomic in a single commit (all members of a group flip together when the group approves).
