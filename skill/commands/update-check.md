# Update Check

Run this lightweight preamble near the start of the skill when the environment supports local scripts and file access.

## Goal
Check whether a newer version of workout-claw is available and decide whether to prompt the user based on local update preferences.

## Local state
- Current version file: `VERSION`
- Local config file: `~/.workout-planner/config.json`
- Example config: `examples/config.example.json`
- Helper script: `scripts/workout-claw-update-check.py`

## Supported user preferences
Store update preferences under `update_policy`:

```json
{
  "update_policy": {
    "mode": "ask",
    "snooze_until": null,
    "last_prompted_version": null
  }
}
```

Modes:
- `ask` — check for updates and prompt when a newer version is available
- `never` — never prompt again automatically

## Prompt behavior
If the helper script reports `UPDATE_AVAILABLE <current> <latest>` and local policy permits prompting, tell the user briefly:

> workout-claw update available: v<current> → v<latest>
> Options: update now / remind me later / never ask again

Interpret user responses like:
- `update now`
- `remind me later`
- `never ask again`
- `always ask`

## State changes
- `update now` → proceed with the repo's documented update/install flow
- `remind me later` → set a future `snooze_until` timestamp in local config
- `never ask again` → set `mode` to `never`
- `always ask` → set `mode` to `ask` and clear any snooze

## Design notes
- Do not auto-update silently.
- Do not block the user from using the skill if the update check fails.
- Keep the prompt short and easy to dismiss.
- If the environment cannot run the helper script, skip the check quietly.
