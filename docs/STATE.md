# Local State Model

Workout-claw stores user-specific runtime state under `~/.workout-planner/`.

## Core files and directories
- `profile.json` — durable user profile, equipment, goals, preferences, and integration setup
- `config.json` — product/runtime preferences such as update policy
- `plans/` — weekly plans by start date
- `logs/` — workout and event logs
- `goals/` — goal/progress summaries and event-specific notes
- `rehab/` — rehab/program-specific progress logs when useful

## Recommended file conventions
### Weekly plans
- `plans/week-YYYY-MM-DD.md`
- one file per week start date
- store draft/final plan context and major changes

### Workout/event logs
- `logs/YYYY-MM.jsonl`
- append one JSON object per event
- event types may include:
  - `workout_completed`
  - `workout_missed`
  - `plan_adjusted`
  - `goal_review`
  - `rehab_progress`

### Goal summaries
- `goals/progress.md`
- concise rolling summary of major goals, status, and recent trend

### Rehab/program logs
- `rehab/<slug>.md`
- optional detailed notes for active rehab or mobility programs when the user relies on them heavily

## Design rule
Do not invent a complex database.
Prefer simple, inspectable files that are easy for both humans and agents to read and update.
