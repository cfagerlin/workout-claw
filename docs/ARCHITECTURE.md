# Architecture

This document explains how workout-claw works under the hood, for contributors and anyone curious about the design.

## What Is a "Skill"?

A skill is a structured set of instructions that teaches an AI agent how to perform a specific task. It's not a traditional software application — there's no runtime, no server, no compiled code. Instead, it's a collection of markdown files that an AI agent reads and follows.

Think of it like a detailed playbook for an extremely capable assistant. The AI brings the intelligence; the skill brings the domain knowledge and workflow structure.

## File Structure

```
skill/
├── SKILL.md              # The main instruction set (the "brain")
└── references/           # Detailed reference material (the "library")
    ├── oura-api.md       # API docs + decision thresholds
    ├── whoop-api.md      # API docs + strain model
    ├── garmindb.md       # Database schemas + query examples
    ├── google-calendar.md # Scheduling logic + event formatting
    ├── apple-fitness-plus.md  # Workout categories + suggestion strategy
    ├── prehab-app.md     # Program tracking approach
    ├── setup-oura.md     # OAuth2 setup walkthrough
    ├── setup-whoop.md    # OAuth2 setup walkthrough
    └── setup-garmindb.md # Installation guide
```

### SKILL.md (Main Instructions)

This is what the AI agent reads first. It contains:

- **Onboarding flow** — How to set up a new user (device connections, goals, preferences)
- **Daily Coach workflow** — The step-by-step process for morning check-ins, post-workout check-ins, and missed workout handling
- **Weekly Planning workflow** — How to gather data, build a plan, and schedule it
- **Recovery guidelines** — Decision framework mapping biometric signals to training intensity
- **Automation patterns** — How cron-triggered sessions should behave differently from on-demand interactions

SKILL.md stays under 500 lines by delegating API details, setup steps, and app-specific knowledge to reference files.

### Reference Files (Progressive Disclosure)

Reference files are only read when needed. If the AI agent needs to make an Oura API call, it reads `oura-api.md`. If a user is setting up WHOOP for the first time, it reads `setup-whoop.md`. This keeps the agent's context focused on what's relevant.

## Data Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Wearables  │     │   Calendar   │     │   Weather   │
│ Oura/WHOOP/ │────>│   Google     │────>│   Forecast  │
│   Garmin    │     │   Calendar   │     │             │
└──────┬──────┘     └──────┬───────┘     └──────┬──────┘
       │                   │                    │
       v                   v                    v
┌──────────────────────────────────────────────────────┐
│                    AI Agent                           │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐ │
│  │ Recovery  │  │ Schedule │  │ Goal & Program     │ │
│  │ Analysis  │  │ Matching │  │ Tracking           │ │
│  └────┬─────┘  └────┬─────┘  └────────┬───────────┘ │
│       └──────────────┼─────────────────┘             │
│                      v                               │
│              ┌───────────────┐                        │
│              │ Training Plan │                        │
│              └───────┬───────┘                        │
└──────────────────────┼───────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          v            v            v
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ Calendar │ │ Plan.md  │ │ Training │
    │  Events  │ │   File   │ │   Log    │
    └──────────┘ └──────────┘ └──────────┘
```

## Key Design Decisions

### Modular Device Support

Every device integration is self-contained in its own reference file. Adding a new device means writing one reference file and one setup guide, then adding a few lines to SKILL.md. The core coaching logic doesn't change — it works off a normalized recovery framework that maps any device's signals to the same intensity decisions.

### Normalized Recovery Framework

Different devices speak different languages (Oura's "readiness" vs. WHOOP's "recovery" vs. Garmin's stress/sleep data). The skill normalizes everything into four levels: High / Normal / Low / Recovery. This means the weekly planning and daily coaching logic doesn't need device-specific branches.

### Draft-and-Confirm for Weekly Plans

The weekly planner never commits a full plan without user input. This was a deliberate choice — people's weeks are too unpredictable. The AI gathers all the data and produces a draft, but asks 2-3 targeted questions before finalizing. This respects the user's autonomy while still doing 95% of the work automatically.

### Briefing-Style Daily Coach

The daily coach is designed to be concise on normal days and only conversational when something changed. Most people checking their phone at 7 AM don't want an essay — they want "here's what's on tap, you're good to go." The coach only asks questions when the data raises a flag that requires a human decision.

### App Integration Without APIs

Apple Fitness+ and the Prehab app don't have public APIs. Rather than skip them, the skill uses a knowledge-based approach: it knows the categories, workout types, and general structure of these apps, and can make smart recommendations. Completion tracking happens through user check-ins. It's not as seamless as a full API integration, but it's practical and genuinely useful.

### Profile as Single Source of Truth

Everything about the user — devices, apps, equipment, goals, programs, preferences, automation settings — lives in one `profile.json` file. The skill reads it at the start of every interaction and updates it when things change. This makes the system stateful across sessions without requiring a database.

## Adding New Integrations

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines. The short version:

1. Write a reference file with API/data documentation
2. Write a setup guide for first-time users
3. Add a normalization mapping to the recovery framework
4. Update the onboarding flow and profile schema
5. Submit a PR
