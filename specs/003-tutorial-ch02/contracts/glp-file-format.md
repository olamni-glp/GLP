# Contract — `.glp` File Content & Comment Format (chapter 2)

**Plan**: [../plan.md](../plan.md) | **Spec**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)
**Date**: 2026-04-28

This contract defines the content and comment format for the four `.glp` files in chapter 2. It extends the ch01 single-file contract to cover (a) an INTENTIONALLY ill-formed file (the LP-only contrast), (b) a file with a cross-chapter import provenance note, and (c) files with body-kernel-using procedures.

---

## Common rules (apply to all four files)

1. **Header comment block** — each file MUST begin with a `%`-prefixed comment block (3–8 lines) summarising what the file does and citing the PDF source.
2. **Per-clause `%%` comments** — each non-trivial clause MUST carry one `%%` comment paraphrasing the surrounding prose from the relevant book section. (Charter §1.5.)
3. **No `skipSRSW` or anti-spec language flags** — Constitution Principle III is non-negotiable. The LP-only file's intentional rejection is what the SRSW analyser is FOR; we do not bypass it.
4. **No external imports beyond `programs/self.glp`** (which is auto-loaded by the REPL) and the duplicated GLP `append/3` from PDF pp 31–32. Per spec FR-015.
5. **Byte-exactness of imported clauses** — the GLP `append/3` clauses MUST be byte-identical to PDF pp 31–32 (per spec SC-007). The classical LP append clauses MUST be byte-identical to PDF p 10 (per spec SC-006).

---

## File 1 — `exercise-01/ch-02-ex-01-classical-append-LP-only.glp`

**Purpose**: Classical LP append, INTENTIONALLY rejected by the SRSW analyser. The rejection is the demonstration.

**Content** (illustrative — actual prose comes from the implementer rereading PDF p 10 prose during /speckit-implement step 3):

```
% ch-02-ex-01-classical-append-LP-only.glp
% Example 2.1 (Append) from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §2.1, p 10.
% INTENTIONALLY ILL-FORMED FOR GLP — illustrates classical LP contraction.
% In classical Logic Programs, a variable may appear multiple times across head and body
% (e.g., Xs is both a tail-pattern in the head AND an argument to the recursive call).
% GLP forbids this via SRSW (Formal 2.1, p 14, "No contraction" row): each variable
% has exactly one writer and exactly one reader. Loading this file in the GLP REPL
% triggers the SRSW analyser, which rejects the file at load time. That rejection
% IS the chapter's pedagogical demonstration; it is NOT a defect of this tutorial.

append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).  %% classical recursive: Xs occurs twice (head + body); Ys once (head + body); Zs twice (head + body)
append([], Ys, Ys).                                 %% classical base: Ys occurs twice in head — pure structural identity in classical LP
```

**Validation rules**:
- The two clauses MUST be byte-identical to Example 2.1 on PDF p 10 after stripping the header comment block AND the per-clause `%%` annotations (per spec SC-006). Specifically, the two-line code corpus is exactly `append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).\nappend([], Ys, Ys).\n`.
- Header MUST contain the literal phrase `INTENTIONALLY ILL-FORMED FOR GLP` (per spec FR-001).
- File MUST trigger an SRSW rejection when loaded in the GLP REPL (per spec SC-002). If the analyser silently accepts it, halt-and-report.

---

## File 2 — `exercise-01/ch-02-ex-01-glp-append.glp`

**Purpose**: GLP append (cross-chapter import from PDF pp 31–32). Accepted by the SRSW analyser. Used to demonstrate that the same predicate, with `?` reader annotations, satisfies SRSW.

**Content** (illustrative):

```
% ch-02-ex-01-glp-append.glp
%% GLP append/3 byte-exact from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §4.2, pp 31–32.
%% Imported into ch02 to illustrate the SRSW transition described in §2.2 (Linear Logic, Formal 2.1).
%% This is the only cross-chapter import permitted in ch02 per the spec's Out-of-Scope section.
%% Compare with ch-02-ex-01-classical-append-LP-only.glp: same predicate name, same recursion shape,
%% but the `?` reader annotations make each variable's writer and reader explicit, satisfying SRSW.

append([], Ys, Ys?).                                 %% base: writer Ys binds; reader Ys? forwards the second list verbatim
append([X|Xs], Ys, [X?|Zs?]) :- append(Xs?, Ys?, Zs).  %% recursive: writers X, Xs, Ys, Zs in head; readers Xs?, Ys?, X?, Zs? in body — paired
```

**Validation rules**:
- The two `append/3` clauses (lines after the header block) MUST be byte-identical to PDF pp 31–32 after stripping the header AND the per-clause `%%` annotations (per spec SC-007). Specifically: `append([], Ys, Ys?).\nappend([X|Xs], Ys, [X?|Zs?]) :- append(Xs?, Ys?, Zs).\n`.
- Header MUST contain the cross-chapter provenance block per `research.md` R-007.
- File MUST be ACCEPTED by the GLP REPL with zero errors (per spec SC-003). If the REPL rejects it, halt-and-report.

---

## File 3 — `exercise-02/ch-02-ex-02-append-and-sum.glp`

**Purpose**: ex-02's body-kernel-introducing program. Defines `append/3` (duplicated from ex-01), `sum/2`, and `append_and_sum/3` (amended from the original `/4` on 2026-04-29 per spec Clarifications Q3a). Exercises the `:=` arithmetic body kernel.

**Content** (illustrative; final form composes per `research.md` R-008):

```
% ch-02-ex-02-append-and-sum.glp
%% GLP append/3 byte-exact from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §4.2, pp 31–32.
%% Imported into ch02 to illustrate the SRSW transition described in §2.2 (Linear Logic, Formal 2.1).
%% This is the only cross-chapter import permitted in ch02 per the spec's Out-of-Scope section.
%% This file extends ex-01: same GLP append, plus sum/2 and append_and_sum/3 to demonstrate
%% that SRSW lets a downstream consumer (sum) compute on a stream from a producer (append).
%% The arithmetic operator := comes from programs/self.glp.

append([], Ys, Ys?).
append([X|Xs], Ys, [X?|Zs?]) :- append(Xs?, Ys?, Zs).  %% reused verbatim — see ex-01 for paraphrase

sum([], 0).                                              %% base: empty list has sum zero
sum([X|Xs], Total?) :-                                   %% recursive: Total = head + tail-sum
    sum(Xs?, Subtotal),                                  %%   compute the tail's sum first
    Total := Subtotal? + X?.                             %%   then add the head — := is the arithmetic operator from self.glp

append_and_sum(A, B, Sum?) :-                            %% top-level: append A and B locally, sum the result, expose Sum
    append(A?, B?, Zs),                                  %%   the appender writes the local Zs (one writer)
    sum(Zs?, Sum).                                       %%   the summer reads the local Zs? (one reader) — canonical producer-consumer idiom
```

**Validation rules**:
- The two `append/3` clauses MUST be byte-identical to ex-01's GLP append (per spec FR-009). Verifiable by `diff` modulo `%%` annotations.
- File MUST define `sum/2` with two clauses matching `research.md` R-008. **Head pattern of recursive clause MUST be `sum([X|Xs], Total?)`** (writers `X` and `Xs` in head; readers `X?` and `Xs?` in body) — NOT `sum([X|Xs?], ...)` which double-counts `Xs?` as a reader.
- File MUST define `append_and_sum/3` with one clause matching `research.md` R-008.
- File MUST use `:=` at least once with `+` arithmetic (per spec FR-009 + SC-009).
- File MUST NOT call `'_add'`, `'_sub'`, `_mul`, `_div`, `_idiv`, `_mod`, `_abs`, `_pow`, `_sqrt`, or any other math kernel directly.
- File MUST NOT load any other file as a dependency (per spec FR-009 + FR-015).
- File MUST be ACCEPTED by the GLP REPL with zero errors. Running `append_and_sum([1,2,3], [4,5,6], Sum).` MUST bind `Sum = 21` (per spec SC-013).

---

## File 4 — `exercise-03/ch-02-ex-03-timed-append.glp`

**Purpose**: ex-03's body-kernel-introducing program. Defines `append/3` (duplicated from ex-01) and `timed_append/3`. Exercises `now/1` (system time) and `'_output'/1` (ground-term I/O), and reuses ex-02's `:=` arithmetic.

**Content** (illustrative; final form composes per `research.md` R-009):

```
% ch-02-ex-03-timed-append.glp
%% GLP append/3 byte-exact from "The Art of Grassroots Logic Programming" (Shapiro, 2025), §4.2, pp 31–32.
%% Imported into ch02 to illustrate the SRSW transition described in §2.2 (Linear Logic, Formal 2.1).
%% This is the only cross-chapter import permitted in ch02 per the spec's Out-of-Scope section.
%% This file extends ex-02: same GLP append, plus timed_append/3 which demonstrates that the same
%% SRSW discipline that governs lists and numbers also governs side-effecting kernels.
%% now/1 (system time) and '_output'/1 (ground-term I/O) come from programs/self.glp.
%% The ground/1 guard ensures now(End) fires only after append/3 has fully bound Zs.

append([], Ys, Ys?).
append([X|Xs], Ys, [X?|Zs?]) :- append(Xs?, Ys?, Zs).  %% reused verbatim — see ex-01 for paraphrase

timed_append(A, B, Zs?) :-                              %% top-level: time the append and emit the elapsed ms via _output
    now(Start),                                         %%   capture wallclock at start (ms since epoch)
    append(A?, B?, Zs),                                 %%   run the append concurrently
    now(End),                                           %%   capture wallclock at end
    ground(Zs?) |                                       %%   GUARD: wait for Zs to be fully bound before computing elapsed
    Elapsed := End? - Start?,                           %%   compute elapsed ms via := (reused from ex-02)
    '_output'(elapsed_ms(Elapsed?)).                    %%   emit the result as a structured term — easy to grep in the trace
```

**Validation rules**:
- The two `append/3` clauses MUST be byte-identical to ex-01's GLP append (per spec FR-010). Verifiable by `diff`.
- File MUST define `timed_append/3` with one clause matching `research.md` R-009.
- File MUST call `now/1` exactly twice (start + end) and `'_output'/1` at least once with a ground term (per spec FR-010).
- File MUST use `:=` arithmetic at least once (typically for elapsed-time subtraction; per spec FR-010).
- File MUST NOT call `_now` or `_output` body kernels directly (per spec FR-010).
- File MUST NOT load any other file as a dependency.
- File MUST be ACCEPTED by the GLP REPL with zero errors. Running `timed_append([1,2,3], [a,b,c], Zs).` MUST bind `Zs = [1, 2, 3, a, b, c]` AND emit exactly one `'_output'`-printed line of the form `elapsed_ms(N)` where N is a non-negative integer (per spec SC-014).

---

## Cross-file invariants

- The classical-LP `append/3` (in File 1) and the GLP `append/3` (in Files 2, 3, 4) share the same predicate NAME but DIFFERENT clauses. This is intentional — the chapter's pedagogy is that the SAME predicate has TWO definitions across the LP→GLP transition.
- The GLP `append/3` in Files 2, 3, 4 is byte-identical across the three files (per spec FR-009 + FR-010 + Clarification Q2).
- Per-clause `%%` paraphrase comments MAY differ across files even for the duplicated `append/3` clauses, because each file's pedagogical context differs (ex-01 introduces the SRSW idea; ex-02 reuses append as a producer; ex-03 reuses append as the timed operation).

---

## Constitution alignment

- Principle III (SRSW Discipline) — File 1 is the canonical SRSW-violating example; Files 2, 3, 4 are SRSW-compliant.
- Principle VI (Tutorial Charter Compliance) — `%%` per-clause comments per charter §1.5; cross-chapter import documented per `research.md` R-007.
- Language Design Authority — no new kernels introduced; only existing `:=`, `now/1`, `'_output'/1` used via their `programs/self.glp` declarations.
