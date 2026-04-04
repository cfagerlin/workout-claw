# Releasing Workout-Claw

## Lightweight release flow
1. decide whether the change needs a version bump
2. update `VERSION`
3. run:
   - `python3 scripts/check-structure.py`
   - `python3 scripts/check-version-bump.py`
4. create or update release notes if needed
5. merge the PR
6. create a Git tag matching the version, for example `v0.3.1`
7. optionally create/update a GitHub release so the update checker has a clear latest-version source

## Notes
- the repo currently checks GitHub releases first via the API
- if you want update checks to be reliable, publish releases consistently
- do not silently change version numbers without documenting why in the PR
