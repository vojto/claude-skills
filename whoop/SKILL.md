---
name: whoop
description: Access WHOOP health and fitness data. Use when the user asks about their sleep, recovery, strain, workouts, or health metrics.
---

## CLI Usage

Load env vars first, then run commands:

```bash
export $(cat ~/.claude/skills/whoop/.env | xargs)

# Quick health summary (one-liner)
whoopskill summary

# All data as JSON
whoopskill

# Human-readable format
whoopskill --pretty

# Specific date
whoopskill --date 2026-01-17
```

## Setup (One-Time)

1. Install: `npm install -g whoopskill`
2. Set environment variables (in shell profile or `.env`):
   - `WHOOP_CLIENT_ID`
   - `WHOOP_CLIENT_SECRET`
   - `WHOOP_REDIRECT_URI`
3. Authenticate: `whoopskill auth login`

Tokens are stored in `~/.whoop-cli/tokens.json` and auto-refresh.

## Auth Commands

```bash
whoopskill auth login    # Authenticate
whoopskill auth status   # Check auth status
whoopskill auth refresh  # Manually refresh token
whoopskill auth logout   # Clear credentials
```

## Available Data

- **profile** - User info
- **body** - Body measurements
- **sleep** - Sleep records with stages, efficiency, performance
- **recovery** - Recovery %, zone, HRV, resting HR, SpO2, skin temp
- **workouts** - Workouts with strain, HR, calories
- **cycles** - Daily physiological cycles
