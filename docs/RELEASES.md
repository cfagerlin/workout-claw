# Release and Update Strategy

## Current state
Workout-claw now has a lightweight update-check foundation:
- repo version in `VERSION`
- local runtime config in `~/.workout-planner/config.json`
- config helper in `scripts/workout-claw-config.py`
- update-check helper in `scripts/workout-claw-update-check.py`
- upgrade helper in `scripts/workout-claw-upgrade.py`

## Intended behavior
The update checker is prompt-based, not automatic.
If a newer version is available, the user should get a short prompt such as:
- update now
- remind me later
- never ask again

## Important constraints
- do not auto-update silently
- do not block skill usage if the check fails
- persist user choices like `remind me later`, `never ask again`, and `always ask`
- keep the upgrade helper lightweight and inspectable

## Versioning discipline
Version bumps are not automatic.
To avoid relying on memory, contributors should use:
- `docs/VERSIONING.md`
- `scripts/check-version-bump.py`

If core product behavior changes and `VERSION` did not, the check should warn loudly.

## Operational flow
- use `scripts/workout-claw-config.py` to persist update-policy state
- use `scripts/workout-claw-update-check.py` to determine whether prompting should happen
- use `scripts/workout-claw-upgrade.py` as the lightweight documented upgrade helper
- publish GitHub releases consistently so latest-version lookup remains reliable

## Future work
- decide whether to use GitHub releases, tags, or both as the canonical source of latest version
- expand the upgrade helper beyond a lightweight fetch/status flow
- add optional release-note templates
