# Contributing to workout-claw

Thanks for your interest in contributing! This project is an AI skill — a set of instructions and reference files that teach an AI agent how to be a training coach. Contributing here is a bit different from a traditional software project.

## What You Can Contribute

### New Device Integrations

Want to add support for another wearable (Fitbit, Apple Watch via HealthKit, Polar, etc.)?

1. **Create a reference file** at `skill/references/[device]-api.md` with:
   - Authentication method and setup steps
   - Available endpoints/data sources and the fields they return
   - Example code for fetching key metrics (recovery, sleep, HRV, HR, activity)
   - A mapping table showing how this device's recovery/readiness signals translate to the shared intensity framework (see the WHOOP reference for an example)

2. **Create a setup guide** at `skill/references/setup-[device].md` with:
   - Prerequisites
   - Step-by-step setup instructions (assume the user has never done this before)
   - Troubleshooting for common issues

3. **Update SKILL.md**:
   - Add the device to the supported devices table in the Onboarding section
   - Add setup guide reference to the onboarding walkthrough
   - Add the device to the Data Sources section
   - Update the Normalizing Recovery Data table with the new device's signals

4. **Update the profile schema** — add an entry under `devices` in the example profile

### New Workout App Integrations

Want to add support for another workout app (Peloton, Nike Training Club, ROMWOD, etc.)?

1. **Create a reference file** at `skill/references/[app]-app.md` with:
   - What the app offers (workout types, programs, etc.)
   - Integration approach (API if available, knowledge-based if not)
   - How to suggest workouts from this app
   - How to track completion and preferences

2. **Update SKILL.md**:
   - Add the app to the Onboarding section
   - Add integration details to the App Integration Details section

### Improving Coaching Logic

The coaching logic lives in SKILL.md. If you have expertise in exercise science, periodization, or coaching, improvements are welcome:

- Better recovery-to-intensity mapping
- More sophisticated periodization guidance
- Sport-specific training plan templates
- Better variety/rotation algorithms
- Improved handling of multi-sport athletes

When improving coaching logic, please cite sources where applicable (research papers, established coaching frameworks like Bompa's periodization, etc.).

### Bug Fixes & Edge Cases

If you find a scenario where the skill gives bad advice or misses something:

1. Describe the scenario clearly (what the user said, what data was available, what the skill did vs. what it should have done)
2. Propose a fix — usually this means adding or modifying a section in SKILL.md
3. If possible, add a test case to `skill/evals/evals.json`

## How to Submit Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b add-fitbit-support`
3. Make your changes
4. Test the skill with your agent framework if possible
5. Submit a pull request with:
   - A clear description of what you added/changed
   - Why it's useful
   - How you tested it

## Style Guidelines

- **SKILL.md:** Write in the imperative voice. Explain *why* behind instructions, not just *what*. Avoid excessive MUST/NEVER — explain the reasoning so the AI understands the intent. Keep it under 500 lines if possible; use reference files for details.
- **Reference files:** Be thorough but organized. Include tables, code examples, and troubleshooting sections. Write setup guides for someone who's never done this before.
- **Profile schema:** Keep it flat and readable. Use descriptive field names. Always provide sensible defaults.

## Code of Conduct

Be kind, be constructive, be helpful. This project is about helping people train smarter — let's bring that same energy to how we work together.
