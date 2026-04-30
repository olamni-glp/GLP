# Contract — `ch03_tutorial.md` Status Block Format

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md)
**Date**: 2026-04-30

This contract defines the date-stamped per-exercise status block in `olamni/tutorial/ch03/ch03_tutorial.md` (the chapter signpost). It inherits the ch01 + ch02 status-block contracts verbatim, with the only change being the chapter number (3) and the dates.

---

## Format

The status block MUST appear under a Markdown level-2 heading `## Exercise status` and MUST contain exactly three bullets, in order:

```markdown
## Exercise status

- exercise-01: <status> [<date>]
- exercise-02: <status> [<date or empty>]
- exercise-03: <status> [<date or empty>]
```

**`<status>` values** (single source of truth across all per-chapter signposts):

| Value | When used | Example |
|---|---|---|
| `not yet implemented` | exercise dir does NOT exist on disk | `- exercise-02: not yet implemented` |
| `pending exercise-N approval` | predecessor exercise's status is not `approved` (use predecessor's number for N); current exercise dir does NOT exist | `- exercise-02: pending exercise-01 approval` |
| `pending review` | exercise dir EXISTS, files are written, but project-owner has not yet approved | `- exercise-01: pending review` |
| `approved YYYY-MM-DD` | project owner has explicitly approved; this is the canonical "ready for downstream consumption" state | `- exercise-01: approved 2026-04-30` |

**`<date>`** is in `YYYY-MM-DD` format (ISO 8601 date-only). Empty for `not yet implemented` / `pending exercise-N approval` / `pending review`.

---

## Greppable contract

Downstream Claude sessions MUST be able to determine an exercise's approval state via a single grep against `olamni/tutorial/ch03/ch03_tutorial.md`:

```bash
grep -E "^- exercise-NN: (approved [0-9-]+|pending|not yet implemented)" olamni/tutorial/ch03/ch03_tutorial.md
```

A session attempting to begin `exercise-(N+1)` MUST refuse to proceed if the exercise-N line does not match `approved YYYY-MM-DD`.

---

## State transitions

```
[ not yet implemented ]
        │
        │ (predecessor moves to `approved` AND files for this exercise are written)
        ▼
[ pending exercise-N approval ]   (only used while predecessor is non-approved; auto-skipped on lockstep approval)
        │
        ▼
[ pending review ]                (exercise files exist; awaiting human approval)
        │
        │ (project owner approves)
        ▼
[ approved YYYY-MM-DD ]
```

ex-01's predecessor is the chapter signpost itself; ex-01 transitions directly from `not yet implemented` to `pending review` to `approved YYYY-MM-DD`.

---

## Initial state of the chapter-3 status block

When `ch03_tutorial.md` is first written (during ex-01 implementation, before the project owner has approved anything), the status block reads:

```markdown
## Exercise status

- exercise-01: pending review
- exercise-02: pending exercise-01 approval
- exercise-03: pending exercise-02 approval
```

After ex-01 is approved (e.g., on 2026-04-30):

```markdown
## Exercise status

- exercise-01: approved 2026-04-30
- exercise-02: pending review
- exercise-03: pending exercise-02 approval
```

(Implementation moves to ex-02 only after the ex-01 line flips to `approved`.)

After all three are approved:

```markdown
## Exercise status

- exercise-01: approved 2026-04-30
- exercise-02: approved 2026-04-30
- exercise-03: approved 2026-04-30
```

This final state is the trigger for flipping the top-level `tutorial.md` chapter-3 row from `pending review (…)` to `implemented 2026-04-30`.

---

## Validation rules

- Exactly THREE bullets in the block; no more, no fewer.
- Bullet order MUST match `exercise-01 / exercise-02 / exercise-03`.
- Each bullet MUST start with `- exercise-NN: ` (note the leading hyphen-space and the colon).
- `approved` status MUST carry a date; non-`approved` statuses MUST NOT carry one.
- Date MUST be in `YYYY-MM-DD` format.
- The block MUST appear under a level-2 heading `## Exercise status`. Any deeper or shallower heading level is non-conformant.
- Any other text or formatting between the heading and the three bullets is non-conformant; the block is meant to be unambiguously machine-readable.
