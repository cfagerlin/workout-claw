# Workout-Claw Architecture

## Product shape
Workout-claw is evolving from a single large skill into a product repo with:
- a top-level skill orchestrator
- modular command documents
- reference docs for integrations
- local user state in `~/.workout-planner/`
- helper scripts for deterministic tasks such as update checks and config management

## Repository structure
- `skill/SKILL.md` — main entrypoint and router
- `skill/commands/*.md` — modular command/workflow documents
- `skill/references/*.md` — integration and setup references
- `scripts/` — deterministic helpers
- `examples/` — example config/profile files
- `docs/` — architecture and roadmap

## Local state
- `~/.workout-planner/profile.json` — user profile and training configuration
- `~/.workout-planner/config.json` — local product/runtime preferences such as update policy

## Design principle
Keep reusable product logic in the repo and keep user-specific tuning in local state.
