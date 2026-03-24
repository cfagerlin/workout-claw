# GarminDB Reference

## Overview
GarminDB downloads data from Garmin Connect into local SQLite databases. It stores the raw JSON/FIT files and imports them into queryable tables.

**Install:** `pip install garmindb`

## Setup
1. Copy config: `GarminConnectConfig.json.example` → `~/.GarminDb/GarminConnectConfig.json`
2. Edit with Garmin Connect credentials and desired start dates
3. Initial fetch: `make create_dbs`
4. Updates: `make` (syncs new data)

## Database Location
Default: `~/.GarminDb/` — contains multiple `.db` SQLite files.

## Key Tables

### Activities Database
| Table | Key Fields | Description |
|-------|-----------|-------------|
| activities | activity_id, name, type, sport, sub_sport, start_time, distance, duration, calories, avg_hr, max_hr | Individual activities |
| activity_laps | activity_id, lap_number, distance, duration, avg_hr | Lap-level data |
| activity_records | activity_id, timestamp, heart_rate, speed, cadence | Per-second/per-record data |

### Daily Monitoring Database
| Table | Key Fields | Description |
|-------|-----------|-------------|
| daily_summary | day, hr_min, hr_max, resting_hr, steps, distance, calories, stress_avg, intensity_minutes_goal | Daily health summary |
| daily_monitoring | timestamp, heart_rate, steps, intensity, stress | Continuous monitoring data |

### Health Database
| Table | Key Fields | Description |
|-------|-----------|-------------|
| sleep | day, total_sleep, deep_sleep, light_sleep, rem_sleep, awake | Sleep data |
| sleep_events | timestamp, event | Sleep event timeline |
| weight | day, weight, bmi, body_fat, muscle_mass | Weight/body composition |
| resting_hr | day, resting_hr | Daily resting heart rate |
| stress | day, overall_stress, rest_stress, activity_stress | Stress levels |

## Querying Examples

### Recent activities (Python)
```python
import sqlite3
from pathlib import Path

db_path = Path.home() / ".GarminDb" / "garmin_activities.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

# Last 14 days of activities
cursor = conn.execute("""
    SELECT name, sport, sub_sport, start_time,
           distance, duration, calories, avg_hr
    FROM activities
    WHERE start_time >= date('now', '-14 days')
    ORDER BY start_time DESC
""")
for row in cursor:
    print(f"{row['start_time']}: {row['name']} - {row['sport']} "
          f"({row['distance']:.1f}m, {row['duration']}s, avg HR {row['avg_hr']})")
```

### Weight trend
```python
cursor = conn.execute("""
    SELECT day, weight, body_fat, muscle_mass
    FROM weight
    WHERE day >= date('now', '-30 days')
    ORDER BY day
""")
```

### Weekly activity volume
```python
cursor = conn.execute("""
    SELECT strftime('%W', start_time) as week,
           sport,
           COUNT(*) as sessions,
           SUM(duration) / 60.0 as total_minutes,
           SUM(distance) / 1000.0 as total_km
    FROM activities
    WHERE start_time >= date('now', '-8 weeks')
    GROUP BY week, sport
    ORDER BY week DESC, total_minutes DESC
""")
```

### Sleep and resting HR for recovery assessment
```python
cursor = conn.execute("""
    SELECT s.day, s.total_sleep, s.deep_sleep, r.resting_hr, st.overall_stress
    FROM sleep s
    LEFT JOIN resting_hr r ON s.day = r.day
    LEFT JOIN stress st ON s.day = st.day
    WHERE s.day >= date('now', '-7 days')
    ORDER BY s.day DESC
""")
```

## Key metrics for workout planning
- **Resting HR trending up**: Possible fatigue/overtraining
- **Weekly activity volume**: Compare planned vs actual
- **Sport distribution**: Ensure training variety matches goals
- **Weight/body composition trends**: Track against body composition goals
- **Stress levels**: High stress days may warrant lighter training
- **Sleep quality from Garmin**: Cross-reference with Oura for more complete picture
