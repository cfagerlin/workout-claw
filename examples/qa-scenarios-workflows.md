# Additional Workflow QA Scenarios

## Missed-workout scenarios

### 10. Missed key session
**Prompt:** `I missed today's strength session. What should I do with the rest of the week?`

**Expect:**
- no guilt-trip tone
- decides whether to reschedule or shrink it
- does not destroy the rest of the week to make up one workout

### 11. Missed low-priority session
**Prompt:** `I skipped my accessory workout today.`

**Expect:**
- recognizes lower priority
- often lets it go rather than overcorrecting

## Post-workout scenarios

### 12. Normal completed session
**Prompt:** `Just finished squats. 275x5x3. Felt solid.`

**Expect:**
- brief acknowledgment
- captures useful signal
- no unnecessary replanning if nothing suggests it

### 13. Post-workout fatigue/pain signal
**Prompt:** `Finished my run. Hip feels a little sketchy now.`

**Expect:**
- takes pain/instability seriously
- suggests a near-term adjustment
- does not shrug it off as generic soreness

## Goals-review scenarios

### 14. Overall goals check
**Prompt:** `How am I doing on my goals?`

**Expect:**
- top-line summary
- progress by goal category
- clear next focus
- not just a giant stats dump
