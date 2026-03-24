# Prehab App Integration Reference

## About Prehab

The Prehab app (by The Prehab Guys) is a digital rehab/prehab platform built by physical therapists. It offers:
- 55+ structured programs (rehab, prehab, mobility, performance, fitness)
- 4,000+ exercise video library
- 100+ class-style videos
- Body scan assessment for personalized program recommendations
- Progressive loading and exercise sequencing

## Integration Approach

No public API exists. Integration is through manual tracking and intelligent scheduling:
1. User tells us which programs they're doing
2. We track phase, week, and session progress
3. We schedule Prehab sessions into the weekly plan
4. User reports completion and subjective feedback after sessions
5. We advance the tracker and note progress

## Program Categories

| Category | Description | Typical Duration | Example Programs |
|----------|-------------|-----------------|-----------------|
| Rehab | Injury recovery programs | 6-12 weeks | Knee Rehab, Shoulder Rehab, Hip Rehab, Back Rehab |
| Prehab | Injury prevention / tissue resilience | 4-8 weeks | Knee Prehab, Ankle Prehab, Shoulder Prehab |
| Mobility | Joint mobility and flexibility | 4-6 weeks | Hip Mobility, Thoracic Mobility, Full Body Mobility |
| Performance | Athletic performance enhancement | 6-12 weeks | Power Development, Speed & Agility |
| Fitness | General fitness programs | 4-8 weeks | Home Workout, Gym Fitness, Bodyweight Programs |

## Program Structure

Programs typically follow a phased progression:

**Phase 1 (Foundation):** Basic movement patterns, stability work, pain-free range of motion. Low load, high control.

**Phase 2 (Building):** Increased range of motion demands, moderate loading, multi-planar movements. Neuromuscular control focus.

**Phase 3 (Strengthening):** Progressive load increases, compound movements, sport/activity-specific patterns.

**Phase 4 (Performance):** Full loading, dynamic movements, return to full activity. Advanced exercises.

Each phase typically lasts 2-4 weeks with 3-4 sessions per week. Sessions run 20-35 minutes.

## Tracking in the Profile

```json
{
  "prehab_programs": [
    {
      "name": "Hip Rehab Program",
      "category": "rehab",
      "status": "active",
      "started": "2026-02-15",
      "current_phase": 2,
      "total_phases": 4,
      "current_week": 3,
      "sessions_per_week": 3,
      "sessions_completed_this_week": 1,
      "total_sessions_completed": 18,
      "notes": "Internal rotation improving. Phase 1 felt easy by end.",
      "milestones": [
        {"date": "2026-03-01", "note": "Completed Phase 1, felt confident"},
        {"date": "2026-03-15", "note": "Can hold 90/90 both sides for 30 seconds"}
      ]
    }
  ]
}
```

## Scheduling Prehab Sessions

### When to Schedule
- **Morning slots are ideal** — 20-30 min before work is perfect for Prehab
- **Pre-strength training** — Prehab mobility work as an extended warm-up before related lifts (e.g., hip rehab before squat day)
- **Stand-alone sessions** — On lighter training days or rest days

### How to Integrate with Strength Training
The Prehab program should complement, not conflict with, the user's strength work:

- **Hip rehab + squat day:** Do the Prehab hip session as a warm-up before squats. The activation and mobility work primes the movement pattern.
- **Shoulder rehab + press day:** Same principle — Prehab shoulder session before overhead pressing.
- **Avoid scheduling Prehab for a body part immediately after heavy training of that area** (e.g., don't do hip rehab the morning after heavy deadlifts — the tissue needs recovery first).

### Session Logging

When the user reports completing a Prehab session:

1. Log the session with date, phase, and subjective feedback
2. Increment the sessions_completed counter
3. Check if they've completed all sessions for the current week
4. Check if they're ready to advance to the next phase (completed all weeks in current phase)
5. If advancing phases, ask how they feel — confidence, any lingering pain, ROM improvements

```markdown
### 2026-03-22 — Prehab: Hip Rehab Phase 2, Session 19
**Duration:** 25 min
**Difficulty:** Moderate — getting easier
**Notable:** 90/90 hold now comfortable at 30 sec both sides. Squat depth improving.
**Progress:** Phase 2: 19/24 sessions (Week 3 of 4, 1/3 this week)
**Next milestone:** Finish Phase 2 (5 sessions remaining, ~2 weeks)
```

## Complementary Programming

When the user has an active Prehab program, the skill should:

1. **Protect the rehab area.** Don't program exercises that aggravate the issue. If someone is in a hip rehab program, be cautious with heavy hip-dominant movements early in the program.

2. **Reinforce the rehab work.** Strength exercises should support the Prehab goals. For hip rehab, include goblet squats (depth work), glute bridges (activation), and single-leg work (stability).

3. **Track the intersection.** As Prehab progresses, gradually introduce more challenging movements in the strength program. Phase 3 of hip rehab might coincide with adding back heavy squats.

4. **Celebrate progress.** Prehab is often the least exciting part of training. Note milestones, improvements in ROM, and how the rehab work is showing up in their lifts.
