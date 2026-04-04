# Update Check

Run this lightweight preamble near the start of the skill when the environment supports local scripts and file access.

## Goal
Check whether a newer version of workout-claw is available and decide whether to prompt the user based on local update preferences.

## Local state
- Current version file: `VERSION`
- Local config file: `~/.workout-planner/config.json`
- Example config: `examples/config.example.json`
- Read/write helper: `scripts/workout-claw-config.py`
- Update-check helper: `scripts/workout-claw-update-check.py`
- Upgrade helper: `scripts/workout-claw-upgrade.py`

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

Optional field:
- `default_snooze_hours` — how long `remind me later` should snooze prompts by default

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
- `update now` → proceed with the repo's documented upgrade flow, using `scripts/workout-claw-upgrade.py` as the lightweight helper when appropriate
- `remind me later` → set a future `snooze_until` timestamp in local config using `scripts/workout-claw-config.py snooze-hours <n>`
- `never ask again` → set `mode` to `never` using `scripts/workout-claw-config.py set-mode never`
- `always ask` → set `mode` to `ask` and clear any snooze using `scripts/workout-claw-config.py set-mode ask` and `scripts/workout-claw-config.py clear-snooze`
- after showing a prompt for a specific version, mark it with `scripts/workout-claw-config.py mark-prompted <version>`

## Design notes
- Do not auto-update silently.
- Do not block the user from using the skill if the update check fails.
- Keep the prompt short and easy to dismiss.
- If the environment cannot run the helper script, skip the check quietly.
