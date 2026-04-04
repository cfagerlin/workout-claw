#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WATCHED_PREFIXES = [
    'skill/SKILL.md',
    'skill/commands/',
    'scripts/',
    'examples/config.example.json',
    'docs/RELEASES.md',
    'docs/QA.md',
]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else 'HEAD~1'
    changed = git('diff', '--name-only', f'{base}..HEAD').splitlines()
    watched_changed = any(any(path == prefix or path.startswith(prefix) for prefix in WATCHED_PREFIXES) for path in changed)
    version_changed = 'VERSION' in changed

    if watched_changed and not version_changed:
        print('WARN: core behavior/product files changed but VERSION did not.')
        print('Consider whether this PR should bump VERSION.')
        return 1

    print('OK: version bump check passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
