# Workout-Claw Roadmap

## Phase 1: Product foundation
- Add versioning (`VERSION`)
- Add local update-check flow and config example
- Split the monolithic skill into modular command docs
- Keep top-level `skill/SKILL.md` as the main orchestrator

## Phase 2: Runtime helpers
- Add a helper for update checks against GitHub releases/tags
- Add a config helper for reading/writing `~/.workout-planner/config.json`
- Add an install/upgrade helper script
- Add a packaged release flow

## Phase 3: Product hardening
- Add architecture documentation for the skill + scripts split
- Add examples for onboarding, daily coach, and weekly planning
- Add structural checks/tests for docs, files, and version consistency
- Consider generated command docs or command wrappers if the host supports them
