# Onboarding

Use this module when the user is setting up workout-claw for the first time or when `~/.workout-planner/profile.json` does not exist.

## Goal
Create a usable profile without turning setup into a miserable form-filling ritual.

## Conversation flow
Collect the following in a natural order:
1. wearable devices and setup status
2. calendar integration preferences
3. workout apps (Apple Fitness+, Prehab)
4. equipment and training locations
5. goals
6. schedule and training preferences
7. automation preferences
8. coaching-style preferences

The onboarding should feel like a conversation, not a questionnaire.

## Wearables
Supported devices:
- Oura Ring
- WHOOP
- Garmin (via GarminDB)

Rules:
- users can connect multiple devices
- if devices disagree later, the coach should use the more conservative reading
- if the user has no wearable, the skill should still work using self-report + calendar + weather

For setup-heavy flows, read the relevant guide directly:
- `references/setup-oura.md`
- `references/setup-whoop.md`
- `references/setup-garmindb.md`

## Calendar integration
Ask whether workouts should be scheduled directly onto the calendar.
If enabled, confirm the provider and calendar target.
If not enabled, the skill should still work with markdown plan files and conversational recommendations.

## Workout apps
Supported apps:
- Apple Fitness+
- Prehab

For Apple Fitness+, gather trainer and workout-type preferences.
For Prehab, gather active programs and current phase/week if known.

## Equipment and goals
Capture available equipment by location and the user's real training goals:
- health metrics
- activity volume goals
- event goals
- rehab / mobility goals

## Profile output
Write the resulting state to `~/.workout-planner/profile.json`.
If the user later changes devices, goals, equipment, programs, or coach-style settings, update the profile instead of asking them to edit JSON manually.
