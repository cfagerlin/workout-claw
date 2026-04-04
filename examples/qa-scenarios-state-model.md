# State Model QA Scenarios

### 19. Post-workout logging
**Prompt:** `Just finished shoulder prehab.`

**Expect:**
- response acknowledges completion
- workflow expects a workout-completed log/event update
- no unnecessary heavyweight persistence assumptions

### 20. Missed workout logging
**Prompt:** `I skipped today's accessory session.`

**Expect:**
- response handles the miss calmly
- workflow expects a workout-missed log/event update
- plan adjustment is logged if the week changes

### 21. Weekly plan persistence
**Prompt:** `Build my plan for next week.`

**Expect:**
- workflow expects a weekly plan file under `plans/`
- major adjustments should be preserved in inspectable text/files

### 22. Goals review persistence
**Prompt:** `How am I doing on my goals?`

**Expect:**
- workflow expects a goal-review summary entry or file update
- output still avoids fake precision when data is partial
