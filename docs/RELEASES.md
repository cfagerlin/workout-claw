# Release and Update Strategy

## Current state
Workout-claw now has a lightweight update-check foundation:
- repo version in `VERSION`
- local runtime config in `~/.workout-planner/config.json`
- helper script in `scripts/workout-claw-update-check.py`

## Intended behavior
The update checker is prompt-based, not automatic.
If a newer version is available, the user should get a short prompt such as:
- update now
- remind me later
- never ask again

## Important constraints
- do not auto-update silently
- do not block skill usage if the check fails
- treat the current implementation as foundation, not a full installer/upgrader yet

## Versioning discipline
Version bumps are not automatic.
To avoid relying on memory, contributors should use:
- `docs/VERSIONING.md`
- `scripts/check-version-bump.py`

If core product behavior changes and `VERSION` did not, the check should warn loudly.

## Future work
- document tagged release flow
- add an upgrade helper
- add config write helpers for snooze / never-ask state
- decide whether to use GitHub releases, tags, or both as the canonical source of latest version
