# Versioning Policy

Workout-claw uses a simple manual versioning policy.

## Source of truth
- repo version lives in `VERSION`

## Bump guidance
### Patch
Use a patch bump for:
- doc-only fixes with no user-visible behavior change
- typo fixes
- tiny helper fixes that do not materially change behavior
- update/release-flow hardening that improves plumbing without changing the core coaching behavior contract

### Minor
Use a minor bump for:
- new command modules
- meaningful coaching behavior changes
- new integrations
- new update/release behavior
- contributor/runtime changes that alter how the product works in practice

### Major
Reserve major bumps for:
- breaking profile/config schema changes
- major install/runtime redesigns
- behavior-contract changes that would surprise existing users or integrators

## Process
Before merging a PR that changes core product behavior:
1. decide whether `VERSION` should change
2. if yes, update `VERSION`
3. run `python3 scripts/check-version-bump.py`

## Philosophy
This is intentionally not fully automated yet.
The goal is not magic versioning, it is making version decisions explicit and hard to forget.
