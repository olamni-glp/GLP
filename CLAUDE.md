# Instructions for Claude Code

## 1. Bootstrap (start of every conversation)

Read these four files in order, acknowledging each by name when complete:

1. `CLAUDE.md` (this file)
2. `docs/DISCIPLINE.md`
3. `docs/typed-glp-manual.md`
4. `docs/glp-cheat-sheet.md` — compact GLP-vs-Prolog reference; study the wrong-vs-right examples carefully

Then **stop and wait** for user direction before reading anything else (handovers, specs, code).

🔴 **Never program based on ignorance of GLP.** GLP is *not* Prolog. Read the manual and cheat sheet *before* writing or modifying any `.glp` code. If they don't cover your case: STOP, state the gap, wait until it is fixed. Do not speculate, guess, or grope in the dark.

After user gives direction:
1. Detect environment (§2)
2. Set Dart on PATH; verify with `dart --version`
3. Mount reference repos: `git clone --depth 1 https://github.com/EShapiro2/FCP.git /tmp/FCP` and `git clone --depth 1 https://github.com/EShapiro2/Art-of-GLP-2025.git /tmp/Art-of-GLP-2025`
4. Identify current mode (§3)
5. Ask for current state (latest code/errors)
6. Read specs **as needed**, not all upfront
7. Check `docs/current_plan.md` (§18) — if it exists, resume from the marked step

After context compaction (a session summary replaces the original conversation): STOP, tell the user, summarise where things stand, ask how to proceed. Never assume the summary is complete or that prior agreements still hold.

## 2. Project context and environment

**Project:** GLP (Grassroots Logic Programs) — a secure concurrent logic programming language. **Implementation:** Dart. **User:** deep GLP-semantics expertise but does not write code.

| Environment | GLP project root | Dart binary |
|---|---|---|
| Mac (primary) | `/Users/udi/Grassroots/GLP` | `/opt/homebrew/bin/dart` |
| Linux | `/home/user/GLP` | `/home/user/dart-sdk/bin/dart` |
| Windows (research clone) | `D:\bstdev\research\glp\glp` | `C:\Users\gavri\dart-sdk\bin\dart.exe` |

Detect by checking which root exists. Set `PATH` accordingly. Verify with `dart --version`. **When giving shell commands to the user, use paths matching their current environment.** Use forward slashes / `cd /d/bstdev/research/glp/glp` style on Windows-bash.

**Dart requirement: `^3.9.4`** (use 3.10.1 or later). If absent on Linux:
```bash
cd /home/user && curl -L -o dart-sdk.zip "https://storage.googleapis.com/dart-archive/channels/stable/release/3.10.1/sdk/dartsdk-linux-x64-release.zip" && unzip -o dart-sdk.zip && rm dart-sdk.zip && export PATH="/home/user/dart-sdk/bin:$PATH"
```
What does NOT work on Linux: `curl https://dart.dev/get-dart | sh` (403); `apt-get install dart` (not packaged); `busybox unzip` (absent).

**Reference repos** (cloned to `/tmp/`):
- FCP (Flat Concurrent Prolog): authoritative release at `/tmp/FCP/Savannah/`; key term-syntax doc `/tmp/FCP/Savannah/efcp/Logix/CONSTANTS.txt`. GitHub: https://github.com/EShapiro2/FCP. Local Mac copy: `/Users/udi/Dropbox/Concurrent Prolog/FCP/Savannah`.
- Art-of-GLP-2025 (book + LaTeX): main file `/tmp/Art-of-GLP-2025/main_AofGLP.tex`. GitHub: https://github.com/EShapiro2/Art-of-GLP-2025.

**GitHub directory zip URL:** `https://download-directory.github.io/?url=https://github.com/EShapiro2/GLP/tree/<BRANCH>/<path>`

**Verify before referencing** — `ls`, `pwd`, never hallucinate paths.

**Commands sometimes unavailable in shells**: `timeout`, `tail`, `head`. Prefer dedicated tools (Read / Grep / Glob) over shell `grep` / `cat` / `head` / `tail`.

## 3. Working modes — discussion mode is DEFAULT

**🔴 ABSOLUTE RULE: no actions during discussion.** You CANNOT proceed with ANY actions (coding, testing, running commands, git operations) until the user explicitly confirms the discussion is over with phrases like "discussion over", "let's implement", "go ahead", "proceed".

- **"stop" / "wait" means stop immediately.** Do not finish current action. Do not clean up. Just stop. User direct commands override hook feedback — no commits, no pushes, no cleanup.
- **Stay on topic until user agrees the discussion is over.** Do not move away to other work. Accommodate the user's requests; stay on topic until they are fulfilled.
- **Never leave a discussion before it's finished.** Finished = user explicitly says so, or you ask "is the discussion finished?" and they say yes.
- During discussion: brief responses, show output, present findings, ask clarifying questions, no "let me just try" — even small tests or builds require approval.

**Implementation mode — only after explicit agreement.**
1. User explicitly signals: "let's implement", "go ahead", etc.
2. Confirm: "moving to implementation mode"
3. Implement what was discussed; test immediately after each change; report exactly what changed.

**Discussion-before-implementation when user gives feedback:** STOP, discuss, wait for agreement, never mix.

**Working with Udi's design process:** don't agree too quickly — Udi often changes his mind. Ask clarifying questions; point out inconsistencies or potential issues; wait for design to stabilise; push back if something seems problematic.

## 4. Spec-first development (NON-NEGOTIABLE)

**No implementation without spec. No exceptions.**

Before writing ANY code:
1. **Identify** all spec documents covering the affected area
2. **Read** the spec; quote the relevant section verbatim
3. **Verify** the spec is clear enough to implement from
4. **If unclear, missing, or inconsistent**: STOP. Discuss. Clarify or write the spec FIRST.
5. **Only then** implement, exactly matching the spec.

When code and spec disagree, three possibilities — never silently pick one:
1. Spec is clear → revise the code to match the spec
2. Spec is unclear → clarify the spec first, then code
3. Spec seems incorrect → discuss spec revision before any code work

**Reading specs correctly** (do not paraphrase or interpret):
- "If spec covers it: 'The spec says X.'"
- "If silent: 'The spec doesn't address Y.'"
- Never say "the spec is clear" then spend ten minutes explaining it.

**Single source of truth:** each subsystem has ONE authoritative spec. Other docs reference it; they don't duplicate content. Update the authoritative spec; verify references still make sense. Example: `docs/heap/heap-pointer-architecture-spec.md` is authoritative for heap design; `docs/glp-runtime-spec.txt` references it.

**"Robustness" is often a workaround in disguise.** If a function is being called with invalid input, the BUG is in the caller. Don't make the function accept invalid input to be "robust" — fix the caller. Example: if `writerForReader(addr)` receives a writer address, don't make it "handle" that — fix the caller.

**If you find yourself**: making code "work" without spec backing / adding logic not in the spec / fixing by guessing what the behaviour should be / using try-catch or null-checks to "handle" cases the spec doesn't address / adding interleaving or race-condition workarounds without understanding the protocol → STOP, report ("The spec does not cover X. Here's what I found: [quote spec]. We need to clarify/extend before I can implement"), discuss spec update, only then proceed.

This applies to all code — including actor scripts and demo plays. Before writing or modifying any actor script that uses agent/4 protocols (groups, befriending, introductions, etc.), find and read the relevant spec (e.g., `SGLP/docs/group-glp-implementation-spec.md`). Do not reverse-engineer from test output or guess from procedure names.

**Spec consistency check before any feature/fix:** identify ALL spec documents that cover the area; verify they are consistent; if conflicts exist STOP and harmonise the specs first; never implement against conflicting specs.

## 5. GLP language design authority

The GLP language definition — guards, system predicates, body kernels, directives, type system features, primitive types — **cannot be revised, extended, or added to without explicit discussion with Udi and his express approval.** This includes adding new guards, new system predicates, new body kernels, new directives, or extending the type system. Propose first, wait for approval, then implement. See DISCIPLINE.md §1.14.

## 6. Code modification protocol

| File category | Rule |
|---|---|
| `.glp` written by user | NEVER modify without discussing first; explicit approval required |
| `.glp` written by Claude in current session | Free to modify |
| Dart files | May modify; tell user before/as you do (what + why) |
| `CLAUDE.md` | When user says `#remember <X>`, add to this file (§18) |

**Before running or tracing GLP code in the REPL:** show the file path, show the goal, wait for approval (or use pre-approved commands from `.claude/settings.local.json`).

**Preserve working code.** Never remove without explicit approval: `_ClauseVar` (HEAD-phase unresolved variables — CRITICAL), `_TentativeStruct` (HEAD structure building), fallback cases, any code you don't understand. The current implementation may differ from standard WAM — respect existing patterns.

**Never delete content** (specs, code, comments, files) without explicit user approval. **Never decide on your own not to implement a change you were instructed to implement.** **Never revert a change you were instructed to make without explicit permission.** **Never divert** from the instructed task; if you encounter an obstacle, STOP, REPORT, WAIT for direction.

**Do exactly what is asked and nothing else.** Don't add extra steps, analysis, or actions beyond the request. If clarification is needed, ask first rather than assuming.

## 7. Bug protocol — no workarounds

**🔴 MANDATORY when a bug is discovered or unexpected GLP behaviour is observed:**

1. **STOP immediately.** No fixes, no workarounds, no alternative approaches.
2. **Identify clearly.** Describe what was expected, what happened, where it occurs.
3. **Check the spec** — three possibilities:
   - The code violates the spec (bug in implementation)
   - The spec is unclear (spec needs clarification first)
   - The spec seems incorrect (spec needs discussion / revision)
4. **Report and discuss** — present facts, not speculation.
5. **Wait for agreement** before any code changes.

No try-catch hacks. No null-checks for "robustness". No interleaving workarounds. No invented `skipSRSW` options. No silent corrections. The aim of debugging is the *root cause*, not making the symptom go away.

**Anonymous variable `_`** is exempt from SRSW (a writer that nobody reads); use it in abort clauses where the result is never bound.

**When debugging a GLP program:** read and follow `docs/Mandatory protocol for debugging the GLP implementation with GLP programs.txt`. Do not skip steps. Stop and report on any step failure.

**GLP Bug Reporting Format** — when a suspected GLP bug is found, report in this exact format with no intervening text:

```
**Failing Goal:**
<the goal that fails>

**Type and Procedure Declarations:**
<relevant type definitions>
<procedure declaration>

**Suspected Clause(s):**
<the clause(s) that should match but don't>
```

Then STOP and wait for discussion. Do NOT attempt to fix. Do NOT add explanations between sections.

## 8. Verify, never assume

Before referencing any file, path, or fact:
1. Verify file exists (`ls`, Glob)
2. Verify file location
3. Verify file contents (read it before describing)
4. Verify directory structure (`ls` before assuming contents)
5. No hallucinated paths — if unverifiable, say so

Applies to test files, source code, documentation, anything mentioned in instructions or memory.

## 9. File handling

Large or binary files (PDFs, PPTX, etc.) not in your context window: **ask the user to upload immediately.** Do NOT waste time on multiple tools, workarounds, or copy commands. If a path contains spaces or the first read attempt fails: ask for upload, don't retry.

## 10. Communication style

- Terse, brief, direct. No fluff, no apologies, no long explanations. Get to the point.
- Mistakes: acknowledge and move on. No promises, no verbose politeness.
- **Single-line shell commands** when giving them to the user — no comments, no multi-line, copy-pasteable.
- **Single-line commit messages** always. Multi-line confuses the shell.
- Show GLP code with **full context**: type declarations, procedure declarations, full clauses; group related definitions in one code block; no intervening text between related blocks.
- Never use the word "pattern" except in the technical "pattern-matching" sense.
- **Questions to Udi: max 2 sentences. Be concise.**
- Never ask closed-form questions (multiple choice, yes/no, pick-from-list). Free-text only when clarification is needed.
- Don't use `AskUserQuestion` boxed prompts — ask in plain text conversation.
- Don't ask "should I continue?" on obvious next steps. Make forward progress autonomously when path is clear; ask only on genuine ambiguity.
- Never BS, guess, speculate, or hallucinate. If unsure: "I'm not sure, need to check X."
- **Always offer to fetch/merge/push when finishing a task.**

## 11. Test protocol

**Suites:**

| Suite | Location | Purpose |
|---|---|---|
| Unified REPL | `test/run_all_tests.sh` | All REPL-based tests; ALWAYS run before committing |
| Book examples | `test/run_book_tests.sh` | Compilation-only check of book Programs |
| Dart unit | `glp_runtime/test/` (`dart test`) | Dart-level unit tests |
| Type-checker | `glp_runtime/bin/run_typechecker_tests.sh` | (legacy — uses archived `check_types.dart`; verify before relying on it) |

Section breakdown of `run_all_tests.sh` (subject to growth — verify by reading the script):
A typed runtime · B positive type-check · C negative type · D SRSW violations · E invalid guard · F CSSG modules · G social graph · H CSSN · I self.glp procedures · J CSSG v2 · K CSSN v2 · L dynamic dispatch · M multi-isolate (madGLP) · N Bonds v2 · O Bonds v2 multi-isolate · P module boundary · Q AOT REPL exe regression smoke

**Standard protocol:**
```bash
cd <GLP-root>
bash test/run_all_tests.sh    # ALWAYS — before AND after changes
bash test/run_book_tests.sh   # book compilation
cd glp_runtime && dart test   # Dart units
```

If baseline fails BEFORE your changes: STOP and inform the user.

**Mandatory test protocol for GLP system changes:**
1. Run unified tests
2. Commit and push (baseline checkpoint)
3. Implement
4. Run unified tests again
5. On success: commit and push

This gives a known-good baseline, attributes failures to your changes, allows easy revert.

**Tutorial-chapter exception:** captured REPL traces ARE the regression artefacts; per-chapter `.glp` files under `olamni/tutorial/chXX/` are NOT added to `test/run_all_tests.sh` (per FR-016 of each chapter spec).

**Bug fix:** add a test to Section A/B/C that verifies the fix works (not just "no crash"). Prevents regression.

**New feature:** add tests to `test/run_all_tests.sh` covering main use cases.

**REPL development cycle:** change `glp_runtime/lib/` or `glp_runtime/bin/glp_repl.dart` → run unified tests → report results.

**Adding tests to `run_all_tests.sh`:**
- Section A (runtime): heredoc REPL session + `check` assertions on output. Use separate sessions when programs define conflicting procedure names.
  ```bash
  echo "--- Description ---"
  output=$($DART run "$REPL" <<HEREDOC
  $TYPED/my_program.glp
  my_query(X).
  :quit
  HEREDOC
  2>&1)
  check "Test name" "X = expected" "$output"
  ```
- Section B (type-check positive): add path to `POSITIVE_FILES` array.
- Section C (type-check negative): add path to `NEGATIVE_FILES` array.
- New typed test programs go in `programs/tests/typed/`. All must have `procedure` declarations and pass type-checking.

**Troubleshooting:**
- Stale REPL kernel snapshot: `rm glp_runtime/.dart_tool/repl.dill` and re-run.
- Working dir: must run from GLP root.
- `DART` env var: auto-detected via `which dart`; override with `DART=/path/to/dart`.
- Path resolution: `$GLP_DIR` should be absolute.

**Debug an individual test manually:**
```bash
echo -e '<file.glp>\n<query>.\n:quit' | dart run glp_runtime/.dart_tool/repl.dill
```

**Always start with baseline tests + commit before fixing the next bug.** Always run all REPL tests after a change.

## 12. The GLP REPL — unified tool

**One tool: the REPL.** `dart run glp_runtime/bin/glp_repl.dart`. There is no separate type checker, no separate compiler, no separate runner.

Loading a `.glp` file in the REPL automatically runs the full pipeline:
1. **SRSW analysis** (single-reader / single-writer)
2. **Partial evaluation** (defined guards)
3. **Type checking** (mode/type correctness)
4. **Compilation** (bytecode)
5. **Execution** (run goals)

Successful load = passed SRSW + PE + type-check + compile. To typecheck a file, load it in the REPL. To run a file, load it then submit a goal. **That is all.**

Old standalone tools (`check_types.dart`, `glp_pe.dart`, `glpc.dart`, `dump_bc.dart`, …) are archived under `glp_runtime/bin/archive/` and **must not be executed**.

**REPL invocation patterns:**

```bash
# Interactive (Udi's standing request — use when running interactively):
dart run glp_runtime/bin/glp_repl.dart

# Batch — pipe (NO approval needed — uses pipe, NOT heredoc <<<):
echo -e '<path>.glp\n<goal>.\n:quit' | dart run glp_runtime/bin/glp_repl.dart

# Compiled exe for repeated testing:
dart compile exe glp_runtime/bin/glp_repl.dart --define=GLP_BUILD_COMMIT="$(git log -1 --format='%h %s')" -o glp_runtime/glp_repl.exe
echo -e '<path>\n<goal>.\n:quit' | ./glp_runtime/glp_repl.exe

# Kernel snapshot (test scripts use this for speed):
echo -e '<path>\n<goal>.\n:quit' | dart run glp_runtime/.dart_tool/repl.dill
```

`<<<` heredoc requires per-command user approval — avoid it.

**REPL commands:** `:trace` (toggle tracing — not `trace goal.`), `:debug` (toggle debug output), `:limit <N>`, `:activate`, `:boot`, `:help`, `:quit`. Load file first, then run goals.

**Bonds plays** (`programs/typed_book/bonds/`, NOT in `run_all_tests.sh`):
```bash
BONDS=<GLP-root>/programs/typed_book/bonds
# Single play (fplay1-6, fplay8-11):
printf 'load $BONDS/agent.glp\nload $BONDS/mediator.glp\nload $BONDS/actors.glp\nload $BONDS/boot.glp\n:limit 1000000\nfplay1.\n' | dart run glp_runtime/bin/glp_repl.dart
# Play 12 (village market — needs play12 actors + higher limit):
printf 'load $BONDS/agent.glp\nload $BONDS/mediator.glp\nload $BONDS/actors.glp\nload $BONDS/play12/alice.glp\nload $BONDS/play12/bob.glp\nload $BONDS/play12/charlie.glp\nload $BONDS/play12/diana.glp\nload $BONDS/play12/eve.glp\nload $BONDS/play12/frank.glp\nload $BONDS/boot.glp\n:limit 5000000\nfplay12.\n' | dart run glp_runtime/bin/glp_repl.dart
```
There is no `fplay7` — plays are fplay1-6, fplay8-12, plus fplay4b. Expected results: `→ succeeds` or `→ suspended` (suspended is normal for plays with escrow timers: fplay3, fplay4, fplay4b, fplay12).

**Do not load the bonds directory as a project** — it has no top-level `self.glp`; `loadProject` succeeds but doesn't export the fplay goals. Load files individually with absolute paths.

**Key paths** (relative to GLP root):
- REPL source: `glp_runtime/bin/glp_repl.dart`
- Root prelude: `programs/self.glp` (types, procedures, unit clauses)
- All `.glp` source: `programs/`  ← **single source of truth**; no copies in paper repos (SGLP, CGLP, etc.)
- REPL test files: `programs/tests/`

## 13. Directory structure (Mac primary; mirrored on Linux/Windows)

```
<GLP-root>/
├── CLAUDE.md                              # this file
├── README.md
├── docs/                                  # NORMATIVE specifications
│   ├── glp-bytecode-v216-complete.md      # instruction set spec
│   ├── glp-runtime-spec.txt               # Dart runtime architecture
│   ├── typed-glp-manual.md                # GLP programming + interactive protocols
│   ├── glp-cheat-sheet.md                 # GLP-vs-Prolog reference
│   ├── DISCIPLINE.md                      # discipline rules
│   ├── Mandatory protocol for debugging the GLP implementation with GLP programs.txt
│   ├── wam.pdf                            # Warren's Abstract Machine
│   └── 1-s2.0-0743106689890113-main.pdf   # FCP implementation paper
├── glp_runtime/                           # main Dart project
│   ├── lib/
│   │   ├── bytecode/                      # VM (runner.dart, opcodes.dart)
│   │   ├── compiler/                      # GLP→bytecode
│   │   ├── runtime/                       # heap, scheduler, cells, terms
│   │   └── analysis/type_checker/         # type checker + DFA
│   ├── test/                              # Dart unit tests
│   └── bin/
│       ├── glp_repl.dart                  # REPL source
│       └── archive/                       # old standalone tools (DO NOT execute)
├── programs/                              # ALL .glp source (single source of truth)
│   ├── self.glp                           # root prelude
│   ├── book/                              # book examples
│   ├── typed_book/                        # typed variants (incl. bonds/)
│   ├── tests/                             # REPL test files (incl. typed/)
│   ├── lib/                               # reusable library modules
│   ├── archive/                           # historical/experimental
│   └── misc/                              # miscellaneous examples
├── olamni/tutorial/                       # tutorial chapters (separate workstream)
└── test/                                  # test scripts
    ├── run_all_tests.sh                   # unified — ALWAYS run before commit
    └── run_book_tests.sh                  # book compilation
```

## 14. Git workflow

### Single-session basics

Before any work:
```bash
git status                  # clean state?
git log -1 --oneline        # current commit
dart test                   # baseline (and bash test/run_all_tests.sh)
```

**Single-line commit messages always** — multi-line confuses the shell:
```bash
# CORRECT
git commit -m "Fix Channel definition to match prelude"

# WRONG (do NOT — quote/shell breakage)
git commit -m "Fix Channel definition

- Updated transitions"
```

**Safety checkpoint** before risky changes:
```bash
git add <specific-files>
git commit -m "Checkpoint: before attempting X"
```

If things break: `git reset --hard HEAD~1` (your own last commit only) or to a known-good commit. **Never reset/revert work other than your own session's** without express user permission.

### Multi-Claude collaboration

| Concept | Rule |
|---|---|
| `main` branch | Source of truth; only the user merges into it |
| Each session's branch | `claude/...-<session-id>` (or feature branch like `006-tutorial-ch05`) |
| Pull permissions | Any branch |
| Push permissions | Own branch only (HTTP 403 otherwise) |

**Workflow:**
```
main ◄─── merge (user only) ◄────────────┐
                                         │
              pull                       │
                ▼                        │
Claude A: work → push → branch-A         │
Claude B: work → push → branch-B ────────┘
```

**At session start:** `git pull origin main` (or relevant feature branch); run baseline tests; work on your own branch.

**During work:** commit frequently with clear messages; test after each change; push to your branch (`git push -u origin <your-branch>`).

**Continuing from another session's branch:**
- *Option 1:* `git checkout -b claude/<your-branch> origin/claude/<their-branch>`; work; push to your own.
- *Option 2 (recommended):* user merges their work to main first, then you start fresh from main.

**After completing a task: ALWAYS provide merge instructions** using the **mandatory format** (copy-pasteable, with actual values — no placeholders):

```bash
cd <GLP-root>
git checkout main
git pull origin main
git fetch origin <ACTUAL-BRANCH-NAME>
git merge -m "Merge <ACTUAL-BRANCH-NAME> into main" origin/<ACTUAL-BRANCH-NAME>
git push origin main
```

- ALWAYS include `cd <GLP-root>` (user may be in wrong directory) — use the path for *their* environment.
- ALWAYS substitute the actual branch name; never use `<branch-name>` placeholder.
- ALWAYS include the fetch step.

When user says "merge with main" or "push to main": output the EXACT commands with actual values.

**Common merge issues:**
- *"not something we can merge":* `git fetch origin <branch>` first, then merge.
- *"refusing to merge unrelated histories":* add `--allow-unrelated-histories`.
- *Merge conflicts:* resolve, `git add <files>`, `git commit -m "Merge..."`, `git push origin main`.
- *Divergent local/remote:* `git pull origin main --no-rebase`.

**Verify a merge:** `cd glp_runtime && dart test && bash ../test/run_all_tests.sh`.

**Alternative: GitHub web UI** — open a PR from `claude/<branch>` to `main`, review, merge.

### Commit scope and revert discipline

Multiple Claude sessions may work on this repo concurrently:

1. **Commit only files YOU modified this session.** No `git add -A` or `git add .` (could include another session's work or sensitive files like `.env`). Use `git add <specific-files>`.

2. **Never revert / reset / undo without Udi's express permission.** Don't use `git reset`, `git revert`, `git checkout -- <file>`, or `git restore` on files you didn't modify. Undoing your own session's change is OK; undoing anyone else's needs permission. If you believe a revert is needed, STOP and explain why.

3. **On merge conflicts or unexpected changes from other sessions:** STOP and report. Don't resolve silently — the other session's work may be more recent and important.

4. **Pre-commit hooks:** never `--no-verify` or skip signing. If a hook fails, fix the underlying issue.

5. **At session end:** ensure all work is committed, pushed to your branch, and merge instructions provided.

## 15. Implementation guidance protocol

When the user (or external instructions copy-pasted from elsewhere) provide directives like:

```
File: glp_runtime/lib/bytecode/runner.dart
Line 684: Replace GetVariable handler
Logic: Check if Xi is reader, if arg is writer, allocate fresh var…
```

You: open the file → find the location → implement → test immediately → report results.

**Reviewing external instructions:** read first; raise concerns/questions before executing; don't blindly execute; don't exceed scope. Wait for confirmation if anything seems unclear.

**General-but-clear instructions are acceptable.** Verbatim code is welcome when precision is critical, but not mandatory. Required: clear WHAT, reference to spec/paper section, success criteria, file paths.

**When external instructions modify tracked files (plans, specs):** ask the user to push those changes BEFORE giving you implementation instructions, to prevent merge conflicts.

**Complete solutions, not partial victories:** think through ALL implications; test comprehensively (don't stop at first successful case); fix ALL related bugs; only declare done when EVERYTHING works.

**Small targeted fixes** you handle directly: changing operators/conditions (`>`, `>=`, `==`, `!=`); adding null/bounds checks; fixing typos / off-by-one / missing semicolons; updating variable names; adding/removing debug prints.

**Escalate (discuss with the user before acting)** for: algorithm changes; new data structures; control-flow changes; function-signature changes; new methods/classes; error-handling pattern changes; performance optimisation strategy; architectural patterns; API design.

**When user provides a complete code block to install:** save exactly as provided — no modifications. Test immediately (`dart test`, `git diff`). Report results. If it fails: "Should I revert, or discuss a fix?"

## 16. GLP implementation internals

### Core constraints

- **SRSW (single-reader / single-writer):** each variable occurs at most once per clause as reader and at most once as writer. Mandatory for all GLP code; no `skipSRSW` option.
- **Three-phase execution:** HEAD (tentative unification) → GUARDS (pure tests) → BODY (mutations).
- **Suspension:** goals suspend on unbound readers and reactivate when writers are bound.
- **Writer MGU:** binds writers only — never readers; never writer-to-writer.
- **Anonymous `_`:** writer that nobody reads; exempt from SRSW. Use in abort clauses where the result is never bound.

### Three-valued unification

1. **Success:** terms unify; σ̂w extended or verified.
2. **Suspend:** unbound reader encountered; add to Si/U.
3. **Fail:** terms cannot unify (mismatch).

### Architecture

- `RunnerContext` — execution state (`clauseVars`, `sigmaHat`, `si`, `U`)
- `BytecodeRunner` — executes bytecode instructions
- `_TentativeStruct` — HEAD-phase structure building
- `_ClauseVar` — HEAD-phase unresolved variables (CRITICAL — do not remove)
- Structure completion tracked by `argsProcessed >= structureArity`

### FCP AM adherence

- **Always follow FCP AM design precisely** — no shortcuts, "improvements", or simplifications.
- If you consider any deviation: STOP and discuss with the user first.
- Exception: general unification not needed (SRSW restriction — already agreed).
- Default: if FCP does it that way, we do it that way unless SRSW gives a simpler path.

### Bytecode disassembler (`dump_bytecode.dart`)

Location: `<GLP-root>/udi/dump_bytecode.dart` (Mac path; equivalent under Linux/Windows clone).

```bash
cd <GLP-root>/udi
dart dump_bytecode.dart glp/<filename>.glp                       # disassemble
dart dump_bytecode.dart glp/qsort.glp > /tmp/qsort_bytecode.txt  # to file
```

Output format: `PC <n>: <opcode>`. Use for: debugging compilation issues; understanding clause compilation; verifying opcode sequences; investigating variable mode conversions; checking clause structure / guard placement; analysing HEAD/GUARD/BODY instruction placement.

## 17. Reference documents

**Primary specifications (mandatory) — read at bootstrap (§1):**
1. `docs/glp-bytecode-v216-complete.md` — instruction set spec (NORMATIVE)
2. `docs/glp-runtime-spec.txt` — Dart runtime architecture (NORMATIVE)
3. `docs/typed-glp-manual.md` — GLP programming + interactive protocols
4. `docs/glp-cheat-sheet.md` — GLP-vs-Prolog reference

**Read AS NEEDED, not all at conversation start** (other than the four bootstrap files in §1).

**Mandatory debugging protocol:** `docs/Mandatory protocol for debugging the GLP implementation with GLP programs.txt` — required when debugging GLP programs; do not skip steps; STOP and report on any step failure.

**Secondary references** (consult as needed):
- `<SGLP>/docs/group-glp-implementation-spec.md` — CSSN group creation, membership, messaging
- `docs/wam.pdf` — Warren's Abstract Machine
- `/tmp/Art-of-GLP-2025/main_AofGLP.tex` — formal GLP specification (book/paper source)
- `docs/1-s2.0-0743106689900113-main.pdf` — FCP implementation paper
- `/tmp/FCP/Savannah/` — FCP source (cloned at startup)

## 18. Workflow patterns and project-specific rules

### Multi-stage task persistence (`docs/current_plan.md`)

Conversations can be compacted, losing in-progress task lists. For any multi-stage effort (3+ steps), write the plan to `docs/current_plan.md`:

```markdown
# Current Plan: [Task Name]
Started: 2026-MM-DD

## Steps
- [x] 1. Update papers
- [x] 2. Update spec
- [ ] 3. Implement in runtime ← CURRENT
- [ ] 4. Add tests
- [ ] 5. Run full test suite

## Context
[Brief description of what we're doing and why]
```

Update as you complete each step. Delete when complete. **At session start: check if `docs/current_plan.md` exists — if so, read and resume from the marked step.**

### `#remember` directive

When the user says `#remember <X>`, add it to this CLAUDE.md so it persists across sessions.

### maGLP development scope

When working on maGLP (multi-agent GLP):
- ONLY modify files in `glp_runtime/lib/multiagent/` and `glp_runtime/test/multiagent/`
- CANNOT modify core GLP files (`runner.dart`, `heap_fcp.dart`, `compiler/`, etc.) without explicit discussion and approval
- If a core-GLP bug blocks maGLP work: STOP and report — do not attempt workarounds
- Test infrastructure must work within existing GLP implementation constraints

### GrassrootsApp testing framework

See `docs/grassroots-testing-framework.md` for the theatre-style approach:
- **Agents:** personal agents from the GLP paper
- **Actors:** simulated users following scripts
- **Plays:** test scenarios in `GrassrootsApp/plays/`

Key files: `GrassrootsApp/glp/agent.glp` (personal agent), `GrassrootsApp/glp/network.glp` (2-agent network switch), `GrassrootsApp/plays/play01_cold_call/` (first scenario).

### Flutter multiagent app rebuild

After modifying `glp_runtime` code that affects the Flutter multiagent app (`glp_multiagent`):
```bash
cd <GLP-root>/glp_multiagent
pkill -f "glp_multiagent" 2>/dev/null   # kill running app
flutter clean                            # clear cached builds
flutter pub get                          # re-resolve dependencies
flutter build macos                      # rebuild
```

The Flutter app uses `glp_runtime` via path dependency; without `flutter clean` it may use cached deps and miss your changes. Verify build timestamp matches your changes. Clear log before testing: `rm -f /private/tmp/glp_multiagent_trace.log`. The app logs to `/private/tmp/glp_multiagent_trace.log`.

### Settings and approvals

When you collect commands during a session that need user approval, place them in `.claude/settings.local.json` so future sessions skip the prompts.

### Error response template

When something fails:
```
The operation failed:

[Complete error message]

Current test status: <X/N> unit tests, <Y/N> REPL tests

The error appears to be [brief description].

Options:
1. Revert the change (recommended if tests were passing before)
2. Discuss the architecture before retrying
3. Attempt a minimal fix (only if the issue is clear)

What would you like me to do?
```

### Efficiency

- No unnecessary scratch test files when an existing tool / test suite works.
- No unnecessary "should I continue?" prompts on obvious next steps.
- When you figure out a path / command / environment quirk after multiple tries, **add it to this CLAUDE.md** so future sessions don't repeat the trial-and-error.

## 19. Known limitations

### Parser: `=..` not supported in clause bodies

```glp
% FAILS:
compose(List, Tuple) :- Tuple? =.. List?.
%   Error: "Expected predicate name or comparison" at =..

% WORKS (in clause head):
X? =.. [Y|Ys] :- list(Ys?) | list_to_tuple([Y|Ys], X).
```

Status: not yet fixed. Parser needs to recognise `=..` as a valid goal in bodies.

### REPL: structs in lists in goal arguments

```glp
% FAILS in REPL goal:
distribute_indexed([send(1,a), send(2,b)], Y, Z).
%   Exception: Unsupported list head type: StructTerm

% WORKS:
distribute_indexed([], Y, Z).
[a, b, c]         % simple list ✓
[[a,b], [1,2]]    % nested list ✓
[X?, Y?]          % vars in list ✓
```

What fails: structs in lists, any compound term as a list element in a goal. Location: `glp_repl.dart` — `_buildListTermForConj` and `_buildListTerm` handle `ConstTerm` / `VarTerm` / `ListTerm` but not `StructTerm`. Impact: can't test predicates that take lists of structures (indexed distributor, binary distributor, message routing).

**Empirical-staleness note:** some chapter specs (e.g., ch04 Q2) have re-verified these limitations and found them stale on the current REPL build. **Always check empirically when relevant**, and update this section if confirmed stale.

<!-- SPECKIT START -->
Active feature: `008-tutorial-ch07` (Olamni Tutorial — Chapter 7: Module System).

For technologies, dependencies, project structure, shell commands, and other implementation context for the active feature, read the current plan: [`specs/008-tutorial-ch07/plan.md`](specs/008-tutorial-ch07/plan.md).

Companion artefacts under `specs/008-tutorial-ch07/`:
- `spec.md` — feature specification (with 5 resolved Clarifications: Q1 cluster A derived from `programs/cssg_modules/` reduced to 3-agent friend-mediated plays; Q2 6+6=12 total exercises; Q3 new dedicated test section; Q4 ex-12 covers one play per §7.7 use case; Q5 cluster A keeps all 3 plays play1/play2/play3) **+ 4 Q-amendments to be recorded during /speckit-analyze remediation** (Q1a cluster A keeps `ui/{mediator.glp, actors.glp}` byte-exact + only `boot.glp` is pruned; Q-FR003a FR-003 file listing corrected — no `ui/self.glp`, includes `mad_boot.glp`; Q-FR014a Section letter R not S; Q4a ex-12 play subset = play1+play2+play3+play4+play5).
- `research.md` — Phase 0 decisions (R-001 byte-exact `%%` comments inherited from canonical, R-002 cluster A shape reconciliation Q1+Q5 + Q1a + Q-FR003a, R-003 top-level update + ch07 transition footnote, R-004 inspection goals deferred to /speckit-implement T-PROPOSE, R-005 Dart 3.10.1 + Flutter SDK NEW pre-flight, R-006 type-checker + project-loader pre-flight, R-007 Section letter R not S + Q-FR014a, R-008 cross-chapter relationship contract NEW = multimodule-project-derivation distinct from ch04/ch05/ch02/ch06 prior types, R-009 filenames + cluster project subdirs + Flutter pairings, R-010 cluster A `boot.glp` pruning content per Q1a, R-011 Flutter pairing content per FR-011 + FR-020, R-012 ex-12 play subset locked at /speckit-plan = 1+2+3+4+5 per Q4a).
- `data-model.md` — entities NEW for ch07 (Cluster ×2, Cluster Project ×2, Cluster Project File ×11, Approval Gate within-cluster ×10, Cluster Boundary Gate ×1, Flutter Pairing ×2, Test Mirror Section R ×10 cases, Cross-chapter Relationship of type multimodule-project-derivation NEW for ch07) with state transitions.
- `contracts/trace-file-format.md` — REPL traces (10 exercises); primary action varies (project load demo for ex-01/ex-07; mechanic inspection for ex-02..ex-04 + ex-11; play sequence for ex-05 + ex-08..ex-10); strict byte-equality.
- `contracts/flutter-trace-format.md` — Flutter traces NEW for ch07 (ex-06 + ex-12); 5 phases (pre-flight + build + launch + per-play + recommended clean-session); manual-test-first per FR-017.
- `contracts/status-block-format.md` — 13-line block (12 exercise lines + 1 cluster-A boundary line); pairwise within-cluster grep contract (10 within-cluster gates) + cluster-boundary grep contract (1 boundary gate); inherits ch01–ch03 + ch06 pairwise pattern with ch07's cluster-boundary addition.
- `contracts/glp-file-format.md` — cluster project files (5 cluster A + 6 cluster B); byte-exact for all cluster B + 4 of 5 cluster A files; cluster A `boot.glp` is the ONLY DERIVED file (pruned per R-010); multimodule-project-derivation header block NEW for ch07 per R-008; per-clause `%%` paraphrase comments inherited unchanged from canonical.
- `contracts/test-mirror-format.md` — Section R structure NEW for ch07 (R-1 cluster A 4 cases load+play; R-2 cluster B 6 cases per-file diff); pre-ch07 baseline 485 → post-ch07 expected 495; explicit override of CLAUDE.md §11 tutorial-chapter exception per spec Assumptions.
- `quickstart.md` — implementer's sequential implementation order (~75 conceptual steps; cluster A first then cluster B; 11 gates total); pre-flight checklist + R-006 type-checker verification + Flutter SDK NEW pre-flight + Section F project-loader pre-flight + canonical-state verification + spec amendment recording.
- `checklists/requirements.md` — quality checklist from `/speckit-specify` (existing).
- `tasks.md` — Phase 2 task list (generated by `/speckit-tasks`).

Predecessor (ch01 through ch06) artefacts at `specs/002-tutorial-ch01/` through `specs/007-tutorial-ch06/` are inherited as the model. Branch number → dir number mapping per workflow memory: ch01→002, ch02→003, ch03→004, ch04→005, ch05→006, ch06→007, ch07→008, …, ch13→014.

Constitution governing this feature: [`.specify/memory/constitution.md`](.specify/memory/constitution.md) v1.2.0.

Workflow memory for replicating this on ch08–ch13: [`memory/olamni_tutorial_chapter_workflow.md`](memory/olamni_tutorial_chapter_workflow.md) (in the Claude memory dir).
<!-- SPECKIT END -->

<!-- BUILDKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- BUILDKIT END -->
