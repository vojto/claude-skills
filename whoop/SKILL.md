---
name: whoop
description: Access WHOOP health and fitness data. Use when the user asks about their sleep, recovery, strain, workouts, or health metrics.
---

## CLI Usage

Run from `~/.claude/skills/whoop/`:

```bash
cd ~/.claude/skills/whoop

# Today's summary (sleep + recovery)
python cli.py summary

# Specific date
python cli.py summary 2026-01-17

# Individual commands
python cli.py sleep [DATE]
python cli.py recovery [DATE]
python cli.py workouts [DATE]
python cli.py cycles [DATE]
python cli.py profile
```

DATE format: `YYYY-MM-DD` (defaults to today)

## Setup (One-Time)

If credentials don't exist or are expired:

```bash
cd ~/.claude/skills/whoop && python setup.py
```

## Available Data

- **sleep** - Bedtime, wake time, duration, stages (REM/deep/light), efficiency, performance
- **recovery** - Recovery %, zone (green/yellow/red), HRV, resting HR, SpO2, skin temp
- **workouts** - Individual workouts with strain, HR, calories
- **cycles** - Daily strain totals
- **profile** - User info
