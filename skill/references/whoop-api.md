# WHOOP API Reference

## Authentication
- **Method:** OAuth 2.0 (Authorization Code flow)
- **Authorization URL:** `https://api.prod.whoop.com/oauth/oauth2/auth`
- **Token URL:** `https://api.prod.whoop.com/oauth/oauth2/token`
- **Header:** `Authorization: Bearer <access_token>`
- **Credentials:** Client ID + Client Secret from WHOOP Developer Dashboard (developer.whoop.com)
- **Rate Limits:** 100 requests/minute, 10,000 requests/day

## Base URL
`https://api.prod.whoop.com`

All collection endpoints support pagination with `limit`, `start`, and `end` (ISO 8601 datetime) query parameters. Results sorted by start time descending.

## Endpoints

### Recovery — `GET /v2/recovery`
The primary metric for training decisions. Recovery tells you how much strain the body can handle today.

| Field | Type | Description |
|-------|------|-------------|
| recovery_score | int (0-100%) | Daily recovery percentage |
| resting_heart_rate | float (bpm) | RHR from sleep |
| hrv_rmssd_milli | float (ms) | HRV calculated from deep sleep readings |
| spo2_percentage | float (%) | Blood oxygen saturation (WHOOP 4.0+) |
| skin_temp_celsius | float (°C) | Skin temperature (WHOOP 4.0+) |
| score_state | string | "SCORED", "PENDING_SCORE", or "UNSCORABLE" |
| user_calibrating | bool | True during initial calibration period |

**Recovery zones:**
- **GREEN (67-100%):** Well recovered — can handle high strain
- **YELLOW (34-66%):** Moderate recovery — keep strain moderate
- **RED (0-33%):** Under-recovered — prioritize rest or light activity

### Cycles — `GET /v2/cycles`
24-hour physiological cycles containing strain data.

| Field | Type | Description |
|-------|------|-------------|
| strain | float (0-21) | Day strain on logarithmic Borg scale |
| kilojoule | float | Energy expended |
| average_heart_rate | int (bpm) | Mean HR during cycle |
| max_heart_rate | int (bpm) | Peak HR during cycle |

**Strain levels:**
- **Light (0-9):** Minimal stress, active recovery
- **Moderate (9-14):** Balanced training load
- **High (14-18):** Significant load, recovery needed
- **All Out (18-21):** Maximal effort, expect recovery impact

Note: Strain is logarithmic — it gets exponentially harder to add strain at higher scores.

### Sleep — `GET /v2/sleep`
| Field | Type | Description |
|-------|------|-------------|
| start/end | datetime | Sleep period timestamps |
| total_sleep_duration | int (ms) | Total time asleep |
| rem_sleep_duration | int (ms) | REM sleep time |
| deep_sleep_duration | int (ms) | Slow wave sleep time |
| light_sleep_duration | int (ms) | Light sleep time |
| awake_duration | int (ms) | Time awake during period |
| respiratory_rate | float | Breaths per minute |
| sleep_performance_percentage | float (%) | Sleep vs. needed |
| sleep_needed | object | Baseline + debt breakdown |

### Workouts — `GET /v2/workouts`
| Field | Type | Description |
|-------|------|-------------|
| sport_id | int | Activity type identifier |
| start/end | datetime | Workout timestamps |
| strain | float (0-21) | Workout strain contribution |
| average_heart_rate | int (bpm) | Mean HR |
| max_heart_rate | int (bpm) | Peak HR |
| kilojoule | float | Energy expended |
| zone_durations | object | Time in each HR zone (ms) |

### Body Measurements — `GET /v2/users/{id}/body_measurement`
| Field | Type | Description |
|-------|------|-------------|
| height_meter | float | Height in meters |
| weight_kilogram | float | Weight in kg |
| max_heart_rate | int | Estimated max HR |

### User Profile — `GET /v2/users/me`
Basic user info: name, email, created_at.

## Example: Fetch last 7 days of recovery (Python)
```python
import requests
from datetime import datetime, timedelta

headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    "start": (datetime.now() - timedelta(days=7)).isoformat() + "Z",
    "end": datetime.now().isoformat() + "Z"
}
resp = requests.get(
    "https://api.prod.whoop.com/v2/recovery",
    headers=headers, params=params
)
data = resp.json()["records"]
for record in data:
    score = record["score"]
    print(f"Recovery: {score['recovery_score']}%, "
          f"HRV: {score['hrv_rmssd_milli']:.0f}ms, "
          f"RHR: {score['resting_heart_rate']:.0f}bpm")
```

## WHOOP vs. Oura: Mapping for Training Decisions

Both devices provide recovery/readiness data but use different models. The skill normalizes them to a common decision framework:

| Decision | WHOOP Signal | Oura Equivalent |
|----------|-------------|-----------------|
| Full intensity OK | Recovery GREEN (67-100%) | Readiness 75+ |
| Moderate intensity | Recovery YELLOW (34-66%) | Readiness 60-74 |
| Recovery day | Recovery RED (0-33%) | Readiness < 60 |
| Overreaching alert | 3+ days yellow/red | 3+ days declining HRV |
| Sleep concern | Sleep performance < 70% | Sleep score < 70, efficiency < 75% |
| Illness flag | SpO2 drop + elevated skin temp | Temperature deviation > 1.0°C |

### Key Differences
- **WHOOP strain** is a unique metric Oura doesn't have — it quantifies total daily physiological load on a 0-21 scale. This is valuable for ensuring the user isn't accumulating too much strain across the week.
- **WHOOP recovery** is more training-focused ("how much strain can I handle?") while **Oura readiness** is more holistic ("am I ready to perform?").
- **WHOOP HRV** is calculated from deep sleep and last-stage readings; **Oura HRV** is averaged across the whole night. They may differ for the same night.

When a user has both devices, prefer WHOOP for strain/training-load decisions and Oura for overall wellness/readiness context. If they conflict, err on the side of caution (use the more conservative signal).
