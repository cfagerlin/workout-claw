# GarminDB Installation & Setup Guide

This guide walks you through installing GarminDB, which downloads your Garmin Connect data into local SQLite databases that the workout-planner skill can query directly.

## Prerequisites

- **Python 3.8+** — check with `python3 --version`
- **pip** — Python package manager (usually comes with Python)
- **A Garmin Connect account** with fitness data (you need an active Garmin device syncing to Garmin Connect)
- Terminal/command line access

## Step 1: Install GarminDB

```bash
pip install garmindb
```

That's it for installation. This installs the `garmindb_cli.py` command and all dependencies.

**Alternative — install from source** (if you want the latest development version):
```bash
git clone git@github.com:tcgoetz/GarminDB.git
cd GarminDB
make setup
```

## Step 2: Create the Config Directory

```bash
mkdir -p ~/.GarminDb
```

## Step 3: Configure Garmin Connect Credentials

Create the configuration file:

```bash
cat > ~/.GarminDb/GarminConnectConfig.json << 'EOF'
{
    "credentials": {
        "user": "your.email@example.com",
        "password": "your_garmin_password"
    },
    "data": {
        "weight_start_date": "2024-01-01",
        "sleep_start_date": "2024-01-01",
        "rhr_start_date": "2024-01-01",
        "monitoring_start_date": "2024-01-01",
        "activities_start_date": "2024-01-01"
    },
    "copy": {
        "activities_directory": ""
    },
    "enabled_stats": {
        "monitoring": true,
        "steps": true,
        "itime": true,
        "sleep": true,
        "rhr": true,
        "weight": true,
        "activities": true
    }
}
EOF
```

**Edit the file** and fill in:
- Your Garmin Connect **email** and **password**
- **Start dates** — set these to when your Garmin data begins (or how far back you want to import). The further back you go, the longer the initial download takes

```bash
nano ~/.GarminDb/GarminConnectConfig.json
```

## Step 4: Handle Two-Factor Authentication (2FA)

Garmin may require 2FA during login. GarminDB uses the `garth` library which handles this:

1. On your **first run**, `garth` will attempt to authenticate
2. If 2FA is enabled, you'll be prompted for an MFA code
3. Check your email or authenticator app for the code and enter it
4. `garth` stores a local session token so future runs authenticate automatically

If you run into 2FA issues:
```bash
# Make sure garth is installed and up to date
pip install --upgrade garth
```

## Step 5: Initial Data Download

Run the full download, import, and analysis:

```bash
garmindb_cli.py --all --download --import --analyze
```

**What this does:**
1. **Downloads** your data from Garmin Connect (raw JSON/FIT files)
2. **Imports** the data into SQLite databases
3. **Analyzes** the data and generates summary tables

**Expect this to take a while on first run** — 10-30+ minutes depending on how much historical data you have. Don't interrupt it. You can monitor progress with:

```bash
tail -f garmindb.log
```

## Step 6: Verify the Installation

After the initial run completes, check that everything worked:

**Check 1: Database files exist**
```bash
ls -la ~/HealthData/DBs/
```

You should see `.db` files like `garmin_activities.db`, `garmin_monitoring.db`, `garmin.db`, etc.

**Check 2: Query some data**
```bash
python3 -c "
import sqlite3
from pathlib import Path

db_path = Path.home() / 'HealthData' / 'DBs' / 'garmin.db'
if db_path.exists():
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\" LIMIT 10')
    tables = [row[0] for row in cursor]
    print(f'Database found with tables: {tables}')
    conn.close()
else:
    print(f'Database not found at {db_path}')
    # Try alternate locations
    for p in Path.home().glob('**/garmin*.db'):
        print(f'Found database at: {p}')
"
```

**Check 3: Stats file**
```bash
cat ~/HealthData/stats.txt
```

This shows a summary of imported data.

## Step 7: Ongoing Sync

To download new data going forward (much faster than the initial download):

```bash
garmindb_cli.py --all --download --import --analyze --latest
```

The `--latest` flag only downloads recent data. Run this daily or before the skill's weekly planning session.

**Tip:** You can set this up as a cron job:
```bash
# Run GarminDB sync daily at 5 AM
0 5 * * * /usr/local/bin/garmindb_cli.py --all --download --import --analyze --latest >> ~/.GarminDb/sync.log 2>&1
```

## Database Locations

**Default database directory:** `~/HealthData/DBs/`

| Database File | Contents |
|--------------|----------|
| `garmin.db` | Weight, resting HR, sleep, stress (health metrics) |
| `garmin_activities.db` | All activities with laps and records |
| `garmin_monitoring.db` | Daily monitoring (steps, HR, intensity, stress) |
| `garmin_summary.db` | Daily/weekly/monthly/yearly summaries |
| `summary.db` | Combined summary data |

**Key tables the skill queries:**

| Table | Database | Used For |
|-------|----------|----------|
| `weight` | garmin.db | Weight and body composition trends |
| `sleep` | garmin.db | Sleep duration and quality |
| `resting_hr` | garmin.db | Resting heart rate trends |
| `stress` | garmin.db | Daily stress levels |
| `activities` | garmin_activities.db | Activity history (type, duration, distance, HR) |
| `activity_laps` | garmin_activities.db | Lap-level detail |
| `daily_summary` | garmin_monitoring.db | Daily health overview |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `garmindb_cli.py: command not found` | The pip install didn't add it to your PATH. Try `python3 -m garmindb` or find it with `pip show garmindb` |
| Authentication fails | Double-check email and password in the config file. Try logging into connect.garmin.com manually first |
| 2FA prompt not appearing | Update garth: `pip install --upgrade garth`. Make sure you're running interactively (not in a background job) for the first auth |
| 2FA session expired | Delete the garth session cache and re-authenticate: check `~/.garth/` for session files |
| Very slow download | Normal for first run with years of data. Use `--latest` for subsequent syncs |
| "Permission denied" errors | Check that `~/.GarminDb/` and `~/HealthData/` are writable |
| Missing data types | Check `enabled_stats` in your config — make sure the data type you want is set to `true` |
| Database path differs | The skill's profile stores the DB path. If yours isn't the default `~/HealthData/DBs/`, update the profile accordingly |
| Import errors after Garmin API changes | Update GarminDB: `pip install --upgrade garmindb`. Check GitHub issues for known problems |

## Providing the Path to the Skill

During onboarding, the skill asks for your GarminDB database path. The default is `~/HealthData/DBs/`. If your databases are in a different location, provide that path instead. The skill uses this to find and query the SQLite files directly.
