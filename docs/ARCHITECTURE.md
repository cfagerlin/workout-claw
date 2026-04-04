# Workout-Claw Architecture

This document explains how workout-claw is structured as a product repo and how the pieces relate to each other.

## What this repo is
Workout-claw is not just a long markdown skill anymore.
It is evolving into a small product repo with:
- a top-level skill orchestrator
- modular command/workflow documents
- reference docs for integrations
- local user state in `~/.workout-planner/`
- helper scripts for deterministic tasks such as update checks and structural validation

## Repository structure
- `skill/SKILL.md` — main entrypoint and router
- `skill/commands/*.md` — modular command/workflow documents
- `skill/references/*.md` — integration and setup references
- `scripts/` — deterministic helpers
- `examples/` — example config/profile files
- `docs/` — architecture, roadmap, QA, and contributor-facing product docs

## Local state
- `~/.workout-planner/profile.json` — user profile and training configuration
- `~/.workout-planner/config.json` — local product/runtime preferences such as update policy

The core design rule is simple:
**keep reusable product logic in the repo and keep user-specific tuning in local state.**

## Data flow
A typical interaction pulls together several layers:
1. local profile and config
2. wearable/recovery data
3. calendar availability
4. weather context when relevant
5. app/program context (Prehab, Apple Fitness+)
6. command-specific coaching logic

Then the skill produces:
- a daily recommendation
- or a weekly plan
- or a profile/config update
- or a product/update prompt when relevant

## Why modular command docs exist
The old monolithic skill was powerful but getting harder to extend.
The command split exists to:
- make routing more explicit
- make contributor edits more targeted
- keep top-level context smaller
- let different workflows evolve without turning one file into a swamp

Current command modules:
- `onboarding.md`
- `coach-style.md`
- `daily-coach.md`
- `weekly-plan.md`
- `update-check.md`

## Design decisions
### Router + modules
`skill/SKILL.md` should explain the product and route to the right module.
The heavy workflow detail should live in command docs.

### References stay separate
Integration-specific details belong in `skill/references/*.md`, not in the command modules.
This keeps command docs focused on behavior and decision-making.

### Deterministic helpers belong in scripts
If something is better handled by code than prose, such as update checks or structural validation, put it in `scripts/`.

### Local state is the source of personalization
Repo files define how workout-claw works in general.
Local files define how it behaves for a specific user.

## Contributor mental model
If you want to change:
- installation/setup behavior → update onboarding docs and setup references
- day-to-day coaching behavior → update `skill/commands/daily-coach.md`
- weekly planning behavior → update `skill/commands/weekly-plan.md`
- personalization logic → update `skill/commands/coach-style.md`
- version/update logic → update `skill/commands/update-check.md` and related scripts
- integration details → update the relevant reference file
