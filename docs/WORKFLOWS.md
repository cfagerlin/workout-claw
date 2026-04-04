# Core Coaching Workflows

Workout-claw's core coaching workflows now include:
- onboarding
- daily coach
- weekly plan
- missed workout
- post-workout
- goals review
- coach style / personalization
- update check

## Why these workflows matter
These are the situations a real coaching product needs to handle well:
- getting set up
- deciding what to do today
- planning the week
- reacting when life disrupts the plan
- learning from completed sessions
- measuring whether the overall plan is working

## Workflow split principle
If a coaching behavior has a distinct user intent and distinct decision logic, it deserves its own command module.

## Local state expectations
These workflows should also update simple inspectable local state when the environment allows it.
See `docs/STATE.md` for the file model.
