#!/usr/bin/env python3
"""
WHOOP CLI - Fetch health and fitness data from WHOOP API

Usage:
    python cli.py sleep [DATE]
    python cli.py recovery [DATE]
    python cli.py workouts [DATE]
    python cli.py cycles [DATE]
    python cli.py profile
    python cli.py summary [DATE]

DATE format: YYYY-MM-DD (defaults to today)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import yaml

# Change to script directory
SCRIPT_DIR = Path(__file__).parent
os.chdir(SCRIPT_DIR)

CREDENTIALS_FILE = SCRIPT_DIR / ".whoop_credentials.json"
API_BASE = "https://api.prod.whoop.com"


def format_duration(ms):
    """Format milliseconds as h:mm."""
    total_minutes = int(ms / 60000)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}:{minutes:02d}"


def parse_timezone_offset(offset_str):
    """Parse timezone offset string like '+01:00' or '-05:00' into a timezone object."""
    match = re.match(r'([+-])(\d{2}):(\d{2})', offset_str)
    if not match:
        return timezone.utc
    sign, hours, minutes = match.groups()
    delta = timedelta(hours=int(hours), minutes=int(minutes))
    if sign == '-':
        delta = -delta
    return timezone(delta)


def to_local_time(dt, tz_offset_str):
    """Convert a datetime to the given timezone offset."""
    tz = parse_timezone_offset(tz_offset_str)
    return dt.astimezone(tz)


def parse_date(date_str):
    """Parse date string YYYY-MM-DD or return today."""
    if not date_str:
        return datetime.now().date()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"error: Invalid date format '{date_str}'. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)


def format_pct(value):
    """Format percentage."""
    return f"{value:.0f}%"


def load_credentials():
    if not CREDENTIALS_FILE.exists():
        print("error: Credentials not found. Run 'python setup.py' first.", file=sys.stderr)
        sys.exit(1)
    with open(CREDENTIALS_FILE) as f:
        return json.load(f)


def get_headers():
    creds = load_credentials()
    return {"Authorization": f"Bearer {creds['access_token']}"}


def api_get(endpoint, params=None):
    """Make a GET request to the WHOOP API."""
    response = requests.get(f"{API_BASE}{endpoint}", headers=get_headers(), params=params)
    if response.status_code == 401:
        print("error: Token expired. Run 'python setup.py' to re-authenticate.", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()
    return response.json()


def get_whoop_client():
    """Get an authenticated WhoopClient and save refreshed tokens."""
    from whoopy import WhoopClient
    creds = load_credentials()
    client = WhoopClient.from_token(
        access_token=creds["access_token"],
        refresh_token=creds["refresh_token"],
        client_id=creds["client_id"],
        client_secret=creds["client_secret"]
    )
    # Save token after creation (will persist any refreshed tokens)
    client.save_token(str(CREDENTIALS_FILE))
    return client


def output_yaml(data):
    """Output data as YAML."""
    print(yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True))


def cmd_sleep(args):
    """Get sleep data for a specific date."""
    target_date = parse_date(args.date)

    # Sleep that ends on target_date (sleep from night before)
    start = datetime.combine(target_date, datetime.min.time()) - timedelta(days=1)
    end = datetime.combine(target_date, datetime.max.time())

    client = get_whoop_client()
    sleep_data = client.sleep.get_all(start=start, end=end)

    # Find sleep that ended on target date
    result = None
    for s in sleep_data:
        tz_offset = getattr(s, 'timezone_offset', '+00:00')
        local_end = to_local_time(s.end, tz_offset)
        if local_end.date() == target_date:
            local_start = to_local_time(s.start, tz_offset)
            result = {
                "date": local_start.strftime("%Y-%m-%d"),
                "bedtime": local_start.strftime("%I:%M %p"),
                "wake_time": local_end.strftime("%I:%M %p"),
            }
            if s.score:
                result["performance"] = format_pct(s.score.sleep_performance_percentage)
                result["efficiency"] = format_pct(s.score.sleep_efficiency_percentage)
                if s.score.stage_summary:
                    ss = s.score.stage_summary
                    sleep_ms = ss.total_sleep_time_milli
                    result["time_in_bed"] = format_duration(ss.total_in_bed_time_milli)
                    result["actual_sleep"] = format_duration(sleep_ms)
                    result["stages"] = {
                        "rem": f"{format_duration(ss.total_rem_sleep_time_milli)} ({ss.total_rem_sleep_time_milli/sleep_ms*100:.0f}%)",
                        "deep": f"{format_duration(ss.total_slow_wave_sleep_time_milli)} ({ss.total_slow_wave_sleep_time_milli/sleep_ms*100:.0f}%)",
                        "light": f"{format_duration(ss.total_light_sleep_time_milli)} ({ss.total_light_sleep_time_milli/sleep_ms*100:.0f}%)",
                        "awake": format_duration(ss.total_awake_time_milli),
                    }
                if s.score.respiratory_rate:
                    result["respiratory_rate"] = f"{s.score.respiratory_rate:.1f} breaths/min"
            break

    if result:
        output_yaml({"sleep": result})
    else:
        output_yaml({"sleep": None, "message": f"No sleep data for {target_date}"})


def cmd_recovery(args):
    """Get recovery data for a specific date."""
    target_date = parse_date(args.date)

    data = api_get("/developer/v2/recovery")
    records = data.get("records", [])

    result = None
    for r in records:
        record_date = datetime.strptime(r["created_at"][:10], "%Y-%m-%d").date()
        if record_date == target_date:
            score = r["score"]
            recovery_pct = score["recovery_score"]

            if recovery_pct >= 67:
                zone = "green"
            elif recovery_pct >= 34:
                zone = "yellow"
            else:
                zone = "red"

            result = {
                "date": r["created_at"][:10],
                "recovery_score": f"{recovery_pct:.0f}%",
                "zone": zone,
                "hrv": f"{score['hrv_rmssd_milli']:.1f} ms",
                "resting_hr": f"{score['resting_heart_rate']:.0f} bpm",
            }
            if score.get("spo2_percentage"):
                result["spo2"] = f"{score['spo2_percentage']:.1f}%"
            if score.get("skin_temp_celsius"):
                result["skin_temp"] = f"{score['skin_temp_celsius']:.1f}°C"
            break

    if result:
        output_yaml({"recovery": result})
    else:
        output_yaml({"recovery": None, "message": f"No recovery data for {target_date}"})


def cmd_workouts(args):
    """Get workout data for a specific date."""
    target_date = parse_date(args.date)

    start = datetime.combine(target_date, datetime.min.time())
    end = datetime.combine(target_date, datetime.max.time())

    client = get_whoop_client()
    workouts = client.workouts.get_all(start=start, end=end)

    results = []
    for w in workouts:
        tz_offset = getattr(w, 'timezone_offset', '+00:00')
        local_start = to_local_time(w.start, tz_offset)

        if local_start.date() == target_date:
            entry = {
                "time": local_start.strftime("%I:%M %p"),
                "sport_id": w.sport_id,
            }
            if w.score:
                entry["strain"] = f"{w.score.strain:.1f}"
                entry["calories"] = f"{w.score.kilojoule / 4.184:.0f} kcal"
                if w.score.average_heart_rate:
                    entry["avg_hr"] = f"{w.score.average_heart_rate} bpm"
                    entry["max_hr"] = f"{w.score.max_heart_rate} bpm"
            results.append(entry)

    output_yaml({"date": str(target_date), "workouts": results if results else None})


def cmd_cycles(args):
    """Get daily cycle (strain) data for a specific date."""
    target_date = parse_date(args.date)

    start = datetime.combine(target_date, datetime.min.time()) - timedelta(days=1)
    end = datetime.combine(target_date, datetime.max.time())

    client = get_whoop_client()
    cycles = client.cycles.get_all(start=start, end=end)

    result = None
    for c in cycles:
        tz_offset = getattr(c, 'timezone_offset', '+00:00')
        local_start = to_local_time(c.start, tz_offset)

        if local_start.date() == target_date:
            result = {"date": local_start.strftime("%Y-%m-%d")}
            if c.score:
                result["strain"] = f"{c.score.strain:.1f}"
                result["calories"] = f"{c.score.kilojoule / 4.184:.0f} kcal"
                if c.score.average_heart_rate:
                    result["avg_hr"] = f"{c.score.average_heart_rate} bpm"
                    result["max_hr"] = f"{c.score.max_heart_rate} bpm"
            break

    if result:
        output_yaml({"cycle": result})
    else:
        output_yaml({"cycle": None, "message": f"No cycle data for {target_date}"})


def cmd_profile(args):
    """Get user profile."""
    client = get_whoop_client()
    user = client.user.get_profile()

    output_yaml({
        "profile": {
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "user_id": user.user_id,
        }
    })


def cmd_summary(args):
    """Get summary for a specific date (sleep + recovery)."""
    target_date = parse_date(args.date)

    summary = {"date": str(target_date)}

    # Get sleep
    start = datetime.combine(target_date, datetime.min.time()) - timedelta(days=1)
    end = datetime.combine(target_date, datetime.max.time())

    client = get_whoop_client()
    sleep_data = client.sleep.get_all(start=start, end=end)

    for s in sleep_data:
        tz_offset = getattr(s, 'timezone_offset', '+00:00')
        local_end = to_local_time(s.end, tz_offset)
        if local_end.date() == target_date:
            local_start = to_local_time(s.start, tz_offset)
            sleep_entry = {
                "bedtime": local_start.strftime("%I:%M %p"),
                "wake_time": local_end.strftime("%I:%M %p"),
            }
            if s.score:
                sleep_entry["performance"] = format_pct(s.score.sleep_performance_percentage)
                sleep_entry["efficiency"] = format_pct(s.score.sleep_efficiency_percentage)
                if s.score.stage_summary:
                    ss = s.score.stage_summary
                    sleep_ms = ss.total_sleep_time_milli
                    sleep_entry["time_in_bed"] = format_duration(ss.total_in_bed_time_milli)
                    sleep_entry["actual_sleep"] = format_duration(sleep_ms)
                    sleep_entry["stages"] = {
                        "rem": f"{format_duration(ss.total_rem_sleep_time_milli)} ({ss.total_rem_sleep_time_milli/sleep_ms*100:.0f}%)",
                        "deep": f"{format_duration(ss.total_slow_wave_sleep_time_milli)} ({ss.total_slow_wave_sleep_time_milli/sleep_ms*100:.0f}%)",
                        "light": f"{format_duration(ss.total_light_sleep_time_milli)} ({ss.total_light_sleep_time_milli/sleep_ms*100:.0f}%)",
                        "awake": format_duration(ss.total_awake_time_milli),
                    }
                if s.score.respiratory_rate:
                    sleep_entry["respiratory_rate"] = f"{s.score.respiratory_rate:.1f} breaths/min"
            summary["sleep"] = sleep_entry
            break

    # Get recovery
    data = api_get("/developer/v2/recovery")
    records = data.get("records", [])

    for r in records:
        record_date = datetime.strptime(r["created_at"][:10], "%Y-%m-%d").date()
        if record_date == target_date:
            score = r["score"]
            recovery_pct = score["recovery_score"]

            if recovery_pct >= 67:
                zone = "green"
            elif recovery_pct >= 34:
                zone = "yellow"
            else:
                zone = "red"

            recovery_entry = {
                "recovery_score": f"{recovery_pct:.0f}%",
                "zone": zone,
                "hrv": f"{score['hrv_rmssd_milli']:.1f} ms",
                "resting_hr": f"{score['resting_heart_rate']:.0f} bpm",
            }
            if score.get("spo2_percentage"):
                recovery_entry["spo2"] = f"{score['spo2_percentage']:.1f}%"
            if score.get("skin_temp_celsius"):
                recovery_entry["skin_temp"] = f"{score['skin_temp_celsius']:.1f}°C"
            summary["recovery"] = recovery_entry
            break

    output_yaml(summary)


def main():
    parser = argparse.ArgumentParser(
        description="WHOOP CLI - Fetch health data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="DATE format: YYYY-MM-DD (defaults to today)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Sleep command
    sleep_parser = subparsers.add_parser("sleep", help="Get sleep data")
    sleep_parser.add_argument("date", nargs="?", help="Date (YYYY-MM-DD)")

    # Recovery command
    recovery_parser = subparsers.add_parser("recovery", help="Get recovery data")
    recovery_parser.add_argument("date", nargs="?", help="Date (YYYY-MM-DD)")

    # Workouts command
    workouts_parser = subparsers.add_parser("workouts", help="Get workout data")
    workouts_parser.add_argument("date", nargs="?", help="Date (YYYY-MM-DD)")

    # Cycles command
    cycles_parser = subparsers.add_parser("cycles", help="Get daily strain cycle")
    cycles_parser.add_argument("date", nargs="?", help="Date (YYYY-MM-DD)")

    # Profile command
    subparsers.add_parser("profile", help="Get user profile")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Get summary (sleep + recovery)")
    summary_parser.add_argument("date", nargs="?", help="Date (YYYY-MM-DD)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "sleep": cmd_sleep,
        "recovery": cmd_recovery,
        "workouts": cmd_workouts,
        "cycles": cmd_cycles,
        "profile": cmd_profile,
        "summary": cmd_summary,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
