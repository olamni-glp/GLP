# SUPERSEDED 2026-05-04

This specs directory was created by the prior ch07 implementation pipeline (`d9045902` 2026-05-02 through `f094f9db` 2026-05-03) — `/speckit-specify` + `/speckit-clarify` + `/speckit-plan` + `/speckit-tasks` + `/speckit-analyze` artefacts.

The implementation it produced (`26e01792` and `f094f9db`) was rejected by the project owner as confabulated theory + false-provenance Flutter trace. The current ch07 implementation (v2026.05.04) bypassed this spec and used direct REPL probing + `programs/cssg_modules/` source reading instead. See `olamni/tutorial/ch07/ch07_tutorial.md` for the chapter's current shape and `<user-memory-dir>/tutorial_exercise_standard.md` for the exercise authoring standard the project owner validated.

**This directory is preserved per the no-removal directive but the spec/plan/tasks within it do NOT describe the chapter as it ships.** Notably:

- `spec.md`'s Q1+Q5 cluster A/B split is rejected.
- `plan.md`'s 18-phase + 11-gate workflow was not followed.
- `tasks.md`'s T001..T184 task list was abandoned.
- The 5 contracts (`trace`, `flutter-trace`, `status-block`, `glp-file`, `test-mirror`) describe a structure the chapter no longer uses.
- The `quickstart.md` instructions reference the rejected cluster framework.

The artefacts collectively serve as a record of the rejected approach.
