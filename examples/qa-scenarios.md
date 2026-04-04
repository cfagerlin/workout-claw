# Workout-Claw QA Scenarios

Use these scenarios for manual QA and behavioral regression checks.

## Daily coach scenarios

### 1. Normal morning, decent recovery
**Prompt:** `What should I do today?`

**Expect:**
- short daily recommendation
- no unnecessary question
- acknowledges yesterday if relevant
- includes at least one useful sports-psychology element when appropriate
- tone matches coach-style settings

### 2. Low recovery / poor sleep
**Prompt:** `I slept 4.5 hours and feel wrecked. What should I do today?`

**Expect:**
- reduced intensity or recovery recommendation
- clear fallback option
- no fake hype
- no pressure to force the original plan

### 3. Same-day disruption
**Prompt:** `My afternoon blew up with meetings. Can you adjust today?`

**Expect:**
- realistic same-day replanning
- shorter fallback session if needed
- preserves the spirit of the plan without fantasy scheduling

## Weekly planning scenarios

### 4. Standard weekly planning request
**Prompt:** `Build my plan for next week.`

**Expect:**
- realistic weekly structure by timeslot
- short adherence review
- no more than 2-3 targeted questions
- clear focus for the week

### 5. Weekly rebuild after slippage
**Prompt:** `I missed two workouts this week. Help me reset next week.`

**Expect:**
- no guilt-trip tone
- practical adherence review
- fallback rules for the coming week
- does not overstuff the next week to make up everything

## Coach style scenarios

### 6. Motivation adjustment
**Prompt:** `Turn motivation up.`

**Expect:**
- treats this as a profile change
- confirms or reflects the updated setting
- future responses should show stronger energy, not random verbosity

### 7. Accountability adjustment
**Prompt:** `Increase accountability.`

**Expect:**
- treats this as a profile change
- future reviews should more clearly compare plan vs actual

## Update-check scenarios

### 8. Update available
**Prompt/context:** helper script returns `UPDATE_AVAILABLE 0.2.0 0.3.0`

**Expect:**
- short update prompt
- options like update now / remind me later / never ask again
- no blocking behavior

### 9. Update suppressed
**Prompt/context:** local config mode = `never`

**Expect:**
- no update prompt

## Contributor QA note
When changing command behavior, add or revise at least one scenario here if the expected behavior meaningfully changes.
