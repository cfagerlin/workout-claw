# workout-claw

An AI-powered daily training coach that integrates your wearable data, calendar, and workout apps to build adaptive, personalized training plans.

workout-claw is a skill for AI agent frameworks (designed for [OpenClaw](https://github.com/openclaw), compatible with Claude Code and other skill-based systems). It acts as a daily coach that pulls biometric data from your devices, checks your schedule and the weather, and produces smart training recommendations — then schedules them on your calendar.

## What It Does

- **Daily coaching** — Checks your recovery, sleep, and readiness each morning and tells you what to train, when, and how hard. Adapts in real-time when you miss sessions, report fatigue, or when conditions change.
- **Weekly planning** — Generates a full weekly training plan based on your goals, biometrics, calendar availability, and weather forecast. Drafts a plan for your review, then locks it in and schedules everything.
- **Recovery-aware intensity** — Uses HRV, readiness/recovery scores, sleep quality, and strain data to dial intensity up or down. Suggests recovery sessions when you're beat up, green-lights hard training when you're fresh.
- **Goal tracking** — Tracks health metrics (weight, resting HR, body fat), activity volumes (weekly cycling miles, running mileage), event training (race prep with periodization), and rehab progress.
- **Calendar scheduling** — Finds open timeslots in your calendar, respects time-of-day preferences (mobility in the morning, strength in the afternoon), and creates detailed workout events you can reference from your phone.
- **App-based workout suggestions** — Recommends specific Apple Fitness+ and Prehab app workouts when they fit the plan.
- **Equipment & program management** — Tracks your equipment by location and your structured programs (5/3/1, PPL, etc.), scheduling around them without overriding your programming.
- **Adjustable coaching style** — Supports `accountability` and `motivation` settings (1-10) so the coach can be more blunt, more encouraging, or more adherence-focused based on the user.
- **Sports psychology layer** — Adds process goals, if-then fallback plans, self-talk cues, and clear win conditions to improve adherence and reduce decision friction.

## Supported Integrations

| Integration | Type | Connection |
|-------------|------|-----------|
| **Oura Ring** | Wearable | REST API (OAuth2) |
| **WHOOP** | Wearable | REST API (OAuth2) |
| **Garmin** (via GarminDB) | Wearable + Activity | Local SQLite database |
| **Google Calendar** | Scheduling | MCP tools |
| **Apple Fitness+** | Workout App | Knowledge-based (no API) |
| **Prehab** (The Prehab Guys) | Rehab App | Manual tracking (no API) |

All integrations are optional. The skill works with any combination — even with no wearable at all (it falls back to self-reported energy levels).

## Quick Start

### 1. Install the skill

Copy the `skill/` directory into your agent's skill directory:

```bash
cp -r skill/ ~/.your-agent/skills/workout-claw/
```

Or if your framework supports `.skill` files:

```bash
# The packaged skill file is in the releases
your-agent install workout-claw.skill
```

### 2. Run onboarding

Start a conversation with your agent and say:

> Set up workout-claw

The onboarding flow will walk you through:
1. Connecting your wearable devices (with step-by-step API setup guides)
2. Enabling calendar integration
3. Connecting workout apps (Apple Fitness+, Prehab)
4. Listing your equipment and training locations
5. Setting your goals
6. Configuring your schedule preferences
7. Setting up automated daily/weekly coaching (optional cron jobs)
8. Tuning coaching style (`accountability`, `motivation`, and daily psychology prompts)

### 3. Start training

Once setup is complete, you can:

- **Morning check-in:** "What should I do today?"
- **Plan a week:** "Build my plan for next week"
- **Log a workout:** "Just finished squats — 275x5x3, felt heavy"
- **Check in post-workout:** "That session wrecked me, legs are toast"
- **Track goals:** "How am I doing on my goals?"
- **Adjust on the fly:** "I'm going to skip today's ride, can you adjust the week?"

## Project Structure

```
workout-claw/
├── skill/
│   ├── SKILL.md                    # Main orchestrator / router
│   ├── commands/                   # Modular command/workflow docs
│   │   ├── coach-style.md
│   │   ├── daily-coach.md
│   │   ├── onboarding.md
│   │   ├── update-check.md
│   │   └── weekly-plan.md
│   └── references/                 # API docs, setup guides, app references
│       ├── oura-api.md
│       ├── whoop-api.md
│       ├── garmindb.md
│       ├── google-calendar.md
│       ├── apple-fitness-plus.md
│       ├── prehab-app.md
│       ├── setup-oura.md
│       ├── setup-whoop.md
│       └── setup-garmindb.md
├── scripts/
│   └── workout-claw-update-check.py
├── examples/
│   ├── profile.example.json
│   └── config.example.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── QA.md
│   ├── RELEASES.md
│   └── ROADMAP.md
├── VERSION
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## How It Works

The skill operates in three modes:

### Automated Weekly Planning (cron)
A scheduled job gathers your biometric trends, scans your calendar, checks the weather, and drafts a weekly plan. It asks you 2-3 targeted questions before finalizing and scheduling everything.

### Automated Daily Coaching (cron)
A morning briefing that checks last night's sleep and recovery, cross-references today's plan, and confirms or adjusts your sessions. On normal days it's a quick 3-line summary. On abnormal days (bad sleep, missed workout, weather change) it suggests specific adjustments.

It can also layer in lightweight sports-psychology prompts when useful:
- **Process focus** — what to execute well today
- **If-then backup** — what to do if energy, schedule, pain, or weather interferes
- **Cue** — a short self-talk phrase
- **Win condition** — what counts as success today

### On-Demand Interaction
Invoke the coach anytime — early morning, post-workout, mid-week when plans change. It runs the same logic regardless of when you trigger it.

## Coaching Style

The coach supports two user-tunable settings:

- **Accountability (1-10)** — how strongly it emphasizes adherence, missed sessions, and plan-vs-actual review
- **Motivation (1-10)** — how much motivational / inspirational energy it uses in delivery

These can be adjusted conversationally:
- "turn motivation up"
- "turn motivation down"
- "increase accountability"
- "set motivation to 8"

The skill also supports a lightweight sports-psychology layer designed to improve adherence without turning into cheesy hype.

## Versioning and update checks

workout-claw now has a product-level `VERSION` file and a lightweight update-check design.

- current repo version lives in `VERSION`
- example local runtime config lives in `examples/config.example.json`
- update-check behavior is documented in `skill/commands/update-check.md`
- helper script lives in `scripts/workout-claw-update-check.py`

The intended behavior is simple: if a newer version exists, prompt the user with short options like **update now**, **remind me later**, or **never ask again**. No silent auto-updates.

Right now this is intentionally a foundation, not a full installer/upgrader. See `docs/RELEASES.md`.

## Recovery Decision Framework

The skill normalizes data from different wearables into a common intensity framework:

| Decision | Oura | WHOOP | No Wearable |
|----------|------|-------|-------------|
| Full intensity | Readiness 75+ | Recovery GREEN (67-100%) | "Feeling great" |
| Normal training | Readiness 60-74 | Recovery YELLOW (34-66%) | "Feeling OK" |
| Back off | Readiness < 60 | Recovery RED (0-33%) | "Tired" / "Sore" |

When multiple devices are connected, it uses all available signals and errs on the side of caution when they disagree.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new device integrations, workout app support, or improving the coaching logic.

### Contributor golden path
1. Read `README.md`
2. Read `docs/ARCHITECTURE.md`
3. Read `skill/SKILL.md`
4. Read the command module you want to modify
5. Run `python3 scripts/check-structure.py`
6. Test representative prompts manually
7. Update docs/examples if behavior changed

## License

[MIT](LICENSE)
