# Contract — `ch05_tutorial.md` Status Block Format (post-Q7+Q12)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md)
**Date**: 2026-05-01 (Q12 binding form)

This contract defines the date-stamped per-exercise status block in `olamni/tutorial/ch05/ch05_tutorial.md` (the chapter signpost). Per Clarifications **Q3 (per-exercise format) + Q7 (renumbering 8→7) + Q12 (post-Q7 internal-consistency cleanup)**, ch05 uses the per-exercise **7-line format** post-Q7 (was 8 lines pre-Q7). Inherits ch01–ch04 format unchanged. Group-boundary semantics are encoded in the gate-checking logic (FR-008), not the status-block format.

---

## Format

The status block MUST appear under a Markdown level-2 heading `## Exercise status` and MUST contain exactly **SEVEN** bullets, in order:

```markdown
## Exercise status

- exercise-01: <status> [<date>]
- exercise-02: <status> [<date>]
- exercise-03: <status> [<date>]
- exercise-04: <status> [<date>]
- exercise-05: <status> [<date>]
- exercise-06: <status> [<date>]
- exercise-07: <status> [<date>]
```

**`<status>` values** (single source of truth across all per-chapter signposts):

| Value | When used | Example |
|---|---|---|
| `not yet implemented` | exercise dir does NOT exist on disk; the predecessor group is also not yet implemented | `- exercise-04: not yet implemented` |
| `pending exercise-N approval` | predecessor exercise's status is not `approved` (within-group) OR predecessor group's last exercise is not `approved` (cross-group); current exercise dir does NOT exist | `- exercise-04: pending exercise-03 approval` |
| `pending review` | exercise dir EXISTS, files are written, but project-owner has not yet approved | `- exercise-01: pending review` |
| `approved YYYY-MM-DD` | project owner has explicitly approved (typically as part of a group approval) | `- exercise-01: approved 2026-05-01` |

**`<date>`** is in `YYYY-MM-DD` format. Empty for `not yet implemented` / `pending exercise-N approval` / `pending review`.

---

## Greppable contract (post-Q7+Q12 BINDING)

Downstream Claude sessions MUST be able to determine:

- An individual exercise's approval state via `grep -E "^- exercise-NN: (approved [0-9-]+|pending|not yet implemented)" olamni/tutorial/ch05/ch05_tutorial.md`
- A sub-section group's approval state via:
  - **Foundations** (post-Q7+Q12 = ex-01 + ex-02; §5.1 + §5.2): `grep -cE "^- exercise-(01|02): approved" ...` returns **2**
  - **Mode-checking-flow** (post-Q7+Q12 = ex-03 + ex-04; §5.3+§5.4 merged + §5.5): `grep -cE "^- exercise-(03|04): approved" ...` returns **2**
  - **Flagship** (post-Q7+Q12 = ex-05; §5.6): `grep -cE "^- exercise-05: approved" ...` returns **1**
  - **Negatives** (post-Q7+Q12 = ex-06 + ex-07; §5.7.1 + §5.7.2): `grep -cE "^- exercise-(06|07): approved" ...` returns **2**

A session attempting to begin Mode-checking-flow work MUST refuse to proceed unless the Foundations grep returns 2. A session attempting Flagship work MUST refuse unless Mode-checking-flow grep returns 2. A session attempting Negatives work MUST refuse unless Flagship grep returns 1.

**⚠ Pre-Q7 stale grep contracts**: any session encountering `grep -cE "^- exercise-(01|02|03): approved" ... returns 3` (3 matches for Foundations, pre-Q7) MUST treat this as STALE per Q7+Q12 retraction (Q7 merged §5.3 into ex-03 of the Mode-checking-flow group; only ex-01 + ex-02 belong to Foundations post-Q7). Falling back to spec.md Q12 + Assumptions (line 314) as binding source per FR-013.

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

Group approval flips all member exercises' lines together. For example, when Foundations group is approved, ex-01 + ex-02 ALL flip from `pending review` to `approved YYYY-MM-DD` in one commit (post-Q7 — only 2 exercises, NOT 3).

---

## Initial state of the chapter-5 status block

When `ch05_tutorial.md` is first written (during ex-01 implementation, before any approval), the status block reads:

```markdown
## Exercise status

- exercise-01: pending review
- exercise-02: pending exercise-01 approval
- exercise-03: pending exercise-02 approval
- exercise-04: pending exercise-03 approval
- exercise-05: pending exercise-04 approval
- exercise-06: pending exercise-05 approval
- exercise-07: pending exercise-06 approval
```

After ex-01 + ex-02 are written but Foundations group is not yet approved:

```markdown
- exercise-01: pending review
- exercise-02: pending review
- exercise-03: pending exercise-02 approval
... (rest unchanged)
```

After Foundations group approval (e.g., on 2026-05-01):

```markdown
- exercise-01: approved 2026-05-01
- exercise-02: approved 2026-05-01
- exercise-03: pending review
... (rest follows once written)
```

Within-group "pending" semantics: per FR-009, within a group exercises don't pairwise gate. So once Foundations is approved, ex-03 starts writing → its status becomes `pending review` → then ex-04 starts writing → its status becomes `pending review`. The `pending exercise-N approval` state is used ONLY for cross-group-predecessor pending (e.g., ex-05 stays `pending exercise-04 approval` until Mode-checking-flow group is fully approved, at which point ex-05 starts and flips to `pending review`). Within a group, the implementer writes exercises sequentially but they all flip to `pending review` as they're written, not blocked by a within-group predecessor's approval.

After all 7 exercises approved (chapter complete, e.g., 2026-05-04):

```markdown
- exercise-01: approved 2026-05-01
- exercise-02: approved 2026-05-01
- exercise-03: approved 2026-05-02
- exercise-04: approved 2026-05-02
- exercise-05: approved 2026-05-03
- exercise-06: approved 2026-05-04
- exercise-07: approved 2026-05-04
```

This final state is the trigger for flipping the top-level `tutorial.md` chapter-5 row from `pending review (…)` to `implemented 2026-05-04`. Note: dates above are illustrative; actual implementation may compress to a single day if the implementer is autonomous.

---

## Validation rules

- Exactly **SEVEN** bullets in the block; no more, no fewer (post-Q7+Q12 binding).
- Bullet order MUST match `exercise-01 / exercise-02 / … / exercise-07`.
- Each bullet MUST start with `- exercise-NN: ` (note the leading hyphen-space and the colon).
- `approved` status MUST carry a date; non-`approved` statuses MUST NOT carry one.
- Date MUST be in `YYYY-MM-DD` format.
- The block MUST appear under a level-2 heading `## Exercise status`.
- Group-boundary approval flips MUST be atomic in a single commit (all members of a group flip together when the group approves). For Foundations: ex-01+ex-02 flip together (2 lines). For Mode-checking-flow: ex-03+ex-04 (2 lines). For Flagship: ex-05 (1 line). For Negatives: ex-06+ex-07 (2 lines).
