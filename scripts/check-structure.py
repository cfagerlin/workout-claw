#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    ROOT / 'VERSION',
    ROOT / 'README.md',
    ROOT / 'docs' / 'ARCHITECTURE.md',
    ROOT / 'docs' / 'QA.md',
    ROOT / 'docs' / 'RELEASES.md',
    ROOT / 'docs' / 'ROADMAP.md',
    ROOT / 'docs' / 'VERSIONING.md',
    ROOT / 'docs' / 'WORKFLOWS.md',
    ROOT / 'examples' / 'config.example.json',
    ROOT / 'examples' / 'qa-scenarios.md',
    ROOT / 'examples' / 'qa-scenarios-workflows.md',
    ROOT / 'examples' / 'versioning.example.md',
    ROOT / 'skill' / 'SKILL.md',
    ROOT / 'skill' / 'commands' / 'onboarding.md',
    ROOT / 'skill' / 'commands' / 'coach-style.md',
    ROOT / 'skill' / 'commands' / 'daily-coach.md',
    ROOT / 'skill' / 'commands' / 'update-check.md',
    ROOT / 'skill' / 'commands' / 'weekly-plan.md',
    ROOT / 'skill' / 'commands' / 'missed-workout.md',
    ROOT / 'skill' / 'commands' / 'post-workout.md',
    ROOT / 'skill' / 'commands' / 'goals-review.md',
    ROOT / 'scripts' / 'check-version-bump.py',
]


def fail(msg):
    print(f'FAIL: {msg}')
    raise SystemExit(1)


for path in REQUIRED_FILES:
    if not path.exists():
        fail(f'missing required file: {path.relative_to(ROOT)}')

try:
    json.loads((ROOT / 'examples' / 'config.example.json').read_text())
except Exception as exc:
    fail(f'invalid examples/config.example.json: {exc}')

skill_text = (ROOT / 'skill' / 'SKILL.md').read_text()
for rel in [
    'commands/onboarding.md',
    'commands/coach-style.md',
    'commands/daily-coach.md',
    'commands/update-check.md',
    'commands/weekly-plan.md',
    'commands/missed-workout.md',
    'commands/post-workout.md',
    'commands/goals-review.md',
]:
    if rel not in skill_text:
        fail(f'SKILL.md does not reference {rel}')

print('OK: structure looks consistent')
