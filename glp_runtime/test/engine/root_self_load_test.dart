/// Regression tests for root self.glp load behaviour.
///
/// History: ch02 implementation surfaced a silent-load-failure bug in the AOT
/// compiled REPL exe — `Platform.script.resolve('../../programs/self.glp')`
/// resolved to a non-existent path because the .exe lives one directory
/// shallower than the .dart source, but `_loadRootSelf` swallowed the
/// resulting "file not found" silently. The "Loaded root self.glp" banner
/// was printed regardless, masking the failure. Every spawn of a
/// self.glp procedure (`:=/2`, `now/1`, `'_output'/1`, `wait/1`,
/// `dl_append/3`, `send/3`, `receive/3`, `mwm/2`, …) then failed with
/// "Spawn could not find procedure label: …".
///
/// Per Constitution Principle II ("Bugs Reported, Not Bypassed"), `_loadRootSelf`
/// MUST throw rather than silently skip. These tests pin that behaviour AND
/// verify a successful construction actually populates `__root_self__`.

import 'dart:io';
import 'package:test/test.dart';
import 'package:glp_runtime/engine/glp_engine.dart';

void main() {
  group('GlpEngine root self.glp load', () {
    test('successful construction loads self.glp procedures (regression: AOT-exe path bug)', () async {
      final engine = GlpEngine(
          rootSelfGlpPath: File('../programs/self.glp').absolute.path);
      // After construction, self.glp procedures MUST be reachable. The
      // simplest end-to-end check: := arithmetic must work, which exercises
      // the := procedure and the _add body kernel via self.glp's clauses.
      final result = await engine.runGoal('R := 1 + 2');
      expect(result.succeeded, isTrue,
          reason: 'self.glp\'s := must resolve. '
              'If this fails, root self.glp was not loaded into the engine '
              '(see _loadRootSelf and the path resolution in the entry-point script).');
      expect(result.bindings['R'].toString(), contains('3'));
    });

    test('successful construction makes now/1 reachable (regression: ch02 ex-03 bug)', () async {
      final engine = GlpEngine(
          rootSelfGlpPath: File('../programs/self.glp').absolute.path);
      final result = await engine.runGoal('now(T)');
      expect(result.succeeded, isTrue,
          reason: 'self.glp\'s now/1 must resolve. '
              'If this fails, root self.glp was not loaded into the engine.');
      expect(result.bindings['T'], isNotNull);
    });

    test('missing self.glp throws StateError (regression: silent skip is no longer permitted)', () {
      // Constitution Principle II: bugs reported, not bypassed.
      // Constructing GlpEngine with a non-existent self.glp path MUST throw,
      // not silently produce a half-initialised engine.
      expect(
        () => GlpEngine(rootSelfGlpPath: '/nonexistent/path/self.glp'),
        throwsA(isA<StateError>().having(
            (e) => e.message,
            'message',
            allOf(
                contains('root self.glp not found'),
                contains('/nonexistent/path/self.glp')))),
      );
    });
  });
}
