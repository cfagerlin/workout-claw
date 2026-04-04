#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=False)


def main():
    # Lightweight upgrade helper: fetch latest refs and tell the caller what changed.
    rc = run('git', 'fetch', '--tags', 'origin')
    if rc.returncode != 0:
        return rc.returncode
    run('git', 'status', '--short')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
