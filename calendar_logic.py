import json
from datetime import datetime, timedelta

EVENTS_FILE = "events.json"


def load_events():
    with open(EVENTS_FILE, "r") as f:
        return json.load(f)


def save_events(events):
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=2)


def list_events(date):
    events = load_events()
    return [e for e in events if e["date"] == date]


def create_event(event):
    events = load_events()
    events.append(event)
    save_events(events)
    return f"Created '{event['name']}' on {event['date']} from {event['start']} to {event['end']}."


def delete_event(name):
    events = load_events()
    original_count = len(events)
    events = [e for e in events if e["name"].lower() != name.lower()]
    if len(events) == original_count:
        return f"No event found with name '{name}'."
    save_events(events)
    return f"Deleted '{name}'."


def move_event(name, shift_minutes):
    events = load_events()
    for event in events:
        if event["name"].lower() == name.lower():
            start = datetime.strptime(event["start"], "%H:%M")
            end = datetime.strptime(event["end"], "%H:%M")
            new_start = start + timedelta(minutes=shift_minutes)
            new_end = end + timedelta(minutes=shift_minutes)
            event["start"] = new_start.strftime("%H:%M")
            event["end"] = new_end.strftime("%H:%M")
            save_events(events)
            return f"Moved '{name}' to {event['start']} - {event['end']}."
    return f"No event found with name '{name}'."


def check_conflicts(date, start, end):
    events = load_events()
    day_events = [e for e in events if e["date"] == date]
    conflicts = []
    new_start = datetime.strptime(start, "%H:%M")
    new_end = datetime.strptime(end, "%H:%M")
    for event in day_events:
        e_start = datetime.strptime(event["start"], "%H:%M")
        e_end = datetime.strptime(event["end"], "%H:%M")
        if new_start < e_end and new_end > e_start:
            conflicts.append(event)
    return conflicts


def move_all_events(date, shift_minutes):
    events = load_events()
    moved = []
    for event in events:
        if event["date"] == date:
            start = datetime.strptime(event["start"], "%H:%M")
            end = datetime.strptime(event["end"], "%H:%M")
            event["start"] = (start + timedelta(minutes=shift_minutes)).strftime("%H:%M")
            event["end"] = (end + timedelta(minutes=shift_minutes)).strftime("%H:%M")
            moved.append(event["name"])
    if not moved:
        return f"No events found on {date}."
    save_events(events)
    return f"Moved {len(moved)} event(s) on {date}: {', '.join(moved)}."


def move_event_to(name, new_start):
    events = load_events()
    for event in events:
        if event["name"].lower() == name.lower():
            old_start = datetime.strptime(event["start"], "%H:%M")
            old_end = datetime.strptime(event["end"], "%H:%M")
            duration = old_end - old_start
            new_start_dt = datetime.strptime(new_start, "%H:%M")
            new_end_dt = new_start_dt + duration
            event["start"] = new_start_dt.strftime("%H:%M")
            event["end"] = new_end_dt.strftime("%H:%M")
            save_events(events)
            return f"Moved '{name}' to {event['start']} - {event['end']}."
    return f"No event found with name '{name}'."


def list_upcoming_events(days=7):
    from datetime import date as date_type
    events = load_events()
    today = date_type.today()
    upcoming = []
    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        delta = (event_date - today).days
        if 0 <= delta <= days:
            upcoming.append(event)
    upcoming.sort(key=lambda e: (e["date"], e["start"]))
    return upcoming


def find_free_time(date, duration_minutes):
    events = load_events()
    day_events = sorted(
        [e for e in events if e["date"] == date],
        key=lambda e: e["start"]
    )

    day_start = datetime.strptime("08:00", "%H:%M")
    day_end = datetime.strptime("22:00", "%H:%M")
    free_slots = []
    current = day_start

    for event in day_events:
        e_start = datetime.strptime(event["start"], "%H:%M")
        e_end = datetime.strptime(event["end"], "%H:%M")
        gap = int((e_start - current).total_seconds() // 60)
        if gap >= duration_minutes:
            free_slots.append({
                "start": current.strftime("%H:%M"),
                "end": e_start.strftime("%H:%M")
            })
        if e_end > current:
            current = e_end

    gap = int((day_end - current).total_seconds() // 60)
    if gap >= duration_minutes:
        free_slots.append({
            "start": current.strftime("%H:%M"),
            "end": day_end.strftime("%H:%M")
        })

    return free_slots
