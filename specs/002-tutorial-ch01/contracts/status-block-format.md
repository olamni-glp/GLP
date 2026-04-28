# Contract: `chXX_tutorial.md` status block format

**Feature**: Olamni Tutorial Chapter 1 (`002-tutorial-ch01`)
**Source**: spec.md FR-007, FR-004; spec.md Clarifications Q2.

This contract defines the approval-gate status block embedded in every chapter signpost (`chXX_tutorial.md`). Downstream Claude sessions and human reviewers MUST be able to grep / read this block to determine whether an exercise may be implemented.

## Block structure

The status block lives under a fixed heading **`## Exercise status`** in `chXX_tutorial.md`. Format:

```markdown
## Exercise status

- exercise-01: <status> [<date>]
- exercise-02: <status> [<date or empty>]
- exercise-03: <status> [<date or empty>]
```

## Status enum

| status                              | meaning                                                                                        |
|-------------------------------------|------------------------------------------------------------------------------------------------|
| `approved YYYY-MM-DD`               | Project owner has explicitly approved this exercise. Successor exercises may be implemented.   |
| `pending <predecessor> approval`    | Files exist on disk; awaiting human review. Successor exercises MUST NOT be implemented.       |
| `pending exercise-NN approval`      | Same as above, with explicit predecessor name.                                                 |
| `not yet implemented`               | Files do NOT exist on disk; gated behind predecessor's `approved` status.                      |

Exactly one status applies per exercise at any time.

## Date format

`YYYY-MM-DD` (ISO 8601 date, no time). Dates appear ONLY for `approved` status.

## Greppability invariants

- The block heading `## Exercise status` MUST be exactly as shown (capital E, no trailing punctuation).
- Each status line begins with `- exercise-NN: ` (literal hyphen + space + `exercise` + zero-padded number + colon + space).
- The status word is the FIRST word after the colon; downstream `grep -E '^- exercise-NN: approved' chXX_tutorial.md` MUST work.
- No additional formatting (no bold, no emoji) inside the status lines themselves. The block stays grep-friendly.

## Update protocol

When transitioning exercise-NN from one status to another:
1. Implementer presents the diff to Udi (the project owner).
2. Udi explicitly approves (chat message OR commit).
3. Implementer edits `chXX_tutorial.md`: replaces the old status line with the new one.
4. Commit + push the edit. The commit IS the approval audit trail.
5. Downstream sessions can then grep the new status.

## Pre-flight check (downstream sessions)

Before writing any file under `exercise-NN/` (where N ≥ 2), the implementer MUST:

```
$ grep -E "^- exercise-$((N-1)):" olamni/tutorial/chXX/chXX_tutorial.md
- exercise-01: approved 2026-04-28
```

If the matched line does NOT contain `approved`, the implementer MUST refuse to proceed and ask Udi for explicit approval first.

## Examples

### State at end of this spec's implementation (before Udi's review)

```markdown
## Exercise status

- exercise-01: pending exercise-01 approval
- exercise-02: pending exercise-01 approval
- exercise-03: not yet implemented
```

### State after Udi approves exercise-01

```markdown
## Exercise status

- exercise-01: approved 2026-04-28
- exercise-02: pending exercise-01 approval
- exercise-03: not yet implemented
```

### State after exercise-02 implementation (before Udi review)

```markdown
## Exercise status

- exercise-01: approved 2026-04-28
- exercise-02: pending exercise-02 approval
- exercise-03: not yet implemented
```
