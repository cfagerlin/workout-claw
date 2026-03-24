# Apple Fitness+ Reference

## Integration Approach

Apple Fitness+ has no public API, no programmatic catalog access, and no deep-linking support. This skill integrates through a knowledge-based approach:
- Suggest workouts by type, trainer, and approximate duration
- Track user preferences (favorite trainers, workout types)
- Log completed workouts via user check-ins
- Use Fitness+ strategically within the broader training plan

## Workout Categories

| Category | Typical Duration | Equipment Needed | Best For |
|----------|-----------------|-----------------|----------|
| HIIT | 10, 20, 30, 45 min | None or dumbbells | Conditioning, fat loss, time-efficient cardio |
| Yoga | 10, 20, 30, 45 min | None (mat helpful) | Recovery, flexibility, active rest days |
| Core | 10, 20, 30 min | None | Core strength, complements lifting |
| Pilates | 10, 20, 30, 45 min | None or resistance band | Core, stability, low-impact strength |
| Strength | 10, 20, 30, 45 min | Dumbbells | Full-body or targeted strength when no gym access |
| Treadmill Walk | 10, 20, 30, 45 min | Treadmill | Easy cardio, active recovery |
| Treadmill Run | 10, 20, 30, 45 min | Treadmill | Structured running (intervals, tempo, endurance) |
| Cycling | 10, 20, 30, 45 min | Stationary bike | Indoor cardio alternative to outdoor rides |
| Rowing | 10, 20, 30, 45 min | Rowing machine | Full-body conditioning |
| Dance | 20, 30, 45 min | None | Fun cardio, variety, low motivation days |
| Kickboxing | 10, 20, 30 min | None | Conditioning with upper body engagement |
| Mindful Cooldown | 5, 10 min | None | Post-workout cooldown |
| Meditation | 5, 10, 20 min | None | Stress management, sleep preparation |

## When to Suggest Fitness+ Workouts

**Recovery days:** Suggest Yoga (30 min) or Mindful Cooldown. Much better than "just stretch" because the guided format helps people actually do it.

**Low motivation days:** Suggest shorter sessions (10-20 min HIIT or Core). Something is better than nothing, and the production quality of Fitness+ can help overcome inertia.

**Cardio variety:** If the user's main cardio is outdoor cycling/running, occasionally suggest a Dance or Kickboxing workout for variety — different movement patterns, different energy.

**Travel / no gym days:** Suggest bodyweight Strength or HIIT sessions. These need no equipment and can be done in a hotel room.

**Warm-up/cooldown:** A 10-min Core or 5-min Mindful Cooldown can be paired with custom strength work.

**Weather backup:** If rain cancels an outdoor ride, suggest a Fitness+ Cycling session as the indoor alternative.

## Suggesting Workouts

When recommending a Fitness+ workout, give enough detail for the user to find it:

**Good:** "Try a 30-minute Yoga session — look for one focused on flexibility or recovery. If you like Jessica, she has great options in that range."

**Better:** "I'd suggest a 30-minute Yoga for Flexibility — you'll find several in the Yoga section. Filter by 30 minutes. This will complement your hip mobility work without taxing your legs."

Don't pretend to know specific workout titles or release dates — the catalog changes. Instead, guide by type, duration, and purpose.

## Tracking

When the user completes a Fitness+ workout, log it:
```json
{
  "date": "2026-03-22",
  "type": "Yoga",
  "duration_min": 30,
  "trainer": "Jessica",
  "user_rating": "loved it",
  "context": "recovery day after heavy squats"
}
```

Over time, this data helps personalize suggestions — lean toward trainers they enjoy, avoid types they don't connect with.
