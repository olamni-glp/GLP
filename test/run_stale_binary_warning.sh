#!/usr/bin/env bash
# Regression test: stale-binary warning must fire when the AOT exe's baked
# GLP_BUILD_COMMIT differs from the repo's current git HEAD.
#
# History: the ch02 tutorial bug was masked because users couldn't tell their
# .exe was stale — the "Build:" line was dynamically computed from `git log`
# at REPL startup, so it always reported the current checkout regardless of
# what the binary actually contained. The fix bakes GLP_BUILD_COMMIT at compile
# time (--define) and warns when it differs from the current HEAD.

set -e

GLP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GLP_RUNTIME="$GLP_DIR/glp_runtime"

if [ -z "$DART" ]; then
    if command -v dart >/dev/null 2>&1; then
        DART="dart"
    elif [ -x "/c/Users/gavri/dart-sdk/bin/dart" ]; then
        DART="/c/Users/gavri/dart-sdk/bin/dart"
    elif [ -x "/opt/homebrew/bin/dart" ]; then
        DART="/opt/homebrew/bin/dart"
    else
        echo "ERROR: dart not found" >&2
        exit 1
    fi
fi

cd "$GLP_RUNTIME"

PASS=0
FAIL=0

check() {
    local name="$1" pattern="$2" output="$3"
    if echo "$output" | grep -q -- "$pattern"; then
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name"
        echo "    Expected pattern: $pattern"
        echo "    Output:"
        echo "$output" | head -25 | sed 's/^/      /'
        FAIL=$((FAIL + 1))
    fi
}

check_not() {
    local name="$1" pattern="$2" output="$3"
    if echo "$output" | grep -q -- "$pattern"; then
        echo "  FAIL: $name (unexpected pattern present: $pattern)"
        FAIL=$((FAIL + 1))
    else
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    fi
}

echo ""
echo "=== Stale-binary warning regression ==="
echo ""

# Case 1: build with a deliberately-fake commit hash → warning MUST fire
FAKE_EXE="$GLP_RUNTIME/glp_repl_fake.exe"
rm -f "$FAKE_EXE"
"$DART" compile exe bin/glp_repl.dart --define=GLP_BUILD_COMMIT="deadbeef simulated stale" -o "$FAKE_EXE" >/dev/null 2>&1
output=$(printf ":quit\n" | "$FAKE_EXE" 2>&1)
check     "Fake-stale binary fires STALE BINARY warning"  "STALE BINARY"                  "$output"
check     "Warning quotes the baked commit (deadbeef)"    "built from deadbeef"           "$output"
check     "Warning suggests the rebuild command"          "dart compile exe"              "$output"

# Case 2: build with no --define at all → "Built from: unknown" but no warning
NODEF_EXE="$GLP_RUNTIME/glp_repl_nodef.exe"
rm -f "$NODEF_EXE"
"$DART" compile exe bin/glp_repl.dart -o "$NODEF_EXE" >/dev/null 2>&1
output=$(printf ":quit\n" | "$NODEF_EXE" 2>&1)
check     "No --define produces 'Built from: unknown'"   "Built from: unknown"            "$output"
check_not "No --define does NOT spuriously warn STALE"   "STALE BINARY"                   "$output"

# Case 3: build with the actual current commit → no warning
CURR_EXE="$GLP_RUNTIME/glp_repl_curr.exe"
rm -f "$CURR_EXE"
BUILD_COMMIT="$(git -C "$GLP_DIR" log -1 --format='%h %s')"
"$DART" compile exe bin/glp_repl.dart --define=GLP_BUILD_COMMIT="$BUILD_COMMIT" -o "$CURR_EXE" >/dev/null 2>&1
output=$(printf ":quit\n" | "$CURR_EXE" 2>&1)
check     "Current-commit build reports 'Built from: <hash>'"  "Built from: $BUILD_COMMIT"  "$output"
check_not "Current-commit build does NOT warn STALE"           "STALE BINARY"                "$output"

# Cleanup
rm -f "$FAKE_EXE" "$NODEF_EXE" "$CURR_EXE"

echo ""
echo "Stale-binary warning: PASS=$PASS FAIL=$FAIL"
if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
