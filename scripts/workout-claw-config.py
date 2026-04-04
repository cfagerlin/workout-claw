#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

CONFIG_FILE = Path.home() / '.workout-planner' / 'config.json'


def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_config(data):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2) + '\n')


def ensure_policy(data):
    policy = data.setdefault('update_policy', {})
    policy.setdefault('mode', 'ask')
    policy.setdefault('snooze_until', None)
    policy.setdefault('last_prompted_version', None)
    return policy


def cmd_get():
    data = load_config()
    print(json.dumps(data, indent=2))
    return 0


def cmd_set_mode(mode):
    if mode not in {'ask', 'never'}:
        print('usage: workout-claw-config.py set-mode [ask|never]', file=sys.stderr)
        return 1
    data = load_config()
    policy = ensure_policy(data)
    policy['mode'] = mode
    if mode == 'never':
        policy['snooze_until'] = None
    save_config(data)
    return 0


def cmd_snooze(hours):
    data = load_config()
    policy = ensure_policy(data)
    until = datetime.now(timezone.utc) + timedelta(hours=hours)
    policy['mode'] = 'ask'
    policy['snooze_until'] = until.isoformat().replace('+00:00', 'Z')
    save_config(data)
    return 0


def cmd_mark_prompted(version):
    data = load_config()
    policy = ensure_policy(data)
    policy['last_prompted_version'] = version
    save_config(data)
    return 0


def cmd_clear_snooze():
    data = load_config()
    policy = ensure_policy(data)
    policy['snooze_until'] = None
    save_config(data)
    return 0


def main(argv):
    if len(argv) < 2:
        print('usage: workout-claw-config.py [get|set-mode|snooze-hours|mark-prompted|clear-snooze] ...', file=sys.stderr)
        return 1
    cmd = argv[1]
    if cmd == 'get':
        return cmd_get()
    if cmd == 'set-mode' and len(argv) == 3:
        return cmd_set_mode(argv[2])
    if cmd == 'snooze-hours' and len(argv) == 3:
        return cmd_snooze(int(argv[2]))
    if cmd == 'mark-prompted' and len(argv) == 3:
        return cmd_mark_prompted(argv[2])
    if cmd == 'clear-snooze':
        return cmd_clear_snooze()
    print('usage: workout-claw-config.py [get|set-mode|snooze-hours|mark-prompted|clear-snooze] ...', file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
