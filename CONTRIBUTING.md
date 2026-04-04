# Contributing to workout-claw

Thanks for your interest in contributing.

Workout-claw is now structured like a small product repo, not just one long skill file. That means contributions usually touch one of four areas:
- `skill/SKILL.md` for top-level routing and product behavior
- `skill/commands/*.md` for workflow-specific behavior
- `skill/references/*.md` for integrations and setup guides
- `scripts/` for deterministic helper behavior

## Contributor golden path
1. Read `README.md`
2. Read `docs/ARCHITECTURE.md`
3. Read `skill/SKILL.md`
4. Read the specific command or reference file you want to modify
5. Run `python3 scripts/check-structure.py`
6. Run `python3 scripts/check-version-bump.py`
7. Test representative prompts manually using `examples/qa-scenarios.md`
8. Update docs/examples if behavior changed

## What you can contribute

### New device integrations
To add another wearable or recovery data source:
1. Create a reference file at `skill/references/[device]-api.md`
2. Create a setup guide at `skill/references/setup-[device].md`
3. Update `skill/SKILL.md` routing or onboarding references if needed
4. Update example profile/config structure if the new integration changes schema

### New workout app integrations
To add another workout app:
1. Create a reference file at `skill/references/[app]-app.md`
2. Document the integration approach clearly (API-based or knowledge-based)
3. Update `skill/SKILL.md` and command docs if the app changes routing or planning behavior

### Improving coaching logic
Most behavior changes should now go into the command docs:
- daily behavior → `skill/commands/daily-coach.md`
- weekly planning → `skill/commands/weekly-plan.md`
- missed-session handling → `skill/commands/missed-workout.md`
- post-session handling → `skill/commands/post-workout.md`
- progress review logic → `skill/commands/goals-review.md`
- personalization logic → `skill/commands/coach-style.md`
- onboarding/setup behavior → `skill/commands/onboarding.md`
- product/update behavior → `skill/commands/update-check.md`

### Runtime helpers and structure
If a behavior is better expressed as deterministic code than markdown, add it to `scripts/`.
Examples:
- update checks
- config validation
- structural checks

## QA expectations
At minimum:
- run `python3 scripts/check-structure.py`
- run `python3 scripts/check-version-bump.py`
- make sure JSON examples still parse
- manually test representative prompts for the workflow you changed using `examples/qa-scenarios.md`
- update `docs/QA.md` or related docs if your change affects the QA story
- update `docs/VERSIONING.md` or `examples/versioning.example.md` if your change affects release discipline

## Style guidelines
- Keep top-level docs clear and direct
- Keep workflow detail in command docs, not scattered everywhere
- Keep integration-specific detail in reference files
- Keep user-specific tuning out of repo files
- Prefer small, explicit changes over vague cleverness

## Pull requests
A good PR should explain:
- what changed
- why it helps the user or contributor
- how you tested it
- whether it changes structure, behavior, or both

Be direct. Keep the repo cleaner than you found it.
