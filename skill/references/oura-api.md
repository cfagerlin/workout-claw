# Oura Ring API v2 Reference

## Authentication
- **Method:** OAuth2 (Personal Access Tokens deprecated)
- **Authorization URL:** `https://cloud.ouraring.com/oauth/authorize`
- **Token URL:** `https://api.ouraring.com/oauth/token`
- **Header:** `Authorization: Bearer [ACCESS_TOKEN]`
- **Rate Limit:** 5,000 requests per 5-minute window (HTTP 429 on exceed)

## Base URL
`https://api.ouraring.com/v2/usercollection/`

All date params use ISO 8601 (`YYYY-MM-DD`). Most endpoints accept `start_date` and `end_date` query params.

## Endpoints

### Daily Sleep — `/v2/usercollection/daily_sleep`
| Field | Type | Description |
|-------|------|-------------|
| score | int (1-100) | Overall sleep score |
| total_sleep_duration | int (seconds) | Total sleep time |
| deep_sleep_duration | int (seconds) | Deep sleep time |
| rem_sleep_duration | int (seconds) | REM sleep time |
| light_sleep_duration | int (seconds) | Light sleep time |
| awake_time | int (seconds) | Time awake during sleep period |
| efficiency | int (1-100) | Sleep efficiency |
| average_heart_rate | int (bpm) | Average HR during sleep |
| average_hrv | int (ms) | Average HRV during sleep |
| lowest_heart_rate | int (bpm) | Lowest HR during sleep |
| bedtime_start | datetime | When user went to bed |
| bedtime_end | datetime | When user got up |

### Daily Readiness — `/v2/usercollection/daily_readiness`
| Field | Type | Description |
|-------|------|-------------|
| score | int (1-100) | Overall readiness score |
| temperature_deviation | float | Core temp deviation from baseline |
| temperature_trend_deviation | float | Temp trend deviation |
| contributors.activity_balance | int (1-100) | Activity balance score |
| contributors.body_temperature | int (1-100) | Body temp contributor |
| contributors.hrv_balance | int (1-100) | 14-day vs 3-month HRV comparison |
| contributors.previous_day_activity | int (1-100) | Previous day activity impact |
| contributors.previous_night | int (1-100) | Previous night sleep impact |
| contributors.recovery_index | int (0-100) | Recovery index |
| contributors.resting_heart_rate | int (1-100) | RHR contributor |
| contributors.sleep_balance | int (1-100) | Sleep debt/balance score |

### Daily Activity — `/v2/usercollection/daily_activity`
| Field | Type | Description |
|-------|------|-------------|
| score | int (1-100) | Overall activity score |
| active_calories | int | Calories from activity |
| equivalent_walking_distance | int (meters) | Walking equivalent |
| high_activity_met_minutes | int | Vigorous MET minutes |
| medium_activity_met_minutes | int | Moderate MET minutes |
| low_activity_met_minutes | int | Light MET minutes |
| high_activity_time | int (seconds) | Vigorous activity duration |
| medium_activity_time | int (seconds) | Moderate activity duration |
| low_activity_time | int (seconds) | Light activity duration |

### Heart Rate — `/v2/usercollection/heartrate`
Continuous HR measurements with timestamps. Filter by datetime range.

### Workouts — `/v2/usercollection/workout`
Oura-detected or manually logged workout data with HR metrics and intensity.

### Sessions — `/v2/usercollection/session`
Recovery and meditation sessions with duration and type.

## Example: Fetch last 7 days of readiness data (Python)
```python
import requests
from datetime import date, timedelta

headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    "start_date": (date.today() - timedelta(days=7)).isoformat(),
    "end_date": date.today().isoformat()
}
resp = requests.get(
    "https://api.ouraring.com/v2/usercollection/daily_readiness",
    headers=headers, params=params
)
data = resp.json()["data"]
for day in data:
    print(f"{day['day']}: Readiness {day['score']}, HRV Balance {day['contributors']['hrv_balance']}")
```

## Key metrics for workout planning decisions
- **Readiness score < 60**: Suggest recovery/light day
- **Readiness score 60-75**: Moderate intensity OK
- **Readiness score > 75**: Green light for hard training
- **HRV trending down over multiple days**: Possible overreaching, suggest deload
- **Sleep < 6 hours or efficiency < 75%**: Flag recovery concern
- **Temperature deviation > 1.0**: Possible illness, suggest rest
