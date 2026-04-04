# Workout-Claw QA and DevEx Review

## QA layers
Workout-claw should be reviewed at three layers:

1. **Spec QA**
   - check for contradictions, ambiguity, and missing branches in the markdown skill docs
   - verify the router, command docs, references, and examples stay aligned

2. **Helper/runtime QA**
   - validate helper scripts like `scripts/workout-claw-update-check.py`
   - verify example JSON files parse
   - verify structural assumptions hold

3. **Agent-behavior QA**
   - test real prompts like "What should I do today?" and "Build my plan for next week"
   - verify routing, brevity, adherence framing, and update behavior

## DevEx review questions
Use these questions on structural PRs:
- does this reduce or increase contributor confusion?
- is the start-here path obvious?
- is the split between repo logic and local user state clear?
- is time-to-first-understanding getting shorter or longer?
- is the extension path for new modules / integrations obvious?

## Golden-path contributor flow
1. Read `README.md`
2. Read `docs/ARCHITECTURE.md`
3. Read `skill/SKILL.md`
4. Read the command module you want to modify
5. Run `python3 scripts/check-structure.py`
6. Run `python3 scripts/check-version-bump.py`
7. Test representative prompts manually using `examples/qa-scenarios.md`
8. Update docs/examples when behavior changes

## Scenario fixtures
Use `examples/qa-scenarios.md` as the canonical set of manual behavior checks.
When the product behavior changes meaningfully, update the relevant scenario expectations.
