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
├── skill/                          # The skill itself (install this)
│   ├── SKILL.md                    # Main skill instructions
│   └── references/                 # API docs, setup guides, app references
│       ├── oura-api.md             # Oura Ring API endpoints & fields
│       ├── whoop-api.md            # WHOOP API endpoints & fields
│       ├── garmindb.md             # GarminDB tables & queries
│       ├── google-calendar.md      # Calendar scheduling logic
│       ├── apple-fitness-plus.md   # Fitness+ workout categories & suggestions
│       ├── prehab-app.md           # Prehab program tracking
│       ├── setup-oura.md           # Oura OAuth2 setup walkthrough
│       ├── setup-whoop.md          # WHOOP OAuth2 setup walkthrough
│       └── setup-garmindb.md       # GarminDB installation guide
├── examples/
│   └── profile.example.json        # Example profile (no real credentials)
├── docs/
│   └── ARCHITECTURE.md             # How the skill works under the hood
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
└── README.md                       # This file
```

## How It Works

The skill operates in three modes:

### Automated Weekly Planning (cron)
A scheduled job gathers your biometric trends, scans your calendar, checks the weather, and drafts a weekly plan. It asks you 2-3 targeted questions before finalizing and scheduling everything.

### Automated Daily Coaching (cron)
A morning briefing that checks last night's sleep and recovery, cross-references today's plan, and confirms or adjusts your sessions. On normal days it's a quick 3-line summary. On abnormal days (bad sleep, missed workout, weather change) it suggests specific adjustments.

### On-Demand Interaction
Invoke the coach anytime — early morning, post-workout, mid-week when plans change. It runs the same logic regardless of when you trigger it.

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

## License

[MIT](LICENSE)
