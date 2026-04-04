# Update policy examples

## Remind me later
Command:
```bash
python3 scripts/workout-claw-config.py snooze-hours 72
```

## Never ask again
Command:
```bash
python3 scripts/workout-claw-config.py set-mode never
```

## Always ask again
Command:
```bash
python3 scripts/workout-claw-config.py set-mode ask
python3 scripts/workout-claw-config.py clear-snooze
```

## Mark a version as already prompted
Command:
```bash
python3 scripts/workout-claw-config.py mark-prompted 0.3.1
```
