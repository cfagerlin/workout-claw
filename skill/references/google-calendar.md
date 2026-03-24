# Google Calendar Integration Reference

## Available MCP Tools

### Reading the Calendar
- **`gcal_list_calendars`** — List all calendars the user has access to
- **`gcal_list_events`** — List events within a date range. Use this to see the user's schedule for a day or week
- **`gcal_get_event`** — Get details of a specific event
- **`gcal_find_my_free_time`** — Find available timeslots. Essential for scheduling workouts

### Creating & Managing Events
- **`gcal_create_event`** — Create a new calendar event (workout session)
- **`gcal_update_event`** — Update an existing event (when rescheduling a workout)
- **`gcal_delete_event`** — Remove an event (when canceling a workout)
- **`gcal_respond_to_event`** — Respond to event invitations

### Scheduling Meetings
- **`gcal_find_meeting_times`** — Find times that work for multiple people (rarely needed for workouts)

## Workout Event Formatting

When creating workout calendar events, use this structure:

**Title:** Keep it descriptive but scannable
- "5/3/1 Squat Day + Accessories"
- "Easy Bike Ride — Zone 2 (30mi)"
- "Prehab: Hip Rehab Phase 2"
- "Apple Fitness+ HIIT (Bakari, 30 min)"
- "Morning Mobility + Foam Rolling"

**Description:** Include the full workout so the user can reference it on their phone:
```
5/3/1 Squat Day — Cycle 2, Week 3

Warm-up: 5 min bike + squat mobility

Squat: 5@275, 3@295, 1+@315
BBB Squat: 5x10@185
Bulgarian Split Squat: 3x10/leg @35lb DBs
Hanging Leg Raise: 3x12
Face Pulls: 3x15

Notes: Readiness 81 — full intensity. New accessory: BSS replaces lunges this cycle.
```

**Location:** Specify where the workout happens
- "Home Gym"
- "LA Fitness — Main St"
- "Outdoor — Torrey Pines Loop"
- "Home (Prehab App)"

**Duration:** Set to the expected session length including warm-up/cooldown

**Color/Calendar:** If the user has a separate fitness calendar, use it. Otherwise use their primary calendar.

## Scheduling Logic

### Finding Available Timeslots

1. Call `gcal_find_my_free_time` for the target day
2. Filter the results by:
   - Minimum duration needed for the session (e.g., 60 min for strength, 25 min for Prehab)
   - Time-of-day preferences (user prefers mobility in AM, strength in PM)
   - Buffer time — don't schedule a workout that ends right when a meeting starts. Leave 15-30 min buffer
3. If multiple slots work, pick the one that best matches the user's preferences

### Time-of-Day Preferences

The user's profile specifies which activities they prefer at different times of day. Use this to slot sessions intelligently:

- **Morning (before work):** Shorter sessions — mobility, Prehab, yoga, easy cardio
- **Midday (lunch break):** Quick strength circuits, short runs, Fitness+ sessions
- **Afternoon/Evening (after work):** Longer sessions — full strength workouts, long rides, interval training

### Multi-Session Days

Some days may have two training sessions (e.g., morning mobility + afternoon strength). Create separate calendar events for each. Make sure there's adequate time between sessions.

### Rescheduling

When a workout needs to move:
1. Use `gcal_delete_event` or `gcal_update_event` to clear the old slot
2. Find a new available slot using `gcal_find_my_free_time`
3. Create the new event
4. Briefly tell the user what moved and why

### Weekly Batch Scheduling

When generating a full weekly plan:
1. Get the full week's events first
2. Identify all available training windows
3. Assign sessions to slots (respecting time-of-day preferences and recovery sequence)
4. Create all events, then confirm with the user
5. The user can ask to move things around — update accordingly
