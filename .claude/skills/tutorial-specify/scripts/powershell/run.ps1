#!/usr/bin/env pwsh
# /tutorial-specify slash-command PowerShell runner.
# See .claude/skills/tutorial-specify/SKILL.md.

$ErrorActionPreference = 'Stop'

$repoRoot = (& git rev-parse --show-toplevel 2>$null)
if (-not $repoRoot) { $repoRoot = (Get-Location).Path }

if (-not $env:TUTORIAL_SPECIFY_ROOT) { $env:TUTORIAL_SPECIFY_ROOT = $repoRoot }

$py = if ($env:TUTORIAL_SPECIFY_PYTHON) { $env:TUTORIAL_SPECIFY_PYTHON } else { 'python' }

# Ensure the package is importable; if not, prepend the src directory to PYTHONPATH.
$null = & $py -c "import tutorial_specify" 2>$null
if ($LASTEXITCODE -ne 0) {
    $srcDir = Join-Path $repoRoot 'scripts/tutorial_specify/src'
    if ($env:PYTHONPATH) {
        $env:PYTHONPATH = "$srcDir;$env:PYTHONPATH"
    } else {
        $env:PYTHONPATH = $srcDir
    }
}

& $py -m tutorial_specify @args
exit $LASTEXITCODE
