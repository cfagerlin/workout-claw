#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "https://api.github.com/repos/cfagerlin/workout-claw/releases/latest"
ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "VERSION"
CONFIG_FILE = Path.home() / ".workout-planner" / "config.json"


def read_current_version():
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "0.0.0"


def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            return {}
    return {}


def parse_iso(value):
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except Exception:
        return None


def should_prompt(config, latest):
    policy = config.get("update_policy", {})
    if policy.get("mode") == "never":
        return False
    snooze_until = parse_iso(policy.get("snooze_until"))
    if snooze_until and snooze_until > datetime.now(timezone.utc):
        return False
    if policy.get("last_prompted_version") == latest and not snooze_until:
        return False
    return True


def fetch_latest_version():
    req = urllib.request.Request(REPO, headers={"User-Agent": "workout-claw-update-check"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    tag = data.get("tag_name") or data.get("name") or ""
    return tag.lstrip("v")


def main():
    current = read_current_version()
    config = load_config()
    try:
        latest = fetch_latest_version()
    except Exception:
        return 0
    if latest and latest != current and should_prompt(config, latest):
        print(f"UPDATE_AVAILABLE {current} {latest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
